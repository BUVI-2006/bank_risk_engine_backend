FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD uvicorn evaluator:app --host 0.0.0.0 --port 5000 --workers 4
