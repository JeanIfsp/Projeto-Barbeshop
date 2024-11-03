# Usa uma imagem base Python
FROM python:3.10

WORKDIR /app

COPY ./src /app

COPY ./src/requeriments.txt /app/requeriments.txt

RUN pip install --no-cache-dir -r requeriments.txt

# Copia o código do projeto para dentro do container
COPY . .

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED 1

# Expõe a porta usada pelo Gunicorn
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
