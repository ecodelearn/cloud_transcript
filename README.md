# Cloud Transcript 🎵➡️📝

Transcritor inteligente de conversas WhatsApp que processa múltiplos áudios de forma sequencial, permitindo inserção de contexto textual e exportação organizada.

## ✨ Funcionalidades

- 📁 **Upload múltiplo** de áudios (.opus, .mp3, .wav, .m4a)
- 🤖 **Transcrição automatizada** usando Groq (Whisper-large-v3)
- ✏️ **Editor visual** para inserção de contexto entre áudios
- 🔄 **Reordenação** drag & drop dos blocos de conversa
- 📤 **Exportação flexível** (TXT, JSON, Markdown, Chat format)
- 🚀 **Interface web** intuitiva com Streamlit
- 🐳 **Docker Compose** para desenvolvimento local

## 🛠️ Tecnologias

- **Python 3.9+**
- **Streamlit** - Interface web
- **Groq API** - Transcrição com Whisper-large-v3
- **pydub** - Processamento de áudio
- **Docker & Docker Compose** - Containerização

## 🚀 Início Rápido

### Pré-requisitos

- Docker e Docker Compose instalados
- Chave da API Groq (gratuita: 6.000 segundos/minuto)

### Configuração

1. **Clone o repositório**
   ```bash
   git clone https://github.com/ecodelearn/cloud_transcript.git
   cd cloud_transcript
   ```

2. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas chaves de API
   ```

3. **Inicie a aplicação**
   ```bash
   docker-compose up --build
   ```

4. **Acesse a aplicação**
   ```
   http://localhost:8501
   ```

## 📋 Comandos de Desenvolvimento

```bash
# Iniciar aplicação
docker-compose up --build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Parar aplicação
docker-compose down

# Rebuild após mudanças
docker-compose up --build
```

## 🏗️ Arquitetura

```
cloud_transcrip/
├── app.py                 # Interface principal Streamlit
├── services/
│   ├── transcription.py   # APIs de transcrição
│   ├── audio_processor.py # Processamento de áudio
│   └── export_manager.py  # Gerenciamento de exports
├── components/
│   ├── audio_uploader.py  # Componente de upload
│   ├── block_editor.py    # Editor de blocos
│   └── export_panel.py    # Painel de exportação
├── utils/
│   ├── file_utils.py      # Utilitários de arquivo
│   └── format_utils.py    # Formatação de dados
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 📊 APIs de Transcrição Suportadas

### 1. Groq (Recomendada)
- **Modelo**: Whisper-large-v3
- **Free-tier**: 6.000 segundos/minuto
- **Qualidade**: Excelente para PT-BR
- **Latência**: ~2-3 segundos

### 2. Google Cloud Speech-to-Text
- **Free-tier**: 60 minutos/mês
- **Qualidade**: Muito boa para PT-BR
- **Suporte nativo**: Pontuação automática

### 3. Hugging Face Inference API
- **Modelo**: openai/whisper-large-v3
- **Free-tier**: Limitado por requests/hora
- **Vantagem**: Sem necessidade de chave paga

## 🔄 Fluxo de Trabalho

1. **Upload**: Faça upload de múltiplos arquivos de áudio
2. **Processamento**: A aplicação processa automaticamente via API
3. **Edição**: Use o editor visual para inserir contexto e reorganizar
4. **Export**: Escolha o formato de saída desejado

## 📦 Deploy

### Local (Docker Compose)
```bash
docker-compose up --build
```

### Google Cloud Run
```bash
# Build e deploy para Cloud Run
gcloud run deploy cloud-transcrip --source .
```

### VPS
```bash
# Deploy tradicional com Docker
docker build -t cloud-transcrip .
docker run -p 8501:8501 cloud-transcrip
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Para dúvidas, sugestões ou suporte técnico:

- 🌐 **Website**: [IA Forte](https://iaforte.com.br)
- 📧 **Email**: ecodelearn@outlook.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/ecodelearn/cloud_transcript/issues)

---

**Desenvolvido com ❤️ pela equipe [IA Forte](https://iaforte.com.br)**