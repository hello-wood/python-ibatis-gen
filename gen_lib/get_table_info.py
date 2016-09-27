# coding=utf-8
import pymysql
from config.sql_config import *
from table_info.field_info import FieldInfo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_table_info():

    connect = pymysql.connect(connect_config['url'], connect_config['user'],
                              connect_config['password'], connect_config['db'],
                              charset=gen_config['charset'])
    cursor = connect.cursor()
    cursor.execute("show full columns from %s" % gen_config['table'])

    table_field_info = []
    for row in cursor.fetchall():
        index = row[1].find('(')
        if index > 0:
            field_type = row[1][0:index]
        else:
            field_type = row[1]

        table_field_info.append(FieldInfo(row[0], field_type, row[8], row[4] == 'PRI'))
    return table_field_info

