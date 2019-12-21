import pymongo
from pymongo.collection import Collection
class pymongo_connect(object):
    def __init__(self):
        self.client=pymongo.MongoClient("地址")
        self.data_name=self.client["douguo_meishi"]
    def insert_item(self,item):
        db_collection=Collection(self.data_name,"douguo_meishi_item")
        db_collection.insert(item)



mongo_info=pymongo_connect()
