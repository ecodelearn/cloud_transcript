# VPS Deployment Configuration

## 🚨 Conflito Detection & Resolution

### **Situação Atual**:
- VPS: vps.frontzin.com.br (Ubuntu 22.04)
- Projeto existente rodando em Docker
- Supabase + PostgreSQL já configurados (300GB limit)

### **Estratégia de Deploy Isolado**:

## 📋 Option 1: Subdomain (Recomendado)
```
Projeto existente: https://vps.frontzin.com.br
Cloud Transcript: https://transcript.frontzin.com.br
```

**Deploy Config**:
```yaml
# docker-compose.vps.yml
services:
  cloud_transcript:
    container_name: cloud_transcript_prod
    ports:
      - "8502:8501"  # Different port from existing project
    environment:
      - VIRTUAL_HOST=transcript.frontzin.com.br
      - LETSENCRYPT_HOST=transcript.frontzin.com.br
    networks:
      - nginx-proxy  # Use existing nginx-proxy network
```

## 📋 Option 2: Different Port (Backup)
```
Projeto existente: https://vps.frontzin.com.br
Cloud Transcript: https://vps.frontzin.com.br:8502
```

## 📋 Option 3: Path-Based (Se necessário)
```
Projeto existente: https://vps.frontzin.com.br/
Cloud Transcript: https://vps.frontzin.com.br/transcript/
```

---

## 🔧 VPS Resource Management

### **Current Resources Check**:
```bash
# Check current Docker containers
docker ps -a

# Check port usage
netstat -tulpn | grep :8501
netstat -tulpn | grep :8502

# Check disk usage (for 300GB limit)
df -h
docker system df

# Check Supabase connection
docker logs supabase_container_name
```

### **Shared Resources**:
- ✅ **Nginx Proxy**: Reutilizar proxy existente
- ✅ **SSL Certificates**: Let's Encrypt já configurado
- ✅ **Supabase**: Compartilhar mesma instância (cuidar do limite 300GB)
- ✅ **Docker Network**: nginx-proxy network

### **Isolated Resources**:
- 🔧 **Container Name**: `cloud_transcript_prod`
- 🔧 **Port**: `8502` (ao invés de 8501)
- 🔧 **Volume Paths**: `/opt/cloud_transcript/`
- 🔧 **Database**: Schema separado no mesmo Supabase

---

## 🗄️ Database Strategy

### **Option A: Shared Supabase with Schema Isolation**
```sql
-- Create dedicated schema
CREATE SCHEMA cloud_transcript;

-- Move tables to schema  
CREATE TABLE cloud_transcript.projects (...);
CREATE TABLE cloud_transcript.meetings (...);

-- Update connection string
DATABASE_URL=postgresql://user:pass@supabase/db?schema=cloud_transcript
```

### **Option B: Separate Database**
```sql
-- Create new database in same Supabase instance
CREATE DATABASE cloud_transcript_db;
```

---

## 📂 VPS Directory Structure

```bash
/opt/
├── existing_project/        # Projeto atual
├── cloud_transcript/        # Novo projeto
│   ├── docker-compose.yml
│   ├── .env
│   ├── data/
│   └── logs/
└── shared/
    ├── nginx-proxy/         # Shared nginx
    └── letsencrypt/         # Shared SSL
```

---

## 🚀 Deploy Commands

### **1. Preparation**
```bash
# SSH into VPS
ssh user@vps.frontzin.com.br

# Create directory
sudo mkdir -p /opt/cloud_transcript
cd /opt/cloud_transcript

# Clone repo
git clone https://github.com/ecodelearn/cloud_transcript.git .
```

### **2. Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit with VPS-specific settings
nano .env

# Key settings:
# DATABASE_URL=postgresql://supabase...
# VIRTUAL_HOST=transcript.frontzin.com.br  
# STREAMLIT_SERVER_PORT=8501
```

### **3. DNS Configuration** 
```bash
# Add A record (if using subdomain)
transcript.frontzin.com.br -> VPS_IP
```

### **4. Deploy**
```bash
# Deploy to VPS
docker-compose -f docker-compose.vps.yml up -d

# Check logs
docker logs cloud_transcript_prod

# Test access
curl http://localhost:8502
```

---

## ⚠️ Considerations

### **Resource Limits**:
- **300GB Supabase**: Monitor usage closely
- **VPS Resources**: Check CPU/RAM impact
- **Port Conflicts**: Ensure 8502 is free

### **Backup Strategy**:
- **Database**: Supabase auto-backup
- **Audio Files**: Regular rsync to external storage
- **Configuration**: Git repo backup

### **Monitoring**:
- **Container Health**: Docker healthchecks
- **Database Size**: Weekly monitoring script
- **SSL Certificates**: Auto-renewal check

Qual opção você prefere? **Subdomain** seria o mais profissional, ou você prefere **port-based** para ser mais simples?