from argparse import ArgumentParser
import datetime
from fabric import Connection
import matplotlib
from matplotlib import animation, dates, pyplot, ticker
import psutil
import random
import time

# remove the toolbar with zoom, pan, view buttons
matplotlib.rcParams['toolbar'] = 'None'

# axes formatters/locators
xfmt = dates.DateFormatter('%H:%M:%S')
xloc = ticker.LinearLocator(numticks=5)


def initialize():
    global local, nodes, connections
    local = False
    nodes = []
    connections = []


def init_axes(ax):
    # initial axes formatting
    ax.set_title('average CPU activity')
    ax.set_ylabel('% active')
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(False)
    ax.xaxis_date()
    format_axes(ax, init=True)


def format_axes(ax, init=False):
    # these properties need to be re-applied per update
    if not init:
        ax.clear()
        ax.set_title('average CPU activity')
        ax.set_ylabel('% active')
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_major_locator(xloc)
    ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)


def get_cpu():
    if local:
        return psutil.cpu_percent(percpu=True)
    else:
        pass


def update(i, x, y):
    x.append(datetime.datetime.now())

    new_ys = get_cpu()
    for i in range(len(y)):
        y[i].append(new_ys[i])

    x = x[-30:]

    format_axes(ax)
    for yv in y:
        yv = yv[-30:]
        ax.plot_date(x, yv, fmt='-')


initialize()

if __name__ == '__main__':
    global local
    global nodes

    parser = ArgumentParser(prog='clam',
                            description='a basic Cluster/Local Activity Monitor')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--local', action='store_true',
                       help='report local CPU activity')
    group.add_argument('--nodes', nargs='+', metavar='NAME',
                       help='space-separated list of node hostnames on which to report CPU activity')
    args = parser.parse_args()

    local = args.local

    # our figure and axes
    fig = pyplot.figure(figsize=(6, 3), tight_layout=True)
    ax = fig.add_subplot(1, 1, 1)
    init_axes(ax)

    # init time and cpu activity lists
    t = [datetime.datetime.now()]
    cpu = []
    if local:
        n_cpu = psutil.cpu_count()
        cpu = [[0.0] for _ in range(n_cpu)]
    else:
        n_node = len(args.nodes)
        cpu = [[0.0] for _ in range(n_node)]
        nodes = args.nodes
        connections = [Connection(hostname) for hostname in nodes]

    anim = animation.FuncAnimation(fig, update, fargs=(t, cpu), interval=1000)
    pyplot.show()