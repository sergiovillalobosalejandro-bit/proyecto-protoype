// Couder search and management
let currentCouder = null;

// Search couder by CC
async function searchCouder() {
    const cc = document.getElementById('cc-search').value.trim();
    
    if (!cc) {
        showError('Por favor ingrese un número de cédula');
        return;
    }
    
    try {
        showLoading();
        const couder = await api.searchCouderByCC(cc);
        
        if (couder) {
            currentCouder = couder;
            displayCouderSearchResult(couder);
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al buscar couder: ' + error.message);
    }
}

// Display couder search result
function displayCouderSearchResult(couder) {
    const resultsContainer = document.getElementById('search-results');
    
    resultsContainer.innerHTML = `
        <div class="couder-result">
            <div class="couder-info-header">
                <div>
                    <div class="couder-name">${couder.nombre_completo}</div>
                    <div class="couder-cc">CC: ${couder.cc}</div>
                </div>
                <div>
                    <span class="badge badge-${getStateBadgeClass(couder.estado)}">
                        ${getStateLabel(couder.estado)}
                    </span>
                </div>
            </div>
            
            <div class="couder-details">
                <div class="detail-item">
                    <span class="detail-label">Fecha de Nacimiento:</span>
                    <span class="detail-value">${formatDate(couder.fecha_nacimiento) || 'No registrada'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Teléfono:</span>
                    <span class="detail-value">${couder.telefono || 'No registrado'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value">${couder.email || 'No registrado'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Dirección:</span>
                    <span class="detail-value">${couder.direccion || 'No registrada'}</span>
                </div>
            </div>
            
            ${couder.clan ? `
                <div class="couder-path-info">
                    <h4><i class="fas fa-route"></i> Ruta Educativa</h4>
                    <div class="path-details">
                        <div class="path-item">
                            <span class="path-label">Sede:</span>
                            <span class="path-value">${couder.sede?.nombre || 'No asignada'}</span>
                        </div>
                        <div class="path-item">
                            <span class="path-label">Corte:</span>
                            <span class="path-value">${couder.corte?.nombre || 'No asignado'}</span>
                        </div>
                        <div class="path-item">
                            <span class="path-label">Clan:</span>
                            <span class="path-value">${couder.clan.nombre}</span>
                        </div>
                        <div class="path-item">
                            <span class="path-label">Jornada:</span>
                            <span class="path-value">${couder.clan.jornada}</span>
                        </div>
                        <div class="path-item">
                            <span class="path-label">Tipo de Ruta:</span>
                            <span class="path-value">
                                <span class="badge badge-${couder.corte?.tipo_ruta === 'avanzada' ? 'success' : 'info'}">
                                    ${couder.corte?.tipo_ruta === 'avanzada' ? 'Avanzada' : 'Básica'}
                                </span>
                            </span>
                        </div>
                    </div>
                </div>
            ` : ''}
            
            <div class="couder-actions">
                <button onclick="viewClinicalHistory(${couder.id})" class="btn btn-primary">
                    <i class="fas fa-notes-medical"></i> Ver Historial Clínico
                </button>
                <button onclick="editCouder(${couder.id})" class="btn btn-secondary">
                    <i class="fas fa-edit"></i> Editar
                </button>
            </div>
        </div>
    `;
}

// Get state badge class
function getStateBadgeClass(estado) {
    switch (estado) {
        case 'activo': return 'success';
        case 'retirado': return 'warning';
        case 'completado': return 'info';
        default: return 'secondary';
    }
}

// Get state label
function getStateLabel(estado) {
    switch (estado) {
        case 'activo': return 'Activo';
        case 'retirado': return 'Retirado';
        case 'completado': return 'Completado';
        default: return 'Desconocido';
    }
}

// View clinical history
function viewClinicalHistory(couderId) {
    // Set current couder if not already set
    if (!currentCouder || currentCouder.id !== couderId) {
        // We need to fetch the couder data again
        searchCouderById(couderId);
    }
    
    // Switch to clinical view
    showView('clinical');
    
    // Load clinical data
    loadClinicalHistory();
}

// Search couder by ID (internal function)
async function searchCouderById(couderId) {
    try {
        showLoading();
        // This would require an additional API endpoint or we can search by CC
        // For now, we'll assume we have the couder data from the previous search
        if (currentCouder && currentCouder.id === couderId) {
            loadClinicalHistory();
        }
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar datos del couder: ' + error.message);
    }
}

// Load clinical history
async function loadClinicalHistory() {
    if (!currentCouder) return;
    
    try {
        showLoading();
        
        // Display couder basic info in clinical view
        displayCouderInfo();
        
        // Load interventions
        await loadInterventions();
        
        // Load AI analyses
        await loadAIAnalyses();
        
        // Load audio recordings
        await loadAudioRecordings();
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar historial clínico: ' + error.message);
    }
}

// Display couder info in clinical view
function displayCouderInfo() {
    const container = document.getElementById('couder-info');
    
    container.innerHTML = `
        <div class="couder-clinical-info">
            <div class="info-header">
                <div class="info-title">
                    <h3>${currentCouder.nombre_completo}</h3>
                    <p class="info-subtitle">CC: ${currentCouder.cc}</p>
                </div>
                <div class="info-status">
                    <span class="badge badge-${getStateBadgeClass(currentCouder.estado)}">
                        ${getStateLabel(currentCouder.estado)}
                    </span>
                </div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Clan:</span>
                    <span class="info-value">${currentCouder.clan?.nombre || 'No asignado'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Jornada:</span>
                    <span class="info-value">${currentCouder.clan?.jornada || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Ruta:</span>
                    <span class="info-value">
                        <span class="badge badge-${currentCouder.corte?.tipo_ruta === 'avanzada' ? 'success' : 'info'}">
                            ${currentCouder.corte?.tipo_ruta === 'avanzada' ? 'Avanzada' : 'Básica'}
                        </span>
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Fecha Ingreso:</span>
                    <span class="info-value">${formatDate(currentCouder.fecha_ingreso)}</span>
                </div>
            </div>
        </div>
    `;
}

// Edit couder (placeholder)
function editCouder(couderId) {
    showSuccess('Función de edición en desarrollo');
}

// Add styles for couder components
const couderStyles = document.createElement('style');
couderStyles.textContent = `
    .couder-clinical-info {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .info-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eee;
    }
    
    .info-title h3 {
        margin: 0 0 0.25rem 0;
        color: #333;
        font-size: 1.5rem;
    }
    
    .info-subtitle {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .info-item {
        display: flex;
        flex-direction: column;
    }
    
    .info-label {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.25rem;
    }
    
    .info-value {
        font-weight: 500;
        color: #333;
    }
    
    .couder-path-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .couder-path-info h4 {
        margin: 0 0 1rem 0;
        color: #333;
        font-size: 1rem;
    }
    
    .path-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.75rem;
    }
    
    .path-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .path-label {
        font-size: 0.8rem;
        color: #666;
    }
    
    .path-value {
        font-weight: 500;
        color: #333;
    }
    
    .couder-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    
    @media (max-width: 768px) {
        .info-header {
            flex-direction: column;
            gap: 1rem;
        }
        
        .couder-actions {
            flex-direction: column;
        }
        
        .path-details {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(couderStyles);
