A task was done as web application using Python and Flask.

Requirements: Docker (https://www.docker.com/get-docker)

Run docker-compose - "docker-compose up --build"

Test localhost application - http://localhost:5000/

Using:
 * On the home page you can download some big file. Currently list of allowed files is
 ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv']
 * Jquery plugin uploads the chunks in 10 Mb
 * After upload is done, you can find list of all uploaded files in the page http://localhost:5000/files


