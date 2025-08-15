"""Long-term persistent memory"""
import json
import sqlite3
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

class KPIPersistentMemory:
    """Long-term persistent memory using SQLite"""
    
    def __init__(self, db_path: str = "./kpi_memory.db"):
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # KPI contexts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpi_contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kpi_name TEXT UNIQUE,
                context_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analysis sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                session_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                feedback TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_kpi_context(self, kpi_context: 'KPIContext'):
        """Store KPI context persistently"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        context_data = json.dumps(kpi_context.__dict__, default=str)
        
        cursor.execute('''
            INSERT OR REPLACE INTO kpi_contexts 
            (kpi_name, context_data, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (kpi_context.kpi_name, context_data))
        
        conn.commit()
        conn.close()
    
    def retrieve_kpi_context(self, kpi_name: str) -> Optional['KPIContext']:
        """Retrieve KPI context from persistent storage"""
        from .core import KPIContext
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT context_data FROM kpi_contexts WHERE kpi_name = ?
        ''', (kpi_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            context_dict = json.loads(result[0])
            # Convert timestamp strings back to datetime objects
            if 'last_analyzed' in context_dict and context_dict['last_analyzed']:
                context_dict['last_analyzed'] = datetime.fromisoformat(
                    context_dict['last_analyzed']
                )
            return KPIContext(**context_dict)
        
        return None
    
    def store_analysis_session(self, session: 'AnalysisSession'):
        """Store analysis session persistently"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        session_data = json.dumps(session.__dict__, default=str)
        
        cursor.execute('''
            INSERT OR REPLACE INTO analysis_sessions 
            (session_id, session_data, feedback)
            VALUES (?, ?, ?)
        ''', (session.session_id, session_data, session.feedback))
        
        conn.commit()
        conn.close()