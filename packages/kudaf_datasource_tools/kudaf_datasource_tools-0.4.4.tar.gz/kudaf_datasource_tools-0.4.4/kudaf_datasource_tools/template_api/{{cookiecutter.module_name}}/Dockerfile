FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get upgrade -y

# Install Python-dev and required packages
RUN apt-get install python3-dev libpq-dev gcc -y
RUN pip3 install --upgrade pip setuptools wheel
WORKDIR /usr/src
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Copy the App's source
COPY . .

# Launch FastAPI backend
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]