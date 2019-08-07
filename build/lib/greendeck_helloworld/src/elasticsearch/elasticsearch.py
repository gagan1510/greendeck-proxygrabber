from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import time
import os
import sys


class ElasticSearch:
    def __init__(self, ECS_HOST, ECS_INDEX_PATTERN="*", username=None, password=None):
        try:

            self.ECS_HOST = ECS_HOST
            self.ECS_INDEX_PATTERN = ECS_INDEX_PATTERN
            self.password = password
            self.username = username

            if self.username is None and self.password is None:
                try:
                    self.ECS_CONNECTION = Elasticsearch(self.ECS_HOST)
                except Exception as e:
                    print("\n"+str(e))
            else:
                try:
                    self.ECS_CONNECTION = Elasticsearch(self.ECS_HOST,http_auth=(self.username,self.password))
                except Exception as e:
                    print("\n"+str(e))
            print("\n ECS connection established successfully.")
        except Exception as e:
            print("\n"+str(e))

    def list_indices(self):
        indices = self.ECS_CONNECTION.indices.get_alias(self.ECS_INDEX_PATTERN)
        return sorted(indices)
