# -----------------------------
# 🐍 Base Image
# -----------------------------
FROM python:3.11-slim

# -----------------------------
# ⚙️ Environment Variables
# -----------------------------
ENV PYTHONUNBUFFERED=True
ENV APP_HOME=/app

WORKDIR $APP_HOME

# -----------------------------
# 📦 System Dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 📥 Install Python Dependencies
# -----------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# -----------------------------
# 📂 Copy Project Files
# -----------------------------
COPY . .

# -----------------------------
# 🚀 Run App (Cloud Run Compatible)
# -----------------------------
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 0 app:app
