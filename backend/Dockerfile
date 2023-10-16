FROM python:3.9
WORKDIR /usr/local/src/app

COPY ./requirements.txt /usr/local/src/app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r  requirements.txt

COPY . /usr/local/src/app

CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000} --workers 1