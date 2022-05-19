FROM python:3.7.13
COPY ./app /app
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install pymysql

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--port","8000", "--reload"]