import json
import random
import re
import urllib.request
from datetime import datetime
from urllib.request import build_opener, HTTPPasswordMgrWithDefaultRealm
import cv2 as open_cv
import numpy as np
import logging
import pandas as pd
from shapely.geometry import Polygon
from flask import jsonify
from ultralytics import YOLO
import time
from colors import *
from drawing_utils import draw_contours

class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 0
    model = YOLO('models/yolov8l-seg.pt')

    def __init__(self,coordinates, parking, shouldReturn = True):
        self.coordinates_data = coordinates
        self.parking = parking
        self.shouldReturn = shouldReturn
        self.start_frame = 0
        self.contours = []
        self.bounds = []
        self.mask = []

    def detect_motion(self):

        return {'free': 1}
        my_file = open("models/coco.txt", "r")
        data = my_file.read()
        class_list = data.split("\n")

        vidcap = open_cv.VideoCapture('video/parking.mp4')
        totalFrames = vidcap.get(open_cv.CAP_PROP_FRAME_COUNT)
        randomFrameNumber = random.randint(0, totalFrames)
        # set frame position
        vidcap.set(open_cv.CAP_PROP_POS_FRAMES, randomFrameNumber)
        success, image = vidcap.read()

        # получаем результат распознования
        results = self.model.predict(image)
        a = results[0].boxes.data

        # извлекаем координат распознаных объектов
        try:
            masks = results[0].masks.xy
        except Exception:
            # если объектов не найдено
            if self.shouldReturn:
                return jsonify({'free': 2})
            else:
                station_coor = self._coordinates(self.coordinates_data[0])
                polygon_all = Polygon(station_coor)
                coords = polygon_all.exterior.coords[:-1]
                coords = [(int(x), int(y)) for x, y in coords]
                coords = np.array(coords)
                open_cv.polylines(image, [coords], True, COLOR_GREEN, 2)

        px = pd.DataFrame(a).astype("float")

        # вычисляем парковку
        coordinates_data = self.coordinates_data[1:]
        free = len(coordinates_data)
        for i, p in enumerate(coordinates_data):
            # координаты парковки
            coordinates = self._coordinates(p)
            if not self.shouldReturn:
                draw_contours(image, coordinates, str(p["id"] + 1), COLOR_WHITE, COLOR_RED)
            polygon_all = Polygon(coordinates)  # исходная рамка
            polygon_1 = Polygon(coordinates)  # исходная рамка
            for index, row in px.iterrows():
                d = int(row[5])
                c = class_list[d]
                if 'car' in c or 'truck' in c or 'bus' in c or 'motorcycle' in c:
                    try:
                        coords = masks[index]
                        polygon_2 = Polygon(coords)  # получаем рамку автомобиля
                        polygon_1 = polygon_1.difference(polygon_2)  # отрезаем от рамки станции рамку авто
                    except Exception:
                        print('erorr')
            # вычисляем отношение обрезанной рамки станции к исходной
            results = polygon_1.area / polygon_all.area
            if results < 0.8:  # если машина занимает более 20% места, то парковка занята
                free -= 1

            # вывод для отладки
            if not self.shouldReturn:
                try:
                    polygons = list(polygon_1.geoms)
                    for polygon in polygons:
                        coords = polygon.exterior.coords[:-1]
                        coords = [(int(x), int(y)) for x, y in coords]
                        coords = np.array(coords)
                        open_cv.polylines(image, [coords], True, COLOR_GREEN, 2)
                except Exception:
                    coords = polygon_1.exterior.coords[:-1]
                    coords = [(int(x), int(y)) for x, y in coords]
                    coords = np.array(coords)
                    open_cv.polylines(image, [coords], True, COLOR_GREEN, 2)

        print({'free': free})
        if self.shouldReturn:
            return {'free': free}
        else:
            while 1:
                open_cv.imshow('img', image)
                k = open_cv.waitKey(1)
                if k == ord("q") or k == ord("й"):
                    break

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index]
        logging.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        logging.debug("status: %s", status)

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
