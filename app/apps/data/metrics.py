from routines.connection import connect_bq, connect_mongo
from datetime import datetime, timedelta
import pandas

def get_pos_max_date(collection):
    old_table_name = {'Sales': 'sales_1',
                      'ItemsInCart': 'itemsInCart_1',
                      'Discounts': 'discounts_1',
                      'Payments': 'payments_1'}
    client = connect_bq()
    query = f'SELECT MAX(createdAt) AS CreatedAt FROM pos.{old_table_name[collection]}'
    try:
        try:
            result = client.query(query).result().to_dataframe()
        except Exception as e:
            raise
        if not result:
            query = f'SELECT MAX(createdAt) AS CreatedAt FROM pos.{old_table_name[collection]}'
            query = query.replace('_1', '_2')
            result = client.query(query).result().to_dataframe()
    except:
        raise

    max_date = result['CreatedAt'].dt.tz_localize(None).to_list()[0]
    return max_date


def get_reporting_max_date(collection, dataset):
    if dataset == 'Weekly':
        table_name = f'POSReportingBackup.{collection}WeeklyBackup'
    elif dataset == 'Backup':
        table_name = f'POSReportingBackup.{collection}Backup'
    else:
        table_name = f'POSReporting.{collection}'
    client = connect_bq()
    query = f'SELECT MAX(createdAt) AS CreatedAt FROM {table_name}'
    result = client.query(query).result().to_dataframe()
    max_date = result['CreatedAt'].to_list()[0]
    return max_date


def get_bq_count(collection, locationId, table_id):
    table = 'Sales'
    if collection == 'sales':
        table = 'Sales'
    elif collection == 'payments':
        table = 'Payments'
    elif collection == 'discounts':
        table = 'Discounts'
    elif collection == 'itemsInCart':
        table = 'ItemsInCart'
    client = connect_bq()
    if table_id == 'Weekly':
        table_name = f'POSReportingBackup.{table}WeeklyBackup'
    elif table_id == 'Backup':
        table_name = f'POSReportingBackup.{table}Backup'
    else:
        table_name = f'POSReporting.{table}'
    if not locationId:
        query = f'SELECT COUNT(*) as Total FROM {table_name}'
    else:
        query = f'SELECT COUNT(*) as Total FROM {table_name} WHERE locationId = "{locationId}"'
    results = client.query(query).result().to_dataframe()
    return results['Total'][0]


def get_mongo_count(collection, locationId):
    results = 0
    mongo = connect_mongo('meteor')
    if not locationId:
        filter = {}
    else:
        filter = {'locationId': locationId}
    if not collection:
        collection = 'sales'
    elif collection == 'itemInCart':
        pipeline = [
            {'$match': {'locationId': locationId}},
            {'$project': {'_id': 1}},
            {'$unwind': '$itemsInCart'}
        ]
        results = mongo['sales'].aggregate(pipeline)
        df = pandas.DataFrame(list(results))
        return df['_id'].size
    elif collection == 'discounts':
        pipeline = [
            {'$match': {'locationId': locationId}},
            {'$project': {'_id': 1}},
            {'$unwind': '$itemsInCart'},
            {'$unwind': '$itemsInCart.itemDiscounts'}
        ]
        results = mongo['sales'].aggregate(pipeline)
        df = pandas.DataFrame(list(results))
        return df['_id'].size

    elif collection == 'payments':
        pipeline = [
            {'$match': {'locationId': locationId}},
            {'$project': {'_id': 1}},
            {'$unwind': '$payments'},
        ]
        results = mongo['sales'].aggregate(pipeline)
        df = pandas.DataFrame(list(results))
        return df['_id'].size

    else:
        collection = collection
        results = mongo[collection].count_documents(filter=filter)
    return results


def get_location_detail_view(collection='Sales', dataset=None, max_date=None):
    old_table_name = {'Sales': 'sales_1', 'ItemsInCart': 'itemsInCart_1', 'Discounts': 'discounts_1', 'Payments': 'payments_1'}
    if collection == 'Payments':
        return pandas.DataFrame()
    client = connect_bq()
    if dataset == 'Weekly':
        table_name = f'POSReportingBackup.{collection}WeeklyBackup'
    elif dataset == 'Backup':
        table_name = f'POSReportingBackup.{collection}Backup'
    else:
        table_name = f'POSReporting.{collection}'

    if max_date:
        where_stmt = f"createdAt BETWEEN TIMESTAMP('2017-01-01') AND TIMESTAMP('{max_date}')"
    else:
        where_stmt = f"createdAt >= TIMESTAMP('2017-01-01')"
    query = f'''
    WITH bak as ( 
SELECT MAX(CreatedAt) as MaxCreatedAt, Min(CreatedAt) as MinCreatedAt, locationId, count(*) AS TotalBakRows
FROM {table_name}
WHERE {where_stmt}
GROUP BY locationId
), 
pos AS (
SELECT locationId, Count(*) AS TotalPOSRows, MAX(CreatedAt) as MaxPOSCreatedAt, MIN(CreatedAt) as MinPOSCreatedAt 
FROM pos.{old_table_name[collection]}
WHERE {where_stmt}
GROUP BY locationId
)
SELECT pos.locationId, location.name, pos.TotalPOSRows, bak.TotalBakRows, bak.MaxCreatedAt, bak.MinCreatedAt
FROM pos
LEFT JOIN bak on pos.locationId = bak.locationId
INNER JOIN POSReporting.Locations location on pos.locationId = location._id
    '''
    return client.query(query).result().to_dataframe()



def get_total_sales(locationId=None):
    client = connect_bq()
    if not locationId:
        return pandas.DataFrame(columns=['locationID', 'SalesMonth', 'CartTotal'])

    table_name = f'DataMarts.SalesMetrics'
    todays_year = datetime.today().year

    query = f'''SELECT SUM(cartTotalInDollars) AS CartTotal 
FROM DataMarts.SalesMetrics
WHERE locationId = '{locationId}'
  AND createdAt >= '{todays_year}-01-01'

    '''
    return client.query(query).result().to_dataframe()

