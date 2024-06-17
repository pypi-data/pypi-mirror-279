import json
import os
import sys

import cv2
from PIL import Image

from ok.feature.FeatureSet import read_from_json


def compress_coco(coco_json) -> None:
    feature_dict, *_ = read_from_json(coco_json)
    with open(coco_json, 'r') as file:
        image_dict = {}
        data = json.load(file)
        coco_folder = os.path.dirname(coco_json)
        image_map = {image['id']: image['file_name'] for image in data['images']}
        category_map = {category['id']: category['name'] for category in data['categories']}

        for annotation in data['annotations']:
            image_id = annotation['image_id']
            category_id = annotation['category_id']

            feature = feature_dict.get(category_map[category_id])
            if feature:
                # Load and scale the image
                image_path = str(os.path.join(coco_folder, image_map[image_id]))
                image_features = image_dict.get(image_path, [])
                image_features.append(feature)
                image_dict[image_path] = image_features

        # Loop through the image_dict and write all the image_feature associated with it in a new PNG
        for image_path, features in image_dict.items():
            background = None
            for feature in features:
                # Create a white background
                if not background:
                    original_image = cv2.imread(image_path)
                    background = Image.new('RGBA', (original_image.shape[1], original_image.shape[0]),
                                           (255, 255, 255, 255))
                # Convert the OpenCV image (numpy array) to a PIL image
                image = Image.fromarray(cv2.cvtColor(feature.mat, cv2.COLOR_BGR2RGBA))
                background.paste(image, (feature.x, feature.y), image)
                # Save the image with compression level 9
            # background.save(image_path, 'PNG', optimize=True, compress_level=9)

            # Add metadata
            metadata = {
                "ok_compressed": "1"
            }

            for key, value in metadata.items():
                background.info[key] = value

            # Save the image with metadata
            background.save(image_path, 'PNG', optimize=True)


if __name__ == '__main__':
    json_file = sys.argv[1]
    compress_coco(json_file)
