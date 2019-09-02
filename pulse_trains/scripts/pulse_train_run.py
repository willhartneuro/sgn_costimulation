"""
A class for containing run data for a single pulse frequency run
"""

import math
from typing import Sequence, TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import quantities as q
from scipy.signal import vectorstrength
import seaborn as sns

from time_constants import TimeConstants
import definitions as d

# circular import, so type checking required this way
if TYPE_CHECKING:
    from file_data import FileData # pylint: disable=unused-import

class PulseTrainRun(object):
    """Contains data for a stimulation run looking at costimulation pulse trains"""

    cell: int
    opt_pulse_width: float
    opt_pulse_isi: float
    opt_pow: float
    elec_power: float
    elec_perc: float
    peaks: Sequence[int]
    data: Sequence[q.UnitQuantity]

    def __init__(self,
                 file_data: 'FileData',
                 meta: list,
                 elec_power: float,
                 data: Sequence[float]
                ):
        self.data = (data * q.V).rescale('mV') + d.JNC_POT
        self.opt_pulse_width = file_data.opt_pulse_width
        self.opt_pulse_isi = file_data.opt_pulse_isi
        self.opt_pow = file_data.opt_pow
        self.elec_power = elec_power
        self.elec_thresh = meta[d.E_T]
        self.cell = meta[d.CELL]

        self.get_peaks()

    def get_peaks(self):
        """
        Determines the data indices of peaks. Called by the constructor.

        Returns detailed peak data
        """
        peak_data = TimeConstants.describe_peaks(self.data)
        self.peaks = [x['peak'] for x in peak_data if x['superthresh']]
        return peak_data

    def get_vector_strength(self, times):
        """
        Calculates the vector strength of this run

        returns: (strength, phase)
        """

        period = self.opt_pulse_isi + self.opt_pulse_width
        events = [times[x] for x in self.peaks]
        return vectorstrength(events, period)

    def get_adaption_ratio(self):
        """
        Gets the ratio between the amplitude of the first peak
        and the amplitude of the last peak, or 0 if <2 peaks are found
        """
        if len(self.peaks) < 2:
            return 0. * q.dimensionless

        baseline = np.mean(self.data[0:500])
        return (self.data[self.peaks[-1]] - baseline) / (self.data[self.peaks[0]] - baseline)

    def get_spike_ratio(self, num_stimuli=10):
        """
        Gets the proportion of spikes generated, assuming a default
        of 10 pulses in the train.
        """
        return len(self.peaks) / num_stimuli

    def get_frequency(self):
        """Gets the freuqency of this stimulation run"""
        return math.floor(1000. / (self.opt_pulse_isi + self.opt_pulse_width))

    @staticmethod
    def bucket(val, bucket):
        """Converts a value into a bucketed value"""
        return int(bucket * round(val / bucket))

    def plot(
            self,
            times: Sequence[q.UnitTime],
            start_idx: int,
            end_idx: int,
            include_peaks: bool,
            ax: plt.Axes = None,
            show_title: bool = True,
            o_bucket: int = 10,
            e_bucket: int = 5,
            **kwargs
    ):
        """Plots the sequence, marking peaks if include_peaks is True"""

        if ax is None:
            __, ax = plt.subplots(1, 1)

        ax.plot(times[start_idx:end_idx], self.data[start_idx:end_idx], **kwargs)

        freq = self.get_frequency()

        if include_peaks:
            ax.scatter(
                [times[i] for i in self.peaks if i >= start_idx and i <= end_idx],
                [self.data[i] for i in self.peaks if i >= start_idx and i <= end_idx],
                marker='+', color='r')

        sns.despine(ax=ax)

        ax.set_ylim((-75, 30))
        ax.set_yticks([-75, -50, -25, 0, 25])
        ax.set_xlabel("Time (sec)")
        ax.set_ylabel("Membrane Voltage (mV)")
        if show_title:
            opow = self.opt_pow if o_bucket is None else \
                PulseTrainRun.bucket(self.opt_pow, o_bucket)
            epow = self.elec_power if e_bucket is None else \
                PulseTrainRun.bucket(self.elec_power, e_bucket)

            ax.set_title(
                f"{freq} Hz\n{opow:.0f}% Optical \n{epow:.0f}% Electrical")
