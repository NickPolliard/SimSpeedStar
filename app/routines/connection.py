from google.cloud import bigquery
from pymongo import MongoClient
from simple_salesforce import Salesforce

import ssl
import dns
import os


def connect_bq(is_magic=False):
    """
    A function that connects to Google BigQuery and returns a client (if magic is True)
    :is_magic: A bool that idicates if the connection is made through Jupyter magic commands.
    :return: A BigQuery connection client. Use client.query(query).to_dataframe() to return a query in a dataframe.
    """
    if is_magic:
        bq_client = None
    else:
        project_id = os.environ.get('GCP_PROJECT_ID')
        bq_client = bigquery.Client(project=project_id)
        print('GCP project id set to', project_id)

    return bq_client


def connect_mongo(db_name, connection_string=None):
    """
    A function that connects to Mongo and returns a client
    :param db_name: The name of the database to connect
    :param connection_string: The connection string that will overwrite the default one.
    :return: A Mongo connection client. Use client[collection].find({}) to query a collection.
    """
    if connection_string:
        url = connection_string
    else:
        url = os.environ.get('MONGO_URL')
    client = MongoClient(url, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    mongo_client = client[db_name]
    rs = client._MongoClient__options.__dict__['_ClientOptions__options']['replicaset']
    print('Connected to Mongo replicaset', rs)
    return mongo_client


def connect_sfdc():
    """
    A function that connects to Salesforce and returns a client
    :return: A Salesforce connecion client. Use client.query(query) to run a SOQL query.
    """
    user = os.environ.get('SF_USER')
    sfdc_client = Salesforce(username=user, password=os.environ.get('SF_PASSWORD'),
                             security_token=os.environ.get('SF_TOKEN'))
    print('Connected to Salesforce with user', user)
    return sfdc_client
