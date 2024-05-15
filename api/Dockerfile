FROM python:3.9

COPY key.json .
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000:8000

CMD ["python", "main.py"]