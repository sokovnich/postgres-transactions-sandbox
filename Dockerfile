FROM python:3.8-slim-buster

EXPOSE 5000
WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && apt install -y libpq-dev gcc ssh
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY id_rsa id_rsa.pub /root/.ssh/

CMD ["python", "app.py"]
