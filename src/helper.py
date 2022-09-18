import os

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


def upload_images(images_dir, hasty_project):
    """
    Upload all images for a folder stored locally to a hasty project.
    NB: This creates a new dataset in the project with the folder name

    :param(str) images_dir: Path to folder on local machine where all images to be uploaded are stored
    :param(hasty.Project) hasty_project: The project where the dataset and respective images are to be created
    :return(list of hasty.Image): Freshly created Hasty Image objects (check Hasty docs for data str.)
    """
    if not os.path.isdir(images_dir):
        print('ERROR: Given path `{}` is not a directory'.format(images_dir))
        return
    dataset_name = images_dir.split('/')[-1]  # Using the folder name as dataset name
    images_dataset = hasty_project.create_dataset(name=dataset_name)
    print("Created new dataset with ID: {} and name: {}".format(images_dataset.id, images_dataset.name))
    uploaded_images = []
    for file_name in os.listdir(path=images_dir):
        image_file_path = images_dir + '/' + file_name
        uploaded_image = hasty_project.upload_from_file(dataset=images_dataset, filepath=image_file_path)
        uploaded_images.append(uploaded_image)
    return uploaded_images
