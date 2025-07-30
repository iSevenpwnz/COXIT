# 📄 PDF Summary AI

Потужний веб-застосунок для завантаження великих PDF файлів (до 100 сторінок, 50MB) та отримання стислих AI-резюме за допомогою OpenAI API.

## 🚀 Особливості

- **📤 Завантаження PDF**: Користувачі можуть легко завантажувати PDF файли через drag & drop або файловий браузер
- **🔍 Комплексний парсинг PDF**: Точне витягування контенту з PDF з повною підтримкою тексту, зображень та складних таблиць
- **🤖 AI-резюме**: Інтеграція з OpenAI API для створення високоякісних резюме завантажених документів
- **📚 Остання історія**: Відображення списку 5 останніх опрацьованих PDF з ключовими метаданими та можливістю перегляду резюме

## 🛠 Технології

### Backend

- **FastAPI** - Сучасний, швидкий веб-фреймворк для Python
- **OpenAI API** - Для генерації AI-резюме
- **PyPDF2, PyMuPDF, pdfplumber** - Для парсингу PDF файлів
- **Uvicorn** - ASGI сервер

### Frontend

- **Vue 3** - Прогресивний JavaScript фреймворк
- **TypeScript** - Типізований JavaScript
- **Vite** - Швидкий збирач проекту
- **Pinia** - Стан менеджмент для Vue

### DevOps

- **Docker** - Контейнеризація застосунку
- **Nginx** - Веб-сервер для frontend
- **Docker Compose** - Оркестрація сервісів

## 📋 Передумови

- Docker та Docker Compose
- OpenAI API ключ

## 🚀 Швидкий старт

### 1. Клонування репозиторію

\`\`\`bash
git clone <repository-url>
cd cotix_test
\`\`\`

### 2. Налаштування змінних оточення

\`\`\`bash

# Скопіюйте .env файл та додайте свій OpenAI API ключ

cp .env.example .env

# Відредагуйте .env файл та додайте ваш OPENAI_API_KEY

\`\`\`

### 3. Запуск через Docker Compose

\`\`\`bash

# Збірка та запуск всіх сервісів

docker-compose up --build

# Або в фоновому режимі

docker-compose up -d --build
\`\`\`

### 4. Доступ до застосунку

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документація**: http://localhost:8000/docs

## 🔧 Розробка

### Backend

\`\`\`bash
cd backend

# Створіть віртуальне середовище

python -m venv venv
source venv/bin/activate # Linux/Mac

# або

venv\\Scripts\\activate # Windows

# Встановіть залежності

pip install -r requirements.txt

# Запустіть сервер розробки

uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

### Frontend

\`\`\`bash
cd frontend

# Встановіть залежності

npm install

# Запустіть сервер розробки

npm run dev

# Збірка для продакшну

npm run build

# Тестування

npm run test:unit
npm run test:e2e
\`\`\`

## 📡 API Ендпоїнти

### POST /upload

Завантаження PDF файлу для обробки

- **Тіло запиту**: MultipartForm з файлом
- **Відповідь**: Метадані файлу та AI-резюме

### GET /history

Отримання останніх 5 опрацьованих PDF

- **Відповідь**: Список файлів з метаданими

### GET /download/{summary_id}

Отримання AI-резюме за ID

- **Параметри**: summary_id (string)
- **Відповідь**: Текст резюме

### GET /health

Перевірка стану сервера

- **Відповідь**: Статус сервера

## 🐳 Docker команди

\`\`\`bash

# Збірка образів

docker-compose build

# Запуск сервісів

docker-compose up

# Запуск у фоні

docker-compose up -d

# Зупинка сервісів

docker-compose down

# Перегляд логів

docker-compose logs -f

# Перестворення з нуля

docker-compose down -v
docker-compose up --build
\`\`\`

## 📁 Структура проекту

\`\`\`
cotix_test/
├── backend/ # FastAPI backend
│ ├── main.py # Головний файл застосунку
│ ├── requirements.txt # Python залежності
│ ├── Dockerfile # Docker образ для backend
│ ├── .env # Змінні оточення
│ └── .env.example # Приклад змінних оточення
├── frontend/ # Vue.js frontend
│ ├── src/
│ │ ├── components/ # Vue компоненти
│ │ ├── App.vue # Головний компонент
│ │ ├── main.ts # Точка входу
│ │ └── style.css # Глобальні стилі
│ ├── package.json # Node.js залежності
│ ├── Dockerfile # Docker образ для frontend
│ ├── nginx.conf # Налаштування Nginx
│ └── vite.config.ts # Конфігурація Vite
├── storage/ # Зберігання файлів
│ ├── pdfs/ # Завантажені PDF файли
│ ├── summaries/ # Згенеровані резюме
│ └── meta/ # Метадані файлів
├── docker-compose.yml # Оркестрація Docker
├── .env # Глобальні змінні оточення
└── README.md # Документація проекту
\`\`\`

## 🔒 Безпека

- CORS налаштовано для дозволених доменів
- Валідація типів файлів (тільки PDF)
- Обмеження розміру файлів (50MB максимум)
- Обмеження кількості сторінок (100 максимум)
- Санітизація введених даних

## 🚨 Усунення проблем

### Помилки з OpenAI API

- Переконайтеся, що ваш API ключ правильний
- Перевірте квоти на вашому OpenAI акаунті
- Переконайтеся, що у вас є доступ до GPT-3.5-turbo

### Проблеми з Docker

\`\`\`bash

# Очищення Docker кешу

docker system prune -a

# Перестворення volumes

docker-compose down -v
docker volume prune
\`\`\`

### Помилки з PDF парсингом

- Переконайтеся, що PDF не захищений паролем
- Файл повинен бути валідним PDF
- Розмір файлу не повинен перевищувати 50MB

## 📝 Ліцензія

Цей проект створено для технічного завдання COXIT.

## 🤝 Вклад у розробку

1. Створіть fork репозиторію
2. Створіть feature гілку (\`git checkout -b feature/AmazingFeature\`)
3. Зробіть commit змін (\`git commit -m 'Add some AmazingFeature'\`)
4. Push на гілку (\`git push origin feature/AmazingFeature\`)
5. Відкрийте Pull Request

## 📞 Підтримка

Якщо у вас виникли питання або проблеми, створіть issue в цьому репозиторії.
