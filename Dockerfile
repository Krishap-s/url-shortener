
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 80/tcp

CMD ["gunicorn","main:app", "-b", "0.0.0.0:80", "-k" , "uvicorn.workers.UvicornWorker"]