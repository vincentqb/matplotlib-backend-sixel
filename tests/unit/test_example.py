import numpy as np


def test_example():
    import matplotlib

    matplotlib.use("module://matplotlib-backend-sixel")
    import matplotlib.pyplot as plt

    fig = plt.figure()
    plt.style.use("dark_background")

    t = np.linspace(0, 5, 200)
    plt.fill_between(t, np.sin(t), np.cos(2 * t), alpha=0.5)
    plt.fill_between(t, np.cos(t), np.sin(2 * t), alpha=0.5)

    assert fig.get_axes()
