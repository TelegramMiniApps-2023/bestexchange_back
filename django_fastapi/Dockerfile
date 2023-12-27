FROM python:3.10

WORKDIR /app

# EXPOSE 8000

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

COPY . .