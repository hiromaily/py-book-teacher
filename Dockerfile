# Dockerfile for py-book-teacher

FROM python:3.5

RUN mkdir /app

WORKDIR /app

#ENTRYPOINT ["pip", "install", "-r", "pip_packages.txt"]
