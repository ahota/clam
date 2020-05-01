from argparse import ArgumentParser
import datetime
from fabric import Connection
import matplotlib
from matplotlib import animation, dates, pyplot, ticker
import psutil
import random
import time

import clam_colors

# remove the toolbar with zoom, pan, view buttons
matplotlib.rcParams['toolbar'] = 'None'

# axes formatters/locators
xfmt = dates.DateFormatter('%H:%M:%S')
xloc = ticker.LinearLocator(numticks=5)


def initialize():
    global local, nodes, connections, colors
    local = False
    nodes = []
    connections = []
    colors = []
    labels = []


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
        command = 'top -bn2 | grep "Cpu(s)" | tail -n 1 | awk \'{ print $2; }\''
        # launch the command asynchronously (it takes a while)
        results = [conn.run(command, asynchronous=True) for conn in connections]
        # join all commands to get the result
        results = [float(r.join().stdout.strip()) for r in results]
        return results


def update(i, x, y):
    new_ys = get_cpu()
    for i in range(len(y)):
        y[i].append(new_ys[i])
    x.append(datetime.datetime.now())

    x = x[-30:]

    format_axes(ax)
    for yi in range(len(y)):
        y[yi] = y[yi][-30:]
        line = ax.plot_date(x, y[yi], fmt='-', label=labels[yi] if local else nodes[yi])
    fig.legend(fontsize='xx-small', loc='center right')


initialize()

if __name__ == '__main__':
    global local, nodes, colors, labels

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
    fig = pyplot.figure(figsize=(7, 3), tight_layout=True)
    ax = fig.add_subplot(1, 1, 1)
    init_axes(ax)

    # init time and cpu activity lists
    t = [datetime.datetime.now()]
    cpu = []
    if local:
        n_cpu = psutil.cpu_count()
        cpu = [[0.0] for _ in range(n_cpu)]
        colors = clam_colors.build_colors(n_cpu)
        labels = [f'cpu{c:02d}' for c in range(n_cpu)]
    else:
        n_node = len(args.nodes)
        cpu = [[0.0] for _ in range(n_node)]
        nodes = args.nodes
        connections = [Connection(hostname) for hostname in nodes]
        colors = clam_colors.build_colors(n_node)

    anim = animation.FuncAnimation(fig, update, fargs=(t, cpu), interval=1000)
    pyplot.show()
