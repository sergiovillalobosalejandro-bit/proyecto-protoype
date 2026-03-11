// API Configuration
import { CONFIG } from './config.js';
const API_BASE_URL = CONFIG.API_BASE_URL;

// Global state
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// API Client
class ApiClient {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.token = authToken;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                // Token expired or invalid
                logout();
                return null;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await this.request('/auth/login', {
            method: 'POST',
            body: formData,
            headers: {} // Don't set Content-Type for FormData
        });

        if (response) {
            this.token = response.access_token;
            localStorage.setItem('authToken', this.token);
            await this.getCurrentUser();
        }

        return response;
    }

    async register(userData) {
        return await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getCurrentUser() {
        const user = await this.request('/auth/me');
        if (user) {
            currentUser = user;
        }
        return user;
    }

    // Couders
    async searchCouderByCC(cc) {
        return await this.request(`/couders/search/${cc}`);
    }

    async getCouders(params = {}) {
        const query = new URLSearchParams(params).toString();
        return await this.request(`/couders?${query}`);
    }

    async createCouder(couderData) {
        return await this.request('/couders', {
            method: 'POST',
            body: JSON.stringify(couderData)
        });
    }

    async updateCouder(couderId, couderData) {
        return await this.request(`/couders/${couderId}`, {
            method: 'PUT',
            body: JSON.stringify(couderData)
        });
    }

    // Interventions
    async getInterventionsByCouder(couderId, params = {}) {
        const query = new URLSearchParams(params).toString();
        return await this.request(`/intervenciones/couder/${couderId}?${query}`);
    }

    async createIntervention(interventionData) {
        return await this.request('/intervenciones', {
            method: 'POST',
            body: JSON.stringify(interventionData)
        });
    }

    async updateIntervention(interventionId, interventionData) {
        return await this.request(`/intervenciones/${interventionId}`, {
            method: 'PUT',
            body: JSON.stringify(interventionData)
        });
    }

    async deleteIntervention(interventionId) {
        return await this.request(`/intervenciones/${interventionId}`, {
            method: 'DELETE'
        });
    }

    async getClinicalHistory(couderId, params = {}) {
        const query = new URLSearchParams(params).toString();
        return await this.request(`/intervenciones/clinical-history/${couderId}?${query}`);
    }

    // Dashboard
    async getDashboardOverview() {
        return await this.request('/dashboard/overview');
    }

    async getSedeDetails(sedeId) {
        return await this.request(`/dashboard/sedes/${sedeId}`);
    }

    async getCorteDetails(corteId) {
        return await this.request(`/dashboard/cortes/${corteId}`);
    }

    async getClanDetails(clanId) {
        return await this.request(`/dashboard/clanes/${clanId}`);
    }

    // AI Services
    async synthesizeInterventions(couderId, interventionIds) {
        return await this.request(`/ai/synthesize/${couderId}`, {
            method: 'POST',
            body: JSON.stringify(interventionIds)
        });
    }

    async generateDiagnosis(couderId, interventionIds) {
        return await this.request(`/ai/diagnose/${couderId}`, {
            method: 'POST',
            body: JSON.stringify(interventionIds)
        });
    }

    async getHistoricalAnalyses(couderId, analysisType = null) {
        const query = analysisType ? `?analysis_type=${analysisType}` : '';
        return await this.request(`/ai/analyses/${couderId}${query}`);
    }

    async getSpecificAnalysis(analysisId) {
        return await this.request(`/ai/analysis/${analysisId}`);
    }

    async deleteAnalysis(analysisId) {
        return await this.request(`/ai/analysis/${analysisId}`, {
            method: 'DELETE'
        });
    }

    // Audio Services
    async uploadAudio(couderId, usuarioId, file, metadata = {}) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('couder_id', couderId);
        formData.append('usuario_id', usuarioId);
        
        if (metadata.titulo) formData.append('titulo', metadata.titulo);
        if (metadata.descripcion) formData.append('descripcion', metadata.descripcion);
        if (metadata.intervencion_id) formData.append('intervencion_id', metadata.intervencion_id);

        const response = await fetch(`${this.baseURL}/audio/upload`, {
            method: 'POST',
            headers: this.token ? { 'Authorization': `Bearer ${this.token}` } : {},
            body: formData
        });

        if (response.status === 401) {
            logout();
            return null;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Upload failed');
        }

        return data;
    }

    async getAudioByCouder(couderId, limit = 50) {
        return await this.request(`/audio/couder/${couderId}?limit=${limit}`);
    }

    async downloadAudio(recordingId) {
        const url = `${this.baseURL}/audio/${recordingId}/download`;
        const config = {
            headers: {}
        };

        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                logout();
                return null;
            }

            if (!response.ok) {
                throw new Error('Download failed');
            }

            return response.blob();
        } catch (error) {
            console.error('Audio download error:', error);
            throw error;
        }
    }

    async transcribeAudio(recordingId) {
        return await this.request(`/audio/${recordingId}/transcribe`, {
            method: 'POST'
        });
    }

    async deleteAudio(recordingId) {
        return await this.request(`/audio/${recordingId}`, {
            method: 'DELETE'
        });
    }
}

// Global API client instance
const api = new ApiClient();

// Utility functions
function showLoading() {
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function showError(message) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'toast toast-error';
    toast.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

function showSuccess(message) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'toast toast-success';
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 3000);
}

function formatDate(dateString) {
    if (!dateString) return 'No disponible';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Add toast styles to head
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 3000;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .toast-success {
        background: linear-gradient(135deg, #28a745, #20c997);
    }
    
    .toast-error {
        background: linear-gradient(135deg, #dc3545, #c82333);
    }
    
    .toast button {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        margin-left: auto;
        padding: 0;
    }
    
    .toast button:hover {
        opacity: 0.8;
    }
`;
document.head.appendChild(toastStyles);
