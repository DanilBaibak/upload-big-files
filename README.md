# Upload big files

## Description

Current project is an example how you can orginize upload of the big files using [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload) plugin on the front-end and [Flask](http://flask.pocoo.org/) on the back-end.

Additional feature - versioning files. As soon a file with unique name is exists, new file with the same name will be saved with additional suffix.

## Requirements

[Docker](https://www.docker.com/get-docker)

## Installing

Using docker-compos: `docker-compose up --build`

## Using

Localhost application - (http://localhost:5000/)

* On the home page you can download some big file. Currently list of allowed files is ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv']
* Jquery plugin uploads the chunks in 10 Mb
* After upload is done, you can find list of all uploaded files in the page (http://localhost:5000/files)


