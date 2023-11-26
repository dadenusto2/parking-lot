from colors import COLOR_RED
from coordinates_generator import CoordinatesGenerator
import logging

# Рисование рамок для станции и парковочных мест
def main():
    logging.basicConfig(level=logging.INFO)
    charge_point_id = 'parking'
    image_file = f'images/{charge_point_id}.png'
    data_file = f'data/{charge_point_id}.yml'

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()


if __name__ == '__main__':
    main()
