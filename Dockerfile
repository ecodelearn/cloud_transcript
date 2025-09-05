# Cloud Transcript - Dockerfile para desenvolvimento
FROM python:3.11-slim

# Metadados do projeto
LABEL maintainer="Daniel Dias <ecodelearn@outlook.com>"
LABEL description="Cloud Transcript - WhatsApp Audio Transcription"
LABEL version="1.0.0"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para áudio
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY .env.example .env

# Criar diretórios necessários
RUN mkdir -p uploads exports cache logs

# Usuário não-root para segurança
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expor porta do Streamlit
EXPOSE 8501

# Variáveis de ambiente
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando padrão (usar app simples para teste inicial)
CMD ["streamlit", "run", "src/app_simple.py", "--server.address=0.0.0.0", "--server.port=8501"]