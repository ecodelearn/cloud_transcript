"""
Meeting model - manages individual meetings within projects
"""

import uuid
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from .database import get_db

@dataclass
class Meeting:
    """Meeting model for consultancy sessions"""
    
    id: str
    project_id: str
    numero_meeting: int
    tipo: Optional[str] = None
    data_meeting: Optional[date] = None
    duracao_minutos: Optional[int] = None
    objetivo: Optional[str] = None
    audio_path: Optional[str] = None
    audio_size_mb: Optional[float] = None
    audio_format: Optional[str] = None
    transcricao_text: Optional[str] = None
    transcricao_status: str = 'pending'
    processing_time_seconds: Optional[int] = None
    whisper_model: str = 'large-v3'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def create(cls, project_id: str, **kwargs) -> 'Meeting':
        """Create new meeting for a project"""
        meeting_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Auto-increment meeting number
        numero_meeting = cls._get_next_meeting_number(project_id)
        
        meeting = cls(
            id=meeting_id,
            project_id=project_id,
            numero_meeting=numero_meeting,
            data_meeting=kwargs.get('data_meeting', date.today()),
            created_at=now,
            updated_at=now,
            **{k: v for k, v in kwargs.items() if k != 'data_meeting'}
        )
        
        meeting.save()
        return meeting
    
    @classmethod
    def _get_next_meeting_number(cls, project_id: str) -> int:
        """Get next meeting number for project"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MAX(numero_meeting) FROM meetings WHERE project_id = ?",
                (project_id,)
            )
            result = cursor.fetchone()
            max_num = result[0] if result and result[0] else 0
            return max_num + 1
    
    def save(self):
        """Save meeting to database"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if meeting exists
            cursor.execute("SELECT id FROM meetings WHERE id = ?", (self.id,))
            exists = cursor.fetchone() is not None
            
            if exists:
                # Update existing
                cursor.execute("""
                    UPDATE meetings SET
                        project_id = ?, numero_meeting = ?, tipo = ?,
                        data_meeting = ?, duracao_minutos = ?, objetivo = ?,
                        audio_path = ?, audio_size_mb = ?, audio_format = ?,
                        transcricao_text = ?, transcricao_status = ?,
                        processing_time_seconds = ?, whisper_model = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (
                    self.project_id, self.numero_meeting, self.tipo,
                    self.data_meeting, self.duracao_minutos, self.objetivo,
                    self.audio_path, self.audio_size_mb, self.audio_format,
                    self.transcricao_text, self.transcricao_status,
                    self.processing_time_seconds, self.whisper_model,
                    datetime.now(), self.id
                ))
            else:
                # Insert new
                cursor.execute("""
                    INSERT INTO meetings (
                        id, project_id, numero_meeting, tipo, data_meeting,
                        duracao_minutos, objetivo, audio_path, audio_size_mb,
                        audio_format, transcricao_text, transcricao_status,
                        processing_time_seconds, whisper_model, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.id, self.project_id, self.numero_meeting, self.tipo,
                    self.data_meeting, self.duracao_minutos, self.objetivo,
                    self.audio_path, self.audio_size_mb, self.audio_format,
                    self.transcricao_text, self.transcricao_status,
                    self.processing_time_seconds, self.whisper_model,
                    self.created_at, self.updated_at
                ))
            
            conn.commit()
    
    @classmethod
    def get_by_id(cls, meeting_id: str) -> Optional['Meeting']:
        """Get meeting by ID"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(**dict(row))
            return None
    
    @classmethod
    def get_by_project(cls, project_id: str) -> List['Meeting']:
        """Get all meetings for a project"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM meetings 
                WHERE project_id = ? 
                ORDER BY numero_meeting ASC
            """, (project_id,))
            
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]
    
    @classmethod 
    def get_pending_transcription(cls) -> List['Meeting']:
        """Get meetings pending transcription"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM meetings 
                WHERE transcricao_status = 'pending' 
                  AND audio_path IS NOT NULL
                ORDER BY created_at ASC
            """)
            
            rows = cursor.fetchall()
            return [cls(**dict(row)) for rows in rows]
    
    def delete(self):
        """Delete meeting"""
        db = get_db()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM meetings WHERE id = ?", (self.id,))
            conn.commit()
    
    def set_audio_file(self, file_path: str, file_size_mb: float, file_format: str):
        """Set audio file information"""
        self.audio_path = file_path
        self.audio_size_mb = file_size_mb
        self.audio_format = file_format
        self.save()
    
    def start_transcription(self, whisper_model: str = 'large-v3'):
        """Mark transcription as started"""
        self.transcricao_status = 'processing'
        self.whisper_model = whisper_model
        self.save()
    
    def complete_transcription(self, transcription_text: str, processing_time: int):
        """Mark transcription as completed"""
        self.transcricao_text = transcription_text
        self.transcricao_status = 'completed'
        self.processing_time_seconds = processing_time
        self.save()
    
    def fail_transcription(self, error_msg: str = None):
        """Mark transcription as failed"""
        self.transcricao_status = 'failed'
        if error_msg:
            # Store error in metadata (could be added to schema later)
            pass
        self.save()
    
    @property
    def audio_file_exists(self) -> bool:
        """Check if audio file exists on disk"""
        if not self.audio_path:
            return False
        return Path(self.audio_path).exists()
    
    @property
    def status_emoji(self) -> str:
        """Get emoji for transcription status"""
        status_emojis = {
            'pending': '⏳',
            'processing': '⚙️',
            'completed': '✅',
            'failed': '❌',
            'manual': '✏️'
        }
        return status_emojis.get(self.transcricao_status, '❓')
    
    @property
    def tipo_emoji(self) -> str:
        """Get emoji for meeting type"""
        tipo_emojis = {
            'whatsapp_inicial': '📱',
            'entendimento': '💬',
            'detalhamento': '🔍',
            'apresentacao': '📊',
            'acompanhamento': '📋'
        }
        return tipo_emojis.get(self.tipo, '🎯')
    
    @property
    def duracao_formatted(self) -> str:
        """Format duration as human readable"""
        if not self.duracao_minutos:
            return "N/A"
        
        hours = self.duracao_minutos // 60
        minutes = self.duracao_minutos % 60
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        return f"{minutes}min"
    
    def get_transcription_preview(self, max_chars: int = 200) -> str:
        """Get preview of transcription"""
        if not self.transcricao_text:
            return "Sem transcrição disponível"
        
        if len(self.transcricao_text) <= max_chars:
            return self.transcricao_text
        
        return self.transcricao_text[:max_chars] + "..."
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        
        # Add computed fields
        data.update({
            'audio_file_exists': self.audio_file_exists,
            'status_emoji': self.status_emoji,
            'tipo_emoji': self.tipo_emoji,
            'duracao_formatted': self.duracao_formatted,
            'transcription_preview': self.get_transcription_preview()
        })
        
        return data