# Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Копіюємо package files
COPY package*.json ./

# Встановлюємо залежності
RUN npm install

# Копіюємо код та збираємо
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

# Копіюємо зібрані файли
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копіюємо конфігурацію nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]