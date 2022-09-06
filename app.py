from flask import Flask, render_template, request
from datetime import datetime
from dotenv import load_dotenv
from pytz import timezone

import json
import requests
import os
import time

load_dotenv(verbose=True)
app = Flask(__name__, static_folder='./static/')


@app.route('/', methods=["GET"])
def init():
    return render_template("index.html")


@app.route('/realtime/<page>', methods=["GET"])
def realtime(page):
    url = f"https://apis.openapi.sk.com/puzzle/congestion/rltm/pois/{page}"

    headers = {
        "Accept": "application/json",
        "appkey": os.environ.get("APPKEY")
    }

    response = requests.get(url, headers=headers)
    res = json.loads(response.text)
    return render_template("realtime.html", mall=res["contents"]["poiName"], level=res["contents"]["rltm"]["congestionLevel"], congestion=res["contents"]["rltm"]["congestion"]*100)


app.run(host="0.0.0.0", port=os.environ.get('PORT', 5001), debug=1)
