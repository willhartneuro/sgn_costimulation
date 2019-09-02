"""
Gathers together some analysis tools
"""

import numpy as np
import quantities as q

class Analysis(object):
    """
    A mostly static class to gather analysis tools together
    (allows sharing between notebooks)
    """

    @staticmethod
    def bucket(val, bucket):
        """Converts a value into a bucketed value"""
        return int(bucket * round(val / bucket))

    @staticmethod
    def correct_hold(run, min_val, max_val):
        """Checks if a value is at the correct holding potential"""
        return run.v_rest >= min_val and run.v_rest <= max_val

    @staticmethod
    def no_opt_or_elec_aps(run):
        """Returns true if no opt or elec aps were detected"""
        return run.elec_aps == 0 and run.opt_aps == 0

    @staticmethod
    def any_aps(run):
        """returns true if any aps were detected"""
        return run.elec_aps == 1 or run.opt_aps == 1 or run.costim_aps == 1

    @staticmethod
    def valid_data_selector(run, min_hold, max_hold):
        """
        Predicate that selects runs based on correct starting voltage
        and an optical power between 0 and 150%
        """

        if not Analysis.correct_hold(run, min_hold, max_hold):
            return False
        if run.opt_thresh <= 0 or run.opt_thresh >= 130:
            return False
        return True

    @staticmethod
    def costim_selector(run, min_hold, max_hold):
        """Predicate that selects a run based on the given conditions"""
        if not Analysis.correct_hold(run, min_hold, max_hold):
            return False
        if not Analysis.no_opt_or_elec_aps(run):
            return False
#         if run.offset > 30:
#             return False
        if run.opt_thresh <= 0 or run.opt_thresh >= 100:
            return False
        return True

    @staticmethod
    def subthresh_opt_selector(
            run,
            min_hold: float,
            max_hold: float
    ):
        """
        Predicate that selects a run based on:
         - subthreshold optical response
         - specified range of resting membrane potentials
         - +ve change in membrane voltage under illumination
        """
        if not Analysis.correct_hold(run, min_hold, max_hold):
            return False
        if run.opt_aps == 1:
            return False
        if run.offset > 30:
            return False
        if run.opt_max < run.v_rest:
            return False
        return True

    @staticmethod
    def get_time_constant_thresholds(data):
        """
        Gets the time constant threshold values (i.e. at 66% of peak on the way up
        and 33% peak on the way down) from the given data. The RMP is considered as
        the mean of the first 200 data points

        Returns tuple (idx_of_max, v @ 33%, v @ 66%)
        """

        rmp = np.mean(data[:200])
        max_v_ix = np.argmax(data)
        max_v = data[max_v_ix]

        return (
            max_v_ix,
            rmp + 0.33 * (max_v - rmp),
            rmp + 0.66 * (max_v - rmp)
        )

    @staticmethod
    def find_crossing_index(data, start_idx: int, threshold: float):
        """
        Find the point in the data where the threshold value is crossed.
        Returns the index or -1 if the threshold is never crossed
        """

        check_less = lambda x: x <= threshold
        check_greater = lambda x: x >= threshold
        check = check_less if data[start_idx] > threshold else check_greater

        for idx in range(start_idx, len(data)):
            if check(data[idx]):
                return idx

        return -1

    @staticmethod
    def mavg(data, period):
        """Calculates a moving average of the given data set"""
        return [
            data[i - period : i].sum() / period for i in range(period, len(data))
        ]

    @staticmethod
    def draw_phase_plot(axis, data, legend=False, **kwargs):
        """
        Draws a phase plot on the given axis with the given Costim Run object
        """
        dataq = q.Quantity(data, 'V').rescale('mV')
        # dqma = Analysis.mavg(dataq, 3)
        # dvdt = np.diff(dqma)
        dvdt = np.diff(dataq) / 2e-2 # mV / ms
        axis.plot(dataq[1:], dvdt, **kwargs)

        if legend:
            axis.legend()

        axis.set_xlabel("Voltage (mV)")
        axis.set_ylabel("dV/dt (mV/ms)")
