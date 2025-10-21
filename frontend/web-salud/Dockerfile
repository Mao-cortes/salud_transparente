# Etapa de construcción
FROM node:16-alpine AS build
WORKDIR /app

# Copiar solo los archivos necesarios para la instalación de dependencias
COPY package*.json ./
COPY angular.json ./
COPY tsconfig*.json ./

# Instalar dependencias
RUN npm ci

# Copiar el resto de los archivos del proyecto
COPY . .

# Construir la aplicación para producción
RUN npm run build -- --configuration production

# Etapa de producción
FROM node:16-alpine
WORKDIR /app

# Instalar un servidor ligero
RUN npm install -g serve

# Copiar los archivos construidos desde la etapa de construcción
COPY --from=build /app/dist/web-salud ./dist

# Exponer el puerto 4200
EXPOSE 4200
# Comando para servir la aplicación
CMD ["serve", "-s", "dist", "-l", "4200"]

