"""
Cloud Transcript - Simple Version for Testing
Basic functionality to verify Docker + Database + Dependencies
"""

import streamlit as st
import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# Add src to path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def test_database():
    """Test database connection and creation"""
    try:
        # Create data directory
        data_dir = Path(__file__).parent.parent / 'data'
        data_dir.mkdir(exist_ok=True)
        
        db_path = data_dir / 'test.db'
        
        # Connect and create table
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO test_table (message) VALUES (?)", ("Hello from Docker!",))
        conn.commit()
        
        # Query data
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return True, f"✅ Database working! {count} records"
        
    except Exception as e:
        return False, f"❌ Database error: {str(e)}"

def test_imports():
    """Test critical imports"""
    results = {}
    
    # Test basic imports
    # Test basic Python modules
    try:
        import json
        results['json'] = "✅ JSON available"
    except ImportError as e:
        results['json'] = f"❌ JSON: {str(e)}"
    
    try:
        import sqlite3
        results['sqlite3'] = "✅ SQLite3 available"
    except ImportError as e:
        results['sqlite3'] = f"❌ SQLite3: {str(e)}"
    
    # Test optional modules (expected to fail in minimal setup)
    try:
        import torch
        results['torch'] = f"✅ PyTorch: {torch.__version__}"
    except ImportError:
        results['torch'] = "⚠️ PyTorch: Not installed (expected in minimal setup)"
    
    try:
        import whisper
        results['whisper'] = "✅ Whisper available"
    except ImportError:
        results['whisper'] = "⚠️ Whisper: Not installed (expected in minimal setup)"
    
    return results

def main():
    st.set_page_config(
        page_title="Cloud Transcript - System Test",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 Cloud Transcript - System Test")
    st.subheader("Verificação de componentes básicos")
    
    # Environment info
    with st.sidebar:
        st.markdown("### 🖥️ Environment")
        st.text(f"Python: {sys.version.split()[0]}")
        st.text(f"Streamlit: {st.__version__}")
        st.text(f"Container: {os.getenv('HOSTNAME', 'local')}")
        st.text(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        
    # Test sections
    tab1, tab2, tab3 = st.tabs(["🧪 Import Tests", "🗄️ Database Test", "📁 File System"])
    
    with tab1:
        st.markdown("### 📦 Import Tests")
        
        if st.button("🔄 Test Imports"):
            with st.spinner("Testing imports..."):
                results = test_imports()
                
                for component, status in results.items():
                    st.write(f"**{component}**: {status}")
    
    with tab2:
        st.markdown("### 🗄️ Database Test")
        
        if st.button("🔄 Test Database"):
            with st.spinner("Testing database..."):
                success, message = test_database()
                
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    with tab3:
        st.markdown("### 📁 File System Test")
        
        # Show directory structure
        src_dir = Path(__file__).parent
        st.text(f"Source directory: {src_dir}")
        
        # List files
        if st.button("📋 List Files"):
            try:
                files = []
                for path in src_dir.rglob("*"):
                    if path.is_file() and not path.name.startswith('.'):
                        rel_path = path.relative_to(src_dir.parent)
                        files.append(str(rel_path))
                
                st.write("**Project files:**")
                for file in sorted(files):
                    st.text(f"  {file}")
                    
            except Exception as e:
                st.error(f"Error listing files: {e}")
        
        # Test file creation
        if st.button("✏️ Test File Creation"):
            try:
                test_dir = Path(__file__).parent.parent / 'data' / 'test'
                test_dir.mkdir(parents=True, exist_ok=True)
                
                test_file = test_dir / 'test.txt'
                test_file.write_text(f"Test file created at {datetime.now()}")
                
                st.success(f"✅ File created: {test_file}")
                st.text(f"Content: {test_file.read_text()}")
                
            except Exception as e:
                st.error(f"❌ File creation error: {e}")
    
    # Quick status
    st.markdown("---")
    st.markdown("### 📊 Quick Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            import torch
            st.success("✅ PyTorch OK")
        except ImportError:
            st.error("❌ PyTorch Missing")
    
    with col2:
        try:
            data_dir = Path(__file__).parent.parent / 'data'
            data_dir.mkdir(exist_ok=True)
            st.success("✅ File System OK") 
        except Exception:
            st.error("❌ File System Error")
    
    with col3:
        try:
            from models.database import Database
            st.success("✅ Models OK")
        except ImportError:
            st.error("❌ Models Missing")

if __name__ == "__main__":
    main()