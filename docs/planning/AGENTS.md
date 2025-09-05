# Agentes de Desenvolvimento - Cloud Transcrip

## 🤖 Agentes Especializados

### **1. Backend Developer Agent**
**Responsabilidade**: APIs, serviços, processamento áudio

```python
# Foco em:
- src/services/transcription.py (Groq, Google, HF APIs)
- src/services/audio_processor.py (pydub, conversões)  
- src/services/export_manager.py (TXT, JSON, MD)
- src/utils/file_utils.py (manipulação arquivos)
- Tratamento erros e retry logic
```

**Expertise**:
- Integração APIs REST (Groq, Google Cloud)
- Processamento áudio (pydub, ffmpeg) 
- Gerenciamento estado aplicação
- Otimização performance

---

### **2. Frontend Developer Agent**
**Responsabilidade**: Interface Streamlit, UX/UI

```python
# Foco em:
- src/app.py (interface principal)
- src/components/audio_uploader.py (drag & drop)
- src/components/block_editor.py (editor visual)
- src/components/export_panel.py (downloads)
- Layout responsivo e acessibilidade
```

**Expertise**:
- Streamlit avançado (components, state management)
- UX/UI para aplicações áudio
- Drag & drop interfaces
- Progress bars e feedback visual

---

### **3. DevOps Agent**  
**Responsabilidade**: Docker, deploy, CI/CD

```yaml
# Foco em:
- Dockerfile + docker-compose.yml
- deploy/ scripts (Cloud Run + VPS)
- .github/workflows/ (CI/CD)
- Nginx, SSL, domínios
- Monitoring e logs
```

**Expertise**:
- Docker otimização (multi-stage builds)
- Google Cloud Run deployment
- VPS Ubuntu 22.04 setup
- GitHub Actions
- SSL/TLS, reverse proxy

---

### **4. QA/Testing Agent**
**Responsabilidade**: Testes, qualidade, documentação

```python
# Foco em:
- tests/ (unit, integration)
- docs/ atualização
- Code review checklist
- Performance testing
- Security audit
```

**Expertise**:
- Testing frameworks (pytest, unittest)
- Audio processing testing
- API integration testing
- Documentation técnica

## 📂 Context Files por Agent

### **Backend Developer**
```
docs/context/
├── api-integrations.md      # Groq, Google Cloud, HF
├── audio-processing.md      # pydub workflows
├── data-structures.md       # ConversationBlock schema
└── error-handling.md        # Retry patterns, fallbacks
```

### **Frontend Developer**
```
docs/context/
├── streamlit-patterns.md    # Best practices UI
├── audio-ui-components.md   # Player, waveform, etc
├── drag-drop-editor.md      # sortables implementation
└── responsive-design.md     # Mobile compatibility
```

### **DevOps Agent**
```
docs/context/
├── docker-optimization.md   # Multi-stage, caching
├── cloudrun-config.md       # Secrets, scaling
├── vps-ubuntu-setup.md      # Nginx, SSL, backup
└── ci-cd-pipeline.md        # GitHub Actions
```

### **QA/Testing Agent**
```
docs/context/
├── testing-strategy.md      # Unit, integration, e2e
├── audio-test-data.md       # Sample files, edge cases
├── performance-benchmarks.md # Load testing
└── security-checklist.md    # API keys, CORS, etc
```

## 🎯 Agent Workflow por Sprint

### **Sprint 1: Fundação**
1. **DevOps**: Dockerfile + docker-compose
2. **Backend**: requirements.txt + config.py
3. **Frontend**: app.py Hello World
4. **QA**: Setup testing structure

### **Sprint 2: MVP**
1. **Backend**: Groq API + audio processing
2. **Frontend**: Upload + basic UI
3. **DevOps**: Environment variables
4. **QA**: API integration tests

### **Sprint 3: Advanced**
1. **Frontend**: Block editor + drag & drop
2. **Backend**: Export manager + cache
3. **QA**: UI testing + performance
4. **DevOps**: Production optimizations

### **Sprint 4: Deploy**
1. **DevOps**: Cloud Run deployment
2. **QA**: Production testing
3. **Backend**: Logging + monitoring
4. **Frontend**: Production UI tweaks

## 🤝 Colaboração entre Agents

### **Backend ↔ Frontend**
- Data structures padronizadas
- API contracts claros
- State management consistente

### **DevOps ↔ All**
- Environment parity (dev/prod)
- Deployment feedback loop
- Performance monitoring

### **QA ↔ All** 
- Continuous testing integration
- Code quality gates
- Documentation updates

## 📝 Agent Guidelines

### **Código Elegante**
- Seguir PEP 8 (Python)
- Docstrings em português
- Type hints sempre
- Error handling robusto

### **Documentação**
- README.md sempre atualizado
- Context files por mudança significativa
- API documentation inline
- Deployment guides step-by-step

### **Segurança**
- Nunca commitar secrets
- Validação input/output
- Rate limiting APIs
- Logs sem dados sensíveis