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
import pytest

from LbAPCommon.dirac_conversion import InvalidAPJob, group_in_to_requests


def test_simple():
    data = {
        "A": {"input": {"bk_query": ...}},
        "B": {"input": {"bk_query": ...}},
        "C": {"input": {"bk_query": ...}},
    }
    assert group_in_to_requests(data) == [["A"], ["B"], ["C"]]


def test_valid():
    data = {
        "A": {"input": {"bk_query": ...}},
        "B": {"input": {"bk_query": ...}},
        "C": {"input": {"bk_query": ...}},
        "D": {"input": {"job_name": "C"}},
        "E": {"input": {"job_name": "D"}},
    }
    assert group_in_to_requests(data) == [["A"], ["B"], ["C", "D", "E"]]


@pytest.mark.parametrize(
    "data",
    [
        {"A": {"input": {"job_name": "A"}}},
        {"A": {"input": {"job_name": "B"}}, "B": {"input": {"job_name": "A"}}},
        {
            "A": {"input": {"job_name": "C"}},
            "B": {"input": {"job_name": "A"}},
            "C": {"input": {"job_name": "B"}},
        },
        {
            "A": {"input": {"job_name": "B"}},
            "B": {"input": {"job_name": "A"}},
            "C": {"input": {"job_name": "B"}},
        },
    ],
)
def test_cycle(data):
    with pytest.raises(InvalidAPJob, match="Graph contains a cycle"):
        group_in_to_requests(data)


def test_multiple_children():
    data = {
        "A": {"input": {"bk_query": ...}},
        "B": {"input": {"job_name": "A"}},
        "C": {"input": {"job_name": "B"}},
        "C2": {"input": {"job_name": "B"}},
    }
    with pytest.raises(InvalidAPJob, match="more than one child"):
        group_in_to_requests(data)
