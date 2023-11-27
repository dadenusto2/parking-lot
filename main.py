import yaml

from motion_detector import MotionDetector
import logging

# -
#           id: 0
#           coordinates: [[1828,627],[1860,948],[2263,917],[2237,594]]


# отладка без запуска REST сервиса
def main():
    logging.basicConfig(level=logging.INFO)

    parking = 'parking'
    data_file = f'data/{parking}.yml'

    with open(data_file, "r") as data:
        points = yaml.load(data, Loader=yaml.SafeLoader)
        detector = MotionDetector(points, parking,  False)
        detector.detect_motion()


if __name__ == '__main__':
    main()
