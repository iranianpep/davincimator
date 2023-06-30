# Davincimator
Automate importing media files to Davinci Resolve using `DaVinciResolveScript` and the [documentation](https://resolvedevdoc.readthedocs.io/en/latest/index.html).

[![Maintainability](https://api.codeclimate.com/v1/badges/d006387c059d13beb9ac/maintainability)](https://codeclimate.com/github/iranianpep/davincimator/maintainability)

## Requirements

- Python 3.9
- pip
- pipenv
- Davinci Resolve

## Usage

### Install Pipenv
```
pip install pipenv
```

### Install Dependencies
```
pipenv install
```

### Set environment variables
Create your own `.env` based on `.env.sample` depending on OS. The sample one is based for Mac OS X.
`MEDIA_EXTENSIONS_TO_IMPORT` is a whitelist media if you import files from a directory to a project using `-d` flag

Run:
```
pipenv shell
```

### Run the script
First make sure Davinci Resolve is open and running before running any script. Some examples are:

Import only a media file to a project:
```
python __main__.py -p YOUR_PROJECT_NAME -f PATH_TO_FILE
```

Import media files from a directory to a project:
```
python __main__.py -p YOUR_PROJECT_NAME -d PATH_TO_DIR
```

Import media files from a directory to a project based on a template project:
```
python __main__.py -p YOUR_PROJECT_NAME -d PATH_TO_DIR -b PATH_TO_TEMPLATE_PROJECT
```

Make sure the timeline name, matches the timeline name in the new project (for example `master`)

Copy the media files to a directory (`PATH_TO_BASE_DIR/YOUR_PROJECT_NAME`) and then import them from the new place to a project:
```
python __main__.py -p YOUR_PROJECT_NAME -d PATH_TO_BASE_DIR -c COPY_TO_DIR
```

Another example:
```
pipenv run python __main__.py -p PROJECT_NAME -f FILE_NAME -b BASE_PROJECT_FILE -c COPY_TO_DIR
```


You can also set the timeline name using `-t` flag (default value is `master`).

## TODO
- Test on Windows and Linux. It is only tested on Mac OS X
- Write unit tests!
