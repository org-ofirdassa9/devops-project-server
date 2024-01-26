FROM python:3.10-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install -r init-requirements.txt

CMD ["python3", "database_init.py"]