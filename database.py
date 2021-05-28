from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://dBUser:72qNFNDh5uGIQcrB@maincluster.3mttb.mongodb.net/TicTacToe?retryWrites=true&w=majority')
db = cluster['TicTacToe']
collection = db['gamesData']

#SELECT
#dla wielu wyników:
# results = collection.find({"id_u1":"testUser1"})
#
# for singleResult in results:
#     print(singleResult["id_u1"])

#tylko dla jednego wyniku
# result = collection.find_one({"id_u1":"testUser1"})
# print(result)
# print(result["id_u1"])

#UPDATE (single)
#update = collection.update_one({"id_u1": "testUser1"}, {"$set":{"id_u1": "testUser1_UPDATED"}})  #podajemy najpierw warunek, potem co ma się zadziać ($set jest jedną z wielu komend)



# #INSERT (single)
# test_post = {"id_u1": "testUser1", "id_u2": "testUser2", "room": ["room_name", "0"], "symbol_u1": "X", "symbol_u2": "O", "result": 0}
# collection.insert_one(test_post)

#INSERT (many)
# collection.insert_many([post1, post2])

#DELETE (single)
#delete = collection.delete_one({"id_u1":"testUser1"})

#DELETE (many)
#delete = collection.delete_mane({"id_u1":"testUser1"})
