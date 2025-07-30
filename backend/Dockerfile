FROM python:3.11-slim

WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо requirements та встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY . .

# Створюємо директорії для storage
RUN mkdir -p /app/storage/pdfs /app/storage/summaries /app/storage/meta

# Відкриваємо порт
EXPOSE 8000

# Запускаємо застосунок
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]