# Database Architecture - Cloud Transcript

## 🎯 Filosofia: Schema Evolutivo

**Princípio**: Mesmo schema funciona em todas as fases (SQLite → Supabase → Production)

**Benefício**: Zero refactor entre evoluções, migração suave

---

## 📊 Schema Core

### **Tabela: projects**
```sql
CREATE TABLE projects (
    id TEXT PRIMARY KEY,                    -- UUID for future compatibility
    nome_cliente TEXT NOT NULL,
    empresa TEXT,
    email_contato TEXT,
    whatsapp TEXT,
    
    -- Status do projeto
    status TEXT CHECK (status IN (
        'prospeccao',           -- Primeiro contato WhatsApp
        'entendimento',         -- Fase meeting explicativo  
        'proposta',             -- Elaborando proposta paga
        'aprovado',             -- Cliente aprovou
        'desenvolvimento',      -- Em execução
        'finalizado',           -- Entregue
        'cancelado'             -- Cancelado
    )) DEFAULT 'prospeccao',
    
    -- Financeiro
    valor_estimado REAL,
    valor_aprovado REAL,
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- JSON flexível para evoluções futuras
    metadata_json TEXT                      -- Campos adicionais sem schema change
);
```

### **Tabela: meetings** 
```sql
CREATE TABLE meetings (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- Sequência de meetings
    numero_meeting INTEGER NOT NULL,        -- 1, 2, 3... por projeto
    tipo TEXT CHECK (tipo IN (
        'whatsapp_inicial',     -- Primeiro contato
        'entendimento',         -- Meeting explicativo 
        'detalhamento',         -- Refinamento técnico
        'apresentacao',         -- Apresentação proposta
        'acompanhamento'        -- Follow-ups
    )),
    
    -- Dados do meeting
    data_meeting DATE NOT NULL,
    duracao_minutos INTEGER,
    objetivo TEXT,                          -- "Entender requisitos", "Apresentar MVP"
    
    -- Arquivos
    audio_path TEXT,                        -- Caminho arquivo áudio
    audio_size_mb REAL,                     -- Para controle storage
    audio_format TEXT,                      -- opus, mp3, wav
    
    -- Transcrição  
    transcricao_text TEXT,                  -- Texto completo
    transcricao_status TEXT CHECK (transcricao_status IN (
        'pending',              -- Aguardando processamento
        'processing',           -- Processando no GPU
        'completed',            -- Concluída
        'failed',               -- Erro no processamento
        'manual'                -- Inserida manualmente
    )) DEFAULT 'pending',
    
    -- Processamento
    processing_time_seconds INTEGER,        -- Tempo GPU processamento
    whisper_model TEXT DEFAULT 'large-v3', -- Modelo usado
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índice composto para busca eficiente
    UNIQUE(project_id, numero_meeting)
);
```

### **Tabela: audio_segments**
```sql 
CREATE TABLE audio_segments (
    id TEXT PRIMARY KEY,
    meeting_id TEXT NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    
    -- Segmentação temporal
    segment_number INTEGER NOT NULL,        -- 1, 2, 3... por meeting
    inicio_segundos INTEGER NOT NULL,       -- Timestamp início
    fim_segundos INTEGER NOT NULL,          -- Timestamp fim
    duracao_segundos INTEGER GENERATED ALWAYS AS (fim_segundos - inicio_segundos),
    
    -- Conteúdo
    transcricao_segment TEXT,               -- Texto deste segmento
    speaker_label TEXT,                     -- "Daniel", "Cliente", "Unknown"
    confidence_score REAL,                  -- 0.0 - 1.0 qualidade transcrição
    
    -- Classificação automática
    topic_tags TEXT,                        -- JSON array: ["requisitos", "orçamento"]
    importance_level INTEGER CHECK (importance_level IN (1,2,3,4,5)),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Tabela: insights**
```sql
CREATE TABLE insights (
    id TEXT PRIMARY KEY,
    meeting_id TEXT REFERENCES meetings(id) ON DELETE CASCADE,
    segment_id TEXT REFERENCES audio_segments(id) ON DELETE CASCADE,
    
    -- Tipo de insight
    insight_type TEXT CHECK (insight_type IN (
        'requisito_funcional',   -- "Sistema deve permitir login"
        'requisito_nao_funcional', -- "Deve suportar 1000 usuários"
        'tecnologia_sugerida',   -- "Usar React + Node.js"
        'complexidade_estimada', -- "Alta complexidade"
        'orcamento_mencionado',  -- "Orçamento entre 10k-15k"
        'prazo_mencionado',      -- "Prazer máximo 3 meses"
        'concorrente_citado',    -- "Tipo igual ao Uber"
        'decisor_identificado'   -- "João é quem aprova orçamento"
    )),
    
    -- Conteúdo
    titulo TEXT NOT NULL,                   -- "Login com Google OAuth"
    descricao TEXT,                         -- Detalhamento 
    relevancia INTEGER CHECK (relevancia IN (1,2,3,4,5)),
    
    -- LLM processing
    llm_model TEXT DEFAULT 'gpt-4',         -- Modelo que extraiu insight
    confidence_score REAL,                  -- Confiança da análise IA
    
    -- Relacionamentos
    relacionado_com TEXT,                   -- JSON array IDs outros insights
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index para busca eficiente
    INDEX idx_insights_type (insight_type),
    INDEX idx_insights_meeting (meeting_id)
);
```

### **Tabela: propostas** (Futuro Sprint 3+)
```sql
CREATE TABLE propostas (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id),
    
    -- Versioning (múltiplas versões por projeto)
    versao INTEGER NOT NULL DEFAULT 1,
    status TEXT CHECK (status IN ('rascunho', 'enviada', 'aprovada', 'rejeitada')),
    
    -- Conteúdo
    titulo TEXT NOT NULL,
    resumo_executivo TEXT,
    escopo_detalhado TEXT,                  -- Markdown/HTML
    tecnologias_propostas TEXT,             -- JSON array
    roadmap_desenvolvimento TEXT,           -- Markdown
    
    -- Financeiro
    valor_total REAL,
    forma_pagamento TEXT,                   -- "50% início, 50% entrega"
    prazo_desenvolvimento_dias INTEGER,
    
    -- Geração automática
    gerada_automaticamente BOOLEAN DEFAULT false,
    insights_utilizados TEXT,               -- JSON array insight_ids
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, versao)
);
```

---

## 🚀 Evoluções por Fase

### **Fase 1: SQLite Local**
```python
DATABASE_URL = "sqlite:///./data/cloud_transcript.db"

# Simples, rápido, zero configuração
# Funciona offline, perfeito para desenvolvimento
```

### **Fase 2: Supabase Cloud**
```python
DATABASE_URL = "postgresql://postgres:password@db.supabase.co:5432/postgres"

# Mesmo schema, zero código change
# Backup automático, acesso remoto
```

### **Fase 3: Production Multi-Tenant** 
```sql
-- Adicionar coluna org_id em todas as tabelas
ALTER TABLE projects ADD COLUMN org_id TEXT REFERENCES organizations(id);
ALTER TABLE meetings ADD COLUMN org_id TEXT REFERENCES organizations(id);
-- etc...

-- Row Level Security (RLS) no Supabase
CREATE POLICY "Users see only their org data" ON projects
  FOR ALL USING (org_id = current_setting('app.current_org_id'));
```

---

## 💡 Features Schema

### **Busca Inteligente**
```sql
-- Full-text search em transcrições
CREATE INDEX idx_transcricao_fts ON meetings 
  USING gin(to_tsvector('portuguese', transcricao_text));

-- Busca por período
SELECT * FROM meetings m 
JOIN projects p ON m.project_id = p.id
WHERE m.data_meeting BETWEEN '2024-01-01' AND '2024-12-31'
  AND p.nome_cliente ILIKE '%empresa%'
  AND to_tsvector('portuguese', m.transcricao_text) @@ 
      plainto_tsquery('portuguese', 'requisitos login');
```

### **Analytics Negócio**
```sql  
-- Pipeline de vendas
SELECT 
  status,
  COUNT(*) as quantidade,
  AVG(valor_estimado) as ticket_medio,
  SUM(CASE WHEN status = 'aprovado' THEN valor_aprovado ELSE 0 END) as receita_aprovada
FROM projects 
GROUP BY status;

-- Performance meetings por mês
SELECT 
  DATE_TRUNC('month', data_meeting) as mes,
  COUNT(*) as total_meetings,
  AVG(duracao_minutos) as duracao_media,
  COUNT(DISTINCT project_id) as projetos_ativos
FROM meetings
GROUP BY mes 
ORDER BY mes DESC;
```

### **Insights Automáticos**
```sql
-- Top tecnologias mencionadas
SELECT 
  titulo,
  COUNT(*) as frequencia,
  AVG(relevancia) as relevancia_media
FROM insights 
WHERE insight_type = 'tecnologia_sugerida'
  AND created_at >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY titulo
ORDER BY frequencia DESC;

-- Projetos com orçamento vs sem orçamento
SELECT 
  p.nome_cliente,
  p.valor_estimado,
  COALESCE(COUNT(i.id), 0) as insights_orcamento
FROM projects p
LEFT JOIN meetings m ON p.id = m.project_id  
LEFT JOIN insights i ON m.id = i.meeting_id 
  AND i.insight_type = 'orcamento_mencionado'
GROUP BY p.id, p.nome_cliente, p.valor_estimado
HAVING COUNT(i.id) = 0  -- Projetos SEM orçamento discutido
  AND p.status IN ('entendimento', 'proposta');
```

---

## ⚡ Performance & Storage

### **Storage Estimates (Supabase 300GB)**
```
1 projeto médio:
├── 3 meetings × 2h cada = 6h áudio total
├── Audio files: ~300MB (opus compressed)  
├── Transcrições: ~2MB (text)
├── Insights: ~100KB (structured data)
└── Total por projeto: ~302MB

300GB capacity = ~990 projetos completos
Ou ~2970 meetings individuais
```

### **Otimização Queries**
```sql
-- Indexes essenciais
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_cliente ON projects(nome_cliente);
CREATE INDEX idx_meetings_project_data ON meetings(project_id, data_meeting);
CREATE INDEX idx_segments_meeting ON audio_segments(meeting_id);
CREATE INDEX idx_insights_meeting_type ON insights(meeting_id, insight_type);

-- Partitioning por data (futuro)
CREATE TABLE meetings_2024 PARTITION OF meetings 
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

Esta arquitetura suporta desde o MVP até um SaaS completo, mantendo a mesma estrutura base! 🚀