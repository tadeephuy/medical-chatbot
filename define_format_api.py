"""
define format REST api
"""

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
    user_mess = input_data['mess']
    user_id = input_data['_id']

    result_feedforward = {}

    try:
        """
            load model predict intent + entities
        """
        
        result_feedforward['intent'] = {}
        result_feedforward['intent']['class'] = 'overall'
        result_feedforward['intent']['confidence'] = 0.89

        result_feedforward['entities'] = [tuple('symptom','buồn nôn')]

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
        response['predict'] = result_feedforward
        response['status'] = 500
        
        return jsonify(response)