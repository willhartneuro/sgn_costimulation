r"""
EXPERIMENT PARAMETER GENERATORS
"""

import math
from typing import Dict, List

import numpy as np
import quantities as q


class Protocol(object):
    """Describes parameters used for a given experiment"""

    protocol_id: int
    first_offset: int
    num_offsets: int
    delta_offset: int
    frequency: int
    column_count: int

    durations: Dict[str, q.UnitTime] = {
        "optical": 10 * q.millisecond,
        "electrical": 3 * q.millisecond
    }

    onsets: Dict[str, q.UnitTime]

    stim_type: List[str] = [
        "costim",
        "electrical",
        "optical"
    ]

    pre_stim: q.UnitTime = 0.1 * q.second
    post_stim: q.UnitTime = 0.3 * q.second

    frequency: int = 50000

    def __init__(
            self,
            protocol_id: int,
            first_offset: int = -3,
            num_offsets: int = 18,
            delta_offset: int = 1,
            frequency: int = 50000,
            column_count: int = 3,
            costim_onset: float = 0.5,
            electrical_onset: float = 1.0,
            optical_onset: float = 1.4
    ):
        self.protocol_id = protocol_id
        self.first_offset = first_offset
        self.num_offsets = num_offsets
        self.delta_offset = delta_offset
        self.frequency = frequency
        self.column_count = column_count

        # the start times when the particular stimulus mode starts
        self.onsets = {
            "costim": costim_onset * q.second,
            "electrical": electrical_onset * q.second,
            "optical": optical_onset * q.second
        }

    def offsets(self, limit: int):
        """Generates a list of time offsets for the given stride (delta ms between pulses)"""
        return list(
            range(
                self.first_offset,
                self.first_offset + self.num_offsets * self.delta_offset,
                self.delta_offset)
            ) * int(math.ceil(limit / self.num_offsets))

    def get_groups(self, axo):
        """Generates grouped columns based on the number of columns in the protocol"""
        return axo.data[1::self.column_count]

    @property
    def period(self):
        """Returns the period of the acquisition in the protocol"""
        return (1 / self.frequency) * q.second

    def get_start_idx(self, stimulus: str) -> int:
        """Gets the start index for the data for a given stimulus"""
        return int((self.onsets[stimulus] - self.pre_stim).magnitude * self.frequency)

    def get_end_idx(self, stimulus: str) -> int:
        """Gets the end index for the data for a given stimulus"""
        return int((self.onsets[stimulus] + self.post_stim).magnitude * self.frequency)

    def get_data_slice(self, stimulus: str) -> slice:
        """Gets the slice for the data of the given stimulus type."""
        return np.s_[
            self.get_start_idx(stimulus) : self.get_end_idx(stimulus)
        ]

    def get_onset(self, stimulus: str, elec_offset: int = 0) -> int:
        """
        Gets the onset index of the given stimulus relative to data start.
        Optionally includes an offset, e.g. for generating results relative to
        the start of electrical stimulus
        """
        q_offset = q.Quantity(elec_offset, q.ms)
        return (
            (self.onsets[stimulus] + q_offset).magnitude * self.frequency
        ) - self.get_start_idx(stimulus)
