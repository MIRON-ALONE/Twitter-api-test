FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV API_KEY=""
ENV API_SECRET=""
ENV ACCESS_TOKEN=""
ENV ACCESS_SECRET=""

CMD ["python", "main.py"]
