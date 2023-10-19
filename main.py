from pymongo import MongoClient
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

uri = "mongodb+srv://cluster0.hq133qf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-7954788920278394582.pem')
data = {
                "name": "hi",
                "phone": "test"
        }
db = client.gettingStarted
bbc = db.people
bbc.insert_one(data)
