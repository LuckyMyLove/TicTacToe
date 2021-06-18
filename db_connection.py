from pymongo import MongoClient
from bson.objectid import ObjectId

cluster = MongoClient('mongodb+srv://dBUser:72qNFNDh5uGIQcrB@maincluster.3mttb.mongodb.net/TicTacToe?retryWrites=true&w=majority')
db = cluster['TicTacToe']
users_data = db['userData']
game_data = db['gamesData']