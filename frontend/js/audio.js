// Audio recording functionality
let currentAudioRecordings = [];
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

// Load audio recordings for current couder
async function loadAudioRecordings() {
    if (!currentCouder) return;
    
    try {
        const recordings = await api.getAudioByCouder(currentCouder.id);
        currentAudioRecordings = recordings || [];
        displayAudioRecordings();
    } catch (error) {
        console.error('Error loading audio recordings:', error);
        document.getElementById('audio-list').innerHTML = `
            <div class="empty-state">
                <i class="fas fa-microphone"></i>
                <h3>No hay grabaciones de audio</h3>
                <p>No se han registrado grabaciones de audio para este couder.</p>
            </div>
        `;
    }
}

// Display audio recordings
function displayAudioRecordings() {
    const container = document.getElementById('audio-list');
    
    if (currentAudioRecordings.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-microphone"></i>
                <h3>No hay grabaciones de audio</h3>
                <p>No se han registrado grabaciones de audio para este couder.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = currentAudioRecordings.map(recording => createAudioCard(recording)).join('');
}

// Create audio card
function createAudioCard(recording) {
    return `
        <div class="audio-card">
            <div class="audio-header">
                <div>
                    <h4 class="audio-title">${recording.titulo}</h4>
                    <div class="audio-date">${formatDate(recording.fecha_grabacion)}</div>
                </div>
                <div class="audio-actions">
                    <button onclick="transcribeAudio('${recording._id}')" class="btn btn-sm btn-secondary">
                        <i class="fas fa-closed-captioning"></i>
                    </button>
                    <button onclick="downloadAudio('${recording._id}')" class="btn btn-sm btn-primary">
                        <i class="fas fa-download"></i>
                    </button>
                    <button onclick="deleteAudio('${recording._id}')" class="btn btn-sm btn-danger">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            
            <div class="audio-controls">
                <audio controls class="audio-player">
                    <source src="${API_BASE_URL}/audio/${recording._id}/download" type="audio/${recording.formato}">
                    Su navegador no soporta el elemento de audio.
                </audio>
            </div>
            
            <div class="audio-info">
                <div class="audio-meta">
                    <span><i class="fas fa-file"></i> ${recording.formato.toUpperCase()}</span>
                    <span><i class="fas fa-weight"></i> ${formatFileSize(recording.tamano_bytes)}</span>
                    ${recording.duracion_segundos ? `
                        <span><i class="fas fa-clock"></i> ${formatDuration(recording.duracion_segundos)}</span>
                    ` : ''}
                </div>
                
                <div class="audio-status">
                    <span class="badge badge-${getAudioStatusClass(recording.estado)}">
                        ${getAudioStatusLabel(recording.estado)}
                    </span>
                </div>
            </div>
            
            ${recording.descripcion ? `
                <div class="audio-description">
                    <p>${recording.descripcion}</p>
                </div>
            ` : ''}
            
            ${recording.transcripcion ? `
                <div class="audio-transcription">
                    <h5><i class="fas fa-closed-captioning"></i> Transcripción</h5>
                    <p>${recording.transcripcion}</p>
                    <small class="text-muted">
                        Transcrito el ${formatDate(recording.fecha_transcripcion)}
                    </small>
                </div>
            ` : ''}
        </div>
    `;
}

// Get audio status class
function getAudioStatusClass(estado) {
    switch (estado) {
        case 'grabado': return 'info';
        case 'procesando': return 'warning';
        case 'transcrito': return 'success';
        case 'error': return 'danger';
        default: return 'secondary';
    }
}

// Get audio status label
function getAudioStatusLabel(estado) {
    switch (estado) {
        case 'grabado': return 'Grabado';
        case 'procesando': return 'Procesando';
        case 'transcrito': return 'Transcrito';
        case 'error': return 'Error';
        default: return 'Desconocido';
    }
}

// Format duration
function formatDuration(seconds) {
    if (!seconds) return 'N/A';
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Show audio recorder
function showAudioRecorder() {
    if (!currentCouder) {
        showError('Por favor seleccione un couder primero');
        return;
    }
    
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-microphone"></i> Nueva Grabación de Audio</h3>
                <button onclick="closeAudioRecorder()" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <form id="audio-form">
                    <div class="form-group">
                        <label for="audio-title">Título:</label>
                        <input type="text" id="audio-title" required>
                    </div>
                    <div class="form-group">
                        <label for="audio-description">Descripción:</label>
                        <textarea id="audio-description" rows="3"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="audio-intervention">Asociar a intervención (opcional):</label>
                        <select id="audio-intervention">
                            <option value="">Sin asociación</option>
                            ${currentInterventions.map(intervention => `
                                <option value="${intervention.id}">${intervention.titulo}</option>
                            `).join('')}
                        </select>
                    </div>
                </form>
                
                <div class="audio-recorder-section">
                    <h4><i class="fas fa-microphone"></i> Grabación</h4>
                    
                    <div class="recorder-controls">
                        <button id="record-btn" onclick="toggleRecording()" class="btn btn-danger">
                            <i class="fas fa-microphone"></i> Iniciar Grabación
                        </button>
                        <button id="pause-btn" onclick="pauseRecording()" class="btn btn-warning" disabled>
                            <i class="fas fa-pause"></i> Pausar
                        </button>
                        <button id="stop-btn" onclick="stopRecording()" class="btn btn-secondary" disabled>
                            <i class="fas fa-stop"></i> Detener
                        </button>
                    </div>
                    
                    <div class="recording-status">
                        <div id="recording-indicator" class="recording-indicator hidden">
                            <span class="recording-dot"></span>
                            Grabando... <span id="recording-time">00:00</span>
                        </div>
                        
                        <div id="audio-preview" class="audio-preview hidden">
                            <h5>Preview:</h5>
                            <audio id="preview-audio" controls></audio>
                        </div>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button onclick="closeAudioRecorder()" class="btn btn-secondary">
                        Cancelar
                    </button>
                    <button onclick="uploadAudio()" class="btn btn-primary" id="upload-btn" disabled>
                        <i class="fas fa-upload"></i> Subir Grabación
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Toggle recording
async function toggleRecording() {
    if (!isRecording) {
        await startRecording();
    } else {
        resumeRecording();
    }
}

// Start recording
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            
            // Show preview
            const preview = document.getElementById('audio-preview');
            const previewAudio = document.getElementById('preview-audio');
            preview.classList.remove('hidden');
            previewAudio.src = audioUrl;
            
            // Enable upload button
            document.getElementById('upload-btn').disabled = false;
        };
        
        mediaRecorder.start();
        isRecording = true;
        
        // Update UI
        document.getElementById('record-btn').innerHTML = '<i class="fas fa-microphone"></i> Reanudar';
        document.getElementById('record-btn').disabled = true;
        document.getElementById('pause-btn').disabled = false;
        document.getElementById('stop-btn').disabled = false;
        document.getElementById('recording-indicator').classList.remove('hidden');
        
        // Start timer
        startRecordingTimer();
        
    } catch (error) {
        showError('Error al acceder al micrófono: ' + error.message);
    }
}

// Pause recording
function pauseRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.pause();
        document.getElementById('record-btn').disabled = false;
        document.getElementById('pause-btn').innerHTML = '<i class="fas fa-play"></i> Reanudar';
        stopRecordingTimer();
    }
}

// Resume recording
function resumeRecording() {
    if (mediaRecorder && mediaRecorder.state === 'paused') {
        mediaRecorder.resume();
        document.getElementById('record-btn').disabled = true;
        document.getElementById('pause-btn').innerHTML = '<i class="fas fa-pause"></i> Pausar';
        startRecordingTimer();
    }
}

// Stop recording
function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        isRecording = false;
        
        // Update UI
        document.getElementById('record-btn').innerHTML = '<i class="fas fa-microphone"></i> Iniciar Grabación';
        document.getElementById('record-btn').disabled = false;
        document.getElementById('pause-btn').disabled = true;
        document.getElementById('stop-btn').disabled = true;
        document.getElementById('recording-indicator').classList.add('hidden');
        
        stopRecordingTimer();
    }
}

// Recording timer
let recordingTimer = null;
let recordingSeconds = 0;

function startRecordingTimer() {
    recordingTimer = setInterval(() => {
        recordingSeconds++;
        const minutes = Math.floor(recordingSeconds / 60);
        const seconds = recordingSeconds % 60;
        document.getElementById('recording-time').textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function stopRecordingTimer() {
    if (recordingTimer) {
        clearInterval(recordingTimer);
        recordingTimer = null;
    }
}

// Upload audio
async function uploadAudio() {
    if (!audioChunks.length) {
        showError('No hay audio para subir');
        return;
    }
    
    try {
        showLoading();
        
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
        
        const metadata = {
            titulo: document.getElementById('audio-title').value,
            descripcion: document.getElementById('audio-description').value,
            intervencion_id: document.getElementById('audio-intervention').value || null
        };
        
        const response = await api.uploadAudio(currentCouder.id, currentUser.id, file, metadata);
        
        if (response) {
            showSuccess('Audio subido exitosamente');
            closeAudioRecorder();
            await loadAudioRecordings();
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al subir audio: ' + error.message);
    }
}

// Download audio
async function downloadAudio(recordingId) {
    try {
        showLoading();
        const blob = await api.downloadAudio(recordingId);
        
        if (blob) {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `audio_${recordingId}.wav`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al descargar audio: ' + error.message);
    }
}

// Transcribe audio
async function transcribeAudio(recordingId) {
    try {
        showLoading();
        const response = await api.transcribeAudio(recordingId);
        
        if (response) {
            showSuccess('Audio transcrito exitosamente');
            await loadAudioRecordings();
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al transcribir audio: ' + error.message);
    }
}

// Delete audio
async function deleteAudio(recordingId) {
    if (!confirm('¿Está seguro de que desea eliminar esta grabación? Esta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        showLoading();
        await api.deleteAudio(recordingId);
        showSuccess('Grabación eliminada');
        await loadAudioRecordings();
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al eliminar grabación: ' + error.message);
    }
}

// Close audio recorder
function closeAudioRecorder() {
    // Stop recording if active
    if (isRecording) {
        stopRecording();
    }
    
    // Reset variables
    audioChunks = [];
    recordingSeconds = 0;
    
    // Remove modal
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

// Add styles for audio components
const audioStyles = document.createElement('style');
audioStyles.textContent = `
    .audio-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.8rem;
        color: #666;
        margin: 0.5rem 0;
    }
    
    .audio-status {
        margin: 0.5rem 0;
    }
    
    .audio-description {
        margin: 1rem 0;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 5px;
        border-left: 3px solid #667eea;
    }
    
    .audio-description p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    .audio-transcription {
        margin: 1rem 0;
        padding: 1rem;
        background: #e9ecef;
        border-radius: 5px;
    }
    
    .audio-transcription h5 {
        margin: 0 0 0.75rem 0;
        color: #333;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .audio-transcription p {
        margin: 0 0 0.5rem 0;
        line-height: 1.5;
        color: #555;
    }
    
    .audio-recorder-section {
        margin: 2rem 0;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 5px;
    }
    
    .audio-recorder-section h4 {
        margin: 0 0 1rem 0;
        color: #333;
    }
    
    .recorder-controls {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .recording-status {
        min-height: 60px;
    }
    
    .recording-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem;
        background: #f8d7da;
        color: #721c24;
        border-radius: 5px;
        font-weight: 500;
    }
    
    .recording-dot {
        width: 12px;
        height: 12px;
        background: #dc3545;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .audio-preview {
        margin-top: 1rem;
    }
    
    .audio-preview h5 {
        margin: 0 0 0.5rem 0;
        color: #333;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .recorder-controls {
            flex-wrap: wrap;
        }
        
        .audio-meta {
            flex-wrap: wrap;
            gap: 0.5rem;
        }
    }
`;
document.head.appendChild(audioStyles);
