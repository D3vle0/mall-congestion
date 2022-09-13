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

@app.route('/history', methods=["GET"])
def history():
    return render_template("history.html")

@app.route('/history', methods=["POST"])
def history_post():
    with open('static/place.json', 'r') as f:
        data = json.load(f)
    for i in data["contents"]:
        if i["poiName"] == request.form["mall"]:
            id = i["poiId"]
            break
    
    url = f"https://apis.openapi.sk.com/puzzle/congestion/raw/hourly/pois/{id}?date={request.form['date'].replace('-', '')}"

    headers = {
        "Accept": "application/json",
        "appkey": os.environ.get("APPKEY"),
    }

    response = requests.get(url, headers=headers)

    try:
        return render_template("history_result.html", data=response.json(), mall=request.form["mall"], date=request.form["date"])
    except:
        return '<script>alert("검색 결과가 없습니다!");window.history.back();</script>'


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
