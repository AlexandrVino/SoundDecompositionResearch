import logging

from matplotlib import rcParams

log = logging.getLogger(__name__)


def setup_matplotlib_text_color(color, keys=None):
    """
    :param color: color to set
    :param keys: list of keys
    :return:
    """

    if keys is None:
        keys = [
            'axes.labelcolor', 'axes.titlecolor', 'xtick.color',
            'xtick.labelcolor', 'ytick.color', 'ytick.labelcolor',
            'grid.color', 'hatch.color',
        ]
    setup_matplotlib(**{key: color for key in keys})


def setup_matplotlib(**kwargs):
    """
    :param kwargs: dict like {'font.size': '13'}
    :return:
    """

    for key, value in kwargs.items():
        try:
            rcParams[key] = value
        except KeyError:
            log.error(f'rcParams does not support "{key}" parameter, pls check "rcParams.keys()"')
            return -1
        except ValueError:
            log.error(f'The "{value}" value is incorrect container for rcParams "{key}" parameter')
            return -1
