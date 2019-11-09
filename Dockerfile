FROM python:3.8

WORKDIR /krobotkin

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./krobotkin .

CMD ["python", "krobotkin.py"]
