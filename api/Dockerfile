FROM python:3

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY *.py /app/
RUN chmod a+x *.py

RUN mkdir -p /output && chmod -R 700 /output/

CMD ["./main.py"]

