from datetime import datetime
from motion_detector import MotionDetector
from flask import jsonify
import yaml


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def get(charge_point):
    charge_point_id = charge_point.get("chargePointId")
    try:
        with open(f'data/{charge_point_id}.yml', "r") as data:
            points = yaml.load(data, Loader=yaml.SafeLoader)
            detector = MotionDetector(points, charge_point_id)
            return detector.detect_motion()
    except FileNotFoundError:
        return jsonify({'errorCode': 1})
