FROM python:3.10

WORKDIR /app

COPY . /app

RUN mkdir -p logs output

CMD ["tail", "-f", "/dev/null"]
