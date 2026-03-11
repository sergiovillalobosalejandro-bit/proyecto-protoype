// Authentication functions

// Check if user is authenticated
async function checkAuth() {
    if (!authToken) {
        showLoginForm();
        return false;
    }

    try {
        const user = await api.getCurrentUser();
        if (user) {
            return true;
        } else {
            showLoginForm();
            return false;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        showLoginForm();
        return false;
    }
}

// Show login form
function showLoginForm() {
    const loginHtml = `
        <div class="login-container">
            <div class="login-card">
                <div class="login-header">
                    <h2><i class="fas fa-heartbeat"></i> Sistema de Intervenciones Clínicas</h2>
                    <p>Iniciar sesión</p>
                </div>
                <form id="login-form" onsubmit="handleLogin(event)">
                    <div class="form-group">
                        <label for="username">Usuario:</label>
                        <input type="text" id="username" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Contraseña:</label>
                        <input type="password" id="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary full-width">
                        <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                    </button>
                </form>
                <div id="login-error" class="error-message hidden"></div>
            </div>
        </div>
    `;

    // Replace entire app content with login form
    document.getElementById('app').innerHTML = loginHtml;

    // Add login styles
    const loginStyles = document.createElement('style');
    loginStyles.textContent = `
        .login-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
        }
        
        .login-card {
            background: white;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-header h2 {
            color: #333;
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }
        
        .login-header p {
            color: #666;
            margin: 0;
        }
        
        .login-header i {
            color: #667eea;
            margin-right: 0.5rem;
        }
        
        .full-width {
            width: 100%;
            justify-content: center;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 0.75rem;
            border-radius: 5px;
            margin-top: 1rem;
            text-align: center;
            font-size: 0.9rem;
        }
        
        .error-message.hidden {
            display: none;
        }
    `;
    document.head.appendChild(loginStyles);
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    
    showLoading();
    
    try {
        const response = await api.login(username, password);
        
        if (response) {
            hideLoading();
            // Reload the page to show the main app
            location.reload();
        } else {
            hideLoading();
            errorDiv.textContent = 'Credenciales incorrectas';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        hideLoading();
        errorDiv.textContent = error.message || 'Error al iniciar sesión';
        errorDiv.classList.remove('hidden');
    }
}

// Logout function
async function logout() {
    try {
        // Clear local storage
        localStorage.removeItem('authToken');
        authToken = null;
        currentUser = null;
        
        // Clear API client token
        api.token = null;
        
        // Show login form
        showLoginForm();
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Initialize authentication
async function initAuth() {
    const isAuthenticated = await checkAuth();
    if (isAuthenticated) {
        // Load main app content
        await loadMainApp();
    }
}

// Load main app after successful authentication
async function loadMainApp() {
    // The main app is already in the HTML, just make it visible
    document.getElementById('app').style.display = 'block';
    
    // Initialize dashboard
    if (typeof loadDashboard === 'function') {
        await loadDashboard();
    }
}
