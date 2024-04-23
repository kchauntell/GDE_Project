# GDE_Project
Global Devops Python Weather Project. Use Weather app to see what weather is in your area by zipcode.

#How to run application locally and with Docker
To run locally: `python3 app.py`
To run containerized:
- build image using: `docker build . -t gde_project:1.0.1`
-run the container with: `docker run -d -p 8080:8080 gde_project:1.0.1`

Application is listening on port 8080: http://localhost:8080/