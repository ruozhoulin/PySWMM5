import pandas as pd
import geopandas as gpd
import shapely.geometry as spg


def text2dataframe(content):
    """Create data frame without meaningful headers

    Args:
        content (list): [description]

    Returns:
        dataframe: [description]
    """
    data = [line.strip().split() for line in content]
    df = pd.DataFrame(data)
    # df.set_index(0, inplace=True)
    return df


def rpt_text2dataframe(content):
    """Create data frame without meaningful headers

    Args:
        content (list): [description]

    Returns:
        dataframe: [description]
    """
    data = [line.strip().split() for line in content]
    dataLength = [len(line) for line in data]
    lengthSet = len(set(dataLength))
    if lengthSet == 1:
        df = pd.DataFrame(data)
        # df.set_index(0, inplace=True)
        return df
    else:
        raise ValueError(
            'Length of data is not consistent: %s. '
            'This may caused by very large numbers.' % (lengthSet))


def sect_option(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'value']
    df.set_index('name', inplace=True)
    swmmInp.option = df


def sect_raingage(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 6:
        # infile time series
        df.columns = ['name', 'format', 'interval',
                      'scf', 'source1', 'source2']
        df['source'] = df['source1']+' '+df['source2']
        df.drop(['source1', 'source2'], axis=1, inplace=True)
    elif len(df.columns) == 8:
        # external time series
        df.columns = ['name', 'format', 'interval',
                      'scf', 'src1', 'src2', 'src3', 'src4']
        df['source'] = df['src1']+' '+df['src2'] + \
            ' ' + df['src3']+' ' + df['src4']
        df.drop(['src1', 'src2', 'src3', 'src4'], axis=1, inplace=True)

    df.set_index('name', inplace=True)
    # set data type
    df['scf'] = df['scf'].astype('float', copy=False)
    swmmInp.raingage = df


def sect_subcatch(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 8:
        df.columns = ['name', 'raingage', 'outlet',
                      'area', 'imperv', 'width', 'slope', 'curblen']
    else:
        df.columns = ['name', 'raingage', 'outlet',
                      'area', 'imperv', 'width', 'slope', 'curblen', 'snowpack']
    df.set_index('name', inplace=True)
    # set data type
    df['area'] = df['area'].astype('float', copy=False)
    df['imperv'] = df['imperv'].astype('float', copy=False)
    df['width'] = df['width'].astype('float', copy=False)
    df['slope'] = df['slope'].astype('float', copy=False)
    df['curblen'] = df['curblen'].astype('float', copy=False)
#    df['snowpack'].astype('float', copy=False)
    swmmInp.subcatch = df


def sect_subarea(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 7:
        df.columns = ['name', 'nImperv', 'nPerv',
                      'sImperv', 'sPerv', 'pctZero', 'routeTo']
    else:
        df.columns = ['name', 'nImperv', 'nPerv',
                      'sImperv', 'sPerv', 'pctZero', 'routeTo', 'pctRouted']
    df.set_index('name', inplace=True)
    # set data type
    df['nImperv'] = df['nImperv'].astype('float', copy=False)
    df['nPerv'] = df['nPerv'].astype('float', copy=False)
    df['sImperv'] = df['sImperv'].astype('float', copy=False)
    df['sPerv'] = df['sPerv'].astype('float', copy=False)
    df['pctZero'] = df['pctZero'].astype('float', copy=False)
#    df['pctRouted'].astype('float', copy=False)
    swmmInp.subarea = df


def sect_infiltration(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'maxRate', 'minRate',
                  'decay', 'dryTime', 'maxInfil']
    df.set_index('name', inplace=True)
    # set data type
    df['maxRate'] = df['maxRate'].astype('float', copy=False)
    df['minRate'] = df['minRate'].astype('float', copy=False)
    df['decay'] = df['decay'].astype('float', copy=False)
    df['dryTime'] = df['dryTime'].astype('float', copy=False)
    df['maxInfil'] = df['maxInfil'].astype('float', copy=False)
    swmmInp.infiltration = df


def sect_junction(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'elevation', 'maxDepth',
                  'initDepth', 'surDepth', 'aponded']
    df.set_index('name', inplace=True)
    # set data type
    df['elevation'] = df['elevation'].astype('float', copy=False)
    df['maxDepth'] = df['maxDepth'].astype('float', copy=False)
    df['initDepth'] = df['initDepth'].astype('float', copy=False)
    df['surDepth'] = df['surDepth'].astype('float', copy=False)
    df['aponded'] = df['aponded'].astype('float', copy=False)
    swmmInp.junction = df


def sect_outfall(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 4:
        df.columns = ['name', 'elevation', 'type', 'gated']
    else:
        raise ValueError('Coding not finished.')
    df.set_index('name', inplace=True)
    # set data type
    df['elevation'] = df['elevation'].astype('float', copy=False)
    swmmInp.outfall = df


def sect_conduit(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'fromNode', 'toNode', 'length', 'roughness',
                  'inOffset', 'outOffset', 'initFlow', 'maxFlow']
    df.set_index('name', inplace=True)
    # set data type
    df['length'] = df['length'].astype('float', copy=False)
    df['roughness'] = df['roughness'].astype('float', copy=False)
    df['inOffset'] = df['inOffset'].astype('float', copy=False)
    df['outOffset'] = df['outOffset'].astype('float', copy=False)
    df['initFlow'] = df['initFlow'].astype('float', copy=False)
    df['maxFlow'] = df['maxFlow'].astype('float', copy=False)
    swmmInp.conduit = df


def sect_xsection(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 7:
        df.columns = ['name', 'shape', 'geom1', 'geom2', 'geom3',
                      'geom4', 'barrels']
    else:
        raise ValueError('Coding not finished.')
    df.set_index('name', inplace=True)
    # set data type
    df.fillna('', inplace=True)

    try:
        df['geom1'] = df['geom1'].astype('float', copy=False)
        df['geom2'] = df['geom2'].astype('float', copy=False)
    except:
        pass
    df['geom3'] = df['geom3'].astype('float', copy=False)
    df['geom4'] = df['geom4'].astype('float', copy=False)
    # df['barrels'] = df['barrels'].astype('float', copy=False)
    swmmInp.xsection = df


def sect_transect(swmmInp, content):
    # Transect Data in HEC-2 format
    df = text2dataframe(content)
    df.fillna('', inplace=True)
    df.columns = [str(value) for value in df.columns]
    swmmInp.transect = df


def sect_inflow(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 6:
        df.columns = ['name', 'constituent',
                      'fSeries', 'type', 'mFactor', 'sFactor']
    else:
        raise ValueError('Coding not finished.')
    df.set_index('name', inplace=True)
    # set data type
    df['mFactor'] = df['mFactor'].astype('float', copy=False)
    df['sFactor'] = df['sFactor'].astype('float', copy=False)
    swmmInp.inflow = df


def sect_timeseries(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 3:
        df.columns = ['name', 'time', 'value']
    else:
        raise ValueError('Coding not finished.')
    df.set_index('name', inplace=True)
    # set data type
    df['value'] = df['value'].astype('float', copy=False)
    swmmInp.timeseries = df


def sect_report(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) == 2:
        df.columns = ['name', 'option']
    else:
        raise ValueError('Coding not finished.')
    df.set_index('name', inplace=True)
    swmmInp.report = df


def sect_coordinate(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'x', 'y']
    df.set_index('name', inplace=True)
    # set data type
    df['x'] = df['x'].astype('float', copy=False)
    df['y'] = df['y'].astype('float', copy=False)
    swmmInp.coordinate = df


def sect_polygon(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'x', 'y']
    df.set_index('name', inplace=True)
    # set data type
    df['x'] = df['x'].astype('float', copy=False)
    df['y'] = df['y'].astype('float', copy=False)
    swmmInp.polygon = df


def sect_symbol(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'x', 'y']
    df.set_index('name', inplace=True)
    # set data type
    df['x'] = df['x'].astype('float', copy=False)
    df['y'] = df['y'].astype('float', copy=False)
    swmmInp.symbol = df


def sect_storage(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    if len(df.columns) != 6:
        for irow in df.index:
            row = df.loc[irow]
            if row[4] == 'FUNCTIONAL':  # row[0] is name
                df.loc[irow, 5] = '%s %s %s' % (row[5], row[6], row[7])
                df.loc[irow, 6] = row[8]
                df.loc[irow, 7] = row[9]
        df.drop([8, 9], axis=1, inplace=True)
        df.fillna(0, inplace=True)
        # set data type
        df.columns = ['name', 'elevation', 'maxDepth', 'initDepth', 'shape',
                      'curve', 'na', 'fevap']
    else:
        df.columns = ['name', 'elevation', 'maxDepth', 'initDepth', 'shape',
                      'curve']

    df.set_index('name', inplace=True)
    df['elevation'] = df['elevation'].astype('float', copy=False)
    df['maxDepth'] = df['maxDepth'].astype('float', copy=False)
    df['initDepth'] = df['initDepth'].astype('float', copy=False)
    # df['na'] = df['na'].astype('float', copy=False)
    # df['fevap'] = df['fevap'].astype('float', copy=False)
    swmmInp.storage = df


def sect_pump(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'fromNode', 'toNode',
                  'curve', 'initStatus', 'startupDepth', 'shutoffDepth']
    df.set_index('name', inplace=True)
    # set data type
    df['startupDepth'] = df['startupDepth'].astype('float', copy=False)
    df['shutoffDepth'] = df['shutoffDepth'].astype('float', copy=False)
    swmmInp.pump = df


def sect_orifice(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'fromNode', 'toNode',
                  'type', 'offset', 'Qcoeff', 'gated', 'closeTime']
    df.set_index('name', inplace=True)
    # set data type
    df['offset'] = df['offset'].astype('float', copy=False)
    df['Qcoeff'] = df['Qcoeff'].astype('float', copy=False)
    df['closeTime'] = df['closeTime'].astype('float', copy=False)
    swmmInp.orifice = df


def sect_weir(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'fromNode', 'toNode',
                  'type', 'crestHt', 'Qcoeff', 'gated', 'endCon', 'endCoeff', 'surcharge']
    df.set_index('name', inplace=True)
    # set data type
    df['crestHt'] = df['crestHt'].astype('float', copy=False)
    df['Qcoeff'] = df['Qcoeff'].astype('float', copy=False)
    df['endCon'] = df['endCon'].astype('float', copy=False)
    df['endCoeff'] = df['endCoeff'].astype('float', copy=False)
    swmmInp.weir = df


def sect_outlet(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'fromNode', 'toNode', 'offset',
                  'type', 'Qcoeff', 'gated']
    df.set_index('name', inplace=True)
    # set data type
    df['offset'] = df['offset'].astype('float', copy=False)
    swmmInp.outlet = df


def sect_loss(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'Kentry', 'Kexit', 'Kavg',
                  'gated', 'seepage']
    df.set_index('name', inplace=True)
    # set data type
    df['Kentry'] = df['Kentry'].astype('float', copy=False)
    df['Kexit'] = df['Kexit'].astype('float', copy=False)
    df['Kavg'] = df['Kavg'].astype('float', copy=False)
    swmmInp.loss = df


def sect_control(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'Kentry', 'Kexit', 'Kavg',
                  'gated', 'seepage']
    df.set_index('name', inplace=True)
    # set data type
    df.fillna('', inplace=True)
    df.columns = [str(value) for value in df.columns]
    swmmInp.control = df


def sect_dwf(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'constituent', 'baseline', 'patterns']
    df.set_index('name', inplace=True)
    # set data type
    df['baseline'] = df['baseline'].astype('float', copy=False)
    swmmInp.dwf = df


def sect_curve(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'type', 'x', 'y']
    df.set_index('name', inplace=True)
    # set data type
    df.fillna('', inplace=True)
    # df['x'] = df['x'].astype('float', copy=False)
    # df['y'] = df['y'].astype('float', copy=False)
    swmmInp.curve = df


def sect_pattern(swmmInp, content):
    df = text2dataframe(content)
    # set column names
    df.columns = ['name', 'type', '1', '2', '3', '4', '5', '6']
    df.set_index('name', inplace=True)
    # set data type
    df.fillna('', inplace=True)
    # df['1'] = df['1'].astype('float', copy=False)
    # df['2'] = df['2'].astype('float', copy=False)
    # df['3'] = df['3'].astype('float', copy=False)
    # df['4'] = df['4'].astype('float', copy=False)
    # df['5'] = df['5'].astype('float', copy=False)
    # df['6'] = df['6'].astype('float', copy=False)
    swmmInp.pattern = df


def sect_report_default():
    df = pd.DataFrame(
        {'name': ['INPUT', 'CONTINUITY', 'FLOWSTATS', 'CONTROLS', 'SUBCATCHMENTS',
                  'NODES', 'LINKS'],
         'option': ['NO', 'YES', 'YES', 'NO', 'ALL', 'ALL', 'ALL']})
    # set column names
    df.set_index('name', inplace=True)
    return df


def sect2text_(section, name):
    """Convert data in data frame format to printable string.

    Args:
        section (dataframe): A data frame
        name (str): The name of the section

    Returns:
        [str]: [a very long string]
    """
    sectTitle = '[%s]\n' % (name)
    if section.index.name == 'name':
        df = section.reset_index()
    else:
        df = section
    # set print cell format
    strCellName = '%25s'
    if name == 'OPTIONS' or name == 'RAINGAGES':
        strCell = '%25s'
    else:
        strCell = '%15s'
    # convert
    header = tuple(df.columns.tolist())
    data = strCell*len(header) % header + '\n'
    for i, row in df.iterrows():
        items = tuple(row.tolist())
        if None in items:
            continue  # options may have empty lines resulting in None
        data += strCell*len(items) % items + '\n'
    content = sectTitle + ';;' + data + '\n\n'
    return content


def sect2text(section, name):
    """Convert data in data frame format to printable string.

    Args:
        section (dataframe): A data frame
        name (str): The name of the section

    Returns:
        [str]: [a very long string]
    """
    sectTitle = '[%s]\n' % (name)
    if section.index.name == 'name':
        df = section.reset_index()
    else:
        df = section

    # set print cell format
    strCells = ''
    for (columnName, columnData) in df.iteritems():
        sizeHeader = len(columnName)
        sizeData = columnData.astype('str').str.len().max()
        sizeCell = max(sizeHeader, sizeData) + 3
        strCell = '%%%ds' % (sizeCell)  # format print template
        strCells += strCell  # cell size for print

    columns = tuple(df.columns.tolist())
    header = strCells % columns + '\n'
    header = header[2:]  # drop first two char
    data = ''
    for i, row in df.iterrows():
        # items = tuple(row.tolist())
        # use tuple to format a string later
        items = tuple('%.3f' % (item) if type(item) == float
                      else item for item in row.tolist())
        if None in items:
            continue  # options may have empty lines resulting in None
        data += strCells % items + '\n'
    content = sectTitle + ';;' + header + data + '\n\n'
    return content


'''
def sect2text_oldversion(section, name):
    sectTitle = '[%s]\n' % (name)
    if section.index.name == 'name':
        data = section.to_csv(sep=' ', index=True, line_terminator='\n')
    else:
        data = section.to_csv(sep=' ', index=False, line_terminator='\n')
    content = sectTitle + ';;' + data + '\n\n'
    return content
'''


def create_inpfile_content(swmm):
    warning = 'Warning: save %s section failed.'
    content = ''
    # ! nodes must be listed before links
    try:
        content += sect2text(swmm.option, 'OPTIONS')
    except:
        print('Warning: save OPTIONS section failed.')
    try:
        content += sect2text(swmm.report, 'REPORT')
    except:
        print('Warning: save REPORT section failed.')
    try:
        content += sect2text(swmm.raingage, 'RAINGAGES')
    except:
        print('Warning: save RAINGAGES section failed.')
    try:
        content += sect2text(swmm.subcatch, 'SUBCATCHMENTS')
    except:
        print('Warning: save SUBCATCHMENTS section failed.')
    try:
        content += sect2text(swmm.subarea, 'SUBAREAS')
    except:
        print('Warning: save SUBAREAS section failed.')
    try:
        content += sect2text(swmm.infiltration, 'INFILTRATION')
    except:
        print('Warning: save INFILTRATION section failed.')
    try:
        content += sect2text(swmm.junction, 'JUNCTIONS')
    except:
        print('Warning: save JUNCTIONS section failed.')
    try:
        content += sect2text(swmm.outfall, 'OUTFALLS')
    except:
        print('Warning: save OUTFALLS section failed.')
    try:
        content += sect2text(swmm.storage, 'STORAGE')
    except:
        print('Warning: save SYMBOLS section failed.')
    try:
        content += sect2text(swmm.conduit, 'CONDUITS')
    except:
        print('Warning: save CONDUITS section failed.')
    try:
        content += sect2text(swmm.xsection, 'XSECTIONS')
    except:
        print('Warning: save XSECTIONS section failed.')
    try:
        content += sect2text(swmm.transect, 'TRANSECTS')
    except:
        print('Warning: save TRANSECTS section failed.')
    try:
        content += sect2text(swmm.inflow, 'INFLOWS')
    except:
        print('Warning: save INFLOWS section failed.')
    try:
        content += sect2text(swmm.timeseries, 'TIMESERIES')
    except:
        print('Warning: save TIMESERIES section failed.')
    try:
        content += sect2text(swmm.coordinate, 'COORDINATES')
    except:
        print('Warning: save COORDINATES section failed.')
    try:
        content += sect2text(swmm.polygon, 'Polygons')
    except:
        print('Warning: save Polygons section failed.')
    try:
        content += sect2text(swmm.symbol, 'SYMBOLS')
    except:
        print('Warning: save SYMBOLS section failed.')
    try:
        content += sect2text(swmm.pump, 'PUMPS')
    except:
        print('Warning: save PUMPS section failed.')
    try:
        content += sect2text(swmm.orifice, 'ORIFICES')
    except:
        print('Warning: save ORIFICES section failed.')
    try:
        content += sect2text(swmm.weir, 'WEIRS')
    except:
        print('Warning: save WEIRS section failed.')
    try:
        content += sect2text(swmm.outlet, 'OUTLETS')
    except:
        print('Warning: save OUTLETS section failed.')
    try:
        content += sect2text(swmm.loss, 'LOSSES')
    except:
        print('Warning: save LOSSES section failed.')
    try:
        content += sect2text(swmm.control, 'CONTROLS')
    except:
        print('Warning: save CONTROLS section failed.')
    try:
        content += sect2text(swmm.dwf, 'DWF')
    except:
        print('Warning: save DWF section failed.')
    try:
        content += sect2text(swmm.curve, 'CURVES')
    except:
        print('Warning: save CURVES section failed.')
    try:
        content += sect2text(swmm.pattern, 'PATTERNS')
    except:
        print('Warning: save PATTERNS section failed.')

    return content


def add_content(content, contentAppend, sectionName):
    try:
        content += sect2text(contentAppend, sectionName)
    except:
        print('Warning: save %s section failed.' % (sectionName))


def coord2geometry_link(df):
    geometry = [spg.LineString(nodePair)
                for nodePair in df['coord']]
    df.drop('coord', axis=1, inplace=True)
    return geometry


def coord2geometry_node(df):
    geometry = [spg.Point(x, y) for x, y in df['coord']]
    df.drop('coord', axis=1, inplace=True)
    return geometry


def get_conduit_slope(swmm, index):
    cd = swmm.conduit.loc[index]
    elevFrom = swmm.junction.loc[cd['fromNode'], 'elevation']
    if cd['toNode'] in swmm.junction.index:
        elevTo = swmm.junction.loc[cd['toNode'], 'elevation']
    elif cd['toNode'] in swmm.outfall.index:
        elevTo = swmm.outfall.loc[cd['toNode'], 'elevation']
    else:
        raise ValueError('Code not finished')
    #
    rise = (elevFrom + cd['inOffset']) - (elevTo + cd['outOffset'])
    sr_slope = rise / cd['length']
    return sr_slope


def putoff_time_hm(stringTime, timeLag):
    # expected format: '12:11' ('hours:min')
    hour, minute = list(map(int, stringTime.split(':')))
    hour += timeLag
    newTime = '%02d:%02d' % (hour, minute)
    return newTime


def putoff_time_hms(stringTime, timeLag):
    # expected format: '12:11' ('hours:min')
    h, m, s = list(map(int, stringTime.split(':')))
    h += timeLag
    newTime = '%02d:%02d:%02d' % (h, m, s)
    return newTime


def extend_time_hm(df, timeExtend, step=1):
    name = df.index[0]
    value = df['value'][0]
    timeStart = df['time'][-1]
    df1 = pd.DataFrame({}, columns=['name', 'time', 'value'])
    for i in range(timeExtend):
        time = putoff_time_hm(timeStart, i+1)
        row = [name, time, value]
        df1.loc[i] = row
    df1.set_index('name', inplace=True)
    return df1


def empty_func(swmmInp, content):
    pass


def create_curve_pump(names, xs, ys, curveTypes='Pump2'):
    df = pd.DataFrame({'name': names,
                       'type': curveTypes,
                       'x': xs,
                       'y': ys})
    df.set_index('name', inplace=True)
    return df


def create_pump(names, node1, node2, pumpCurves, status='ON', startupDepth=0, shutoffDepth=0):
    df = pd.DataFrame({'name': names,
                       'fromNode': node1,
                       'toNode': node2,
                       'curve': pumpCurves,
                       'initStatus': status,
                       'startupDepth': startupDepth,
                       'shutoffDepth': shutoffDepth})
    df.set_index('name', inplace=True)
    return df
