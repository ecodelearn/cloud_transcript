# Cloud Transcript 🎵➡️📝

Transcritor inteligente de conversas WhatsApp com **GPU local** (RTX 3060) e fallbacks para APIs cloud.

## ✨ Funcionalidades

- 🚀 **GPU Local**: Whisper rodando direto na RTX 3060 (ultra-rápido!)
- 📁 **Upload múltiplo** de áudios (.opus, .mp3, .wav, .m4a)
- 🤖 **Múltiplas engines**: Local GPU → Groq → Google Cloud → HuggingFace
- ✏️ **Editor visual** para inserção de contexto entre áudios
- 🔄 **Reordenação** drag & drop dos blocos de conversa
- 📤 **Exportação flexível** (TXT, JSON, Markdown, Chat format)
- 🐳 **Docker + GPU** para desenvolvimento otimizado

## 🛠️ Tecnologias

- **NVIDIA CUDA** + **PyTorch** - Aceleração GPU
- **OpenAI Whisper large-v3** - Transcrição local
- **Python 3.11** + **Streamlit** - Interface web
- **Docker + NVIDIA Container Runtime** - Containerização GPU

## ⚡ Configurações de Performance

### **Modo GPU Local (Recomendado)**
- **RTX 3060** - ~10x mais rápido que APIs
- **Whisper large-v3** - Qualidade máxima PT-BR
- **Sem limites** de uso ou rate limiting
- **Privacidade total** - nada sai da máquina

### **Modo API Cloud (Fallback)**
- **Groq**: 6.000 segundos/minuto grátis
- **Google Cloud**: 60 minutos/mês grátis
- **HuggingFace**: Rate limited

## 🚀 Início Rápido

### Pré-requisitos

- **NVIDIA RTX 3060** (ou GPU compatível)
- **NVIDIA Container Toolkit** instalado
- **Docker Desktop** com GPU support
- **WSL2** (se Windows)

### Configuração GPU (Primeira vez)

1. **Instale NVIDIA Container Toolkit**
   ```bash
   # Ubuntu/WSL2
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

2. **Teste GPU Docker**
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
   ```

### Executar com GPU

1. **Clone e configure**
   ```bash
   git clone https://github.com/ecodelearn/cloud_transcript.git
   cd cloud_transcript
   cp .env.example .env
   ```

2. **Configure modo GPU no .env**
   ```env
   TRANSCRIPTION_MODE=local_gpu
   USE_LOCAL_GPU=true
   WHISPER_MODEL=large-v3
   ```

3. **Execute com GPU** 🚀
   ```bash
   docker-compose -f docker-compose.gpu.yml up --build
   ```

4. **Acesse a aplicação**
   ```
   http://localhost:8501
   ```

### Executar sem GPU (CPU/APIs)

```bash
# Modo tradicional com APIs cloud
docker-compose up --build
```

## 📋 Comandos Disponíveis

### **GPU Mode (Recomendado)**
```bash
# Iniciar com GPU
docker-compose -f docker-compose.gpu.yml up --build

# Background com GPU  
docker-compose -f docker-compose.gpu.yml up -d

# Logs GPU
docker-compose -f docker-compose.gpu.yml logs -f app

# Parar GPU
docker-compose -f docker-compose.gpu.yml down
```

### **CPU Mode**
```bash
# Iniciar CPU/API mode
docker-compose up --build

# Ver logs
docker-compose logs -f app

# Parar
docker-compose down
```

### **Monitoramento GPU**
```bash
# Ver uso GPU em tempo real
watch -n 1 nvidia-smi

# Logs GPU do container
docker exec -it cloud_transcript_gpu nvidia-smi
```

## 🏗️ Arquitetura

```
cloud_transcript/
├── src/                   # Código fonte
│   ├── app.py            # Interface Streamlit
│   ├── services/
│   │   ├── transcription.py      # Multi-engine (GPU + APIs)
│   │   ├── whisper_gpu.py        # Whisper local GPU
│   │   └── audio_processor.py    # Processamento áudio
│   └── components/               # Componentes UI
├── docker-compose.yml           # CPU/API mode
├── docker-compose.gpu.yml       # GPU mode
├── Dockerfile                   # Base container
├── Dockerfile.gpu               # GPU container
├── requirements.txt             # CPU dependencies
├── requirements.gpu.txt         # GPU dependencies
└── models/                      # Cache modelos Whisper
```

## 🎯 Benchmarks Performance

| Modo | Áudio 5min | Qualidade | Custo | Privacidade |
|------|------------|-----------|-------|-------------|
| **RTX 3060** | ~30s | 95%+ PT-BR | Grátis | 100% Local |
| Groq API | ~45s | 90% PT-BR | Free tier | Cloud |
| Google Cloud | ~60s | 92% PT-BR | Free tier | Cloud |

## 🔧 Configuração Avançada

### **Otimização GPU**
```env
# .env para RTX 3060
TORCH_CUDA_ARCH_LIST="8.6"
CUDA_VISIBLE_DEVICES=0
WHISPER_MODEL=large-v3
WHISPER_DEVICE=cuda

# Para GPUs com pouca VRAM
WHISPER_MODEL=medium
TORCH_PRECISION=fp16
```

### **Fallback Automático**
O sistema tenta na ordem:
1. **Local GPU** (se disponível)
2. **Groq API** (se configurado)  
3. **Google Cloud** (se configurado)
4. **HuggingFace** (backup)

## 📤 Deploy Produção

### **Google Cloud Run**
```bash
# Build para produção (sem GPU)
docker build -f Dockerfile -t cloud-transcript .
gcloud run deploy --image cloud-transcript
```

### **VPS Ubuntu 22.04**
```bash
# Deploy em vps.frontzin.com.br
./deploy/vps-deploy.sh
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m 'Add nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE)

## 🆘 Suporte

- 🌐 **Website**: [IA Forte](https://iaforte.com.br)
- 📧 **Email**: ecodelearn@outlook.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/ecodelearn/cloud_transcript/issues)

---

**⚡ Powered by RTX 3060 + desenvolvido com ❤️ pela [IA Forte](https://iaforte.com.br)**