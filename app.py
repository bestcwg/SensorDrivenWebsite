from signal import signal, SIGINT
from sys import exit
import json
from flask import Flask, render_template, request
from flask.json import jsonify
from flask_mqtt import Mqtt
import itwot
import getip
import database as db

__CONFIG = itwot.config()
app = Flask(__name__)
app.config["MQTT_BROKER_URL"] = "itwot.cs.au.dk"
app.config["MQTT_BROKER_PORT"] = 1883
mqtt = Mqtt(app)

@app.route("/")
@app.route('/home')
def index():
    latest = db.get_from_database('latest')
    return render_template("index.html", config = __CONFIG, latest=latest, min_max=min_max())

@app.route("/measurements")
def measurements():
    return render_template("html/data.html", config = __CONFIG)

@app.route("/measurements_by_page/<int:page>", methods=["GET"])
def measurements_by_page(page):
    if request.method == "GET":
        offset = (page - 1) * 20
        return jsonify(db.get_data(offset))

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker...", end="")
    mqtt.subscribe("au676174/M5SC0/#")
    print("subscribed")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    if topic.endswith("/json"):
        payload = json.loads(payload)
        if 'temp' and 'hum' and 'pres' and 'time' in payload:
            db.store_data(payload["temp"], payload["hum"], payload["pres"], payload["time"])
            publish("au676174/data", db.get_from_database('latest'))
            publish("au676174/min_max", min_max())
    print(f"Received MQTT on {topic}: {payload}")

def handler(signal_received, frame):
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    mqtt.unsubscribe_all()
    exit(0)

def publish(destination, data):
    mqtt.publish(destination, str(json.dumps(data)))

def min_max():
    result = [
        db.get_from_database('mintemp'), db.get_from_database('maxtemp'),
        db.get_from_database('minhum'), db.get_from_database('maxhum'),
        db.get_from_database('minpres'), db.get_from_database('maxpres')
    ]
    return result

if __name__ == '__main__':
    signal(SIGINT, handler)
    app.run(debug=__CONFIG["debug"],
            host=getip.get_ip(),
            port=__CONFIG["port"],
            use_reloader=False
    )