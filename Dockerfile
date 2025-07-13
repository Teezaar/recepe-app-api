FROM python:3.12-alpine

# Just tells who is maintaining if others are going to work on this
LABEL maintainer="greenDev"
# Prevents buffering - will not buffer the output - good when running python in docker - output will be printed directly to the console which prevents any delay
ENV PYTHONUNBUFFERED=1
# What this block does:
# 1. copy requirements.txt from local to that address in docker image
# 1.1. copy dev requirements.txt
# 2. copy the app dir that contains our django into the docker
# 3. Working directory which contains commands we set it on our app so when we try to run commands we don't have to set the full path for django
# 4. we expose port 8000 from container to our machine
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# python -m venv /py - creates new virtual environments
# pip install --upgrade pip - upgrade pip
# pip install -r /tmp/requirements.txt - installs all the requirements
#  rm -rf /tmp - removes the requirements.txt file
# adduser - creates a new user - DO not run as root user - no password
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = true ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

# tells docker to use the python from the virtual environment
ENV PATH="/py/bin:$PATH"
# tells docker to use the user we created
USER django-user
