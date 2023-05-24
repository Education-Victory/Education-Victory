#base image
FROM python:3.11
# set work directory
WORKDIR /app

# installation of dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app
# copy static files
COPY ../static /static