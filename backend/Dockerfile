# Dockerfile para PequeLectores Backend
FROM python:3.14-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero para cachear mejor
COPY backend/requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY backend/ .

# Crear directorio para la aplicación
RUN mkdir -p /app/app

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]