import os
import json

import hasty.exception
from hasty import Client

import settings

hasty_client = Client(api_key=settings.API_KEY, base_url=settings.BASE_URL)


def create_new_project(name):
    """
    Create a new Hasty project with the given name

    :param(str) name: Desired project name
    :return(hasty.Project): Freshly created Hasty Project object (check Hasty docs for data str.)
    """
    new_project = hasty_client.create_project(name=name, workspace=settings.WORKSPACE_ID)
    print("Created new project with ID: {}".format(new_project.id))
    return new_project


def upload_images(hasty_project, images_dir):
    """
    Upload all images for a folder stored locally to a hasty project.
    NB: This creates a new dataset in the project with the folder name

    :param(hasty.Project) hasty_project: The project where the dataset and respective images are to be created
    :param(str) images_dir: Path to folder on local machine where all images to be uploaded are stored
    :return(dict[str, hasty.Image]): Freshly created Hasty Image objects mapped with their file name as key
    """
    if not os.path.isdir(images_dir):
        print('ERROR: Given path `{}` is not a directory'.format(images_dir))
        return
    dataset_name = images_dir.split('/')[-1]  # Using the folder name as dataset name
    images_dataset = hasty_project.create_dataset(name=dataset_name)
    print("Created new dataset with ID: {} and name: {}".format(images_dataset.id, images_dataset.name))
    uploaded_image_map = {}  # Key: Image file name; Value: Generated Image ID
    # Assumption: Image file names are unique
    print("\nUploading image files processed ...")
    for idx, file_name in enumerate(os.listdir(path=images_dir)):
        image_file_path = images_dir + '/' + file_name
        try:
            uploaded_image = hasty_project.upload_from_file(dataset=images_dataset, filepath=image_file_path)
        except hasty.exception.ValidationException as e:
            print("Error while uploading file `{}`;\nException: {}".format(image_file_path, str(e)))
            continue
        uploaded_image_map[uploaded_image.name] = uploaded_image
        if idx % 20 == 0:    # 20 is a random chunk size for now
            print(idx)
    print("Uploaded {} images to project {}".format(len(uploaded_image_map), hasty_project.name))
    return uploaded_image_map


def upload_labels(hasty_project, labels_file_path, image_name_obj_map):
    """
    Read a JSON file of defined structure and create respective label classes in required Hasty project
    Prescribed JSON structure:
        Root object to have key "label_classes" as list of objects and "images" as list of objects
        Each label_class doc should have mandatory keys: "class_name", "class_type"
        Each image doc should have mandatory key: "image_name"

    :param(dict[str, hasty.Image]) image_name_obj_map: Image name mapped to Hasty image object
    :param(hasty.Project) hasty_project: The project where the dataset and respective images are to be created
    :param(str) labels_file_path: Path to JSON file of image label classes and respective mappings
    """
    if not (os.path.exists(labels_file_path) or labels_file_path.endswith('.json')):
        print('ERROR: Given path`{}` is not a valid JSON file'.format(labels_file_path))
    with open(file=labels_file_path, mode='r') as json_file:
        label_classes_doc = json.load(json_file)
    try:
        label_classes_from_doc = label_classes_doc['label_classes']
        image_label_mapping_from_doc = label_classes_doc['images']
    except KeyError:
        print('ERROR: Key `label_classes` and `images` are required')
        return
    label_class_map = _create_label_classes(label_classes_from_doc, hasty_project)
    _apply_labels_to_images(image_name_obj_map, label_class_map, image_label_mapping_from_doc)


def _create_label_classes(label_classes_from_doc, hasty_project):
    """
    Create multiple label classes in the mentioned Hasty project

    :param(list of dict) label_classes_from_doc: Label class definitions to be created
    :param(hasty.Project) hasty_project: The project where the dataset and respective images are to be created
    :return(dict[str, hasty.LabelClass]): Mapping of label classes created
    """
    generated_label_class_map = {}  # Key: Label class name; Value: label class ID
    # Assumption: Label class names are unique
    for label_class in label_classes_from_doc:
        try:
            label_class_obj = hasty_project.create_label_class(
                name=label_class['class_name'],
                class_type=label_class['class_type'],
                norder=label_class.get('norder'),
                color=label_class.get('color')
            )
        except KeyError:
            continue
        generated_label_class_map[label_class_obj.name] = label_class_obj.id
    print("Created {} new label classes".format(len(generated_label_class_map)))
    return generated_label_class_map


def _apply_labels_to_images(image_name_obj_map, label_class_name_id_map, image_label_mapping_from_doc):
    """
    Apply labels to images
    N.B: The labels and images created in the previous functions to be passed here mapped with names

    :param(dict[str, hasty.Image]) image_name_obj_map: Image name and ID mapping
    :param(dict[str, str]) label_class_name_id_map:
    :param(list of dict[str, Any]) image_label_mapping_from_doc:
    :return:
    """
    updated_images = 0
    for image_doc in image_label_mapping_from_doc:
        image_name = image_doc.get('image_name')
        labels = image_doc.get('labels')
        if not (image_name and labels):
            continue
        try:
            image = image_name_obj_map[image_name]
        except KeyError:
            print("ERROR: No image object created with name `{}`".format(image_name))
            continue
        current_image_label_payload = []
        for label_doc in labels:
            try:
                label_class_name = label_doc['class_name']
                label_class_id = label_class_name_id_map[label_class_name]
                print('ERROR: No label class found for name {}, imagae name: {}'.format(label_class_name, image_name))
            except KeyError:
                continue
            payload_doc = {
                'class_id': label_class_id,
                'bbox': label_doc.get('bbox'),
                'mask': label_doc.get('mask'),
                'polygon': label_doc.get('polygon'),
                'z_index': label_doc.get('z_index')
            }
            current_image_label_payload.append(payload_doc)
        labels = image.create_labels(labels=current_image_label_payload)
        print("{} labels applied to Image named {} with ID {}".format(len(labels), image.name, image.id))
        updated_images += 1
    print("\n Total no. of images annotated with labels".format(updated_images))
