"""
Cloud Transcript - AI Consultancy Management Platform
Aplicação principal Streamlit

Desenvolvido pela IA Forte (https://iaforte.com.br)
"""

import streamlit as st
import os
import logging
from datetime import datetime, date
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for components
db_instance = None
whisper_service = None
Project = None
Meeting = None

def initialize_app():
    """Initialize application components"""
    try:
        # Add src to Python path
        import sys
        from pathlib import Path
        src_path = Path(__file__).parent
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        # Import components
        from models import init_database, get_db, Project as ProjectModel, Meeting as MeetingModel
        
        # Initialize database
        init_database()
        
        # Try to import Whisper (may fail on CPU-only systems)
        try:
            from services.whisper_gpu import get_whisper_service
            whisper_service_instance = get_whisper_service()
        except ImportError as e:
            logger.warning(f"Whisper service not available: {e}")
            whisper_service_instance = None
        
        logger.info("App initialized successfully")
        return get_db(), ProjectModel, MeetingModel, whisper_service_instance
        
    except Exception as e:
        logger.error(f"App initialization failed: {str(e)}")
        st.error(f"❌ Initialization failed: {str(e)}")
        return None, None, None, None

# Initialize app - cached version
@st.cache_resource
def get_app_components():
    return initialize_app()

# Get components
db_instance, Project, Meeting, whisper_service = get_app_components()
app_initialized = Project is not None


def render_sidebar():
    """Render sidebar with system status"""
    with st.sidebar:
        st.markdown("### 📊 System Status")
        
        if not app_initialized:
            st.error("❌ System not initialized")
            return
        
        # Database status
        try:
            if db_instance:
                db_stats = db_instance.get_stats()
                st.success("✅ Database conectado")
                st.metric("Projetos", db_stats.get('projects_count', 0))
                st.metric("Meetings", db_stats.get('meetings_count', 0))
                
                if 'database_size_mb' in db_stats:
                    st.metric("DB Size", f"{db_stats['database_size_mb']:.1f} MB")
            else:
                st.error("❌ Database not available")
                
        except Exception as e:
            st.error(f"❌ Database error: {str(e)}")
        
        # GPU status
        try:
            if whisper_service:
                gpu_stats = whisper_service.get_gpu_stats()
                
                if gpu_stats['device'] == 'cuda':
                    st.success(f"🚀 GPU: {gpu_stats.get('gpu_name', 'NVIDIA')}")
                    if gpu_stats['model_loaded']:
                        st.info(f"Model: {gpu_stats['model_name']}")
                else:
                    st.warning("⚠️ GPU não disponível - usando CPU")
            else:
                st.warning("⚠️ Whisper service not available")
                
        except Exception as e:
            st.error(f"❌ GPU service error: {str(e)}")
        
        # Environment info
        st.markdown("### ℹ️ Environment")
        transcription_mode = os.getenv('TRANSCRIPTION_MODE', 'local_gpu')
        use_gpu = os.getenv('USE_LOCAL_GPU', 'true').lower() == 'true'
        
        st.info(f"""
        **Modo**: {transcription_mode}
        **GPU Local**: {'✅' if use_gpu else '❌'}
        **Ambiente**: {os.getenv('ENVIRONMENT', 'development')}
        """)


def render_projects_tab():
    """Render projects management tab"""
    st.markdown("### 📁 Gestão de Projetos")
    
    # Check if Project is available
    if Project is None:
        st.error("❌ Sistema não inicializado. Recarregue a página.")
        return
    
    # Project creation form
    with st.expander("➕ Novo Projeto", expanded=False):
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_cliente = st.text_input("Nome do Cliente *", placeholder="João Silva")
                empresa = st.text_input("Empresa", placeholder="Tech Corp")
                email_contato = st.text_input("Email", placeholder="joao@techcorp.com")
                
            with col2:
                whatsapp = st.text_input("WhatsApp", placeholder="+55 11 99999-9999")
                valor_estimado = st.number_input("Valor Estimado (R$)", min_value=0.0, step=1000.0)
                status = st.selectbox("Status", [
                    'prospeccao', 'entendimento', 'proposta', 
                    'aprovado', 'desenvolvimento', 'finalizado'
                ])
            
            submitted = st.form_submit_button("Criar Projeto")
            
            if submitted and nome_cliente:
                try:
                    project = Project.create(
                        nome_cliente=nome_cliente,
                        empresa=empresa,
                        email_contato=email_contato,
                        whatsapp=whatsapp,
                        valor_estimado=valor_estimado,
                        status=status
                    )
                    st.success(f"✅ Projeto '{nome_cliente}' criado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar projeto: {str(e)}")
    
    # Projects list
    try:
        projects = Project.get_all(limit=50)
        
        if projects:
            st.markdown("#### 📋 Projetos Recentes")
            
            for project in projects:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{project.status_emoji} {project.nome_cliente}**")
                        if project.empresa:
                            st.caption(f"📢 {project.empresa}")
                    
                    with col2:
                        st.text(f"Status: {project.status_label}")
                        meetings_count = project.get_meetings_count()
                        if meetings_count > 0:
                            st.caption(f"📅 {meetings_count} meetings")
                    
                    with col3:
                        if project.valor_estimado:
                            st.text(f"R$ {project.valor_estimado:,.0f}")
                    
                    with col4:
                        if st.button("📝 Abrir", key=f"open_{project.id}"):
                            st.session_state.selected_project_id = project.id
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("📝 Nenhum projeto encontrado. Crie seu primeiro projeto acima!")
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar projetos: {str(e)}")


def render_meetings_tab():
    """Render meetings management tab"""
    st.markdown("### 📅 Meetings & Transcrições")
    
    # Check if Project is available
    if Project is None:
        st.error("❌ Sistema não inicializado. Recarregue a página.")
        return
    
    # Project selection
    try:
        projects = Project.get_all(limit=100)
        if not projects:
            st.warning("⚠️ Crie um projeto primeiro na aba Projetos")
            return
    except Exception as e:
        st.error(f"❌ Erro ao carregar projetos: {str(e)}")
        return
    
    project_options = {f"{p.nome_cliente} ({p.empresa or 'Sem empresa'})": p.id for p in projects}
    selected_project_name = st.selectbox("Selecionar Projeto", list(project_options.keys()))
    selected_project_id = project_options[selected_project_name]
    selected_project = Project.get_by_id(selected_project_id)
    
    if selected_project:
        st.success(f"📁 Projeto: **{selected_project.nome_cliente}** ({selected_project.status_label})")
        
        # Meeting creation form
        with st.expander("➕ Novo Meeting", expanded=False):
            with st.form("new_meeting_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo = st.selectbox("Tipo do Meeting", [
                        'whatsapp_inicial', 'entendimento', 'detalhamento',
                        'apresentacao', 'acompanhamento'
                    ])
                    data_meeting = st.date_input("Data do Meeting", value=date.today())
                    duracao_minutos = st.number_input("Duração (minutos)", min_value=1, value=60)
                
                with col2:
                    objetivo = st.text_area("Objetivo do Meeting", 
                                          placeholder="Ex: Entender requisitos do sistema de login")
                    uploaded_file = st.file_uploader(
                        "Upload Áudio (opcional)", 
                        type=['mp3', 'wav', 'opus', 'm4a', 'aac']
                    )
                
                submitted = st.form_submit_button("Criar Meeting")
                
                if submitted:
                    try:
                        meeting = Meeting.create(
                            project_id=selected_project.id,
                            tipo=tipo,
                            data_meeting=data_meeting,
                            duracao_minutos=duracao_minutos,
                            objetivo=objetivo
                        )
                        
                        # Handle file upload
                        if uploaded_file is not None:
                            # Save uploaded file
                            upload_dir = Path("data/projects") / selected_project.id
                            upload_dir.mkdir(parents=True, exist_ok=True)
                            
                            file_path = upload_dir / f"meeting_{meeting.numero_meeting}_{uploaded_file.name}"
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Update meeting with file info
                            file_size_mb = file_path.stat().st_size / (1024 * 1024)
                            meeting.set_audio_file(
                                str(file_path), 
                                file_size_mb, 
                                uploaded_file.name.split('.')[-1]
                            )
                        
                        st.success(f"✅ Meeting #{meeting.numero_meeting} criado com sucesso!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao criar meeting: {str(e)}")
        
        # Meetings list for selected project
        meetings = Meeting.get_by_project(selected_project.id)
        
        if meetings:
            st.markdown("#### 📋 Meetings do Projeto")
            
            for meeting in meetings:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                    
                    with col1:
                        st.markdown(f"**#{meeting.numero_meeting}**")
                    
                    with col2:
                        st.markdown(f"{meeting.tipo_emoji} {meeting.tipo or 'Meeting'}")
                        if meeting.objetivo:
                            st.caption(meeting.objetivo)
                    
                    with col3:
                        st.text(f"📅 {meeting.data_meeting}")
                        st.text(f"⏱️ {meeting.duracao_formatted}")
                    
                    with col4:
                        st.text(f"{meeting.status_emoji} {meeting.transcricao_status}")
                        if meeting.audio_path and meeting.transcricao_status == 'pending':
                            if st.button("🚀 Transcrever", key=f"transcribe_{meeting.id}"):
                                st.info("🔄 Transcription will be implemented in next update!")
                    
                    if meeting.transcricao_text:
                        with st.expander(f"📝 Transcrição Meeting #{meeting.numero_meeting}"):
                            st.text_area("", meeting.transcricao_text, height=200, disabled=True)
                    
                    st.divider()
        else:
            st.info("📝 Nenhum meeting encontrado. Crie o primeiro meeting acima!")


def render_gpu_tab():
    """Render GPU testing and benchmarks tab"""
    st.markdown("### 🚀 GPU Performance & Testing")
    
    global whisper_service
    
    if whisper_service is None:
        st.error("❌ Whisper service not available")
        st.info("💡 This may occur on CPU-only systems or if there are import issues.")
        return
    
    try:
        whisper = whisper_service
        gpu_stats = whisper.get_gpu_stats()
        
        # GPU Stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 GPU Status")
            st.json(gpu_stats)
        
        with col2:
            st.markdown("#### ⚡ Performance Test")
            
            test_duration = st.slider("Test Duration (seconds)", 10, 120, 30)
            
            if st.button("🏃 Run Benchmark"):
                with st.spinner("Running GPU benchmark..."):
                    try:
                        benchmark_results = whisper.benchmark_performance(test_duration)
                        
                        if 'error' in benchmark_results:
                            st.error(f"❌ Benchmark failed: {benchmark_results['error']}")
                        else:
                            st.success("✅ Benchmark completed!")
                            st.json(benchmark_results)
                            
                            # Performance metrics
                            speed_multiplier = benchmark_results.get('speed_multiplier', 0)
                            st.metric(
                                "Processing Speed", 
                                f"{speed_multiplier:.1f}x realtime",
                                delta=f"{speed_multiplier - 1:.1f}x faster than realtime" if speed_multiplier > 1 else None
                            )
                            
                    except Exception as e:
                        st.error(f"❌ Benchmark error: {str(e)}")
        
        # File upload test
        st.markdown("#### 🎵 Test Audio Upload")
        test_file = st.file_uploader(
            "Upload test audio file", 
            type=['mp3', 'wav', 'opus', 'm4a', 'aac']
        )
        
        if test_file is not None and st.button("🔄 Test Transcription"):
            # Save temp file
            temp_path = Path("data/temp_test_audio")
            temp_path.mkdir(exist_ok=True)
            test_file_path = temp_path / test_file.name
            
            with open(test_file_path, "wb") as f:
                f.write(test_file.getbuffer())
            
            with st.spinner("Transcribing audio..."):
                try:
                    result = whisper.transcribe_audio(str(test_file_path))
                    
                    if result['success']:
                        st.success("✅ Transcription successful!")
                        st.text_area("Transcription Result:", result['text'], height=200)
                        
                        # Show performance metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Processing Time", f"{result['processing_time_seconds']}s")
                        with col2:
                            st.metric("File Size", f"{result['file_size_mb']:.1f} MB")
                        with col3:
                            audio_duration = result.get('audio_duration_seconds', 0)
                            if audio_duration > 0:
                                speed = audio_duration / result['processing_time_seconds']
                                st.metric("Speed", f"{speed:.1f}x realtime")
                    else:
                        st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    # Clean up temp file
                    test_file_path.unlink(missing_ok=True)
        
    except Exception as e:
        st.error(f"❌ GPU service error: {str(e)}")


def main():
    """Interface principal da aplicação"""
    
    # Configuração da página
    st.set_page_config(
        page_title="Cloud Transcript",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header da aplicação
    st.title("🎵 Cloud Transcript")
    st.subheader("AI Consultancy Management Platform")
    
    # Render sidebar
    render_sidebar()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Projetos", 
        "📅 Meetings", 
        "🚀 GPU Testing",
        "📚 Documentation"
    ])
    
    with tab1:
        render_projects_tab()
    
    with tab2:
        render_meetings_tab()
    
    with tab3:
        render_gpu_tab()
    
    with tab4:
        st.markdown("""
        ### 📖 Documentação do Projeto
        
        #### 🚀 Evolução por Fases
        - **Fase 1** (Atual): GPU + SQLite + Interface básica
        - **Fase 2**: Análise LLM + Geração propostas
        - **Fase 3**: Supabase + Cloud sync
        - **Fase 4**: Multi-usuário + Portal cliente
        
        #### 📋 Arquitetura
        - **Database**: SQLite local (evoluir para Supabase)
        - **GPU**: RTX 3060 + Whisper large-v3
        - **Interface**: Streamlit + componentes customizados
        - **Deploy**: Docker + VPS (vps.frontzin.com.br)
        
        #### 🔧 Configurações
        ```env
        # GPU Mode
        TRANSCRIPTION_MODE=local_gpu
        USE_LOCAL_GPU=true
        WHISPER_MODEL=large-v3
        
        # Database (evolving)
        DATABASE_URL=sqlite:///./data/cloud_transcript.db
        ```
        
        #### 📚 Links Úteis
        - [Roadmap Completo](docs/planning/EVOLUTION.md)
        - [Database Schema](docs/planning/DATABASE.md)
        - [VPS Deploy Config](deploy/vps-config.md)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; font-size: 0.8em;">'
        '🚀 Desenvolvido com <a href="https://iaforte.com.br" target="_blank">IA Forte</a> | '
        'Daniel Dias &lt;ecodelearn@outlook.com&gt;'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()