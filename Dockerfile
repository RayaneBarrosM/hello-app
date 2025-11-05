# Use uma imagem base Python
FROM python:3.11-slim-buster 

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Usuário e diretório (boa prática de segurança)
RUN adduser --system --group app
WORKDIR /app
USER app

# Copiar e instalar dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação (incluindo main.py)
COPY . /app/

# Expor a porta (ajuste conforme necessário, 8000 é comum para Uvicorn)
EXPOSE 8000 

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]