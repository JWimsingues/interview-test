FROM python:3

RUN mkdir -p /code
COPY app.py /code/app.py
COPY requirements.txt  /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

CMD [ "python", "/code/app.py" ]