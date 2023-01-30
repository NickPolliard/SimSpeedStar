import pandas
from datetime import datetime
from routines.connection import connect_mongo, connect_bq

def get_mongo_locations(collection):
    # if collection in ['customers', 'inventoryActivities']:
        # db = connect_mongo('meteor')
        # if collection == 'customers':
        #     pipeline = [
        #         {'$match': {'updatedAt': {'$gte': datetime(2017, 1, 1)}}},
        #         {'$project': {'clientId': 1, '_id': 0}}
        #     ]
        #     location_id = db[collection].aggregate(pipeline)
        #     results = pandas.DataFrame(location_id)
        #     results['clientId'] = results['clientId'].unique()
        # else:
        #     pipeline = [
        #         {'$match': {'updatedAt': {'$gte': datetime(2017, 1, 1)}}},
        #         {'$project': {'locationId': 1, '_id': 0}}
        #     ]
        #     location_id = db[collection].aggregate(pipeline)
        #     results = pandas.DataFrame(location_id)
        #     results['locationId'] = results['locationId'].unique()
        #
        # # distinct_ids = db[collection].distinct('locationId')
        # # if None in location_id:
        # #     location_id.remove(None)
        # return results

    # else:
    client = connect_bq()
    query_string = f"""SELECT DISTINCT locationId FROM pos.{collection} WHERE createdAt >= TIMESTAMP('2017-01-01')"""

    dataframe = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )
    return dataframe

def get_bq_locations(table):
    client = connect_bq()
    if table == 'Customers':
        query_string = f"""SELECT DISTINCT clientId FROM POSReporting.{table}"""
    else:
        query_string = f"""SELECT DISTINCT locationId FROM POSReporting.{table}"""

    dataframe = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )
    return dataframe

def get_locations_count(table_name):
    table = {'sales_1': 'Sales', 'itemsInCart_1': 'ItemsInCart',
             'discounts_1': 'Discounts', 'payments_1': 'Payments',
             'customers': 'Customers', 'inventoryActivities': 'InventoryActivities'}
    if table_name in ['payments_1']:
        mongo_table = 'sales_1'
    else:
        mongo_table = table_name
    mongo = get_mongo_locations(mongo_table)
    bq = get_bq_locations(table[table_name])
    print(table_name)
    print({'mongo': mongo.shape[0], 'bq': bq.shape[0]})
    return {'mongo': mongo.shape[0], 'bq': bq.shape[0]}

def check_clients():
    db = connect_mongo('meteor')
    mongo_data = db['clients'].distinct('_id')
    if None in mongo_data:
        mongo_data.remove(None)
    mongo_clients = pandas.DataFrame(list(mongo_data))

    client = connect_bq()
    query_string = f"""SELECT DISTINCT _id FROM POSReportingBackup.Clients"""

    bq_clients = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )
    print('clients')
    print({'mongo': mongo_clients.shape[0], 'bq': bq_clients.shape[0]})
    return {'mongo': mongo_clients, 'bq': bq_clients}


def check_locations():
    db = connect_mongo('meteor')
    mongo_data = db['locations'].distinct('_id')
    if None in mongo_data:
        mongo_data.remove(None)
    mongo_locations = pandas.DataFrame(list(mongo_data))

    client = connect_bq()
    query_string = f"""SELECT DISTINCT _id FROM POSReporting.Locations"""

    bq_locations = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )
    print('clients')
    print({'mongo': mongo_locations.shape[0], 'bq': bq_locations.shape[0]})
    return {'mongo': mongo_locations, 'bq': bq_locations}


def get_location_ids():
    db = connect_mongo('meteor')
    mongo_data = db['locations'].distinct('_id')
    if None in mongo_data:
        mongo_data.remove(None)
    mongo_locations = list(mongo_data)


    return mongo_locations


def get_dropdown_locations():
    client = connect_bq()
    query_string = '''SELECT 
  Locations._id,
  CONCAT('Client: ', Clients.name, ' - ', 'Location: ', Locations.name) as DisplayName
FROM POSReporting.Clients
INNER JOIN POSReportingBackup.Locations on Clients._id = Locations.clientId'''
    bq_locations = (
        client.query(query_string)
            .result()
            .to_dataframe()
    )


    return bq_locations

