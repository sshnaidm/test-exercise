FROM python:3-alpine
LABEL maintainer "sshnaidm <einarum@gmail.com>"
LABEL name "testex"

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade -r requirements.txt -r test-requirements.txt && \
    python setup.py test

WORKDIR /app/testex
EXPOSE 4000
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true

ENTRYPOINT ["/app/run_server.sh"]
