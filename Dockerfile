FROM python:3.13-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

WORKDIR /eshop

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY main.py .
COPY migrations ./migrations
COPY alembic.ini .
COPY pytest.ini .
COPY .env .

COPY entrypoint.sh .
RUN chmod +x /eshop/entrypoint.sh

ENTRYPOINT ["/eshop/entrypoint.sh"]
