import sys
import os
import argparse

sys.path.append((os.environ.get('SRC_DIR')))

from helper import create_new_project, upload_images, create_label_classes


def driver(project_name, images_dir, labels_file_path):
    """Drives the script by calling needed functions with respective arguments"""
    project = create_new_project(name=project_name)
    upload_images(images_dir=images_dir, hasty_project=project)
    create_label_classes(label_class_file_path=labels_file_path, hasty_project=project)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload set of images and apply labels to Hasty project')
    parser.add_argument('project_name', help='Name of the new project to be created at Hasty workspace')
    parser.add_argument('images_dir', help='Absolute path to directory of images to be labelled', type=str)
    parser.add_argument('labels_file_path', help='Absolute path JSON file with image annotations', type=str)

    args = parser.parse_args()

    driver(project_name=args.project_name, images_dir=args.images_dir, labels_file_path=args.labels_file_path)
