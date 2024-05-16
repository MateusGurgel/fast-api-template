FROM python:3.9

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["bash", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]