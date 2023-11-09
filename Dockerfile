FROM python:3.11

WORKDIR /app

COPY server/ /app/server
COPY wsgi.py /app/wsgi.py
COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 1000
CMD ["python3", "wsgi.py"]
