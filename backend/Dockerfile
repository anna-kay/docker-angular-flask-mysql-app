### Stage 1: Build ###
FROM python:3.7.6
EXPOSE 5000
WORKDIR /app

### Stage 2: Run ###
COPY . /app
# COPY requirements.txt /app
RUN pip install -r requirements.txt
# COPY app.py /app
CMD ["python3", "main.py"]
