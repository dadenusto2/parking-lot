from datetime import datetime
from motion_detector import MotionDetector
from flask import jsonify
import yaml


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def get(parking):
    parking = parking.get("parking")
    try:
        with open(f'data/{parking}.yml', "r") as data:
            points = yaml.load(data, Loader=yaml.SafeLoader)
            detector = MotionDetector(points, parking)
            print('before resp')
            resp = detector.detect_motion()
            print('resp', resp)
            return resp
    except FileNotFoundError:
        return jsonify({'errorCode': 1})
