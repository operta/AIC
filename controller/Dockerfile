FROM python:3.8-slim as base

WORKDIR /code
RUN apt-get update && apt-get install -y build-essential
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

FROM python:3.8-slim

COPY --from=base /code /code
COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /code

CMD [ "python", "-u", "./server.py" ]