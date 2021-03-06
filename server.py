from flask import Flask, render_template

import os
import requests

from dotenv import load_dotenv
load_dotenv()
USERNAME = os.getenv("USERNAME")
APIKEY = os.getenv("APIKEY")

# Setup request session and use session to send auth and header along with every request
session = requests.Session()
session.auth = (USERNAME, APIKEY)
session.headers = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}


def get_models(sku=None):
    url = "https://www.wayfair.com/3dapi/models"
    params = None

    # simple example so we aren't handling multiple skus
    if sku:
        params = {'skus[]': sku}

    response = session.get(url, params=params)
    return response.json()


app = Flask(__name__)


@app.route("/")
def index():
    # Send a GET request to Wayfair 3D model API. Returns JSON for 3D models
    products = get_models()
    return render_template('index.html', products=products)


@app.route("/product/<sku>")
def product(sku):
    products = get_models(sku)
    product = products[0]
    # Fix glb url until it gets fixed on the server side
    product['model']['glb'] = product['model']['glb'].replace('http://img', 'https://secure.img1')
    return render_template('sku.html', product=product)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
