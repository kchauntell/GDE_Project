FROM python:3.10
WORKDIR /gdedevops
COPY . /gdedevops
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["python3", "app.py"]

# docker build --platform linux/amd64 -t kchauntell/gde_project:1.0.0