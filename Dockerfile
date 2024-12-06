FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN curl -Ls https://cli.doppler.com/install.sh | sh

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["doppler", "run", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
