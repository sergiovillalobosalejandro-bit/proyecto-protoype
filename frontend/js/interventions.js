// Interventions management
let currentInterventions = [];
let currentEditingIntervention = null;

// Load interventions for current couder
async function loadInterventions() {
    if (!currentCouder) return;
    
    try {
        const interventions = await api.getInterventionsByCouder(currentCouder.id);
        currentInterventions = interventions || [];
        displayInterventions();
    } catch (error) {
        console.error('Error loading interventions:', error);
        showError('Error al cargar intervenciones: ' + error.message);
    }
}

// Display interventions list
function displayInterventions() {
    const container = document.getElementById('interventions-list');
    
    if (currentInterventions.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-clipboard-list"></i>
                <h3>No hay intervenciones registradas</h3>
                <p>Este couder aún no tiene intervenciones registradas.</p>
                <button onclick="showInterventionForm()" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Primera Intervención
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = currentInterventions.map(intervention => createInterventionCard(intervention)).join('');
}

// Create intervention card
function createInterventionCard(intervention) {
    return `
        <div class="intervention-card">
            <div class="intervention-header">
                <div>
                    <h4 class="intervention-title">${intervention.titulo}</h4>
                    <div class="intervention-meta">
                        <span><i class="fas fa-calendar"></i> ${formatDate(intervention.fecha_intervencion)}</span>
                        ${intervention.duracion_minutos ? `
                            <span><i class="fas fa-clock"></i> ${intervention.duracion_minutos} min</span>
                        ` : ''}
                        ${intervention.tipo_intervencion ? `
                            <span><i class="fas fa-tag"></i> ${intervention.tipo_intervencion}</span>
                        ` : ''}
                    </div>
                </div>
                <div class="intervention-actions">
                    <button onclick="editIntervention(${intervention.id})" class="btn btn-sm btn-secondary">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="deleteIntervention(${intervention.id})" class="btn btn-sm btn-danger">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            
            <div class="intervention-content">
                <p class="intervention-description">${intervention.descripcion}</p>
                ${intervention.observaciones ? `
                    <div class="intervention-observations">
                        <strong>Observaciones:</strong>
                        <p>${intervention.observaciones}</p>
                    </div>
                ` : ''}
            </div>
            
            <div class="intervention-footer">
                <small class="text-muted">
                    <i class="fas fa-user"></i> Registrado por: Usuario ID ${intervention.usuario_id}
                </small>
                <small class="text-muted">
                    <i class="fas fa-clock"></i> Creado: ${formatDate(intervention.creado_en)}
                </small>
            </div>
        </div>
    `;
}

// Show intervention form
function showInterventionForm(interventionId = null) {
    currentEditingIntervention = interventionId;
    
    const modal = document.getElementById('intervention-modal');
    const form = document.getElementById('intervention-form');
    
    // Reset form
    form.reset();
    
    // Set current date/time as default
    const now = new Date();
    const localDateTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
        .toISOString()
        .slice(0, 16);
    document.getElementById('intervention-date').value = localDateTime;
    
    // If editing, load intervention data
    if (interventionId) {
        const intervention = currentInterventions.find(i => i.id === interventionId);
        if (intervention) {
            document.getElementById('intervention-title').value = intervention.titulo;
            document.getElementById('intervention-description').value = intervention.descripcion;
            document.getElementById('intervention-observations').value = intervention.observaciones || '';
            document.getElementById('intervention-duration').value = intervention.duracion_minutos || '';
            document.getElementById('intervention-type').value = intervention.tipo_intervencion || '';
            
            const interventionDate = new Date(intervention.fecha_intervencion);
            const localDateTime = new Date(interventionDate.getTime() - interventionDate.getTimezoneOffset() * 60000)
                .toISOString()
                .slice(0, 16);
            document.getElementById('intervention-date').value = localDateTime;
        }
    }
    
    // Update modal title
    const modalTitle = modal.querySelector('h3');
    modalTitle.innerHTML = interventionId ? 
        '<i class="fas fa-edit"></i> Editar Intervención' : 
        '<i class="fas fa-plus"></i> Nueva Intervención';
    
    // Show modal
    modal.classList.add('active');
}

// Save intervention
async function saveIntervention(event) {
    event.preventDefault();
    
    if (!currentCouder || !currentUser) {
        showError('Error: No se ha seleccionado un couder o no hay usuario autenticado');
        return;
    }
    
    const formData = {
        couder_id: currentCouder.id,
        usuario_id: currentUser.id,
        titulo: document.getElementById('intervention-title').value,
        descripcion: document.getElementById('intervention-description').value,
        observaciones: document.getElementById('intervention-observations').value || null,
        fecha_intervencion: new Date(document.getElementById('intervention-date').value).toISOString(),
        duracion_minutos: parseInt(document.getElementById('intervention-duration').value) || null,
        tipo_intervencion: document.getElementById('intervention-type').value || null
    };
    
    try {
        showLoading();
        
        let response;
        if (currentEditingIntervention) {
            response = await api.updateIntervention(currentEditingIntervention, formData);
        } else {
            response = await api.createIntervention(formData);
        }
        
        if (response) {
            showSuccess(currentEditingIntervention ? 'Intervención actualizada' : 'Intervención creada');
            closeModal('intervention-modal');
            await loadInterventions();
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al guardar intervención: ' + error.message);
    }
}

// Edit intervention
function editIntervention(interventionId) {
    showInterventionForm(interventionId);
}

// Delete intervention
async function deleteIntervention(interventionId) {
    if (!confirm('¿Está seguro de que desea eliminar esta intervención? Esta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        showLoading();
        await api.deleteIntervention(interventionId);
        showSuccess('Intervención eliminada');
        await loadInterventions();
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al eliminar intervención: ' + error.message);
    }
}

// Add styles for interventions
const interventionStyles = document.createElement('style');
interventionStyles.textContent = `
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #666;
    }
    
    .empty-state i {
        font-size: 3rem;
        color: #ddd;
        margin-bottom: 1rem;
    }
    
    .empty-state h3 {
        margin: 1rem 0 0.5rem 0;
        color: #333;
    }
    
    .empty-state p {
        margin: 0 0 2rem 0;
    }
    
    .intervention-content {
        margin: 1rem 0;
    }
    
    .intervention-description {
        margin: 0 0 1rem 0;
        line-height: 1.6;
        color: #555;
    }
    
    .intervention-observations {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 5px;
        border-left: 3px solid #667eea;
    }
    
    .intervention-observations strong {
        display: block;
        margin-bottom: 0.5rem;
        color: #333;
    }
    
    .intervention-observations p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    .intervention-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid #eee;
        margin-top: 1rem;
    }
    
    .intervention-footer small {
        font-size: 0.8rem;
    }
    
    @media (max-width: 768px) {
        .intervention-footer {
            flex-direction: column;
            gap: 0.5rem;
            align-items: flex-start;
        }
    }
`;
document.head.appendChild(interventionStyles);
