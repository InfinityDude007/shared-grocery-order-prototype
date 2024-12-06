# use official Python 3.11 slim image as base
FROM python:3.11-slim

# set environment variables/rules
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# set working directory in container
WORKDIR /app

# update package list and install dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# copy requirements.txt file from host to container
COPY server/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

# copy entire application from host to container
COPY . /app/

# expose port for application to be accessed externally
EXPOSE 5000

# start application using uvicorn
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
