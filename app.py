import http
import json
import ssl

import requests
from flask import render_template, Response, request  # Remove: import Flask
import connexion

from colors import *


from coordinates_generator import CoordinatesGenerator

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

@app.route('/', methods=['GET', 'POST'])
def home():
    parkings = ['parking']
    if request.method == 'POST':
        # проверка логина и пароля
        print(request.form.get('comp_select'))
        url = "http://158.160.134.151:4565/api/parking"

        payload = json.dumps({
            "parking": "parking"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        print(data['free'])
        return render_template('login.html', parkings=parkings, free=data['free'])
    else:
        return render_template('login.html', parkings=parkings, free='')

if __name__ == "_" \
               "_main__":
    from waitress import serve
    app.run(host="0.0.0.0", port=4565, debug=True)

