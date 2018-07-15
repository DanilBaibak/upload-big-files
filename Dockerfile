FROM python:3.6-alpine

COPY . /web
WORKDIR /web/app

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
