FROM python:3.10-slim

WORKDIR /app
COPY script.py .
RUN pip install mysql-connector-python

CMD ["python", "script.py"]