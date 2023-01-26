from matplotlib import rcParams


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

    for key in keys:
        rcParams[key] = color


def setup_matplotlib_font(**kwargs):
    """
    :param kwargs: dict like {'font.size': '13'}
    :return:
    """

    for key, value in kwargs.items():
        rcParams[key] = value
