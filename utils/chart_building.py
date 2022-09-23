from load import get_file_data
import matplotlib.pyplot as plt
import logging

log = logging.getLogger(__name__)


def build_chart(filename):
    log.info(f"get data {filename}")
    data = get_file_data(filename)
    log.info(f"build chart {filename}")
    plt.plot([abs(val) for val in data])
    plt.xlabel(filename)
    plt.show()


build_chart("shashlindos.json")
build_chart("Vivaldi_metal_cover.json")
