import pandas as pd
import geopandas as gpd
import copy

from pandas.core.frame import DataFrame
from .classfunc import *
import ctypes
import os
import time
import uuid
import networkx as nx


class SwmmRun:
    def __init__(self) -> None:
        self.f1 = ''
        self.f2 = ''
        self.f3 = ''
        self.dll = self.read_dll()

    def read_dll(self):
        cwd = os.path.realpath(__file__)
        # print(cwd)
        path = '\\'.join(cwd.split('\\')[:-1])
        filename = path + '\\' + 'swmm5.dll'
        mydll = ctypes.cdll.LoadLibrary(filename)
        return mydll

    def set_IO(self, filename):
        self.f1 = filename
        self.f2 = filename.split('.')[0]+'.rpt'
        self.f3 = ''

    def open(self):
        # set argument type
        self.dll.swmm_run_open.argtypes = [ctypes.c_char_p,
                                           ctypes.c_char_p,
                                           ctypes.c_char_p]
        self.dll.swmm_run_open.restype = ctypes.c_int
        errcode = self.dll.swmm_run_open(
            self.f1.encode('utf-8'),
            self.f2.encode('utf-8'),
            self.f3.encode('utf-8'))
        if errcode != 0:  # check meaning of errcode in SWMM5 source file
            raise ValueError(errcode)

    def start(self):
        self.dll.swmm_run_start.restype = ctypes.c_int
        errcode = self.dll.swmm_run_start()
        if errcode != 0:  # check meaning of errcode in SWMM5 source file
            raise ValueError(errcode)

    def simulation(self):
        self.dll.swmm_run_simulation.restype = ctypes.c_int
        errcode = self.dll.swmm_run_simulation()
        if errcode != 0:  # check meaning of errcode in SWMM5 source file
            raise ValueError(errcode)

    def close(self, deleteInput=False):
        self.dll.swmm_run_close()
        os.remove(self.f2)
        if deleteInput:
            os.remove(self.f1)

    def get_system_total_flood(self):
        self.dll.result_system_total_flood.restype = ctypes.c_double
        value = self.dll.result_system_total_flood()
        return value


class SwmmInp:
    def __init__(self, filename, graph=False) -> None:
        df = None  # DataFrame()
        self.option: DataFrame = df
        self.raingage: DataFrame = df
        self.subcatch: DataFrame = df
        self.subarea: DataFrame = df
        self.infiltration: DataFrame = df
        self.junction: DataFrame = df
        self.outfall: DataFrame = df
        self.conduit: DataFrame = df
        self.xsection: DataFrame = df
        self.transect: DataFrame = df
        self.inflow: DataFrame = df
        self.timeseries: DataFrame = df
        self.report: DataFrame = df
        self.coordinate: DataFrame = df
        self.polygon: DataFrame = df
        self.symbol: DataFrame = df
        self.pattern: DataFrame = df
        self.curve: DataFrame = df
        self.dwf: DataFrame = df
        self.control: DataFrame = df
        self.losses: DataFrame = df
        self.outlet: DataFrame = df
        self.weir: DataFrame = df
        self.orifice: DataFrame = df
        self.pump: DataFrame = df
        self.storage: DataFrame = df

        if len(filename) == 0:
            print('Warning: Create an empty object.')
        else:
            # self.initialize()
            self.dictionary = self.options()
            self.read_file(filename)
            self.run = SwmmRun()
            if graph:
                self.graph = self.create_graph_from_edge()

    def options(self):
        dictionary = {
            'TITLE':            empty_func,
            'TAGS':             empty_func,
            'MAP':              empty_func,
            'EVAPORATION':      empty_func,
            'VERTICES':         empty_func,
            'PROFILES':         empty_func,
            'OPTIONS':          sect_option,
            'RAINGAGES':        sect_raingage,
            'SUBCATCHMENTS':    sect_subcatch,
            'SUBAREAS':         sect_subarea,
            'INFILTRATION':     sect_infiltration,
            'JUNCTIONS':        sect_junction,
            'OUTFALLS':         sect_outfall,
            'CONDUITS':         sect_conduit,
            'XSECTIONS':        sect_xsection,
            'TRANSECTS':        sect_transect,
            'INFLOWS':          sect_inflow,
            'TIMESERIES':       sect_timeseries,
            'REPORT':           sect_report,
            'COORDINATES':      sect_coordinate,
            'Polygons':         sect_polygon,
            'SYMBOLS':          sect_symbol,
            'STORAGE':          sect_storage,
            'PUMPS':            sect_pump,
            'ORIFICES':         sect_orifice,
            'WEIRS':            sect_weir,
            'OUTLETS':          sect_outlet,
            'LOSSES':           sect_loss,
            'CONTROLS':         sect_control,
            'DWF':              sect_dwf,
            'CURVES':           sect_curve,
            'PATTERNS':         sect_pattern}
        return dictionary

    def read_file(self, filename):
        with open(filename, 'r') as file:
            content = file.readlines()
            startIndex, sectName = 0, 0
            dataFlag = False
            sectFlag = False
            for i, line in enumerate(content):
                if dataFlag == False:
                    if line[0] == '[':
                        sectName = \
                            line.strip().replace('[', '').replace(']', '')
                        sectFlag = True
                        startIndex = i+1
                    elif line[0] == ';':
                        startIndex += 1
                    elif sectFlag == False:
                        pass  # empty lines before the section
                    elif sectFlag == True and line.strip() == '':
                        # meet an empty section
                        sectFlag = False
                    else:
                        dataFlag = True
                else:
                    # end of data
                    if i == len(content)-1 or \
                            (content[i+1][0] == '[' and dataFlag == True) or \
                            (line[0] == '\n' and content[i+1][0] == '[' and dataFlag == True):
                        endIndex = i
                        data = content[startIndex:endIndex+1]
                        # drop empty line
                        data = [line for line in data
                                if line.strip() != '' and line[0] != ';']
                        self.read_match_section(sectName, data)
                        dataFlag = False
                        sectFlag = False
                    else:  # this line is a part of the data
                        pass

    def read_match_section(self, sectName, content):
        """[Create data frames with corresponding headers]

        Args:
            sectName ([str]): [description]
            content ([2d list]): [description]

        Raises:
            ValueError: [description]
        """
        option = self.dictionary
        if sectName in option:
            function = option[sectName]
        else:
            raise ValueError(
                'The section name "%s" is not matched.' % (sectName))
        function(self, content)

    def save_inpfile(self, directory, filename=None):
        # combine file
        content = create_inpfile_content(self)
        # save

        if filename == None:
            # generate an unique file name
            uniqueSuffix = uuid.uuid4().hex
            filename = 'tmp'+uniqueSuffix+'.inp'
        elif filename[-4:] == '.inp':
            pass
        else:
            filename += '.inp'
        filename = directory+filename
        with open(filename, 'w') as text_file:
            text_file.write(content)
        print('The %s is saved.' % (filename))
        return filename

    def run_swmm(self, directory, filename=None):
        if filename == None:
            # generate an unique file name
            uniqueSuffix = uuid.uuid4().hex
            filename = 'tmp'+uniqueSuffix
        else:
            pass
        path = directory + filename
        f1 = self.save_inpfile(path)  # do not need '.inp'
        f2 = path + '.rpt'
        f3 = ''
        call_swmm(f1, f2, f3)
        os.remove(f1)
        databaseName = f2.split('.')[0]+'.db'
        return databaseName

    def set_report_default(self):
        self.report = sect_report_default()

    def get_conduit_xsection(self) -> DataFrame:
        # get xsection of conduit that is ordered according to index
        #  of conduit and drop not used xsection.
        indices = self.conduit.index
        # ! return value is not a copy!
        return self.xsection.loc[indices]

    def get_node_coord(self, name):
        """Get the coordinate of a node by its name.

        Args:
            name (str): name of the node (junction, outfall, ...)

        Returns:
            tuple: (x,y)
        """
        sr = self.coordinate.loc[name, ['x', 'y']]
        coord = tuple(sr.tolist())
        return coord

    def get_node_coord_batch(self, df: DataFrame):
        """Get the coordinates of nodes by their category.

        Args:
            df (DataFrame): Data frame of nodes (junction, outfall, ...)

        Returns:
            2d list: [[x1, y1], 
                        [x2, y2], ...]
        """
        # re-arrange sequence of coordinate based on junctions or ourfalls
        df_coord = self.coordinate.loc[df.index]
        coord = df_coord.values.tolist()
        return coord  # 2d list

    def get_link_coord(self, name):
        """Get the coordinate of a link by its name.

        Args:
            name (str): name of the link (conduit, pumps, ...)

        Returns:
            tuple: ((x1,y1), (x2, y2))
        """
        df = self.get_link_df_by_name(name)
        name1, name2 = df.loc[name, ['fromNode', 'toNode']]
        coords = (self.get_node_coord(name1), self.get_node_coord(name2))
        return coords

    def get_link_df_by_name(self, name):
        if name in self.conduit.index:
            return self.conduit
        elif name in self.pump.index:
            return self.pump
        elif name in self.orifice.index:
            return self.orifice
        elif name in self.weir.index:
            return self.weir
        elif name in self.outlet.index:
            return self.outlet
        else:
            raise ValueError('Index not found.')

    def get_link_coord_batch(self, df: DataFrame):
        """Get the coordinates of nodes by their category.

        Args:
            df (DataFrame): Data frame of link (conduit, pumps, ...)

        Returns:
            2d list: [([x1, y1], [x2, y2]), 
                        ([x1, y1], [x3, y3]), ...]
        """
        # link can be conduit, pump and so on.
        nodes1 = self.get_node_coord_batch(df.set_index('fromNode'))
        nodes2 = self.get_node_coord_batch(df.set_index('toNode'))
        coords = [(node1, node2) for node1, node2 in zip(nodes1, nodes2)]
        return coords

    def get_link_map_length(self, df: DataFrame):
        # df (DataFrame): Data frame of link (conduit, pumps, ...)
        coords = self.get_link_coord_batch(df)
        lengthMap = [((coord[0][0]-coord[1][0])**2+(coord[0][1]-coord[1][1])**2)**0.5
                     for coord in coords]
        lengthMap_sr = pd.Series(lengthMap, index=df.index)
        return lengthMap_sr

    def get_node_attr(self, nodeID, attr):
        if nodeID in self.junction.index:
            value = self.junction.at[nodeID, attr]
        elif nodeID in self.outfall.index:
            value = self.outfall.at[nodeID, attr]
        else:
            raise ValueError('My code has not been finished.')
        return value

    def get_link_slope(self, linkID):
        link = self.conduit.loc[linkID]
        node1, node2, length = link[['fromNode', 'toNode', 'length']].tolist()
        offset1, offset2 = link[['inOffset', 'outOffset']].tolist()
        elev1 = self.get_node_attr(node1, 'elevation')
        elev2 = self.get_node_attr(node2, 'elevation')
        slope = ((elev1+offset1)-(elev2+offset2))/length
        return slope

    def transect_parse(self, transectID):
        df = self.transect
        idx = df.index[df['1'] == transectID].tolist()[0]
        x, y = [], []
        for i in range(int(idx)+1, int(1e6)):
            row = df.loc[i].tolist()
            if row[0] != 'GR':
                break  # end of the section
            data = [item for item in row[1:] if item.strip() != '']
            for j, string in enumerate(data):
                value = float(string)
                if j % 2 == 0:
                    y.append(value)
                else:
                    x.append(value)
        return x, y

    def get_adj_link(self, nodeId) -> list:
        nodePairs = self.graph.edges(nodeId)
        linkIndices = [self.graph.get_edge_data(n1, n2)['linkIndex']
                       for n1, n2 in nodePairs]
        return linkIndices

    def get_downstream_link(self, linkId) -> list:
        """
        Get a list of downstream links of the inputed link.
        Usually length of the return list is only 1.
        """
        toNode = self.conduit.loc[linkId, 'toNode']
        linkIds = self.get_adj_link(toNode)
        downstreamLinkIds = [j for j in linkIds
                             if self.conduit.loc[j, 'fromNode'] == toNode]
        return downstreamLinkIds

    def extract_component_by_node(self, nodes):
        inpSub = SwmmInp('')
        inpSub.option = self.option
        inpSub.report = self.report
        inpSub.coordinate = self.coordinate.loc[nodes]
        junctions = list(set(nodes) & set(self.junction.index))
        inpSub.junction = self.junction.loc[junctions]
        outfalls = list(set(nodes) & set(self.outfall.index))
        inpSub.outfall = self.outfall.loc[outfalls]
        if len(junctions) + len(outfalls) < len(nodes):
            raise ValueError(
                "You forget some nodes. nodes: %d, junctions: %d, outfalls: %d-%s",
                (len(nodes), len(junctions), len(outfalls), outfalls[0]))
        subcatchs = self.subcatch[self.subcatch['outlet'].isin(nodes)].index
        inpSub.subcatch = self.subcatch.loc[subcatchs]
        inpSub.subarea = self.subarea.loc[subcatchs]
        raingages = set(inpSub.subcatch['raingage'].tolist())
        inpSub.raingage = self.raingage.loc[raingages]
        inpSub.timeseries = self.timeseries  # do we need to improve this?
        conduits = self.conduit[self.conduit['fromNode'].isin(nodes) |
                                self.conduit['toNode'].isin(nodes)].index

        inpSub.conduit = self.conduit.loc[conduits]
        inpSub.xsection = self.xsection.loc[conduits]
        return inpSub

    def create_graph_from_edge(self, field_start='fromNode',
                               field_end='toNode', printInfo=False):
        graph = nx.Graph()
        # ! in the future, other pumps and so on should be considered
        dfs = [self.conduit[[field_start, field_end]]]
        if self.pump != None:
            dfs.append(self.pump[[field_start, field_end]])
        if self.orifice != None:
            dfs.append(self.orifice[[field_start, field_end]])
        if self.weir != None:
            dfs.append(self.weir[[field_start, field_end]])
        if self.outlet != None:
            dfs.append(self.outlet[[field_start, field_end]])
        df_link = pd.concat(dfs)
        for iRow in df_link.index:
            row = df_link.loc[iRow]
            link = [row[field_start], row[field_end]]
            graph.add_edge(*link, linkIndex=iRow)  # unpack edge tuple*
        if printInfo:
            nx.get_edge_attributes(graph, 'edgeIndex')
            print('---Create Graph from Edges---')
            print('Number of component:', nx.number_connected_components(graph))
            print('Number of edges in the graph:', graph.number_of_edges())
        return graph

    def get_node_elevation(self, nodeId) -> float:
        if not nodeId in self.outfall.index:
            return self.junction.at[nodeId, 'elevation']
        else:
            return self.outfall.at[nodeId, 'elevation']


def call_swmm(f1, f2, f3):
    cwd = os.path.realpath(__file__)
    # print(cwd)
    path = '\\'.join(cwd.split('\\')[:-1])
    filename = path + '\\' + 'swmm5.dll'
    mydll = ctypes.cdll.LoadLibrary(filename)

    # set argument type
    mydll.swmm_run_sqlite.argtypes = [ctypes.c_char_p,
                                      ctypes.c_char_p, ctypes.c_char_p]

    mydll.swmm_run_sqlite(
        f1.encode('utf-8'),
        f2.encode('utf-8'),
        f3.encode('utf-8'))


def node_connected_component(graph, nodeID):
    nodeIDs = nx.node_connected_component(graph, nodeID)
    return nodeIDs
