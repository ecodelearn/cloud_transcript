"""
Whisper GPU service for local transcription using RTX 3060
Fallback to API services if GPU unavailable
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import torch
import whisper
from pydub import AudioSegment

logger = logging.getLogger(__name__)

class WhisperGPUService:
    """GPU-accelerated Whisper transcription service with smart model management"""
    
    # Available models configuration
    AVAILABLE_MODELS = {
        'turbo': {
            'name': 'turbo',
            'size': '39MB',
            'speed': 'Fastest',
            'quality': 'Good',
            'description': 'Fastest transcription, good quality'
        },
        'medium': {
            'name': 'medium', 
            'size': '769MB',
            'speed': 'Fast',
            'quality': 'Better',
            'description': 'Balanced speed and quality'
        },
        'large-v3': {
            'name': 'large-v3',
            'size': '2.88GB', 
            'speed': 'Slower',
            'quality': 'Best',
            'description': 'Best quality, slower processing'
        }
    }
    
    def __init__(self):
        self.model = None
        self.current_model_name = None
        self.device = self._get_device()
        self.models_cache_dir = Path(__file__).parent.parent.parent / 'data' / 'models'
        self.models_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load active model preference (default: turbo for testing)
        self.active_model = self._get_active_model()
        
        logger.info(f"Whisper GPU Service initialized - Device: {self.device}")
        logger.info(f"Active model: {self.active_model or 'None (models available on-demand)'}")
    
    def _get_device(self) -> str:
        """Determine best available device"""
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"CUDA available - GPU: {gpu_name}")
        else:
            device = "cpu"
            logger.warning("CUDA not available - falling back to CPU")
        
        return device
    
    def _get_active_model(self) -> Optional[str]:
        """Get active model from config file or environment"""
        # Check environment variable first
        env_model = os.getenv('WHISPER_MODEL')
        if env_model and env_model in self.AVAILABLE_MODELS:
            return env_model
            
        # Check config file
        config_file = self.models_cache_dir / 'active_model.txt'
        if config_file.exists():
            try:
                active = config_file.read_text().strip()
                if active in self.AVAILABLE_MODELS:
                    return active
            except Exception as e:
                logger.warning(f"Could not read active model config: {e}")
        
        # Default to turbo for testing (fast startup)
        return 'turbo'
    
    def _set_active_model(self, model_name: str) -> bool:
        """Set active model and save to config"""
        if model_name not in self.AVAILABLE_MODELS:
            logger.error(f"Unknown model: {model_name}")
            return False
        
        try:
            config_file = self.models_cache_dir / 'active_model.txt'
            config_file.write_text(model_name)
            self.active_model = model_name
            logger.info(f"Active model set to: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Could not save active model config: {e}")
            return False
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get information about all available models"""
        models_status = {}
        
        for model_name, model_info in self.AVAILABLE_MODELS.items():
            # Check if model is downloaded
            model_files = list(self.models_cache_dir.glob(f"*{model_name}*"))
            is_downloaded = len(model_files) > 0
            
            models_status[model_name] = {
                **model_info,
                'downloaded': is_downloaded,
                'active': model_name == self.active_model,
                'loaded': model_name == self.current_model_name
            }
        
        return models_status
    
    def download_model(self, model_name: str) -> bool:
        """Download a specific model"""
        if model_name not in self.AVAILABLE_MODELS:
            logger.error(f"Unknown model: {model_name}")
            return False
        
        try:
            logger.info(f"Downloading Whisper model: {model_name}")
            whisper.load_model(model_name, download_root=str(self.models_cache_dir))
            logger.info(f"Model {model_name} downloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to download model {model_name}: {e}")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a downloaded model"""
        if model_name not in self.AVAILABLE_MODELS:
            return False
        
        try:
            # Find and delete model files
            model_files = list(self.models_cache_dir.glob(f"*{model_name}*"))
            deleted_count = 0
            
            for model_file in model_files:
                model_file.unlink()
                deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Deleted {deleted_count} files for model {model_name}")
                
                # If this was the loaded model, clear it
                if self.current_model_name == model_name:
                    self.model = None
                    self.current_model_name = None
                
                return True
            else:
                logger.warning(f"No files found for model {model_name}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete model {model_name}: {e}")
            return False
    
    def switch_model(self, model_name: str) -> bool:
        """Switch active model and optionally load it"""
        if not self._set_active_model(model_name):
            return False
        
        # If a model is currently loaded and it's different, unload it
        if self.model and self.current_model_name != model_name:
            logger.info(f"Unloading current model: {self.current_model_name}")
            self.model = None
            self.current_model_name = None
        
        return True
    
    def _load_model(self) -> bool:
        """Load active Whisper model (lazy loading)"""
        if self.model is not None and self.current_model_name == self.active_model:
            return True
        
        if not self.active_model:
            logger.error("No active model set")
            return False
        
        try:
            logger.info(f"Loading Whisper model: {self.active_model}")
            start_time = time.time()
            
            # Load model with GPU support
            self.model = whisper.load_model(
                self.active_model,
                device=self.device,
                download_root=str(self.models_cache_dir)
            )
            
            self.current_model_name = self.active_model
            load_time = time.time() - start_time
            logger.info(f"Model {self.active_model} loaded successfully in {load_time:.2f}s")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Whisper model {self.active_model}: {str(e)}")
            return False
    
    def load_model(self) -> bool:
        """Public method to explicitly load the Whisper model"""
        return self._load_model()
    
    def is_model_loaded(self) -> bool:
        """Check if model is currently loaded"""
        return self.model is not None
    
    def _prepare_audio(self, audio_path: str) -> Tuple[str, float]:
        """Prepare audio file for Whisper processing"""
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Get file size
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        
        # Whisper works best with WAV format
        if audio_path.suffix.lower() not in ['.wav']:
            logger.info(f"Converting {audio_path.suffix} to WAV for optimal processing")
            
            # Load audio with pydub
            if audio_path.suffix.lower() == '.opus':
                audio = AudioSegment.from_file(str(audio_path), format='opus')
            elif audio_path.suffix.lower() == '.mp3':
                audio = AudioSegment.from_mp3(str(audio_path))
            elif audio_path.suffix.lower() == '.m4a':
                audio = AudioSegment.from_file(str(audio_path), format='m4a')
            else:
                audio = AudioSegment.from_file(str(audio_path))
            
            # Convert to WAV (16kHz mono for Whisper)
            audio = audio.set_frame_rate(16000).set_channels(1)
            
            # Save temp WAV file
            temp_wav = audio_path.parent / f"{audio_path.stem}_temp.wav"
            audio.export(str(temp_wav), format="wav")
            
            return str(temp_wav), file_size_mb
        
        return str(audio_path), file_size_mb
    
    def transcribe_audio(self, audio_path: str, language: str = 'pt') -> Dict[str, Any]:
        """
        Transcribe audio file using GPU Whisper
        
        Args:
            audio_path: Path to audio file
            language: Language code (pt for Portuguese)
            
        Returns:
            Dict with transcription results
        """
        
        if not self._load_model():
            raise RuntimeError("Failed to load Whisper model")
        
        try:
            # Prepare audio
            processed_audio_path, file_size_mb = self._prepare_audio(audio_path)
            
            logger.info(f"Starting transcription: {Path(audio_path).name} ({file_size_mb:.1f}MB)")
            start_time = time.time()
            
            # Whisper transcription options
            options = {
                'language': language,
                'task': 'transcribe',
                'fp16': self.device == 'cuda',  # Use FP16 on GPU for speed
                'verbose': False
            }
            
            # Run transcription
            result = self.model.transcribe(processed_audio_path, **options)
            
            processing_time = time.time() - start_time
            
            # Clean up temp file if created
            if processed_audio_path != audio_path:
                Path(processed_audio_path).unlink(missing_ok=True)
            
            # Extract segments with timestamps
            segments = []
            for segment in result.get('segments', []):
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'confidence': segment.get('no_speech_prob', 0.0)
                })
            
            # Build response
            response = {
                'text': result['text'].strip(),
                'language': result['language'],
                'segments': segments,
                'processing_time_seconds': int(processing_time),
                'audio_duration_seconds': result.get('segments', [{}])[-1].get('end', 0),
                'model_used': self.model_name,
                'device_used': self.device,
                'file_size_mb': file_size_mb,
                'success': True
            }
            
            logger.info(f"Transcription completed in {processing_time:.1f}s - "
                       f"Speed: {response['audio_duration_seconds']/processing_time:.1f}x realtime")
            
            return response
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return {
                'text': '',
                'error': str(e),
                'success': False,
                'processing_time_seconds': 0,
                'model_used': self.model_name,
                'device_used': self.device
            }
    
    def transcribe_segments(self, audio_path: str, segments: list, language: str = 'pt') -> Dict[str, Any]:
        """
        Transcribe specific segments of audio (for long meetings)
        
        Args:
            audio_path: Path to audio file
            segments: List of (start_time, end_time) tuples in seconds
            language: Language code
            
        Returns:
            Dict with segmented transcription results
        """
        
        if not segments:
            return self.transcribe_audio(audio_path, language)
        
        try:
            # Load original audio
            audio = AudioSegment.from_file(audio_path)
            
            segment_results = []
            total_processing_time = 0
            
            for i, (start_time, end_time) in enumerate(segments):
                logger.info(f"Processing segment {i+1}/{len(segments)} ({start_time}s-{end_time}s)")
                
                # Extract segment
                start_ms = int(start_time * 1000)
                end_ms = int(end_time * 1000)
                segment_audio = audio[start_ms:end_ms]
                
                # Save temp segment file
                temp_segment_path = Path(audio_path).parent / f"temp_segment_{i}.wav"
                segment_audio.export(str(temp_segment_path), format="wav")
                
                # Transcribe segment
                segment_result = self.transcribe_audio(str(temp_segment_path), language)
                
                if segment_result['success']:
                    segment_results.append({
                        'segment_number': i + 1,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time,
                        'text': segment_result['text'],
                        'processing_time': segment_result['processing_time_seconds']
                    })
                    total_processing_time += segment_result['processing_time_seconds']
                
                # Clean up temp file
                temp_segment_path.unlink(missing_ok=True)
            
            # Combine all segment texts
            full_text = '\n\n'.join([seg['text'] for seg in segment_results])
            
            return {
                'text': full_text,
                'segments': segment_results,
                'total_processing_time_seconds': total_processing_time,
                'model_used': self.model_name,
                'device_used': self.device,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Segment transcription failed: {str(e)}")
            return {
                'text': '',
                'error': str(e),
                'success': False,
                'segments': [],
                'total_processing_time_seconds': 0
            }
    
    def get_gpu_stats(self) -> Dict[str, Any]:
        """Get GPU utilization stats and model information"""
        stats = {
            'device': self.device,
            'model_loaded': self.model is not None,
            'active_model': self.active_model,
            'loaded_model': self.current_model_name,
            'available_models': self.get_available_models()
        }
        
        if self.device == 'cuda' and torch.cuda.is_available():
            stats.update({
                'gpu_name': torch.cuda.get_device_name(0),
                'gpu_memory_allocated_mb': torch.cuda.memory_allocated(0) / (1024**2),
                'gpu_memory_reserved_mb': torch.cuda.memory_reserved(0) / (1024**2),
                'gpu_memory_total_mb': torch.cuda.get_device_properties(0).total_memory / (1024**2)
            })
        
        return stats
    
    def benchmark_performance(self, test_duration_seconds: int = 60) -> Dict[str, Any]:
        """Run performance benchmark"""
        if not self._load_model():
            return {'error': 'Model failed to load'}
        
        # Generate test audio (sine wave)
        from pydub.generators import Sine
        
        test_audio = Sine(440).to_audio_segment(duration=test_duration_seconds * 1000)
        test_path = self.models_cache_dir / 'benchmark_test.wav'
        test_audio.export(str(test_path), format='wav')
        
        # Run benchmark
        start_time = time.time()
        result = self.transcribe_audio(str(test_path))
        
        # Clean up
        test_path.unlink(missing_ok=True)
        
        if result['success']:
            return {
                'test_duration_seconds': test_duration_seconds,
                'processing_time_seconds': result['processing_time_seconds'],
                'speed_multiplier': test_duration_seconds / result['processing_time_seconds'],
                'device': self.device,
                'model': self.model_name,
                'gpu_stats': self.get_gpu_stats()
            }
        else:
            return {'error': result.get('error', 'Benchmark failed')}


# Global instance
whisper_service = WhisperGPUService()

def get_whisper_service() -> WhisperGPUService:
    """Get global Whisper service instance"""
    return whisper_service