FROM python:3.9

COPY key.json .
COPY requirements.txt .

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-477.0.0-linux-x86_64.tar.gz
RUN tar -xf google-cloud-cli-477.0.0-linux-x86_64.tar.gz
RUN ./google-cloud-sdk/install.sh
RUN ./google-cloud-sdk/bin/gcloud auth activate-service-account --key-file key.json
RUN ./google-cloud-sdk/bin/gcloud config set project cloudragmini20242

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000:8000

CMD ["python", "main.py"]