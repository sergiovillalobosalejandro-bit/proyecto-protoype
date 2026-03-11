// Configuration for frontend
const CONFIG = {
    API_BASE_URL: process.env.API_URL || 'http://localhost:8000/api',
    APP_NAME: 'Sistema de Intervenciones Clínicas',
    VERSION: '1.0.0'
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
}
