FROM python:3.8

RUN apk add libffi-dev libnacl-dev python3-dev

WORKDIR /krobotkin

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./krobotkin .

CMD ["python", "krobotkin.py"]
