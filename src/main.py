import sys
import os
import argparse

sys.path.append((os.environ.get('SRC_DIR')))

from helper import create_new_project, upload_images


def driver(project_name, images_dir):
    project = create_new_project(name=project_name)
    images = upload_images(images_dir=images_dir, hasty_project=project)
    # TODO: Apply labels to uploaded images; seek clarification from Andriy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload set of images and apply labels to Hasty project')
    parser.add_argument('project_name', help='Name of the new project to be created at Hasty workspace')
    parser.add_argument('images_dir', help='Absolute path to directory of images to be labelled', type=str)
    # parser.add_argument('labels_file_path', help='Absolute path CSV file with image annotations', type=str)

    args = parser.parse_args()

    driver(project_name=args.project_name, images_dir=args.images_dir)
