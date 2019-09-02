"""
Data structure for analysis of spiking probability by mode
"""


class SpikeResults(object):
    """Analysis spiking probability in a dataset"""
    def __init__(self, ot, et, off):
        self.ot = ot
        self.et = et
        self.off = off
        self.runs = 0
        self.costim_spikes = 0
        self.opt_spikes = 0
        self.elec_spikes = 0
        self.cells = set()

    def costim(self):
        """Gets the proportion of costim APs in the spike set"""
        return round(100. * self.costim_spikes / float(self.runs))

    def opt(self):
        """Gets the proportion of opt APs in the spike set"""
        return round(100. * self.opt_spikes / float(self.runs))

    def elec(self):
        """Gets the proportion of elec APs in the spike set"""
        return round(100. * self.elec_spikes / float(self.runs))

    def thresh(self):
        """Returns true if the costim spike rate is greater than 0"""
        return self.costim() >= 50

    @staticmethod
    def get_spikes(data):
        """Gets spike data from the given dataset"""
        spikes = {}

        for run in data:
            keys = [run.opt_bucket, run.elec_bucket, run.offset]
            if not keys[0] in spikes:
                spikes[keys[0]] = {}

            if not keys[1] in spikes[keys[0]]:
                spikes[keys[0]][keys[1]] = {}

            if not keys[2] in spikes[keys[0]][keys[1]]:
                spikes[keys[0]][keys[1]][keys[2]] = \
                    SpikeResults(run.opt_bucket, run.elec_bucket, run.offset)

            this_spike = spikes[keys[0]][keys[1]][keys[2]]
            this_spike.cells.add(run.cell)
            this_spike.runs += 1
            this_spike.costim_spikes += 1 if run.costim_aps == 1 else 0
            this_spike.opt_spikes += 1 if run.opt_aps == 1 else 0
            this_spike.elec_spikes += 1 if run.elec_aps == 1 else 0

        return spikes
