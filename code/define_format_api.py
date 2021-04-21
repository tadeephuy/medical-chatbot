from flask import Flask, request, jsonify

from inference import NLUprocess



app = Flask(__name__)
NLUproc = NLUprocess("./phobert")

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
    user_id = input_data['_id']

    result_feedforward = {}

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

        return jsonify(response)

    except Exception as e:
        
        print('Fail: {}'.format(str(e)))

        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = []
        response['status'] = 500
        
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
    user_id = input_data['_id']

    result_feedforward = {}

    try:
        """
            load model predict intent + entities
        """
        results = NLUproc.inference([user_mess.split(" ")],use_kb =True)
        # result_feedforward['intent'] = {}
        # result_feedforward['intent']['class'] = results[0]["intent"]
        # result_feedforward['intent']['confidence'] = results[0]["highest_prop"] 

        # result_feedforward['entities'] = [results[0]["entities"]] # mai a sửa lại theo ý em

        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = results
        response['status'] = 200

        return jsonify(response)

    except Exception as e:
        
        print('Fail: {}'.format(str(e)))

        response = {}
        response['_id'] = user_id
        response['mess'] = user_mess
        response['predict'] = []
        response['status'] = 500
        
        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)