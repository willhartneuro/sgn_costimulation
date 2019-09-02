r"""
Contains import / analysis handlers for Axograph files
"""

import math
import os
from typing import List, Sequence

import axographio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import definitions as d
from costimulation_run import CostimulationRun


class FileData(object):
    """
    Reads in a single axograph file
    """
    # pylint: disable=too-many-instance-attributes

    runs: Sequence[CostimulationRun]
    protocol: d.Protocol

    _path: str
    times: List[float]
    _len: int

    opt_pow: float
    elec_pow: float
    opt_thresh: float
    opt_thresh_bucket: int
    elec_thresh: float
    elec_thresh_bucket: int
    cell: int

    def __init__(self, meta):
        self._path = os.path.join(d.BASE_PATH, meta[d.PATH])

        # build up child traces
        try:
            axo = axographio.read(self._path) # pylint:ignore E1101
        except OSError:
            print(f"Unable to find file - {self._path}")
            raise

        self.protocol = d.PARAMS[meta[d.PAR]]
        self._len = (len(axo.data) - 1) // self.protocol.column_count
        offsets = self.protocol.offsets(self._len)

        # read in the axograph data
        self.times = axo.data[0]
        print("Processing %s which has %s runs" % (self._path, self._len))

        # convert optical powers
        converted_opt_pow = self.convert_optical_power(meta[d.O_P])
        converted_opt_thresh = self.convert_optical_power(meta[d.O_T])

        # store cell metadata
        self._meta = meta
        self.opt_pow = converted_opt_pow
        self.elec_pow = meta[d.E_P]
        self.opt_thresh = int(math.floor(100. * (converted_opt_pow / converted_opt_thresh)))
        self.opt_thresh_bucket = self._num_to_bucket(self.opt_thresh)
        self.elec_thresh = int(math.floor(100. * (meta[d.E_P] / meta[d.E_T])))
        self.elec_thresh_bucket = self._num_to_bucket(self.elec_thresh)
        self.cell = meta[d.CEL]

        # print(f"{converted_opt_pow}-{meta[d.O_P]} / {converted_opt_thresh}-{meta[d.O_T]} = {self.opt_thresh}")

        self.runs = [
            CostimulationRun(
                self,
                self.protocol,
                x,
                offsets[i],
                self.elec_thresh,
                self.opt_thresh,
                self.cell
            ) for i, x in enumerate(self.protocol.get_groups(axo))
        ]

        self.any_aps = any(x.costim_aps for x in self.runs)

    def __len__(self):
        return self._len

    def convert_optical_power(self, power: int) -> float:
        """
        Converts an optical power in DAC, normalised to 2200 DAC. Uses the equation developed
        by Alex which is -3.552 + 0.00206664 * POWER
        """
        return -3.552 + (0.00206664 * float(power))

    def plot_run(self, run_id):
        """Plots the given run ID"""
        self.runs[run_id].plot(self.times)

    def plot(self, stride=1):
        """Plots all the given traces"""
        for run in self.runs[:self._len:stride]:
            plt.plot(self.times, run.data.rescale('mV'))

        plt.title(f"Action potentials for optical {self.opt_thresh}%," +\
            f" electrical {self.elec_thresh}%")
        plt.xlabel("Time (s)")
        plt.ylabel("Membrane Voltage (mV)")

    @staticmethod
    def _num_to_bucket(val: float, base: int = 5):
        """
        Generates a "bucket" for the given number, by default rounding
        down to the nearest 5
        """
        return int(base * math.floor(val / base))

    def to_df(self):
        """Converts the summary data to a pandas dataframe"""

        data = {
            "cell": [self.cell] * self._len,
            "run": [self._path] * self._len,
            "optical_threshold": [self.opt_thresh] * self._len,
            "opt_bucket": [self.opt_thresh_bucket] * self._len,
            "electrical_threshold": [self.elec_thresh] * self._len,
            "elec_bucket": [self.elec_thresh_bucket] * self._len,
            "offset": [x.offset for x in self.runs],
            "costim_aps": [1 if x.costim_aps else 0 for x in self.runs],
            "costim_max_mv": [x.costim_max.magnitude for x in self.runs],
            "costim_onset_latency_ms":
                [x.costim_time_constants.onset_latency.magnitude for x in self.runs],
            "costim_peak_latency_ms":
                [x.costim_time_constants.peak_latency.magnitude for x in self.runs],
            "costim_0mV_duration_ms":
                [x.costim_time_constants.mv0_duration.magnitude for x in self.runs],
            "costim_fwhm_duration_ms":
                [x.costim_time_constants.fwhm_duration.magnitude for x in self.runs],
            "costim_t_on_ms": [x.costim_time_constants.on_tau.magnitude for x in self.runs],
            "costim_t_off_ms": [x.costim_time_constants.off_tau.magnitude for x in self.runs],


            "elec_onset_latency_ms":
                [x.elec_time_constants.onset_latency.magnitude for x in self.runs],
            "elec_peak_latency_ms":
                [x.elec_time_constants.peak_latency.magnitude for x in self.runs],
            "elec_0mV_duration_ms":
                [x.elec_time_constants.mv0_duration.magnitude for x in self.runs],
            "elec_fwhm_duration_ms":
                [x.elec_time_constants.fwhm_duration.magnitude for x in self.runs],
            "elec_t_on_ms": [x.elec_time_constants.on_tau.magnitude for x in self.runs],
            "elec_t_off_ms": [x.elec_time_constants.off_tau.magnitude for x in self.runs],


            "opt_onset_latency_ms":
                [x.opt_time_constants.onset_latency.magnitude for x in self.runs],
            "opt_peak_latency_ms":
                [x.opt_time_constants.peak_latency.magnitude for x in self.runs],
            "opt_0mV_duration_ms":
                [x.opt_time_constants.mv0_duration.magnitude for x in self.runs],
            "opt_fwhm_duration_ms":
                [x.opt_time_constants.fwhm_duration.magnitude for x in self.runs],
            "opt_t_on_ms": [x.opt_time_constants.on_tau.magnitude for x in self.runs],
            "opt_t_off_ms": [x.opt_time_constants.off_tau.magnitude for x in self.runs],


            "elec_aps": [1 if x.elec_aps else 0 for x in self.runs],
            "elec_max_mv": [x.elec_max.magnitude for x in self.runs],
            "optical_aps": [1 if x.opt_aps else 0 for x in self.runs],
            "opt_max_mv": [x.opt_max.magnitude for x in self.runs],

            "v_rest": [x.v_rest for x in self.runs]
        }

        return pd.DataFrame(data)


def generate_df_and_write_csv(files: Sequence[FileData], path: str) -> pd.DataFrame:
    """
    Generates a pandas dataframe from the passed FileData objects, and writes
    the resulting dataframe to CSV.

    Returns: the dataframe
    """
    fdf: pd.DataFrame = None

    for file in files:
        if fdf is None:
            fdf = file.to_df()
        else:
            fdf = fdf.append(file.to_df())

    fdf = fdf.reset_index()
    fdf.to_csv(path)
    return fdf
