# Cloud Transcript - Roadmap de Desenvolvimento

## 🎯 Objetivo Evolutivo
**Fase 1**: Transcritor WhatsApp com GPU local (RTX 3060)  
**Fase 2**: Plataforma gestão projetos consultoria IA  
**Fase 3**: Cloud híbrido (Supabase + VPS)  
**Futuro**: SaaS para outros consultores

## 🖥️ Ambientes

### **Desenvolvimento**
- **Local**: WSL2 Arch Linux + VSCode + Docker Desktop (Windows 11)
- **Python**: 3.11 (compatibilidade máxima)
- **Container**: Docker Compose para hot-reload

### **Produção**
- **Cloud Run**: inarte@gmail.com (Free Tier) - Deploy inicial
- **VPS**: vps.frontzin.com.br (Ubuntu 22.04) - Produção final

## 📋 Sprints de Desenvolvimento

### **Sprint 1: Docker + GPU Setup (1 semana)**
**Objetivo**: Base funcionando + GPU RTX 3060

#### Tasks:
- [x] ~~Estrutura de pastas~~ ✅
- [x] ~~Docker CPU/GPU configs~~ ✅ 
- [x] ~~Hello World Streamlit~~ ✅
- [ ] SQLite + schema inicial
- [ ] Whisper GPU funcionando
- [ ] Interface básica upload

#### Entregáveis:
```bash
docker-compose -f docker-compose.gpu.yml up --build
# ✅ App + GPU rodando localhost:8501
```

---

### **Sprint 2: Transcrição Core (1 semana)**
**Objetivo**: Upload + GPU Whisper + Exports

#### Tasks:
- [ ] src/services/whisper_gpu.py (RTX 3060)
- [ ] src/services/audio_processor.py (segmentação 4h)
- [ ] src/components/audio_uploader.py (drag&drop)
- [ ] Processamento áudios longos (2-4h meetings)
- [ ] Progress bar + timeline
- [ ] Export múltiplos formatos

#### Entregáveis:
- Upload → GPU Transcription → Export TXT/JSON/MD
- Performance: 4h áudio = 8min processamento

---

### **Sprint 3: Gestão Projetos (1 semana)**
**Objetivo**: CRUD projetos + múltiplos meetings

#### Tasks:
- [ ] SQLite schema (projects, meetings, insights)
- [ ] src/models/ (database models)
- [ ] CRUD projects/meetings interface
- [ ] Timeline navigation (múltiplas sessões)
- [ ] Busca/filtros por cliente/data
- [ ] LLM analysis (requisitos, tecnologias)

#### Entregáveis:
- Gestão completa projetos consultoria
- Múltiplos meetings por projeto
- Análise automática LLM

---

### **Sprint 4: Cloud Sync (1 semana)**
**Objetivo**: Supabase + backup + acesso remoto

#### Tasks:
- [ ] Supabase integration
- [ ] Migration SQLite → PostgreSQL
- [ ] Sync automático dados
- [ ] Storage otimizado (300GB limit)
- [ ] Web access + API REST

#### Entregáveis:
- Dados sincronizados Supabase
- Acesso remoto funcionando
- Backup automático configurado

---

### **Sprint 5: VPS Migration (1 hora)**
**Objetivo**: Migração para VPS se free tier insufficient

#### Tasks:
- [ ] deploy/vps-setup.sh (Ubuntu 22.04)
- [ ] docker-compose.prod.yml
- [ ] Nginx reverse proxy
- [ ] SSL certificate (Let's Encrypt)
- [ ] Backup strategy

#### Entregáveis:
- App rodando: https://vps.frontzin.com.br
- SSL + domínio personalizado

## 🔧 Tecnologias por Sprint

### **Sprint 1-2: Core**
```python
streamlit>=1.28.0
groq>=0.4.0  
pydub>=0.25.0
python-dotenv>=1.0.0
```

### **Sprint 3: Advanced UI**
```python
streamlit-sortables>=0.2.0
streamlit-ace>=0.1.0
streamlit-aggrid>=0.3.0  # Tabelas interativas
```

### **Sprint 4-5: Deploy**
```yaml
# Cloud Run
gunicorn>=21.2.0

# VPS
nginx
certbot
```

## 🎯 Critérios de Sucesso

### **MVP (Sprint 2)**
- ✅ Upload 5+ áudios WhatsApp (.opus)
- ✅ Transcrição PT-BR 95%+ precisão
- ✅ Export TXT organizado
- ✅ Interface responsiva

### **Produção (Sprint 4)**
- ✅ Deploy automatizado Cloud Run
- ✅ HTTPS funcionando
- ✅ Variáveis ambiente seguras
- ✅ Logs estruturados

### **Escalabilidade (Sprint 5)**
- ✅ VPS pronto para migração
- ✅ Backup automático
- ✅ Monitoring básico
- ✅ SSL personalizado

## ⚡ Quick Start (Desenvolvimento)

```bash
# Setup inicial
git clone https://github.com/ecodelearn/cloud_transcript.git
cd cloud_transcript
cp .env.example .env

# Configurar GROQ_API_KEY no .env
docker-compose up --build

# Acessar: http://localhost:8501
```

## 📝 Notas Importantes

- **Simplicidade**: Foco em código elegante e manutenível  
- **Segurança**: Nunca commitar chaves API
- **Compatibilidade**: Python 3.11 para máxima compatibilidade
- **Deploy**: Cloud Run primeiro, VPS como backup
- **Monitoring**: Logs estruturados desde Sprint 1