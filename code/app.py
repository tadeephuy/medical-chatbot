from flask import Flask, request, jsonify
import pymongo
from flask_pymongo import PyMongo
import os
# from inference import NLUprocess
from manger import Manager
from datetime import datetime
import random

app = Flask(__name__)
# NLUproc = NLUprocess("./phobert")
Manager = Manager()

os.environ["MONGOLAB_URI"] = 'mongodb://taindp:medicalbot@cluster0-shard-00-00.izvgn.mongodb.net:27017,cluster0-shard-00-01.izvgn.mongodb.net:27017,cluster0-shard-00-02.izvgn.mongodb.net:27017/vinbrain?ssl=true&replicaSet=atlas-fkqaqj-shard-0&authSource=admin&retryWrites=true&w=majority'
client = pymongo.MongoClient(os.environ.get('MONGOLAB_URI'))
app.config['MONGO_URI'] = os.environ.get('MONGOLAB_URI')
# database = client.vinbrain
mongo = PyMongo(app)
# collection = database['log_medical_bot']

@app.route('/proc-nlu', methods=['POST'])
# def procNLU():
#     """
#         API call process NLU

#         get message use lib request

#         unit testing:
#         {
#             "mess": "",
#             "_id": uuid()
#         }
#     """

#     ## get user's message
    
#     input_data = request.get_json(force=True) 
#     user_mess = input_data['mess']#mess này là string hả tài
#     # print(user_mess)
#     user_id = input_data['_id']
#     now = datetime.now()
#     date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
#     result_feedforward = {}

#     try:
#         """
#             load model predict intent + entities
#         """
#         # results = NLUproc.inference([user_mess.split(" ")])
#         results = Manager.get_answer(user_mess)
#         # print('res',results)
#         result_feedforward = {}
        
#         ## fix bug
#         # if type(results) is list:
#         #     result_feedforward['class'] = results[0]["intent"]
#         #     result_feedforward['confidence'] = results[0]["highest_prop"] 

#         #     result_feedforward['entities'] = [results[0]["entities"]] # mai a sửa lại theo ý em
#         # else:
#             # result_feedforward['class'] = results["intent"]
#         print('res',results)
#         result_feedforward['intent'] = results["intent"]
#         result_feedforward['confidence'] = results["highest_prop"] 
#         # result_feedforward['confidence'] = 1.0
#         result_feedforward['entity'] = "" # mai a sửa lại theo ý em

#         response = {}
#         response['user_id'] = user_id
#         response['mess'] = user_mess
#         response['time'] = date_time
#         response['task'] = 'nlu'
#         response['predict'] = result_feedforward
#         response['status'] = 200

#         ## insert db log
#         mongo.db.log_medical_bot.insert_one(response)
#         # collection.insert_one(response)
#         response['_id'] = str(random.randint(100000, 999999))
#         return jsonify(response)

#     except Exception as e:
        
#         print((str(e)))

#         response = {}
#         response['user_id'] = user_id
#         response['mess'] = user_mess
#         response['time'] = date_time
#         response['task'] = 'nlu'
#         response['predict'] = []
#         response['status'] = 500
        
#         ## insert db log
#         # collection.insert_one(response)
#         mongo.db.log_medical_bot.insert_one(response)
#         response['_id'] = str(random.randint(100000, 999999))
#         return jsonify(response)



@app.route('/proc-nlu-kb', methods=['POST'])
def procNLU_KB():
    """
        API call process NLU

        get message use lib request

        unit testing:
        {
            "mess": "",
            "_id": uuid()
        }
    """

    ## get user's message
    
    input_data = request.get_json(force=True) 
    user_mess = input_data['mess']#mess này là string hả tài
    # print(user_mess)
    user_id = input_data['_id']

    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

    result_feedforward = {}

    try:
        """
            load model predict intent + entities
        """
        # results = NLUproc.inference([user_mess.split(" ")],use_kb =True)
        results = Manager.get_answer(user_mess,use_kb =True)

        # result_feedforward['intent'] = {}
        # result_feedforward['intent']['class'] = results[0]["intent"]
        # result_feedforward['intent']['confidence'] = results[0]["highest_prop"] 

        # result_feedforward['entities'] = [results[0]["entities"]] # mai a sửa lại theo ý em

        response = {}
        response['user_id'] = user_id
        response['mess'] = user_mess
        response['time'] = date_time
        response['task'] = 'kb'
        response['predict'] = results
        response['status'] = 200

        ## insert db log
        mongo.db.log_medical_bot.insert_one(response)
        # collection.insert_one(response)
        response['_id'] = str(random.randint(100000, 999999))

        return jsonify(response)

    except Exception as e:
        
        print('Fail: {}'.format(str(e)))

        response = {}
        response['user_id'] = user_id
        response['mess'] = user_mess
        response['time'] = date_time
        response['task'] = 'kb'
        response['predict'] = []
        response['status'] = 500

        ## insert db log
        mongo.db.log_medical_bot.insert_one(response)
        # collection.insert_one(response)
        response['_id'] = str(random.randint(100000, 999999))
        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)