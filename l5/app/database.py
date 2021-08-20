import os

#from influxdb_client import InfluxDBClient
from influxdb import InfluxDBClient
import datetime


class InfluxDB:
    def __init__(self, 
                 database_name='subreddit_funny_database', 
                 table_name='submissions'):
        self.database_name = database_name
        self.table_name = table_name
        
        self.client = InfluxDBClient(host=os.environ["INFLUXDB_HOST"], port=os.environ["INFLUXDB_PORT"], username=os.environ["INFLUXDB_USERNAME"], password=os.environ["INFLUXDB_PASSWORD"], database=self.database_name)

        #self.client.drop_database(self.database_name)
        self.client.create_database(self.database_name)
        self.client.switch_database(self.database_name)
    

    def insert_data(self, submission_data):
        json_body = [{
                        'measurement': self.table_name,
                        'tags': {'id': submission_data['post_id']},
                        "time": datetime.datetime.now(),
                        "fields": submission_data
                    }]

        self.client.write_points(json_body)


    def get_latest_timestamp(self):
        query_result = self.client.query(f'SELECT max(post_timestamp) FROM {self.table_name}', database=self.database_name)

        latest = None
        for row in query_result.get_points():
            latest = row['max']

        return latest
