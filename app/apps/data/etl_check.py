from routines.connection import connect_bq, connect_mongo
from datetime import datetime, timedelta
import pandas
import numpy
import os

def etl_tracking():
    client = connect_bq()
    query_string = f"""SELECT TableSet, MAX(CompletedDatetime) AS LastCompletedDate
FROM POSReportingBackup.ETLTracking GROUP BY TableSet"""

    dataframe = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )
    dataframe['LastCompletedDate'] = pandas.to_datetime(dataframe['LastCompletedDate']).dt.tz_localize(None)
    dataframe['isRunCurrent'] = numpy.where(datetime.today() >= dataframe['LastCompletedDate'] + timedelta(days=7), 'Behind', 'Current')
    return dataframe


def get_bq_table_count(table_name):
    client = connect_bq()
    if table_name in ['Locations', 'Clients']:
        query_string = f"SELECT COUNT(*) as row_count FROM POSReportingBackup.{table_name}Backup WHERE CreatedAt >= '2018-01-01'"
    else:
        query_string = f"SELECT COUNT(*) as row_count FROM POSReportingBackup.{table_name}WeeklyBackup WHERE CreatedAt >= '2018-01-01'"
    dataframe = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )

    return dataframe


def get_verify_count(table_name):
    client = connect_bq()
    query_string = f"SELECT SUM(Verify{table_name}Count) as row_count FROM POSReportingBackup.Verify{table_name} WHERE CreatedAt >= '2018-01-01'"
    dataframe = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )

    return dataframe

def get_verify_max_date(table_name):
    client = connect_bq()
    query_string = f"SELECT Max(CreatedAt) as MaxCreatedAt FROM POSReportingBackup.{table_name}WeeklyBackup"
    dataframe = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )

    return dataframe


def get_mongo_collection_count(collection_name, max_date=None):
    clientId = None
    find = {'createdAt': {'$gte': datetime(2018, 1, 1)}}
    if os.environ.get('GCP_PROJECT_ID') == 'flowhub-dev':
        clientId = 'k7f2vNEs8ab6Pbpu2'
    elif os.environ.get('GCP_PROJECT_ID') == 'flowhub-qa':
        clientId = 'k7f2vNEs8ab6Pbpu2'
    elif os.environ.get('GCP_PROJECT_ID') == 'flowhub-uat':
        clientId = 'k7f2vNEs8ab6Pbpu2'
    mongo = connect_mongo('meteor')
    if collection_name in ['locations', 'Clients']:
        clientId = None
    if clientId:
        find['clientId'] = clientId
    if max_date:
        find['createdAt']['$lte'] = max_date + timedelta(seconds=1)
    row_count = mongo[collection_name].find(find).count()
    dataframe =  pandas.DataFrame([{'row_count': row_count}])

    return dataframe


def check_locations_counts():
    bq = get_bq_table_count('Locations')
    mongo = get_mongo_collection_count('locations')
    return {'mongo': mongo['row_count'][0], 'bq': bq['row_count'][0]}


def check_sales_table_counts():
    bq = get_bq_table_count('Sales')
    max_date = pandas.to_datetime(get_verify_max_date('Sales')['MaxCreatedAt'][0])
    mongo = get_mongo_collection_count('sales', max_date)
    return {'mongo': mongo['row_count'][0], 'bq': bq['row_count'][0]}

def check_payments_counts():
    bq_table = get_bq_table_count('Payments')
    verify_count = get_verify_count('Payments')
    return {'mongo': verify_count['row_count'][0], 'bq': bq_table['row_count'][0]}


def check_items_counts():
    bq_table = get_bq_table_count('ItemsInCart')
    verify_count = get_verify_count('ItemsInCart')
    return {'mongo': verify_count['row_count'][0], 'bq': bq_table['row_count'][0]}


def check_customers_count():
    bq = get_bq_table_count('Customers')
    max_date = pandas.to_datetime(get_verify_max_date('Customers')['MaxCreatedAt'][0])
    mongo = get_mongo_collection_count('customers', max_date)
    return {'mongo': mongo['row_count'][0], 'bq': bq['row_count'][0]}


def check_customer_activities_count():
    bq = get_bq_table_count('CustomerActivities')
    max_date = pandas.to_datetime(get_verify_max_date('CustomerActivities')['MaxCreatedAt'][0])
    mongo = get_mongo_collection_count('customerActivities', max_date)
    return {'mongo': mongo['row_count'][0], 'bq': bq['row_count'][0]}


def check_inventory_activities_count():
    bq = get_bq_table_count('InventoryActivities')
    max_date = pandas.to_datetime(get_verify_max_date('InventoryActivities')['MaxCreatedAt'][0])
    mongo = get_mongo_collection_count('inventoryActivities', max_date)
    return {'mongo': mongo['row_count'][0], 'bq': bq['row_count'][0]}


def check_discounts_counts():
    bq_table = get_bq_table_count('Discounts')
    verify_count = get_verify_count('Discounts')
    return {'mongo': verify_count['row_count'][0], 'bq': bq_table['row_count'][0]}

