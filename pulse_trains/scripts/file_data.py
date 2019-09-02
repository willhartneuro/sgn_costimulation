r"""
Contains import / analysis handlers for Axograph files
"""

import math
import os
from typing import List, Sequence

import axographio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import quantities as q
import seaborn as sns

import definitions as d
from pulse_train_run import PulseTrainRun


class FileData(object):
    """
    Reads in a single axograph file
    """
    # pylint: disable=too-many-instance-attributes

    runs: Sequence[PulseTrainRun]

    _path: str
    _times: List[float]
    _len: int
    _meta: list

    opt_pow: float
    min_current: float
    max_current: float
    sample_period: float
    opt_pulse_width: float
    opt_pulse_isi: float

    def __init__(self, meta):
        self._path = os.path.join(d.BASE_PATH, meta[d.PATH])

        # build up child traces
        try:
            axo = axographio.read(self._path)
        except IOError:
            print(f"IOError reading in {self._path}")
            return

        column_count = len(np.unique(np.array(axo.names[1:])))
        self._len = (len(axo.data) - 1) // column_count

        # read in the axograph data
        self._times = axo.data[0] * q.s
        print("Processing %s which has %s runs" % (self._path, self._len))

        # convert optical powers
        converted_opt_pow = self.convert_optical_power(meta[d.O_P])
        converted_opt_thresh = self.convert_optical_power(meta[d.O_T])
        used_opt_pow = 0 if meta[d.O_P] == 0 else math.floor(100 * converted_opt_pow / converted_opt_thresh)

        # store cell metadata
        self._meta = meta
        self.opt_pow = used_opt_pow
        self.min_current = meta[d.E_M]
        self.max_current = meta[d.E_X]
        self.sample_period = self._times[1] - self._times[0]
        self.opt_pulse_width = meta[d.O_W]
        self.opt_pulse_isi = meta[d.O_I]

        elec_currents = self.get_electrical_powers()

        self.runs = [
            PulseTrainRun(
                self,
                meta,
                math.floor(100 * elec_currents[i % meta[d.LVL]] / meta[d.E_T]), x) \
                for i, x in enumerate(axo.data[1::column_count])
        ]

    def convert_optical_power(self, power: int) -> float:
        """
        Converts an optical power in DAC, normalised to 2200 DAC. Uses the equation developed
        by Alex which is -3.552 + 0.00206664 * POWER
        """
        return -3.552 + (0.00206664 * float(power))

    def get_electrical_powers(self, all_runs=False):
        """
        Gets an array of electrical powers used in this protocol.
        If "all_runs" is False, then each power level will only be included once.
        If "all_runs" is True, then the currents array will repeat until there is one
        array item per run in the dataset
        """

        delta_current = (self.max_current - self.min_current) // (self._meta[d.LVL] - 1)
        elec_currents = [self.min_current + i * delta_current for i in range(self._meta[d.LVL])]

        if not all_runs:
            return elec_currents

        elec_currents = elec_currents * (math.ceil(self._len / self._meta[d.LVL]))
        return elec_currents[:self._len]

    def __len__(self):
        return self._len

    def plot_run(self, run_id, start_idx=20000, end_idx=40000, include_peaks=False, ax=None, show_title=True, **kwargs):
        """Plots the given run ID"""
        self.runs[run_id].plot(
            self._times, start_idx, end_idx, include_peaks, ax,
            show_title, **kwargs)

    def plot_all(self,
                 start_idx=20000,
                 end_idx=40000,
                 include_peaks=False,
                 plot_duplicate_param_runs=True
                ):
        """Plots all the runs in a grid"""
        cols = 4
        rows = math.ceil(self._meta[d.LVL] / cols)
        fig, axs = plt.subplots(rows, cols, sharex=True, sharey=True, figsize=(16, 9))

        for i in range(self._meta[d.LVL]): # plot number
            curr_row = i // cols
            curr_col = i % cols
            curr_ax = axs[curr_row][curr_col]

            curr_ax.text(0.4, 30, f"{self.runs[i].elec_power} pA")

            # get all datasets with same params
            for idx in range(i,
                             self._len if plot_duplicate_param_runs else self._meta[d.LVL],
                             self._meta[d.LVL]
                            ):
                run = self.runs[idx]
                curr_ax.plot(
                    self._times[start_idx : end_idx],
                    run.data[start_idx : end_idx],
                    alpha=0.4)
                curr_ax.set_xlabel("Seconds")
                curr_ax.set_ylabel("mV")
                sns.despine()

                if include_peaks:
                    curr_ax.scatter(
                        [self._times[x] for x in run.peaks if x >= start_idx and x <= end_idx],
                        [run.data[y] for y in run.peaks if y >= start_idx and y <= end_idx],
                        marker='+', alpha=0.5
                    )

        mainax = fig.add_subplot(1, 1, 1, frameon=False)
        mainax.get_xaxis().set_visible(False)
        mainax.get_yaxis().set_visible(False)
        plt.title(f"All Pulse Trains\n{self.opt_pow} DACs," +\
            f" {1000 // (self.opt_pulse_isi + self.opt_pulse_width)} Hz")

    def to_df(self):
        """Converts the summary data to a pandas dataframe"""

        data = {
            "Run": [self._path] * self._len,
            "Optical Power": [self.opt_pow] * self._len,
            "Spikes": [len(x.peaks) for x in self.runs],
            "Electrical Power": self.get_electrical_powers(True),
            "Electrical Threshold": [x.elec_thresh for x in self.runs],
            "Vector Strength": [x.get_vector_strength(self._times)[0] for x in self.runs],
            "Vector Strength Phase": [x.get_vector_strength(self._times)[1] for x in self.runs],
            "Adaption Ratio": [x.get_adaption_ratio() for x in self.runs],
            "Spike Ratio": [x.get_spike_ratio() * 100 for x in self.runs],
            "Frequency": [x.get_frequency() for x in self.runs],
            "Cell": [x.cell for x in self.runs]
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
