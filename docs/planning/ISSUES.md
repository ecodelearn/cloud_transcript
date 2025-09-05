# Issues & Tasks - Cloud Transcrip

## 🎯 Sprint 1: Fundação (Issues #1-10)

### #1 - Setup Docker Development Environment
**Agent**: DevOps  
**Priority**: High  
**Estimate**: 1h

**Tasks**:
- [ ] Criar Dockerfile (Python 3.11-slim)
- [ ] docker-compose.yml com hot-reload
- [ ] .env.example com todas variáveis
- [ ] Volume mounts para desenvolvimento
- [ ] Testar `docker-compose up --build`

**Acceptance Criteria**:
- ✅ App Streamlit roda em localhost:8501
- ✅ Hot-reload funcionando
- ✅ Variáveis ambiente carregadas

---

### #2 - Project Structure & Base Files
**Agent**: Backend  
**Priority**: High  
**Estimate**: 30min

**Tasks**:
- [ ] src/app.py (Hello World Streamlit)
- [ ] src/config.py (configurações centralizadas)
- [ ] requirements.txt (dependencies base)
- [ ] src/__init__.py files

**Acceptance Criteria**:
- ✅ Estrutura importável
- ✅ Config carrega variáveis .env
- ✅ Streamlit hello world renderiza

---

### #3 - Update Documentation Structure
**Agent**: QA  
**Priority**: Medium  
**Estimate**: 30min

**Tasks**:
- [ ] Atualizar CLAUDE.md com nova estrutura
- [ ] Update .gitignore para pastas criadas
- [ ] README.md com quick start atualizado

---

## 🚀 Sprint 2: Core MVP (Issues #4-15)

### #4 - Groq API Integration  
**Agent**: Backend  
**Priority**: High  
**Estimate**: 2h

**Tasks**:
- [ ] src/services/transcription.py
- [ ] Groq client configuration
- [ ] Whisper-large-v3 PT-BR optimization
- [ ] Error handling + retry logic
- [ ] Rate limiting compliance

**Acceptance Criteria**:
- ✅ Transcreve .opus WhatsApp
- ✅ Qualidade 95%+ PT-BR
- ✅ Retry automático em falhas
- ✅ Logs estruturados

---

### #5 - Audio Processing Pipeline
**Agent**: Backend  
**Priority**: High  
**Estimate**: 1.5h

**Tasks**:
- [ ] src/services/audio_processor.py
- [ ] pydub integration (.opus, .mp3, .wav)
- [ ] Audio metadata extraction
- [ ] Format conversion pipeline
- [ ] Duration calculation

**Acceptance Criteria**:
- ✅ Suporta formatos: .opus, .mp3, .wav, .m4a
- ✅ Extrai duração + metadata
- ✅ Converte para formato Groq
- ✅ Validação arquivos áudio

---

### #6 - File Upload Component
**Agent**: Frontend  
**Priority**: High  
**Estimate**: 1.5h

**Tasks**:
- [ ] src/components/audio_uploader.py
- [ ] Drag & drop múltiplos arquivos
- [ ] Progress upload individual
- [ ] Preview arquivos carregados
- [ ] Validação tipos arquivo

**Acceptance Criteria**:
- ✅ Upload múltiplos áudios
- ✅ Drag & drop funcionando
- ✅ Progress visual
- ✅ Validation frontend

---

### #7 - Basic Export System
**Agent**: Backend  
**Priority**: Medium  
**Estimate**: 1h

**Tasks**:
- [ ] src/services/export_manager.py
- [ ] Export TXT básico
- [ ] Download automático
- [ ] Formatação timestamp
- [ ] Encoding UTF-8

**Acceptance Criteria**:
- ✅ Export TXT organizado
- ✅ Timestamps incluídos
- ✅ Download direto browser
- ✅ Encoding correto PT-BR

---

### #8 - Progress Tracking UI
**Agent**: Frontend  
**Priority**: Medium  
**Estimate**: 1h

**Tasks**:
- [ ] Progress bar transcrição
- [ ] Status individual por áudio
- [ ] Feedback visual erros
- [ ] Estimated time remaining

---

## 🎨 Sprint 3: Interface Avançada (Issues #9-18)

### #9 - Block Editor Component
**Agent**: Frontend  
**Priority**: High  
**Estimate**: 3h

**Tasks**:
- [ ] src/components/block_editor.py
- [ ] streamlit-sortables integration
- [ ] Visual timeline
- [ ] Inline editing transcrições
- [ ] Add context blocks

**Acceptance Criteria**:
- ✅ Drag & drop reordering
- ✅ Visual de timeline
- ✅ Edição inline
- ✅ Inserção contexto

---

### #10 - Advanced Export Formats
**Agent**: Backend  
**Priority**: Medium  
**Estimate**: 2h

**Tasks**:
- [ ] JSON structured export
- [ ] Markdown com timestamps
- [ ] Chat format para LLMs
- [ ] PDF export (opcional)

---

### #11 - Audio Player Integration
**Agent**: Frontend  
**Priority**: Medium  
**Estimate**: 1.5h

**Tasks**:
- [ ] Streamlit audio player
- [ ] Waveform preview
- [ ] Sync player com blocks
- [ ] Playback controls

---

### #12 - Smart Caching System  
**Agent**: Backend  
**Priority**: Medium  
**Estimate**: 1.5h

**Tasks**:
- [ ] Cache transcrições
- [ ] File hash verification
- [ ] Cache invalidation
- [ ] Storage management

---

## ☁️ Sprint 4: Cloud Deploy (Issues #13-20)

### #13 - Production Dockerfile
**Agent**: DevOps  
**Priority**: High  
**Estimate**: 1h

**Tasks**:
- [ ] docker/Dockerfile.prod
- [ ] Multi-stage build
- [ ] Size optimization
- [ ] Security hardening

---

### #14 - Cloud Run Deployment
**Agent**: DevOps  
**Priority**: High  
**Estimate**: 2h

**Tasks**:
- [ ] deploy/cloudrun-deploy.sh
- [ ] Secret Manager integration
- [ ] Scaling configuration
- [ ] Domain setup

---

### #15 - CI/CD Pipeline
**Agent**: DevOps  
**Priority**: Medium  
**Estimate**: 2h

**Tasks**:
- [ ] .github/workflows/deploy.yml
- [ ] Automated testing
- [ ] Security scanning
- [ ] Deploy on merge

---

## 🖥️ Sprint 5: VPS Migration (Issues #16-22)

### #16 - VPS Ubuntu Setup
**Agent**: DevOps  
**Priority**: Medium  
**Estimate**: 1.5h

**Tasks**:
- [ ] deploy/vps-setup.sh
- [ ] Docker installation
- [ ] Nginx configuration
- [ ] SSL certificate

---

### #17 - Production Monitoring
**Agent**: QA  
**Priority**: Medium  
**Estimate**: 1h

**Tasks**:
- [ ] Health checks
- [ ] Error logging
- [ ] Performance monitoring
- [ ] Backup strategy

---

## 🚨 Critical Issues (Sempre)

### #SECURITY - API Keys Protection
**Agent**: All  
**Priority**: Critical  
**Ongoing**

- [ ] Never commit secrets
- [ ] Environment validation
- [ ] Key rotation strategy
- [ ] Access logging

### #PERFORMANCE - Audio Processing
**Agent**: Backend  
**Priority**: High  
**Ongoing**

- [ ] Memory management large files
- [ ] Parallel processing
- [ ] Streaming upload
- [ ] Cache optimization

### #UX - Portuguese Language
**Agent**: Frontend  
**Priority**: High  
**Ongoing**

- [ ] Interface em português
- [ ] Error messages PT-BR
- [ ] Documentation português
- [ ] Timezone Brasil

## 📊 Issue Templates

### **Bug Report**
```markdown
**Describe the bug**: Clear description
**Steps to reproduce**: 1. 2. 3.
**Expected behavior**: What should happen
**Environment**: Local/Cloud/VPS
**Agent**: Which agent should fix
```

### **Feature Request**
```markdown
**Feature description**: What feature
**User story**: As a [user] I want [goal] so that [benefit]
**Acceptance criteria**: When is it done
**Agent**: Which agent implements
**Sprint**: Target sprint
```

### **Technical Task**
```markdown
**Task**: What needs to be done
**Technical details**: Implementation notes
**Dependencies**: Other issues/tasks
**Estimate**: Time estimate
**Agent**: Responsible agent
```