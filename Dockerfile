FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
