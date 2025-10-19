# Etapa 1: construcción del proyecto Angular
FROM node:16 AS build
WORKDIR /app
COPY web-salud/package*.json ./
RUN npm install -g @angular/cli@16.2.10
RUN npm install
COPY web-salud .
RUN ng build --configuration production

# Etapa 2: servir la aplicación con Nginx
FROM nginx:alpine
COPY --from=build /app/dist/web-salud /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
