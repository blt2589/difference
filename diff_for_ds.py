"""
Usage examples:
   ./process.py ownername_diff --state id --county franklin --ver_a county --ver_b rep --field owner_name
"""
import logging
import difflib
import string
import pandas as pd
import os
import time

from psycopg2 import sql
from settings import EXPORT_PATH

# from sqlalchemy import create_engine
# import io


log = logging.getLogger(__name__)


def description():
    return "Compares owner_name between 2 parcel datasets and gets percent " \
           "difference"


def df_to_csv(df, file_name):
    path = EXPORT_PATH + '/field_comparison_results'

    if not os.path.exists(path):
        os.makedirs(path)

    output = path + '/' + file_name
    df.to_csv(output, index=False)
    return output

# def csv_to_table(csv):
#     f = open(r'C:\Users\n\Desktop\data.csv', 'r')
#     cur.copy_from(f, temp_unicommerce_status, sep=',')


def args(subparser):
    subparser.add_argument('--state',
                           help='Enter state (ex. mt)')
    subparser.add_argument('--county',
                           help='Enter county (ex. gallatin)')
    subparser.add_argument('--ver_a',
                           help='Enter version of first table')
    subparser.add_argument('--ver_b',
                           help='Enter version of first table')
    subparser.add_argument('--field',
                           help='Enter field to compare differences')
    subparser.add_argument('--output',
                           help='Enter output table name')


# removes punctuation
def remove_punctuation(sentence):
    cleaned = sentence.translate(None, string.punctuation)
    nopunct = sorted_sentence(cleaned)
    return nopunct.upper()


# sorts sentence
def sorted_sentence(sentence):
    words = sentence.split(' ')
    words.sort()
    newSentence = ' '.join(words)
    return newSentence.strip()


def process(database_connection, args):
    """
    Usage examples:
       ./process.py ownername_diff --state id --county franklin --ver_a county --ver_b rep --field owner_name
    """
    state = args.state
    county = args.county
    table = 'parcel_{state}_{county}'.format(state=state, county=county)
    table_a = table + '$' + args.ver_a
    table_b = table + '$' + args.ver_b
    field = args.field
    output_table = args.output

    with database_connection.cursor as cursor:
        sql_query = """SELECT a.apn AS a_apn, a.{field} AS a_{field}, b.apn AS b_apn,  b.{field} AS b_{field}
              FROM {table_a} a
              INNER JOIN {table_b} b
              ON a.apn = b.apn
              """.format(table_a=table_a, table_b=table_b,
                         field=field, output=output_table)

        cursor.execute(sql.SQL(sql_query))

        df = pd.DataFrame(cursor.fetchall())
        df.sort_values(by=['a_apn'])



    df = df.fillna(value='NO VALUE')

    field_a = 'a_{}'.format(field)
    field_b = 'b_{}'.format(field)
    df[field_a] = df[field_a].apply(remove_punctuation)
    df[field_b] = df[field_b].apply(remove_punctuation)
    df['percent similar'] = df.apply(lambda x: difflib.SequenceMatcher(None, x[field_a], x[field_b]).ratio(), axis=1)

    # print(df)
    # timestamp = str(int(round(time.time() * 1000)))
    timestamp = str(time.strftime("%Y%m%d-%H%M"))
    file_name = '{state}_{county}_{field}_compare_{timestamp}.csv'\
        .format(state=state, county=county, field=field, timestamp=timestamp)

    output = df_to_csv(df, file_name)


    # with database_connection.cursor as cursor:
    #     f = open(output, 'r')
    #     cursor.copy_from(f, 'temp_comparison', sep=',')



    database_connection.commit()
