import os
from time import time
from quart import Quart, request

tokens = {
    "test": {
        "expire": time() + 60,
        "requester": "174200708818665472",
        "requestee": "174200708818665472"
    }
}

def add_token(token, data):
    tokens[token] = data

app = Quart(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')



@app.route('/logtoken/<token>')
async def logtoken(token):

    if token is None:
        return "400", 400
    if token not in tokens.keys(): # pylint: disable=consider-iterating-dictionary
        return "400", 400

    if tokens[token].get("expire") < time():
        del tokens[token]
        return "400", 400
    
    return "200", 200


@app.route('/logs/', methods=["POST"])
async def get_logs():
    token = request.headers.get("token")
    
    if token is None:
        return "401", 401
    if token not in tokens.keys(): # pylint: disable=consider-iterating-dictionary
        return "401", 401
    
    if tokens[token].get("expire") > time():
        del tokens[token]
        return "401", 401
    
    token = tokens[token]

    
    response = await request.get_json()
    if len(response) == 0:
        return "400", 400
    logs = []
    for key in response.keys():
        logs.append(response[key])
    return "200", 200

app.run(host='0.0.0.0',port=8080)
