# Claude Code - Session Handoff Guidelines

## 🚨 Quando Aparece o Limite de 5h

**Situação**: Claude Code avisa sobre limite de uso por 5 horas.

**Ação Imediata**: Seguir este protocolo para **documentar e transferir** todo o contexto para a próxima sessão.

---

## 📋 Protocolo de Handoff (Pre-Limit)

### **1. Status Report (2-3 minutos)**

**Commitar estado atual IMEDIATAMENTE**:
```bash
# 1. Status atual
git add .
git status

# 2. Commit com estado detalhado
git commit -m "Session handoff: [STATUS]

Current work:
- Sprint: [qual sprint está rodando]
- Last completed: [última tarefa finalizada]  
- In progress: [o que está sendo feito agora]
- Next steps: [próximos 2-3 passos]
- Issues found: [problemas descobertos]

Environment:
- Docker status: [rodando/parado/erro]
- App status: [funcionando/error/não testado]
- Database: [OK/erro/não inicializado]

🚀 Desenvolvido com [IA Forte](https://iaforte.com.br)

Co-Authored-By: Daniel Dias <ecodelearn@outlook.com>"

# 3. Push para preservar
git push origin main
```

### **2. Update PROGRESS.md (1-2 minutos)**

Criar arquivo com status detalhado:

```bash
# Criar arquivo de progresso
cat > PROGRESS.md << 'EOF'
# Cloud Transcript - Progress Report

**Session Date**: $(date)
**Session Duration**: [tempo da sessão]
**Sprint**: [current sprint]

## ✅ Completed Today
- [x] Task 1 completed
- [x] Task 2 completed  

## 🔄 In Progress  
- [ ] Task currently working on
- Status: [detailed status]
- Files changed: [list]
- Next steps: [immediate next steps]

## ❌ Issues Found
- Issue 1: [description + how to reproduce]
- Issue 2: [description + solution attempted]

## 🎯 Next Session Priorities
1. [Most important next task]
2. [Second priority]
3. [Third priority]

## 🔧 Environment Status
- **Docker**: [running/stopped/error - which compose file]
- **App URL**: [http://localhost:8501 or error]
- **Database**: [status/location/issues]
- **Last working state**: [describe last known good state]

## 📁 Key Files Modified This Session
```
find . -type f -mtime -1 -not -path './.git/*' | head -20
```

## 🧠 Context for Next Session
[Any important context, decisions made, approaches tried]

EOF

git add PROGRESS.md
git commit -m "Add progress report for session handoff"
git push
```

### **3. Quick Deployment Test (30 segundos)**

```bash
# Test current state
docker-compose ps

# If not running, note what needs to start:
echo "To continue: docker-compose up --build" > NEXT_STEPS.txt
# or
echo "To continue: docker-compose -f docker-compose.cpu.yml up --build" > NEXT_STEPS.txt
```

---

## 🔄 Protocolo de Handoff (Post-Limit)

### **Para a Nova Sessão Claude Code**:

**Primeira mensagem da nova sessão**:

```
Olá! Estou dando continuidade ao desenvolvimento do projeto Cloud Transcript. 

Por favor:

1. Leia o último commit do git para ver o status
2. Verifique o arquivo PROGRESS.md  
3. Me dê um resumo do que precisa continuar
4. Execute os NEXT_STEPS.txt se houver

Projeto: Sistema de transcrição WhatsApp com GPU RTX 3060
Repo: https://github.com/ecodelearn/cloud_transcript.git
```

### **Para Claude Code Responder**:

1. **ler**: `git log -1 --pretty=format:"%B"` 
2. **ler**: `PROGRESS.md`
3. **ler**: `NEXT_STEPS.txt` (se existir)
4. **resumir**: Status atual + próximos passos
5. **executar**: Comandos necessários para continuar

---

## 📚 Context Files Essenciais

**Sempre manter atualizados**:

### **docs/planning/EVOLUTION.md**
- Roadmap geral das 5 fases
- Contexto do projeto (consultoria IA)

### **CLAUDE.md**  
- Informações técnicas para Claude Code
- Comandos de desenvolvimento
- Arquitetura atual

### **README.md**
- Setup instructions
- Como rodar localmente

### **Last Git Commit Message**
- Estado atual da sessão
- Próximos passos
- Issues conhecidos

---

## ⚡ Quick Commands Reference

### **Status Check**
```bash
# Ver commits recentes
git log --oneline -5

# Ver arquivos modificados  
git status

# Ver se app está rodando
curl -s http://localhost:8501/_stcore/health

# Ver containers
docker ps
```

### **Continue Development**  
```bash
# Opção 1: Versão completa (pesada)
docker-compose up --build

# Opção 2: CPU-only (leve) 
docker-compose -f docker-compose.cpu.yml up --build

# Opção 3: Minimal test
docker-compose -f docker-compose.minimal.yml up --build

# Opção 4: GPU (RTX 3060)
docker-compose -f docker-compose.gpu.yml up --build
```

---

## 🎯 Success Metrics

**Handoff bem-sucedido quando**:
- ✅ Nova sessão consegue resumir o estado atual
- ✅ Nova sessão sabe quais comandos executar
- ✅ Não há perda de contexto sobre decisões técnicas
- ✅ Issues conhecidos estão documentados
- ✅ Próximos passos estão claros

**Tempo total de handoff**: < 5 minutos

---

## 📝 Template Rápido

**Use este template quando o limite aparecer**:

```markdown
## 🚨 SESSION HANDOFF NEEDED

**Current Sprint**: [sprint number/name]
**Last Task**: [what was just completed] ✅  
**Current Task**: [what is in progress] 🔄
**Blocking Issue**: [any current blocker] ❌
**Next Step**: [immediate next action] ➡️

**Docker Status**: [compose file + status]
**App Status**: [URL + working/broken]

**For next session**: 
1. [first thing to do]
2. [second thing to do]
3. [third thing to do]

**Files to check**: 
- [important file 1]
- [important file 2]
```

Este protocolo garante **continuidade perfeita** entre sessões! 🎯