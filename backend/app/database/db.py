from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://shoaibkhn533_db_user:niazi1424@cluster0.rxquod.mongodb.net/recruitai?retryWrites=true&w=majority"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["recruitai"]