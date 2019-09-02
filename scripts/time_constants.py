r"""
contains time constants for a given costimulation run
"""

import math
from typing import Dict, Sequence

from collections import namedtuple
import numpy as np
import quantities as q
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, peak_widths

DerivativeInfo = namedtuple('DerivativeInfo', 'idx_peak_start idx_peak idx_dvdt_thresh idx_dvdt_peak dvdt_peak dvdt_avg dvdt')

class TimeConstants(object):
    """
    A class to contain time constants for action potential data.
    All time constants are in milliseconds
    """

    onset_latency: q.UnitTime = 0 * q.second
    peak_latency: q.UnitTime = 0 * q.second
    fwhm_duration: q.UnitTime = 0 * q.second
    mv0_duration: q.UnitTime = 0 * q.second
    on_tau: q.UnitTime = 0 * q.second
    off_tau: q.UnitTime = 0 * q.second
    derivative: DerivativeInfo = None

    def __init__(
            self,
            peak_data: Dict[str, float],
            sample_period: q.millisecond,
            stim_onset: int,
            derivative_info: DerivativeInfo = None):
        """
        Initialises the array with peak data from CostimulationRun::describe_peaks
        """

        if peak_data is None:
            return

        self.derivative = derivative_info

        # Onset latency is currently undefined - it is unclear what it should be?
        # Should it count from optical or electrical start? What happens when the
        # electrical pulse happens as the optical is already rising?
        self.onset_latency = q.Quantity(-1, 'ms')
        # (peak_data['onset'] - stim_onset) * sample_period * 1000

        # i.e. the number of num_samples * seconds per sample in millis
        self.peak_latency = (peak_data['peak'] - stim_onset) * sample_period * 1000
        self.mv0_duration = peak_data['0mv_duration'] * sample_period * 1000
        self.fwhm_duration = peak_data['fwhm'] * sample_period * 1000

        self.on_tau = (peak_data['t_on'] - stim_onset) * sample_period * 1000
        self.off_tau = (peak_data['t_off'] - peak_data['peak']) * sample_period * 1000

    @staticmethod
    def __exp(x: float, a: float, inverse_tc: float, constant: float):
        return a * np.exp(inverse_tc * x) + constant


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
    def __find_width(data: Sequence[float], start_idx: int, level: float):
        """
        Given some data and a peak index, find the left and right boundaries
        where the signal dips below the given level. Used for finding the 0mV
        width of a peak.

        Not particularly efficient as we've probably already looped this sequence
        but hey I'm not working for google here
        """

        start = start_idx
        end = start_idx
        delta = 0
        max_val = len(data)

        while start_idx - delta > 0:
            if start_idx + delta < max_val and end == start_idx:
                if data[start_idx + delta] < level:
                    end = start_idx + delta

            if start == start_idx and data[start_idx - delta] < level:
                start = start_idx - delta

            if start != start_idx and end != start_idx:
                return end - start

            delta = delta + 1

        return -1 # no peaks found

    @staticmethod
    def describe_peaks(
            data: Sequence[float],
            expected: int = None,
            deriv_thresh: float = 0.02):
        """
        Calculates the time constants for peaks in the given signal.

        If expected is provided and a different number of peaks is found, raise an exception
        """

        baseline = data[:250].mean()
        thresh = baseline - 0.03 * baseline

        peaks, peak_data = find_peaks(data, distance=5000, height=thresh, width=50)

        if (expected is not None) and (len(peaks) != expected):
            raise Exception(
                f"Expected {expected} peaks in calculate_time_constants but found {len(peaks)}")

        widths = [int(x[0] - x[1]) for x in zip(peak_data['right_ips'], peak_data['left_ips'])]
        maxes = [data[x] - baseline for x in peaks] # maximum is the delta to baseline

        ons = peak_widths(data, peaks, rel_height=0.368)[2] # index 2 is the index of the left hand intersection at ~36.8% down from the top
        offs = peak_widths(data, peaks, rel_height=0.632)[3] # index 3 is for right hand intersection at ~63.2% down from the top

        diff = np.diff(data)
        onsets = [TimeConstants.__find_last_idx(
            list(zip(data[:-1], diff)),
            # above thresh and deriv above deriv_thresh
            lambda x: x[0] < thresh and x[1] > deriv_thresh,
            pk
        ) for pk in peaks]

        t_ons = [math.ceil(x) for x in ons]
        t_offs = [math.ceil(x) for x in offs]

        zero_durations = [TimeConstants.__find_width(data[:-1], x, 0) for x in peaks]

        return [{
            "peak": x[0],
            "max": x[1],
            "fwhm": x[2],
            "t_on": x[3],
            "t_off": x[4],
            "onset": x[5],
            "0mv_duration": x[6]
        } for x in zip(peaks, maxes, widths, t_ons, t_offs, onsets, zero_durations)]

    @staticmethod
    def get_derivative(
        data: Sequence[float],
        period: float,
        dvdt_threshold: float,
        samples_to_ms: float,
        include_dvdt: bool=False):
        if np.max(data) < -0.02:
            return None

        (peaks, _) = find_peaks(data, distance=1000, width=50, height=1e-6)
        widths = peak_widths(data, peaks, rel_height=0.95)

        if len(peaks) != 1:
            return None

        peak_start_idx = int(widths[2])
        peak_idx = peaks[0]

        dvdt = [0] + (data[peak_start_idx:peak_idx]-data[peak_start_idx-1:peak_idx-1])/float(period.magnitude)

        (dvdt_peaks, _) = find_peaks(dvdt, width=6, height=25, rel_height=0.5)

        for dvdt_idx in range(0, len(dvdt)):
            if dvdt[dvdt_idx] > dvdt_threshold:
                break

        if peak_start_idx + dvdt_idx > peak_idx:
            dvdt_idx = -1

        dvdt_peak_idx = dvdt_peaks[0] if len(dvdt_peaks) > 0 else -1

        return DerivativeInfo(
            peak_start_idx,
            peak_idx,
            dvdt_idx,
            dvdt_peak_idx,
            dvdt[dvdt_peak_idx] if dvdt_peak_idx > 0 else -1,
            1000*(data[peak_idx] - data[dvdt_idx + peak_start_idx])/(samples_to_ms * (peak_idx - (dvdt_idx + peak_start_idx))),
            dvdt if include_dvdt else None
        )
