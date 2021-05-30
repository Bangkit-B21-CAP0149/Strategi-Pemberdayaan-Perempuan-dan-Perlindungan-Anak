FROM python:3.8-slim-buster
WORKDIR .

COPY requirements.txt /tmp/requirements.txt
COPY . .
RUN pip install cython
RUN python -m pip install tensorflow
RUN pip install -r /tmp/requirements.txt

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]