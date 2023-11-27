from colors import COLOR_RED
from coordinates_generator import CoordinatesGenerator
import logging

# Рисование рамок для станции и парковочных мест
def main():
    logging.basicConfig(level=logging.INFO)
    parking = 'parking'
    image_file = f'images/{parking}.png'
    data_file = f'data/{parking}.yml'

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()


if __name__ == '__main__':
    main()
