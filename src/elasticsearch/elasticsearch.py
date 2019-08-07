import es
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import time
import os
import sys


class ElasticSearch:
    def __init__(self, ECS_HOST, ECS_INDEX, ECS_TYPE, username=None, password=None):
        self.ECS_HOST = ECS_HOST
        self.ECS_INDEX = ECS_INDEX
        self.ECS_TYPE = ECS_TYPE
        self.password = password
        self.username = username
