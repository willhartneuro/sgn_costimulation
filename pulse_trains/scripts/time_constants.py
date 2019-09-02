r"""
contains time constants for a given costimulation run
"""
import math
from typing import Dict, Sequence

import numpy as np
import quantities as q
from scipy.signal import find_peaks, peak_widths

PERIOD = 2e-5

class TimeConstants(object):
    """
    A class to contain time constants for action potential data.
    All time constants are in milliseconds
    """
    onset_latency: q.UnitTime = 0 * q.second
    peak_latency: q.UnitTime = 0 * q.second
    fwhm_duration: q.UnitTime = 0 * q.second
    on_tau: q.UnitTime = 0 * q.second
    off_tau: q.UnitTime = 0 * q.second

    _ap_detection_threshold: float = 100

    def __init__(
            self,
            peak_data: Dict[str, float],
            sample_period: q.millisecond,
            stim_onset: float):
        """
        Initialises the array with peak data from CostimulationRun::describe_peaks
        """

        if peak_data is None:
            return

        self.onset_latency = (peak_data['onset'] - stim_onset) * sample_period * 1000
        self.peak_latency = (peak_data['peak'] - stim_onset) * sample_period * 1000
        self.fwhm_duration = peak_data['fwhm'] * sample_period * 1000
        self.on_tau = peak_data['t_on'] * sample_period * 1000
        self.off_tau = peak_data['t_off'] * sample_period * 1000

    @staticmethod
    def __find_last_idx(data: Sequence[float], comparator, start_idx: int):
        """
        Returns the last index where the comparator returns true, starting from start_idx
        and moving backwards
        """

        idx = start_idx
        while idx > 0:
            if comparator(data[idx]):
                return idx
            idx -= 1

        return 0

    @staticmethod
    def is_above_deriv_thresh(data, thresh):
        """Check if the derivative is above the threshold"""
        diff = np.append([0], (data[1:] - data[:-1]) / (PERIOD))
        return np.max(diff) >= thresh

    @staticmethod
    def describe_peaks(
            data: Sequence[float],
            expected: int = None,
            thresh: float = -20):
        """
        Calculates the time constants for peaks in the given signal.

        If expected is provided and a different number of peaks is found, raise an exception
        """

        peaks, peak_data = find_peaks(data, distance=500, height=thresh, width=50)

        if (expected is not None) and (len(peaks) != expected):
            raise Exception(
                f"Expected {expected} peaks in calculate_time_constants but found {len(peaks)}")

        indices = [
            (int(x[0]), int(x[1])) for x in zip(
                peak_data['left_ips'],
                peak_data['right_ips']
            )
        ]
        above_deriv_thresh = [
            TimeConstants.is_above_deriv_thresh(
                data[x[0]:x[1]],
                TimeConstants._ap_detection_threshold
            ) for x in indices
        ]
        widths = [int(x[1] - x[0]) for x in indices]
        maxes = [data[x] for x in peaks]

        ons = peak_widths(data, peaks, 0.33)[2]
        offs = peak_widths(data, peaks, 0.67)[3]

        onsets = [TimeConstants.__find_last_idx(data, lambda x: x < thresh, pk) for pk in peaks]

        t_ons = [math.ceil(x) for x in ons]
        t_offs = [math.ceil(x) for x in offs]

        return [{
            "peak": x[0],
            "max": x[1],
            "fwhm": x[2],
            "t_on": x[3],
            "t_off": x[4],
            "onset": x[5],
            "superthresh": x[6]
        } for x in zip(peaks, maxes, widths, t_ons, t_offs, onsets, above_deriv_thresh)]
