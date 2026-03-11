// Dashboard functionality
let currentSedeId = null;
let currentCorteId = null;
let currentClanId = null;

// Load dashboard data
async function loadDashboard() {
    try {
        showLoading();
        const data = await api.getDashboardOverview();
        
        if (data) {
            updateMetricsOverview(data.totales);
            updateSedesCards(data.sedes);
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar el dashboard: ' + error.message);
    }
}

// Update metrics overview
function updateMetricsOverview(totals) {
    document.getElementById('total-couders').textContent = totals.total_couders || 0;
    document.getElementById('activos-couders').textContent = totals.activos || 0;
    document.getElementById('retirados-couders').textContent = totals.retirados || 0;
    document.getElementById('completados-couders').textContent = totals.completados || 0;
}

// Update sedes cards
function updateSedesCards(sedes) {
    const container = document.getElementById('sedes-container');
    container.innerHTML = '';
    
    sedes.forEach(sede => {
        const card = createSedeCard(sede);
        container.appendChild(card);
    });
}

// Create sede card
function createSedeCard(sede) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
        <div class="card-header">
            <h4 class="card-title">${sede.nombre}</h4>
            <span class="badge badge-info">${sede.porcentaje_atendidos}% atendidos</span>
        </div>
        <div class="card-body">
            <div class="metrics-mini">
                <div class="metric-mini">
                    <span class="metric-label">Total:</span>
                    <span class="metric-value">${sede.total_couders}</span>
                </div>
                <div class="metric-mini">
                    <span class="metric-label">Activos:</span>
                    <span class="metric-value text-success">${sede.activos}</span>
                </div>
                <div class="metric-mini">
                    <span class="metric-label">Retirados:</span>
                    <span class="metric-value text-warning">${sede.retirados}</span>
                </div>
                <div class="metric-mini">
                    <span class="metric-label">Completados:</span>
                    <span class="metric-value text-info">${sede.completados}</span>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${sede.porcentaje_atendidos}%"></div>
            </div>
            <button onclick="viewSedeDetails(${sede.id})" class="btn btn-primary btn-sm mt-2">
                <i class="fas fa-eye"></i> Ver Detalles
            </button>
        </div>
    `;
    return card;
}

// View sede details
async function viewSedeDetails(sedeId) {
    currentSedeId = sedeId;
    
    try {
        showLoading();
        const data = await api.getSedeDetails(sedeId);
        
        if (data) {
            showSedeDetailsModal(data);
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar detalles de la sede: ' + error.message);
    }
}

// Show sede details modal
function showSedeDetailsModal(data) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-building"></i> ${data.sede.nombre}</h3>
                <button onclick="closeSedeModal()" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <div class="sede-info">
                    <p><strong>Dirección:</strong> ${data.sede.direccion || 'No disponible'}</p>
                    <p><strong>Teléfono:</strong> ${data.sede.telefono || 'No disponible'}</p>
                    <p><strong>Email:</strong> ${data.sede.email || 'No disponible'}</p>
                </div>
                
                <h4><i class="fas fa-calendar-alt"></i> Cortes</h4>
                <div class="cortes-grid">
                    ${data.cortes.map(corte => createCorteCard(corte)).join('')}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Create corte card for modal
function createCorteCard(corte) {
    return `
        <div class="card corte-card">
            <div class="card-header">
                <h5>${corte.nombre}</h5>
                <span class="badge badge-${corte.tipo_ruta === 'avanzada' ? 'success' : 'info'}">
                    ${corte.tipo_ruta === 'avanzada' ? 'Avanzada' : 'Básica'}
                </span>
            </div>
            <div class="card-body">
                <p class="text-muted">
                    <i class="fas fa-calendar"></i> ${formatDate(corte.fecha_inicio)} - ${formatDate(corte.fecha_fin)}
                </p>
                <div class="metrics-mini">
                    <div class="metric-mini">
                        <span class="metric-label">Total:</span>
                        <span class="metric-value">${corte.total_couders}</span>
                    </div>
                    <div class="metric-mini">
                        <span class="metric-label">Activos:</span>
                        <span class="metric-value text-success">${corte.activos}</span>
                    </div>
                    <div class="metric-mini">
                        <span class="metric-label">Retirados:</span>
                        <span class="metric-value text-warning">${corte.retirados}</span>
                    </div>
                    <div class="metric-mini">
                        <span class="metric-label">Completados:</span>
                        <span class="metric-value text-info">${corte.completados}</span>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${corte.porcentaje_atendidos}%"></div>
                </div>
                <button onclick="viewCorteDetails(${corte.id})" class="btn btn-primary btn-sm mt-2">
                    <i class="fas fa-users"></i> Ver Clanes
                </button>
            </div>
        </div>
    `;
}

// View corte details
async function viewCorteDetails(corteId) {
    currentCorteId = corteId;
    
    try {
        showLoading();
        const data = await api.getCorteDetails(corteId);
        
        if (data) {
            closeSedeModal();
            showCorteDetailsModal(data);
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar detalles del corte: ' + error.message);
    }
}

// Show corte details modal
function showCorteDetailsModal(data) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content large">
            <div class="modal-header">
                <h3><i class="fas fa-calendar-alt"></i> ${data.corte.nombre}</h3>
                <button onclick="closeCorteModal()" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <div class="corte-info">
                    <p><strong>Tipo de Ruta:</strong> 
                        <span class="badge badge-${data.corte.tipo_ruta === 'avanzada' ? 'success' : 'info'}">
                            ${data.corte.tipo_ruta === 'avanzada' ? 'Avanzada' : 'Básica'}
                        </span>
                    </p>
                    <p><strong>Periodo:</strong> ${formatDate(data.corte.fecha_inicio)} - ${formatDate(data.corte.fecha_fin)}</p>
                </div>
                
                <div class="clanes-section">
                    <h4><i class="fas fa-sun"></i> Clanes - Jornada AM</h4>
                    <div class="clanes-grid">
                        ${data.clanes_am.length > 0 ? 
                            data.clanes_am.map(clan => createClanCard(clan, 'AM')).join('') :
                            '<p class="text-muted">No hay clanes en jornada AM</p>'
                        }
                    </div>
                </div>
                
                <div class="clanes-section">
                    <h4><i class="fas fa-moon"></i> Clanes - Jornada PM</h4>
                    <div class="clanes-grid">
                        ${data.clanes_pm.length > 0 ? 
                            data.clanes_pm.map(clan => createClanCard(clan, 'PM')).join('') :
                            '<p class="text-muted">No hay clanes en jornada PM</p>'
                        }
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Create clan card
function createClanCard(clan, jornada) {
    const occupationRate = clan.total_couders > 0 ? 
        Math.round((clan.total_couders / clan.capacidad_maxima) * 100) : 0;
    
    return `
        <div class="card clan-card">
            <div class="card-header">
                <h5>${clan.nombre}</h5>
                <span class="badge badge-secondary">${jornada}</span>
            </div>
            <div class="card-body">
                <div class="capacity-info">
                    <span class="occupation-rate">${occupationRate}% ocupado</span>
                    <span class="capacity-text">${clan.total_couders}/${clan.capacidad_maxima}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${occupationRate}%"></div>
                </div>
                <div class="metrics-mini">
                    <div class="metric-mini">
                        <span class="metric-label">Activos:</span>
                        <span class="metric-value text-success">${clan.activos}</span>
                    </div>
                    <div class="metric-mini">
                        <span class="metric-label">Retirados:</span>
                        <span class="metric-value text-warning">${clan.retirados}</span>
                    </div>
                    <div class="metric-mini">
                        <span class="metric-label">Completados:</span>
                        <span class="metric-value text-info">${clan.completados}</span>
                    </div>
                </div>
                <button onclick="viewClanDetails(${clan.id})" class="btn btn-primary btn-sm mt-2">
                    <i class="fas fa-user-friends"></i> Ver Couders
                </button>
            </div>
        </div>
    `;
}

// View clan details
async function viewClanDetails(clanId) {
    currentClanId = clanId;
    
    try {
        showLoading();
        const data = await api.getClanDetails(clanId);
        
        if (data) {
            closeCorteModal();
            showClanDetailsModal(data);
        }
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error al cargar detalles del clan: ' + error.message);
    }
}

// Show clan details modal
function showClanDetailsModal(data) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-users"></i> ${data.clan.nombre}</h3>
                <button onclick="closeClanModal()" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <div class="clan-info">
                    <p><strong>Jornada:</strong> <span class="badge badge-secondary">${data.clan.jornada}</span></p>
                    <p><strong>Capacidad Máxima:</strong> ${data.clan.capacidad_maxima} couders</p>
                </div>
                
                <h4><i class="fas fa-chart-pie"></i> Métricas del Clan</h4>
                <div class="clan-metrics">
                    <div class="metric-card">
                        <div class="metric-icon blue">
                            <i class="fas fa-users"></i>
                        </div>
                        <div class="metric-content">
                            <h3>${data.metricas.total_couders}</h3>
                            <p>Total Couders</p>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon green">
                            <i class="fas fa-user-check"></i>
                        </div>
                        <div class="metric-content">
                            <h3>${data.metricas.activos}</h3>
                            <p>Activos</p>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon orange">
                            <i class="fas fa-user-times"></i>
                        </div>
                        <div class="metric-content">
                            <h3>${data.metricas.retirados}</h3>
                            <p>Retirados</p>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon purple">
                            <i class="fas fa-graduation-cap"></i>
                        </div>
                        <div class="metric-content">
                            <h3>${data.metricas.completados}</h3>
                            <p>Completados</p>
                        </div>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button onclick="closeClanModal()" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Volver
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Modal close functions
function closeSedeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

function closeCorteModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

function closeClanModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

// Add styles for dashboard components
const dashboardStyles = document.createElement('style');
dashboardStyles.textContent = `
    .metrics-mini {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .metric-mini {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.25rem 0;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #666;
    }
    
    .metric-value {
        font-weight: 600;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        transition: width 0.3s ease;
    }
    
    .cortes-grid, .clanes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .corte-card, .clan-card {
        margin-bottom: 0;
    }
    
    .capacity-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .occupation-rate {
        font-weight: 600;
        color: #667eea;
    }
    
    .capacity-text {
        font-size: 0.8rem;
        color: #666;
    }
    
    .clanes-section {
        margin-top: 2rem;
    }
    
    .clan-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .modal-content.large {
        max-width: 900px;
        width: 95%;
    }
    
    .modal-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    
    .btn-sm {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
    }
    
    .text-success { color: #28a745; }
    .text-warning { color: #ffc107; }
    .text-info { color: #17a2b8; }
    .text-danger { color: #dc3545; }
`;
document.head.appendChild(dashboardStyles);
