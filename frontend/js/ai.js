// AI Analysis functionality
let currentAIAnalyses = [];

// Load AI analyses for current couder
async function loadAIAnalyses() {
    if (!currentCouder) return;
    
    try {
        const analyses = await api.getHistoricalAnalyses(currentCouder.id);
        currentAIAnalyses = analyses || [];
        displayAIAnalyses();
    } catch (error) {
        console.error('Error loading AI analyses:', error);
        // Don't show error for AI analyses as it's not critical
        document.getElementById('ai-analyses-list').innerHTML = `
            <div class="empty-state">
                <i class="fas fa-brain"></i>
                <h3>No hay análisis disponibles</h3>
                <p>Genere un análisis para ver los resultados aquí.</p>
            </div>
        `;
    }
}

// Display AI analyses
function displayAIAnalyses() {
    const container = document.getElementById('ai-analyses-list');
    
    if (currentAIAnalyses.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-brain"></i>
                <h3>No hay análisis disponibles</h3>
                <p>Genere un análisis para ver los resultados aquí.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = currentAIAnalyses.map(analysis => createAIAnalysisCard(analysis)).join('');
}

// Create AI analysis card
function createAIAnalysisCard(analysis) {
    const content = analysis.contenido;
    const typeLabel = getAnalysisTypeLabel(analysis.tipo_analisis);
    const typeIcon = getAnalysisTypeIcon(analysis.tipo_analisis);
    
    return `
        <div class="ai-analysis-card">
            <div class="ai-analysis-header">
                <div class="analysis-type">
                    <i class="fas ${typeIcon}"></i>
                    <span>${typeLabel}</span>
                </div>
                <div class="analysis-date">
                    ${formatDate(analysis.fecha_generacion)}
                </div>
            </div>
            
            <div class="ai-analysis-content">
                ${content.resumen ? `
                    <div class="ai-analysis-summary">
                        <h4><i class="fas fa-file-alt"></i> Resumen</h4>
                        <p>${content.resumen}</p>
                    </div>
                ` : ''}
                
                ${content.puntos_clave && content.puntos_clave.length > 0 ? `
                    <div class="ai-analysis-section">
                        <h4><i class="fas fa-list"></i> Puntos Clave</h4>
                        <ul class="ai-analysis-points">
                            ${content.puntos_clave.map(point => `<li>${point}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${content.diagnostico_preliminar ? `
                    <div class="ai-analysis-section">
                        <h4><i class="fas fa-stethoscope"></i> Diagnóstico Preliminar</h4>
                        <p>${content.diagnostico_preliminar}</p>
                    </div>
                ` : ''}
                
                ${content.sugerencias && content.sugerencias.length > 0 ? `
                    <div class="ai-analysis-section">
                        <h4><i class="fas fa-lightbulb"></i> Sugerencias</h4>
                        <ul class="ai-analysis-points">
                            ${content.sugerencias.map(suggestion => `<li>${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${content.nivel_riesgo ? `
                    <div class="ai-analysis-section">
                        <h4><i class="fas fa-exclamation-triangle"></i> Nivel de Riesgo</h4>
                        <span class="risk-badge risk-${content.nivel_riesgo}">
                            ${getRiskLabel(content.nivel_riesgo)}
                        </span>
                    </div>
                ` : ''}
                
                ${content.recomendaciones && content.recomendaciones.length > 0 ? `
                    <div class="ai-analysis-section">
                        <h4><i class="fas fa-clipboard-check"></i> Recomendaciones</h4>
                        <ul class="ai-analysis-points">
                            ${content.recomendaciones.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
            
            <div class="ai-analysis-footer">
                <small class="text-muted">
                    <i class="fas fa-robot"></i> Modelo: ${analysis.modelo_ia || 'GPT-4'}
                </small>
                <button onclick="deleteAnalysis('${analysis._id}')" class="btn btn-sm btn-danger">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </div>
        </div>
    `;
}

// Get analysis type label
function getAnalysisTypeLabel(type) {
    switch (type) {
        case 'sintesis': return 'Síntesis';
        case 'diagnostico': return 'Diagnóstico';
        default: return 'Análisis';
    }
}

// Get analysis type icon
function getAnalysisTypeIcon(type) {
    switch (type) {
        case 'sintesis': return 'fa-compress-alt';
        case 'diagnostico': return 'fa-stethoscope';
        default: return 'fa-brain';
    }
}

// Get risk label
function getRiskLabel(risk) {
    switch (risk) {
        case 'bajo': return 'Bajo';
        case 'medio': return 'Medio';
        case 'alto': return 'Alto';
        default: return 'Desconocido';
    }
}

// Generate synthesis
async function generateSynthesis() {
    if (!currentCouder) {
        showError('Por favor seleccione un couder primero');
        return;
    }
    
    if (currentInterventions.length === 0) {
        showError('No hay intervenciones para sintetizar');
        return;
    }
    
    // Show intervention selection modal
    showInterventionSelectionModal('sintesis');
}

// Generate diagnosis
async function generateDiagnosis() {
    if (!currentCouder) {
        showError('Por favor seleccione un couder primero');
        return;
    }
    
    if (currentInterventions.length === 0) {
        showError('No hay intervenciones para analizar');
        return;
    }
    
    // Show intervention selection modal
    showInterventionSelectionModal('diagnostico');
}

// Show intervention selection modal
function showInterventionSelectionModal(analysisType) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>
                    <i class="fas ${analysisType === 'sintesis' ? 'fa-compress-alt' : 'fa-stethoscope'}"></i>
                    ${analysisType === 'sintesis' ? 'Generar Síntesis' : 'Generar Diagnóstico'}
                </h3>
                <button onclick="closeInterventionSelectionModal()" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <p>Seleccione las intervenciones que desea incluir en el análisis:</p>
                
                <div class="intervention-selection">
                    <div class="selection-header">
                        <label class="checkbox-container">
                            <input type="checkbox" id="select-all-interventions" onchange="toggleAllInterventions(this)">
                            <span class="checkmark"></span>
                            Seleccionar todas
                        </label>
                        <span class="selection-count">
                            <span id="selected-count">0</span> de ${currentInterventions.length} seleccionadas
                        </span>
                    </div>
                    
                    <div class="interventions-checkbox-list">
                        ${currentInterventions.map(intervention => `
                            <label class="checkbox-container intervention-checkbox">
                                <input type="checkbox" value="${intervention.id}" onchange="updateSelectionCount()">
                                <span class="checkmark"></span>
                                <div class="intervention-checkbox-content">
                                    <strong>${intervention.titulo}</strong>
                                    <small>${formatDate(intervention.fecha_intervencion)}</small>
                                </div>
                            </label>
                        `).join('')}
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button onclick="closeInterventionSelectionModal()" class="btn btn-secondary">
                        Cancelar
                    </button>
                    <button onclick="executeAIAnalysis('${analysisType}')" class="btn btn-primary">
                        <i class="fas ${analysisType === 'sintesis' ? 'fa-compress-alt' : 'fa-stethoscope'}"></i>
                        Generar ${analysisType === 'sintesis' ? 'Síntesis' : 'Diagnóstico'}
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Toggle all interventions
function toggleAllInterventions(checkbox) {
    const checkboxes = document.querySelectorAll('.intervention-checkbox input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = checkbox.checked);
    updateSelectionCount();
}

// Update selection count
function updateSelectionCount() {
    const checkboxes = document.querySelectorAll('.intervention-checkbox input[type="checkbox"]:checked');
    const count = checkboxes.length;
    document.getElementById('selected-count').textContent = count;
    
    // Update select all checkbox state
    const selectAllCheckbox = document.getElementById('select-all-interventions');
    const totalCheckboxes = document.querySelectorAll('.intervention-checkbox input[type="checkbox"]').length;
    selectAllCheckbox.checked = count === totalCheckboxes && count > 0;
}

// Execute AI analysis
async function executeAIAnalysis(analysisType) {
    const selectedCheckboxes = document.querySelectorAll('.intervention-checkbox input[type="checkbox"]:checked');
    const interventionIds = Array.from(selectedCheckboxes).map(cb => parseInt(cb.value));
    
    if (interventionIds.length === 0) {
        showError('Por favor seleccione al menos una intervención');
        return;
    }
    
    try {
        showLoading();
        closeInterventionSelectionModal();
        
        let response;
        if (analysisType === 'sintesis') {
            response = await api.synthesizeInterventions(currentCouder.id, interventionIds);
        } else {
            response = await api.generateDiagnosis(currentCouder.id, interventionIds);
        }
        
        if (response) {
            showSuccess(`${analysisType === 'sintesis' ? 'Síntesis' : 'Diagnóstico'} generado exitosamente`);
            await loadAIAnalyses();
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError(`Error al generar ${analysisType === 'sintesis' ? 'síntesis' : 'diagnóstico'}: ${error.message}`);
    }
}

// Delete analysis
async function deleteAnalysis(analysisId) {
    if (!confirm('¿Está seguro de que desea eliminar este análisis? Esta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        showLoading();
        await api.deleteAnalysis(analysisId);
        showSuccess('Análisis eliminado');
        await loadAIAnalyses();
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al eliminar análisis: ' + error.message);
    }
}

// Close intervention selection modal
function closeInterventionSelectionModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

// Add styles for AI components
const aiStyles = document.createElement('style');
aiStyles.textContent = `
    .ai-analysis-section {
        margin: 1.5rem 0;
    }
    
    .ai-analysis-section h4 {
        margin: 0 0 0.75rem 0;
        color: #333;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .risk-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .risk-bajo {
        background: #d4edda;
        color: #155724;
    }
    
    .risk-medio {
        background: #fff3cd;
        color: #856404;
    }
    
    .risk-alto {
        background: #f8d7da;
        color: #721c24;
    }
    
    .ai-analysis-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid #eee;
        margin-top: 1rem;
    }
    
    .intervention-selection {
        margin: 1rem 0;
    }
    
    .selection-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    .selection-count {
        font-size: 0.9rem;
        color: #666;
    }
    
    .interventions-checkbox-list {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    
    .checkbox-container {
        display: flex;
        align-items: flex-start;
        cursor: pointer;
        padding: 0.75rem;
        border-bottom: 1px solid #eee;
        margin: 0;
    }
    
    .checkbox-container:last-child {
        border-bottom: none;
    }
    
    .checkbox-container input[type="checkbox"] {
        display: none;
    }
    
    .checkmark {
        width: 18px;
        height: 18px;
        border: 2px solid #667eea;
        border-radius: 3px;
        margin-right: 0.75rem;
        margin-top: 2px;
        position: relative;
        flex-shrink: 0;
    }
    
    .checkbox-container input[type="checkbox"]:checked + .checkmark {
        background: #667eea;
    }
    
    .checkbox-container input[type="checkbox"]:checked + .checkmark:after {
        content: "";
        position: absolute;
        left: 5px;
        top: 2px;
        width: 5px;
        height: 10px;
        border: solid white;
        border-width: 0 2px 2px 0;
        transform: rotate(45deg);
    }
    
    .intervention-checkbox-content {
        flex: 1;
    }
    
    .intervention-checkbox-content strong {
        display: block;
        margin-bottom: 0.25rem;
        color: #333;
    }
    
    .intervention-checkbox-content small {
        color: #666;
        font-size: 0.8rem;
    }
    
    @media (max-width: 768px) {
        .selection-header {
            flex-direction: column;
            gap: 0.5rem;
            align-items: flex-start;
        }
        
        .ai-analysis-footer {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
        }
    }
`;
document.head.appendChild(aiStyles);
