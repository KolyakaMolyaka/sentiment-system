# pull official base image
FROM python:3.10-slim-buster

WORKDIR /usr/src/app
# set invironment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
#COPY . .
#RUN chmod +x ./entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]