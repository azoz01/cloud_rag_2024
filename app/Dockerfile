FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001:8001
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

CMD ["streamlit", "run", "main.py", "--server.port", "8001", "--server.address", "0.0.0.0"]