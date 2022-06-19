import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri  # set colormap
from .plot_publication import *
from matplotlib.figure import Figure
from matplotlib.axes import _subplots


class VisualLink():
    def __init__(self, id):
        self.id = id
        self.style = 0
        self.color = [0, 0, 0, 1]  # default color: black
        self.linewidth = 0

    def set_visualization(self, style, color, linewidth):
        self.style = style
        self.color = color  # default color: black
        self.linewidth = linewidth

    def show(self):
        pass


class VisualNode():
    def __init__(self, id):
        self.id = id
        self.marker = 0
        self.color = [0, 0, 0, 1]  # default color: black
        self.size = 0

    def set_visualization(self, marker, color, size):
        self.marker = marker
        self.color = color  # default color: black
        self.size = size


class Visualization():
    def __init__(self, inp, ax=None, fig=None) -> None:
        self.inp = inp  # this attriubte must be read-only
        self.nodes = create_node(inp)
        self.links = create_link(inp)
        self.ax = ax
        self.fig: Figure = fig
        self.colorbars = []
        if ax == None and fig == None:
            self.create_map()  # get ax and fig
        else:
            ax.axis('off')
            ax.axis('equal')

    def highlight_link(self, indices, style='-', color=(0, 0, 0, 1),
                       linkWidth=2, colorbar=False):
        # default color is black
        links = [link for link in self.links if link.id in indices]
        if type(style) == str:
            style = [style] * len(links)
        if is_1D_list(color, lengthOfConstant=4):
            color = [color] * len(links)
        if type(linkWidth) != list:
            linkWidth = [linkWidth] * len(links)
        # set parameters
        for i, link in enumerate(links):
            j = indices.index(link.id)
            links[i].set_visualization(style[j], color[j], linkWidth[j])
        # plot
        params = {'colorbar': colorbar}
        self.visualize_link(indices, **params)

    def highlight_node(self, indices, marker='o', color=(0, 0, 0, 1),
                       nodeSize=8, colorbar=False, colorbarRange=None):
        if len(indices) == 0:
            return 0
        # default color is black
        nodes = [node for node in self.nodes if node.id in indices]
        if type(marker) == str:
            marker = [marker] * len(nodes)
        if is_1D_list(color, lengthOfConstant=4):
            color = [color] * len(nodes)
        if type(nodeSize) != list:
            nodeSize = [nodeSize] * len(nodes)
        # set parameters
        for i, node in enumerate(nodes):
            j = indices.index(node.id)
            nodes[i].set_visualization(marker[j], color[j], nodeSize[j])
        # plot
        params = {'colorbar': colorbar, 'colorbarRange': colorbarRange}
        self.visualize_node(indices, **params)

    def create_map(self):
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.axis('equal')
        # 1/3 of A4
        fig.set_size_inches(8.27, 11.69/3)
        self.ax = ax
        self.fig = fig

    def visualize_link(self, indices, cmap='jet', zorder=1, colorbar=False):
        links = [link for link in self.links
                 if link.id in indices]

        for link in links:
            (x1, y1), (x2, y2) = self.inp.get_link_coord(link.id)
            color = link.color
            linewidth = link.linewidth
            style = link.style
            s = self.ax.plot((x1, x2), (y1, y2), style, color=color,
                             linewidth=linewidth, zorder=1)
            # ax.scatter(x, y, color='blue', s=10, zorder=2)

    def visualize_node(self, indices, cmap='jet',
                       colorbar=False, zorder=3, colorbarRange=None):
        # filter out selected nodes
        nodes = [node for node in self.nodes
                 if node.id in indices]
        coords = [self.inp.get_node_coord(node.id) for node in nodes]
        x = [coordinate[0] for coordinate in coords]
        y = [coordinate[1] for coordinate in coords]
        color = [node.color for node in nodes]
        size = [node.size for node in nodes]
        marker = nodes[0].marker
        if colorbar == True:
            assert len(colorbarRange) == 2
            vmin, vmax = colorbarRange
            s = self.ax.scatter(x, y, marker=marker, c=color,
                                vmin=vmin, vmax=vmax,
                                cmap=cmap, s=size, zorder=zorder)
            self.fig.colorbar(s, ax=self.ax)
        else:
            s = self.ax.scatter(x, y, marker=marker, c=color,
                                cmap=cmap, s=size, zorder=zorder)

    def base_map(self,
                 nodeMarker='o', nodeColor=(0, 0, 0, 1), nodeSize=4,
                 linkStyle='-', linkColor=(0, 0, 0, 1), linkWidth=1):
        params = {}
        # set parameters
        for i in range(len(self.links)):
            self.links[i].set_visualization(linkStyle, linkColor, linkWidth)
        for i in range(len(self.nodes)):
            self.nodes[i].set_visualization(nodeMarker, nodeColor, nodeSize)
        indices = [link.id for link in self.links]
        self.visualize_link(indices, **params)
        indices = [node.id for node in self.nodes]
        self.visualize_node(indices, **params)

    def plot_contour(self, inp, z, colormap):
        coords = [inp.get_node_coord(node.id) for node in self.nodes]
        x = [coordinate[0] for coordinate in coords]
        y = [coordinate[1] for coordinate in coords]
        cntr = self.ax.tricontourf(x, y, z, levels=10, cmap=colormap)

    def annotate_node(self, indices, value, zorder=999):
        # default color is black
        # set parameters
        # filter out selected nodes
        nodes = [node for node in self.nodes if node.id in indices]
        coords = [self.inp.get_node_coord(node.id) for node in nodes]
        x = [coordinate[0] for coordinate in coords]
        y = [coordinate[1] for coordinate in coords]
        # plot
        for x, y, text in zip(x, y, value):
            s = self.ax.text(x, y, text, zorder=zorder)

    def annotate_link(self, indices, value, zorder=999):
        # default color is black
        links = [link for link in self.links if link.id in indices]
        # set parameters
        #
        coordsLink = [self.inp.get_link_coord(link.id) for link in links]
        coordsMidpoint = [((x1+x2)/2, (y1+y2)/2)
                          for (x1, y1), (x2, y2) in coordsLink]
        x = [coordinate[0] for coordinate in coordsMidpoint]
        y = [coordinate[1] for coordinate in coordsMidpoint]
        # plot
        for x, y, text in zip(x, y, value):
            s = self.ax.text(x, y, text, zorder=zorder)


def is_1D_list(variables, lengthOfConstant):
    var = variables[0]
    if len(variables) == lengthOfConstant and \
            (isinstance(var, int) or isinstance(var, float)):
        return True
    else:
        return False


def create_node(inp):
    IDs = inp.junction.index.tolist()
    string = 'Initialize visual node: section %s not found.'
    try:
        IDs += inp.outfall.index.tolist()
    except:
        print(string % ('outfall'))
    try:
        IDs += inp.storage.index.tolist()
    except:
        print(string % ('storage'))
    nodes = [VisualNode(id) for id in IDs]
    return nodes


def create_link(inp):
    IDs = inp.conduit.index.tolist()
    string = 'Initialize visual link: section %s not found.'
    try:
        IDs += inp.pump.index.tolist()
    except:
        print(string % ('pump'))
    links = [VisualLink(id) for id in IDs]
    return links
