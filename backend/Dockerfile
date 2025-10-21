# Usar imagen oficial de Python
FROM python:3.11
# Directorio de trabajo
WORKDIR /app
# Copiar archivos
COPY requirements.txt .
# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copiar todo el backend
COPY ./app ./app
# Exponer puerto
EXPOSE 8000
# Comando para levantar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
