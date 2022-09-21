# Hasty Test

`Trying out Hasty APIs`

## Objective

Using Hasty APIs, write a module that does the following:
1. Create a new project
2. Upload images from a folder
3. Generate label classes reading from a JSON file and apply labels

### Reference
Hasty Python API Doc: https://hasty.readthedocs.io/en/latest/

### Steps to run
1. Git clone this repository
2. Create .env file and add values to respective env variables
3. Run `main.py` with 3 positional arguments
```
python main.py <project_name> <path_to_images_folder> <path_to_labels_json>
```

### Env Variables
- SRC_DIR
- API_KEY
- WORKSPACE_ID
- BASE_URL

###### Data Files:
- https://storage.googleapis.com/hasty-test-fixtures/test-tasks/cable-cars/Cable%20Cars%20Images.zip
- https://storage.googleapis.com/hasty-test-fixtures/test-tasks/cable-cars/Cable%20Cars%20Labels.zip