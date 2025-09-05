"""
Database connection and initialization
Supports SQLite (local) and PostgreSQL (Supabase) with same interface
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database connection manager - supports SQLite and PostgreSQL"""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection"""
        self.database_url = database_url or self._get_database_url()
        self.is_sqlite = self.database_url.startswith('sqlite')
        
    def _get_database_url(self) -> str:
        """Get database URL from environment or default to SQLite"""
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            return db_url
            
        # Default to local SQLite
        db_path = Path(__file__).parent.parent.parent / 'data' / 'cloud_transcript.db'
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f'sqlite:///{db_path}'
    
    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup"""
        if self.is_sqlite:
            # SQLite connection
            db_path = self.database_url.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
        else:
            # PostgreSQL connection (future Supabase)
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        
        try:
            yield conn
        finally:
            conn.close()
    
    def initialize_schema(self):
        """Initialize database with core schema"""
        logger.info("Initializing database schema...")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    nome_cliente TEXT NOT NULL,
                    empresa TEXT,
                    email_contato TEXT,
                    whatsapp TEXT,
                    status TEXT CHECK (status IN (
                        'prospeccao', 'entendimento', 'proposta', 
                        'aprovado', 'desenvolvimento', 'finalizado', 'cancelado'
                    )) DEFAULT 'prospeccao',
                    valor_estimado REAL,
                    valor_aprovado REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata_json TEXT
                )
            """)
            
            # Create meetings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meetings (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    numero_meeting INTEGER NOT NULL,
                    tipo TEXT CHECK (tipo IN (
                        'whatsapp_inicial', 'entendimento', 'detalhamento',
                        'apresentacao', 'acompanhamento'
                    )),
                    data_meeting DATE NOT NULL,
                    duracao_minutos INTEGER,
                    objetivo TEXT,
                    audio_path TEXT,
                    audio_size_mb REAL,
                    audio_format TEXT,
                    transcricao_text TEXT,
                    transcricao_status TEXT CHECK (transcricao_status IN (
                        'pending', 'processing', 'completed', 'failed', 'manual'
                    )) DEFAULT 'pending',
                    processing_time_seconds INTEGER,
                    whisper_model TEXT DEFAULT 'large-v3',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
                    UNIQUE(project_id, numero_meeting)
                )
            """)
            
            # Create audio_segments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audio_segments (
                    id TEXT PRIMARY KEY,
                    meeting_id TEXT NOT NULL,
                    segment_number INTEGER NOT NULL,
                    inicio_segundos INTEGER NOT NULL,
                    fim_segundos INTEGER NOT NULL,
                    duracao_segundos INTEGER GENERATED ALWAYS AS (fim_segundos - inicio_segundos),
                    transcricao_segment TEXT,
                    speaker_label TEXT,
                    confidence_score REAL,
                    topic_tags TEXT,
                    importance_level INTEGER CHECK (importance_level IN (1,2,3,4,5)),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE
                )
            """)
            
            # Create insights table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS insights (
                    id TEXT PRIMARY KEY,
                    meeting_id TEXT,
                    segment_id TEXT,
                    insight_type TEXT CHECK (insight_type IN (
                        'requisito_funcional', 'requisito_nao_funcional',
                        'tecnologia_sugerida', 'complexidade_estimada',
                        'orcamento_mencionado', 'prazo_mencionado',
                        'concorrente_citado', 'decisor_identificado'
                    )),
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    relevancia INTEGER CHECK (relevancia IN (1,2,3,4,5)),
                    llm_model TEXT DEFAULT 'gpt-4',
                    confidence_score REAL,
                    relacionado_com TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE,
                    FOREIGN KEY (segment_id) REFERENCES audio_segments (id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)",
                "CREATE INDEX IF NOT EXISTS idx_projects_cliente ON projects(nome_cliente)",
                "CREATE INDEX IF NOT EXISTS idx_meetings_project_data ON meetings(project_id, data_meeting)",
                "CREATE INDEX IF NOT EXISTS idx_segments_meeting ON audio_segments(meeting_id)",
                "CREATE INDEX IF NOT EXISTS idx_insights_meeting_type ON insights(meeting_id, insight_type)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            conn.commit()
            logger.info("Database schema initialized successfully!")
    
    def get_stats(self) -> dict:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Count records in each table
            tables = ['projects', 'meetings', 'audio_segments', 'insights']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0] if self.is_sqlite else cursor.fetchone()['count']
                stats[f'{table}_count'] = count
            
            # Database size (SQLite only)
            if self.is_sqlite:
                db_path = self.database_url.replace('sqlite:///', '')
                if os.path.exists(db_path):
                    stats['database_size_mb'] = os.path.getsize(db_path) / (1024 * 1024)
                else:
                    stats['database_size_mb'] = 0
            
            return stats


# Global database instance
db = Database()

def init_database():
    """Initialize database - call this at app startup"""
    db.initialize_schema()

def get_db():
    """Get database instance"""
    return db