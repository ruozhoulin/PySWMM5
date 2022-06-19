from .inpfile import *


class Swmm2Gis:
    def __init__(self, swmmInp) -> None:
        self.crs = {'init': 'epsg:4326'}  # default value WSG 1984
        self.node = self.create_node(swmmInp)
        self.link = self.create_link(swmmInp)

    def create_node(self, swmmInp):
        junction = swmmInp.junction.copy()
        junction['objectType'] = 'junction'
        outfall = swmmInp.outfall.copy()
        outfall['objectType'] = 'outfall'
        # combine node objects
        frames = [junction, outfall]
        df = pd.concat(frames)
        df['coord'] = swmmInp.get_node_coord_batch(df)
        df['geometry'] = coord2geometry_node(df)
        return df

    def create_link(self, swmmInp):
        conduit = swmmInp.conduit.copy()
        conduit['objectType'] = 'conduit'
        # combine node objects
        frames = [conduit]
        df = pd.concat(frames)
        df['coord'] = swmmInp.get_link_coord_batch(df)
        df['geometry'] = coord2geometry_link(df)
        return df

    def create_geoDataFrame(self, df):
        gdf = gpd.GeoDataFrame(
            df, crs=self.crs,
            geometry=df['geometry'])
        return gdf

    def save(self, gdf, filename):
        gdf.to_file('%s.shp' % (filename), encoding='UTF-8')

    def save_all(self, prefix):
        # reset index to save node id
        gdf_node = self.node.reset_index()
        self.create_geoDataFrame(gdf_node).to_file(
            '%s_node.shp' % (prefix), encoding='UTF-8')
        self.create_geoDataFrame(self.link).to_file(
            '%s_link.shp' % (prefix), encoding='UTF-8')
        # self.link.to_file('%s_link.shp' % (prefix), encoding='UTF-8')
        # polygon
        print('All data are saved in .shp format. 2 files are created.')

    def adjust_get_scale(self, bound):
        minx0, miny0, maxx0, maxy0 = bound  # t: top, b: botto, l: left, r: right
        minx, miny, maxx, maxy = gpd.GeoSeries(
            self.link['geometry']).total_bounds
        assert (maxx-minx > 1e-4) and (maxy-miny > 1e-4)
        # raise ValueError('Denominator is close to zero!')
        xscale = (maxx0-minx0)/(maxx-minx)
        yscale = (maxy0-miny0)/(maxy-miny)
        return (xscale, yscale)

    def adjust_get_translation(self, bound):
        # distance of translation motion
        minx0, miny0, maxx0, maxy0 = bound
        minx, miny, maxx, maxy = gpd.GeoSeries(
            self.link['geometry']).total_bounds
        xc0 = (maxx0+minx0)/2
        yc0 = (maxy0+miny0)/2
        xc = (maxx+minx)/2
        yc = (maxy+miny)/2
        xTranslation = xc0 - (maxx+minx)/2
        yTranslation = yc0 - (maxy+miny)/2
        return (xTranslation, yTranslation, xc0, yc0)

    def adjust_node(self, scale, translation, swmmInp):
        xs, ys = scale  # scale of x, scale of y
        # translation of x and y
        # center coordinate of destination
        xt, yt, xc, yc = translation
        self.node['coord'] = swmmInp.get_node_coord_batch(self.node)
        # translation
        self.node['coord'] = [(xy[0]+xt, xy[1]+yt)
                              for i, xy in self.node['coord'].iteritems()]
        # scale
        self.node['coord'] = [(xc+(xy[0]-xc)*xs, yc+(xy[1]-yc)*ys)
                              for i, xy in self.node['coord'].iteritems()]
        # save coord to tmp inp
        swmmInp.coordinate = self.node['coord']
        # create geometry
        self.node['geometry'] = coord2geometry_node(self.node)

    def adjust_link(self, scale, translation, swmmInp):
        xs, ys = scale  # scale of x, scale of y
        # translation of x and y
        # center coordinate of destination
        xt, yt, xc, yc = translation
        self.link['coord'] = swmmInp.get_link_coord_batch(self.link)
        # create geometry
        self.link['geometry'] = coord2geometry_link(self.link)

    def spatial_adjustment(self, bound, swmmInp):
        """Achieve rough spatial adjustment for further manual adjustment
        in ArcMap. This can make sure the result is in an acceptable
         geographic coordinate system.

        Args:
            bound (tuple): minx, miny, maxx, maxy
            swmmInp (class): 
        """
        # copy orignal swmmInp for temporal modification
        inp = copy.copy(swmmInp)  # ! this is essential!
        scale = self.adjust_get_scale(bound)
        translation = self.adjust_get_translation(bound)
        self.adjust_node(scale, translation, inp)
        self.adjust_link(scale, translation, inp)


class Gis2Swmm:
    def __init__(self) -> None:
        pass
