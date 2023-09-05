FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /app/

WORKDIR /app/

RUN pip3 install -r requirements.txt

COPY ./app /app
ENV PYTHONPATH=/app
