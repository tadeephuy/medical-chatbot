from flask import Flask, request, jsonify
# from flask_cors import CORS
from datetime import datetime
from inference import NLUprocess

import os

app = Flask(__name__)

## modify
# CORS(app)

NLUproc = NLUprocess("./phobert")

_PATH_LOG = '../log'

@app.route('/proc-nlu', methods=['POST'])
def procNLU():
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
    user_id = str(input_data['_id'])

    result_feedforward = {}
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    # date_folder = os.path.join(_PATH_LOG,date_time.split(',')[0])
    dir_log_nlu = os.path.join(_PATH_LOG,'NLU')
    # print('dir_log_nlu',dir_log_nlu)
    if not os.path.isdir(dir_log_nlu):
        os.mkdir(dir_log_nlu)
    print('user_id',user_id)
    date_folder = os.path.join(dir_log_nlu,user_id.split('-')[0])

    if not os.path.isdir(date_folder):
        os.mkdir(date_folder)

    date_file = os.path.join(date_folder,date_time+'.json')


    try:
        """
            load model predict intent + entities
        """
        results = NLUproc.inference([user_mess.split(" ")])
        result_feedforward['intent'] = {}
        result_feedforward['intent']['class'] = results[0]["intent"]
        result_feedforward['intent']['confidence'] = results[0]["highest_prop"] 

        result_feedforward['entities'] = [results[0]["entities"]] # mai a sửa lại theo ý em

        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = result_feedforward
        response['status'] = 200

        ## write log

        # res_json_log = jsonify(response)

        file_out=open(date_file,'w')
        item_str=str(response).replace(r"'",r'"')
        file_out.write(item_str)
        file_out.write('\n')

        return jsonify(response)

    except Exception as e:
        
        print('Fail: {}'.format(str(e)))

        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = []
        response['status'] = 500

        # res_json_log = jsonify(response)

        file_out=open(date_file,'w')
        item_str=str(response).replace(r"'",r'"')
        file_out.write(item_str)
        file_out.write('\n')
        
        return jsonify(response)



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
    user_id = str(input_data['_id'])

    result_feedforward = {}

    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    # date_folder = os.path.join(_PATH_LOG,date_time.split(',')[0])

    dir_log_kb = os.path.join(_PATH_LOG,'KB')

    if not os.path.isdir(dir_log_kb):
        os.mkdir(dir_log_kb)

    date_folder = os.path.join(dir_log_kb,user_id.split('-')[0])

    if not os.path.isdir(date_folder):
        os.mkdir(date_folder)

    date_file = os.path.join(date_folder,date_time+'.json')

    try:
        """
            load model predict intent + entities
        """
        results = NLUproc.inference([user_mess.split(" ")],use_kb =True)
        # result_feedforward['intent'] = {}
        # result_feedforward['intent']['class'] = results[0]["intent"]
        # result_feedforward['intent']['confidence'] = results[0]["highest_prop"] 

        # result_feedforward['entities'] = [results[0]["entities"]] # mai a sửa lại theo ý em
        # print('results',results)
        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = results
        response['status'] = 200

        # res_json_log = jsonify(response)

        file_out=open(date_file,'w')
        item_str=str(response).replace(r"'",r'"')
        file_out.write(item_str)
        file_out.write('\n')

        return jsonify(response)

    except Exception as e:
        
        print('Fail: {}'.format(str(e)))

        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = {}
        response['status'] = 500

        # res_json_log = jsonify(response)
        file_out=open(date_file,'w')
        item_str=str(response).replace(r"'",r'"')
        file_out.write(item_str)
        file_out.write('\n')
        
        return jsonify(response)

if __name__ == "__main__":
    # app.run(debug=True)
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)