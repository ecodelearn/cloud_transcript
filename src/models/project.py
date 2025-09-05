"""
Project model - manages AI consultancy projects
"""

import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from .database import get_db

@dataclass
class Project:
    """Project model for AI consultancy workflow"""
    
    id: str
    nome_cliente: str
    empresa: Optional[str] = None
    email_contato: Optional[str] = None
    whatsapp: Optional[str] = None
    status: str = 'prospeccao'
    valor_estimado: Optional[float] = None
    valor_aprovado: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata_json: Optional[str] = None
    
    @classmethod
    def create(cls, nome_cliente: str, **kwargs) -> 'Project':
        """Create new project"""
        project_id = str(uuid.uuid4())
        now = datetime.now()
        
        project = cls(
            id=project_id,
            nome_cliente=nome_cliente,
            created_at=now,
            updated_at=now,
            **kwargs
        )
        
        project.save()
        return project
    
    def save(self):
        """Save project to database"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if project exists
            cursor.execute("SELECT id FROM projects WHERE id = ?", (self.id,))
            exists = cursor.fetchone() is not None
            
            if exists:
                # Update existing
                cursor.execute("""
                    UPDATE projects SET
                        nome_cliente = ?, empresa = ?, email_contato = ?,
                        whatsapp = ?, status = ?, valor_estimado = ?,
                        valor_aprovado = ?, updated_at = ?, metadata_json = ?
                    WHERE id = ?
                """, (
                    self.nome_cliente, self.empresa, self.email_contato,
                    self.whatsapp, self.status, self.valor_estimado,
                    self.valor_aprovado, datetime.now(), self.metadata_json,
                    self.id
                ))
            else:
                # Insert new
                cursor.execute("""
                    INSERT INTO projects (
                        id, nome_cliente, empresa, email_contato, whatsapp,
                        status, valor_estimado, valor_aprovado, created_at,
                        updated_at, metadata_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.id, self.nome_cliente, self.empresa, self.email_contato,
                    self.whatsapp, self.status, self.valor_estimado,
                    self.valor_aprovado, self.created_at, self.updated_at,
                    self.metadata_json
                ))
            
            conn.commit()
    
    @classmethod
    def get_by_id(cls, project_id: str) -> Optional['Project']:
        """Get project by ID"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(**dict(row))
            return None
    
    @classmethod
    def get_all(cls, status: Optional[str] = None, limit: int = 100) -> List['Project']:
        """Get all projects with optional filtering"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            if status:
                cursor.execute(
                    "SELECT * FROM projects WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                    (status, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM projects ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                )
            
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]
    
    @classmethod
    def search(cls, query: str, limit: int = 50) -> List['Project']:
        """Search projects by client name or company"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            
            cursor.execute("""
                SELECT * FROM projects 
                WHERE nome_cliente LIKE ? OR empresa LIKE ?
                ORDER BY created_at DESC LIMIT ?
            """, (search_pattern, search_pattern, limit))
            
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]
    
    def delete(self):
        """Delete project (and cascade meetings)"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (self.id,))
            conn.commit()
    
    def get_meetings_count(self) -> int:
        """Get number of meetings for this project"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as count FROM meetings WHERE project_id = ?",
                (self.id,)
            )
            result = cursor.fetchone()
            return result[0] if db.is_sqlite else result['count']
    
    def get_total_meeting_time(self) -> int:
        """Get total meeting time in minutes"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(duracao_minutos), 0) as total
                FROM meetings WHERE project_id = ?
            """, (self.id,))
            result = cursor.fetchone()
            return result[0] if db.is_sqlite else result['total']
    
    def set_metadata(self, key: str, value: Any):
        """Set metadata field"""
        metadata = {}
        if self.metadata_json:
            metadata = json.loads(self.metadata_json)
        
        metadata[key] = value
        self.metadata_json = json.dumps(metadata)
        self.save()
    
    def get_metadata(self, key: str, default=None):
        """Get metadata field"""
        if not self.metadata_json:
            return default
        
        metadata = json.loads(self.metadata_json)
        return metadata.get(key, default)
    
    @property
    def status_emoji(self) -> str:
        """Get emoji for project status"""
        status_emojis = {
            'prospeccao': '🔍',
            'entendimento': '💬', 
            'proposta': '📋',
            'aprovado': '✅',
            'desenvolvimento': '⚙️',
            'finalizado': '🎉',
            'cancelado': '❌'
        }
        return status_emojis.get(self.status, '📁')
    
    @property
    def status_label(self) -> str:
        """Get human-readable status label"""
        labels = {
            'prospeccao': 'Prospecção',
            'entendimento': 'Entendimento',
            'proposta': 'Proposta',
            'aprovado': 'Aprovado',
            'desenvolvimento': 'Desenvolvimento',
            'finalizado': 'Finalizado',
            'cancelado': 'Cancelado'
        }
        return labels.get(self.status, self.status.title())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        
        # Add computed fields
        data.update({
            'meetings_count': self.get_meetings_count(),
            'total_meeting_time': self.get_total_meeting_time(),
            'status_emoji': self.status_emoji,
            'status_label': self.status_label
        })
        
        return data