from pymongo import MongoClient
from os import getenv


class MongoConnection:
    """
    A class to manage all interactions with the mongodb instance
    """
    def __init__(self):
        username = getenv("MONGO_USERNAME")
        password = getenv("MONGO_PASSWORD")
        host = getenv("MONGO_HOSTNAME")
        self.client = MongoClient(f"mongodb://{username}:{password}@{host}:27017/")
        database = self.client["site-sketcher"]
        self.collection = database["sketches"]


    def insert_sketch(self, url: str, sketch: list[list[str]]) -> int:
        # TODO: Override any previous entry
        payload = {
            "url": url,
            "sketch": sketch
        }
        result = self.collection.insert_one(payload)
        return result.inserted_id


    def get_sketches(self) -> list[dict]:
        sketches = self.collection.find()
        result = []
        for sketch in sketches:
            result.append(sketch)
        return result


    def __del__(self):
        self.client.close()
        del self.collection
