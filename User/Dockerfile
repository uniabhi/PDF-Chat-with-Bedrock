FROM python:3.11-slim

ENV AWS_ACCESS_KEY_ID=AKIAUQ4L3IQ523K6JEUJ
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_REGION=us-east-1
ENV BUCKET_NAME=youtube-demo-bedrock-chat-pdf56


EXPOSE 8084
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8084", "--server.address=0.0.0.0" ]