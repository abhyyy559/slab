# SENTRY full stack: mocks + console + agent + Chromium in one image.
FROM mcr.microsoft.com/playwright/python:v1.62.0-jammy

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8765
CMD ["bash", "start.sh"]
