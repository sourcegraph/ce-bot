# docker build . -t your-repo/ce-bot
#
FROM python:3.8.5-slim-buster as builder
RUN apt-get update && apt-get clean
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.8.5-slim-buster as app
COPY --from=builder /build/ /app/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
WORKDIR /app/
COPY *.py /app/
ENTRYPOINT python3 app.py

#
#docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e VARIABLE_NAME="api" -p 3000:80 -it your-repo/ce-bot
#