# Davincimator
Automate importing media files to Davinci Resolve using `DaVinciResolveScript` and the [documentation](https://resolvedevdoc.readthedocs.io/en/latest/index.html).

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

Copy the media files to a directory (`PATH_TO_BASE_DIR/YOUR_PROJECT_NAME`) and then import them from the new place to a project:
```
python __main__.py -p YOUR_PROJECT_NAME -d PATH_TO_BASE_DIR -c COPY_TO_DIR
```

You can also set the timeline name using `-t` flag.

## TODO
- Test on Windows and Linux. It is only tested on Mac OS X
- Write unit tests!