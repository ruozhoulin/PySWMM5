'''
Left rpt section behind, we can read source code of what others did first and learn something from them.
After that, writing these codes could be faster, more efficient and meaningful.

Above all, if my supervisor does not support this idea, it is meaningless for me to do this.
'''
from .classfunc import *
import pandas as pd
from io import StringIO
import sqlite3


class SwmmRpt:
    def __init__(self, filename) -> None:
        self.connection = sqlite3.connect(filename)
        self.timeseries = self.get_timeseries()  # Pandas dataframe
        self.objIdx = self.get_objIdx()  # Pandas dataframe

    def get_timeseries(self):
        # format SWMM report time from plain text to better format
        sql = "SELECT * from timePeriod;"
        df_time = pd.read_sql_query(sql, self.connection)
        series = pd.to_datetime(df_time['date'] + ' ' + df_time['time'])
        return series

    def get_objIdx(self):
        sql = "SELECT * from ObjIdx;"
        df = pd.read_sql_query(sql, self.connection)
        return df

    def summary_node_flood(self):
        df = pd.read_sql_query(
            "SELECT * from nodeFloodSummary", self.connection)
        df.set_index('name', inplace=True)
        return df

    def summary_subcatch_runoff(self):
        df = pd.read_sql_query(
            "SELECT * from subcatchRunoffSummary", self.connection)
        df.set_index('name', inplace=True)
        return df

    def get_result_timeseries(self, objName, objType):
        """
        This function is efficient if you want to access several objects.
        However, you should choose another function that could read all
        objects at the same time if you want to access most of the objects.
        """
        # get idx corresponds to object name
        # Use () to create a one-line long string
        con = self.connection
        row = self.objIdx[(self.objIdx['objName'] == objName) &
                          (self.objIdx['objType'] == objType)]
        # check if sql succeed.
        assert not row.empty, 'SQL fails to find what you want!'
        idx = row['objIdx']
        # sql
        sql = "SELECT * from %s WHERE objIdx=%d;" % (objType.capitalize(), idx)
        # return 0
        df = pd.read_sql_query(sql, con).drop('objIdx', axis=1)
        df['period'] = self.timeseries
        return df

    def get_flood_node(self, factor=300):
        # 300 = 5 minutes * 60 seconds
        # the value of the factor depends on your report steps.
        sql = "SELECT * from Node WHERE 'flooding'>0;"
        df = pd.read_sql_query(sql, self.connection)
        df_flood = df.groupby('objIdx').sum()
        sr = pd.Series(df_flood['flooding'],
                       index=df_flood['objIdx'], name='floodVolume')
        return sr

    def summary_from_result(self, field, factor):
        indices = list(self.result.node.keys())
        values = [factor * self.result.node[idx][field].sum()
                  for idx in indices]
        sr = pd.Series(values, index=indices)
        return sr

    def print_compuation_error(self):
        v1 = self.summary.continuity.runoffQuantity.at[
            'Continuity Error (%)', 'volume']
        v2 = self.summary.continuity.flowRouting.at[
            'Continuity Error (%)', 'volume1']
        print('Continuity Error:\n'
              '-- Runoff quantity: %6.2f%%\n'
              '-- Flow routing: %6.2f%%'
              % (v1, v2))
