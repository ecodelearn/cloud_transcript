# Projeto: Transcritor de Conversas WhatsApp

## Objetivo
Criar um transcritor que processa múltiplos áudios de conversas do WhatsApp de forma sequencial, permitindo inserção de contexto textual entre áudios e exportação organizada.

## APIs de Transcrição Recomendadas (Free-Tier)

### 1. **Groq (Recomendação Principal)**
- **Modelo**: Whisper-large-v3
- **Free-tier**: 6.000 segundos/minuto
- **Qualidade**: Excelente para PT-BR
- **Latência**: Muito baixa (~2-3s)
- **Vantagens**: API simples, rápida, boa documentação

### 2. **Google Cloud Speech-to-Text**
- **Free-tier**: 60 minutos/mês
- **Qualidade**: Muito boa para PT-BR
- **Vantagens**: Suporte nativo a PT-BR, pontuação automática
- **Desvantagens**: Setup mais complexo

### 3. **Hugging Face Inference API**
- **Modelo**: openai/whisper-large-v3
- **Free-tier**: Limitado por requests/hora
- **Qualidade**: Boa para PT-BR
- **Vantagens**: Sem necessidade de chave paga

## Arquitetura Proposta

### Interface do Usuário (Streamlit)
```
┌─────────────────────────────────────────┐
│ Upload Múltiplos Áudios (.opus, .mp3)  │
├─────────────────────────────────────────┤
│ Configuração API (Groq/Google/HF)      │
├─────────────────────────────────────────┤
│ Preview dos Áudios Carregados           │
├─────────────────────────────────────────┤
│ Processo de Transcrição (Progress Bar) │
├─────────────────────────────────────────┤
│ Editor de Blocos:                       │
│ ┌─────────────────────────────────────┐ │
│ │ [🎵] Áudio 1: "Oi, como você..."   │ │
│ │ [📝] [Adicionar Contexto]          │ │
│ │ [🎵] Áudio 2: "Eu estava pensa..." │ │
│ │ [📝] [Adicionar Contexto]          │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ Export: TXT | JSON | Markdown          │
└─────────────────────────────────────────┘
```

### Estrutura de Dados
```python
ConversationBlock = {
    "id": str,
    "type": "audio" | "text",
    "content": str,
    "timestamp": datetime,
    "audio_file": str | None,
    "duration": float | None
}
```

### Funcionalidades Core

1. **Upload e Organização**
   - Drag & drop múltiplos arquivos
   - Ordenação automática por timestamp/nome
   - Preview de áudios

2. **Transcrição Inteligente**
   - Processamento em lote
   - Progress bar com status
   - Retry automático em falhas
   - Cache de transcrições

3. **Editor de Contexto**
   - Inserção de blocos de texto entre áudios
   - Reordenação drag & drop
   - Edição inline das transcrições
   - Visualização cronológica

4. **Exportação Flexível**
   - Texto puro (.txt)
   - JSON estruturado
   - Markdown com timestamps
   - Chat format para LLMs

## Tecnologias

### Backend
- **Python 3.9+**
- **Streamlit** (Interface)
- **Groq Python SDK** (API principal)
- **pydub** (Processamento áudio)
- **streamlit-sortables** (Drag & drop)
- **streamlit-ace** (Editor texto)

### Dependências Principais
```
streamlit
groq
pydub
streamlit-sortables
streamlit-ace
python-dotenv
```

## Estrutura do Projeto
```
whatsapp-transcriptor/
├── app.py                 # Interface principal
├── services/
│   ├── transcription.py   # APIs de transcrição
│   ├── audio_processor.py # Processamento áudio
│   └── export_manager.py  # Gerenciamento exports
├── components/
│   ├── audio_uploader.py  # Upload component
│   ├── block_editor.py    # Editor blocos
│   └── export_panel.py    # Panel exportação
├── utils/
│   ├── file_utils.py      # Utilitários arquivo
│   └── format_utils.py    # Formatação dados
├── config.py              # Configurações
├── requirements.txt
└── README.md
```

## Fluxo de Trabalho

1. **Upload**: Usuário faz upload de múltiplos áudios
2. **Pré-processamento**: Ordenação e conversão de formatos
3. **Transcrição**: Processamento via API escolhida
4. **Edição**: Interface para inserir contexto e editar
5. **Export**: Geração de arquivo final estruturado

## Diferenciais

- **Processamento em lote** de múltiplos áudios
- **Interface visual** para organização de blocos
- **Suporte a múltiplas APIs** (fallback)
- **Cache inteligente** para evitar re-transcrições
- **Formatos de export** otimizados para LLMs
- **Timeline visual** da conversa

## Implementação Rápida (2-3 horas)

### Fase 1: Core MVP
- Upload múltiplos áudios
- Transcrição via Groq
- Lista simples de resultados
- Export básico TXT

### Fase 2: Interface Rica
- Editor de blocos
- Inserção de contexto
- Drag & drop reordering

### Fase 3: Polimento
- Múltiplas APIs
- Cache/persistência
- Formatos export avançados

## Estimativa de Tempo
- **Setup inicial**: 30 min
- **MVP funcional**: 2 horas  
- **Interface completa**: 3-4 horas
- **Polimento**: 1-2 horas

**Total: 6-8 horas para versão completa**