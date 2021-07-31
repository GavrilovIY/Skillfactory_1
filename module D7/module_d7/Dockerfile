# Dockerfile
FROM python:3.8
RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
COPY Pipfile* /code/
RUN pipenv install --system --deploy --ignore-pipfile
ADD module_d7 /code/