###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
__all__ = (
    "group_in_to_requests",
    "parse_application_string",
    "step_to_production_request",
)

from difflib import SequenceMatcher
from itertools import chain, tee

import networkx as nx

from LbAPCommon.parsing import create_proc_pass_map


class InvalidAPJob(ValueError):
    pass


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def group_in_to_requests(jobs_data):
    """Build the Production Requests for the analysis productions "jobs".

    Each production request can be made up of one or more jobs, which must be
    a flat dependency chain. This function will attempt to group the "jobs" and
    raises an InvalidAPJob exception if the constraints are violated.
    """
    G = nx.DiGraph()
    for name, job_data in jobs_data.items():
        G.add_node(name)
        if "job_name" in job_data["input"]:
            G.add_edge(job_data["input"]["job_name"], name)

    # Check for cycles
    if not nx.is_directed_acyclic_graph(G):
        raise InvalidAPJob("Graph contains a cycle")

    # Check that each node has at most one child
    for node in G.nodes():
        if G.out_degree(node) > 1:
            raise InvalidAPJob(f"Job {node} has more than one child.")

    # Find roots (nodes with in-degree == 0)
    roots = [node for node, degree in G.in_degree() if degree == 0]

    # Collect all paths from each root
    all_paths = []
    for root in roots:
        descendants = G.out_degree(nx.descendants(G, root))
        if descendants:
            # Find the last node in the chain
            childless_descendants = {n for n, d in descendants if d == 0}
            if len(childless_descendants) != 1:
                raise NotImplementedError(childless_descendants)
            all_paths.append(nx.shortest_path(G, root, childless_descendants.pop()))
        else:
            # If the root has no children
            all_paths.append([root])

    assert len(jobs_data) == sum(map(len, all_paths))
    return all_paths


def parse_application_string(string):
    """Parse the application string into a dictionary.

    The application string is in the format `name/version[@binary_tag]`.
    """
    application = {
        "name": "/".join(string.split("/")[:-1]),
        "version": string.split("/")[-1],
    }
    if "@" in application["version"]:
        app_version, binary_tag = application["version"].split("@", 1)
        application["version"] = app_version
        application["binary_tag"] = binary_tag
    return application


def step_to_production_request(prod_name, jobs_data, job_names, input_spec, tag_name):
    """Convert a AnalysisProductions step object to a LHCbDIRAC production."""
    wgs = {jobs_data[n]["wg"] for n in job_names}
    if len(wgs) != 1:
        raise NotImplementedError("Found a step with multiple WGs: " + repr(job_names))
    wg = wgs.pop()

    proc_pass_map = create_proc_pass_map(job_names, tag_name)

    steps = []
    for i, job_name in enumerate(job_names):
        job_data = jobs_data[job_name]

        options = {}
        if isinstance(job_data["options"], list):
            options["files"] = job_data["options"]
            options["format"] = "WGProd"
        elif isinstance(job_data["options"], dict) and "files" in job_data["options"]:
            if "command" in job_data["options"]:
                options["command"] = job_data["options"]["command"]
            options["files"] = job_data["options"]["files"]
            options["format"] = "WGProd"
        elif isinstance(job_data["options"], dict):
            options["entrypoint"] = job_data["options"]["entrypoint"]
            options["extra_options"] = job_data["options"]["extra_options"]
            if "extra_args" in job_data["options"]:
                options["extra_args"] = job_data["options"]["extra_args"]
        else:
            raise NotImplementedError(type(job_data["options"]), job_data["options"])

        steps.append(
            {
                "name": f"AnaProd#{tag_name}#{job_name}",
                "processing_pass": proc_pass_map[job_name],
                "application": parse_application_string(job_data["application"]),
                "options": options,
                "data_pkgs": [{"name": "AnalysisProductions", "version": tag_name}],
                "input": [
                    {"type": filename_from_input(job_data["input"]), "visible": i == 0}
                ],
                "output": [{"type": ft, "visible": False} for ft in job_data["output"]],
                "visible": True,
                "ready": True,
                "obsolete": True,
            }
        )

    # TODO: Make the merge step support DST
    merge_step = {
        "name": f"AnaProd#Merge#{prod_name}",
        "processing_pass": "merged",
        "application": {"name": "LHCb", "version": "v55r1"},
        "options": {
            "entrypoint": "dynamic.ap_merger:hadd",
            "extra_options": {},
            "extra_args": ["ZSTD:9"],
        },
        "data_pkgs": [{"name": "AnalysisProductions", "version": tag_name}],
        "input": [{"type": str(ft), "visible": False} for ft in job_data["output"]],
        "output": [{"type": str(ft), "visible": False} for ft in job_data["output"]],
        "visible": False,
        "ready": True,
        "obsolete": True,
    }
    steps.append(merge_step)

    # Remove duplicated parts of the production name to avoid it being too long
    step_name = job_names[0]
    for a, b in pairwise(job_names):
        match = SequenceMatcher(None, a, b).find_longest_match()
        step_name += "," + b.replace(a[match.a : match.a + match.size], "")

    data = {
        "type": "AnalysisProduction",
        "name": f"AnaProd#{prod_name}#{step_name}",
        "priority": jobs_data[job_names[0]]["priority"],
        "inform": list(chain(*[jobs_data[n]["inform"] for n in job_names])),
        "wg": wg,
        "comment": jobs_data[job_names[0]].get("comment", ""),
        "input_dataset": {
            k: input_spec[k]
            for k in {"conditions_dict", "conditions_description", "event_type"}
        },
        "steps": steps,
    }

    return [data]


def filename_from_input(input_data):
    if "bk_query" in input_data:
        return str(input_data["bk_query"].split("/")[-1])

    if "job_name" in input_data:
        return input_data["filetype"]

    if "transform_ids" in input_data:
        return input_data["filetype"]

    raise NotImplementedError(input_data)
