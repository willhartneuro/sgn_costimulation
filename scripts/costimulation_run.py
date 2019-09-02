r"""
Defines a "CostimulationRun" object, which contains information
about a single costimulation run.
"""

from typing import List, Sequence

import matplotlib.pyplot as plt
import numpy as np
import quantities as q

import definitions as d
from time_constants import TimeConstants

class CostimulationRun(object):
    """
    Represents a single costimulation run, including three pulses - combined,
    electrical only, optical only.

    Gathers data about particular runs including latency, AP detection, pulse peaks, etc
    """
    # pylint: disable=too-many-instance-attributes

    protocol_id: int
    offset: int
    period: q.UnitTime

    v_rest: float
    # snr: float
    costim_max: float
    elec_max: float
    opt_max: float

    elec_thresh: float
    opt_thresh: float

    costim_aps: bool
    elec_aps: bool
    opt_aps: bool

    data: List[q.UnitQuantity]
    costim_data: List[q.UnitQuantity]
    elec_data: List[q.UnitQuantity]
    opt_data: List[q.UnitQuantity]

    costim_time_constants: TimeConstants
    elec_time_constants: TimeConstants
    opt_time_constants: TimeConstants

    # As per e.g. https://github.com/swharden/SWHLab/blob/master/swhlab/analysis/ap.py
    # an AP is where the derivative of the signal exceeds this threshold, i.e. 20mV / ms
    _ap_detection_threshold: float = 100 * (q.mV / q.ms)

    def __init__(
            self,
            file_data: "FileData",
            protocol: d.Protocol,
            data: Sequence[float],
            offset: int,
            elec_thresh: float,
            opt_thresh: float,
            cell: int
    ):
        """
        Initialises the run with the output data recorded by axograph
        """

        # print(" --> OFFSET %s" % (offset))

        self.file_data = file_data
        self.data = np.array(data) + d.JNC_POT
        self.offset = offset
        self.period = protocol.period
        self.protocol_id = protocol.protocol_id
        self.elec_thresh = elec_thresh
        self.opt_thresh = opt_thresh
        self.cell = cell

        self.v_rest = np.mean(self.data[0:1000]) * 1000 # to mV
        # self.snr = -self.v_rest / (np.std(self.data[0:1000]) * 1000)
        self.costim_data = self.data[protocol.get_data_slice("costim")]
        self.elec_data = self.data[protocol.get_data_slice("electrical")]
        self.opt_data = self.data[protocol.get_data_slice("optical")]

        self.costim_max = np.max(self.costim_data) * 1000 * q.millivolt
        self.elec_max = np.max(self.elec_data) * 1000 * q.millivolt
        self.opt_max = np.max(self.opt_data) * 1000 * q.millivolt

        self.costim_aps = self.detect_aps(self.costim_data)
        self.elec_aps = self.detect_aps(self.elec_data)
        self.opt_aps = self.detect_aps(self.opt_data)

        # In theory could do all at once here, but then if there aren't
        # three peaks would need to allocate the peaks to the correct
        # stimulation mode. This way we can be certain the peak is at
        # least "close" to the stimulation mode
        c_peaks = TimeConstants.describe_peaks(self.costim_data) + [None]
        e_peaks = TimeConstants.describe_peaks(self.elec_data) + [None]
        o_peaks = TimeConstants.describe_peaks(self.opt_data) + [None]

        # alternative method to calculate t_on / t_off based on curve fitting
        # could be expensive, lets see!
        self.c_ton = 0
        self.c_toff = 0
        self.e_ton = 0
        self.e_toff = 0
        self.o_ton = 0
        self.o_toff = 0

        self.costim_time_constants = \
            TimeConstants(
                c_peaks[0],
                self.period,
                protocol.get_onset("costim", self.offset),
                TimeConstants.get_derivative(self.costim_data, self.period, 25, 1000. / 50000.))
        self.elec_time_constants = \
            TimeConstants(
                e_peaks[0],
                self.period,
                protocol.get_onset("electrical", 0),
                TimeConstants.get_derivative(self.elec_data, self.period, 25, 1000. / 50000.))
        self.opt_time_constants = \
            TimeConstants(
                o_peaks[0],
                self.period,
                protocol.get_onset("optical", 0),
                TimeConstants.get_derivative(self.opt_data, self.period, 25, 1000. / 50000.))

    def get_derivative(self, data: Sequence[float]) -> List[float]:
        """
        Calculates and returns the point by point derivative for the given sequence
        REF: https://github.com/swharden/SWHLab/blob/master/swhlab/analysis/ap.py
        NOTE: memoize?

        Returns the value in V/s
        """
        return np.append([0], (data[1:] - data[:-1]) / (self.period))

    def detect_aps(self, data: Sequence[float]) -> bool:
        """
        Detects whether the gradient within the data exceeds the threshold gradient
        """
        deriv = self.get_derivative(data) * (q.volt / q.sec)  # data here is in V/s
        max_d = np.max(deriv).rescale(q.mV / q.ms)            # maximum now in mV/ms

        return max_d >= self._ap_detection_threshold

    def plot(self, time_shift=0, **kwargs):
        """Plots this run"""
        plt.plot([x * 1000. - time_shift for x in self.file_data.times], self.data * 1000, **kwargs)
        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane Voltage (mV)")
