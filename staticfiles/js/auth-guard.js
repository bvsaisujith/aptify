/**
 * Authentication Guard - Reusable utility for authentication checks and redirects
 * Handles token validation and provides redirect mechanisms
 */

const AuthGuard = {
  /**
   * Storage key for authentication token
   */
  TOKEN_KEY: 'auth_token',

  /**
   * API base URL - configure as needed
   */
  API_BASE_URL: 'http://127.0.0.1:8000/api',

  /**
   * Check if user is authenticated (token exists)
   * @returns {boolean} True if token exists in localStorage
   */
  isAuthenticated() {
    const token = localStorage.getItem(this.TOKEN_KEY);
    return token !== null && token !== '';
  },

  /**
   * Get the stored authentication token
   * @returns {string|null} The stored token or null if not present
   */
  getToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  },

  /**
   * Store authentication token in localStorage
   * @param {string} token - The authentication token to store
   */
  setToken(token) {
    if (token && token.trim() !== '') {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
  },

  /**
   * Remove authentication token from localStorage
   */
  clearToken() {
    localStorage.removeItem(this.TOKEN_KEY);
  },

  /**
   * Get authorization header for API requests
   * @returns {object} Headers object with Authorization header
   */
  getAuthHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.getToken()}`,
    };
  },

  /**
   * Redirect to login page (use for unauthenticated users)
   */
  redirectToLogin() {
    window.location.replace('/login/');
  },

  /**
   * Redirect to dashboard page (use for authenticated users)
   */
  redirectToDashboard() {
    window.location.replace('/dashboard/');
  },

  /**
   * Redirect to index (entry gate)
   */
  redirectToIndex() {
    window.location.replace('/');
  },

  /**
   * Guard function to protect pages that require authentication
   * Call this on protected page load
   */
  requireAuth() {
    if (!this.isAuthenticated()) {
      this.redirectToLogin();
    }
  },

  /**
   * Guard function to protect pages that require NO authentication
   * Call this on public pages like login
   */
  requireNotAuth() {
    if (this.isAuthenticated()) {
      this.redirectToDashboard();
    }
  },

  /**
   * Make an authenticated API request
   * @param {string} endpoint - API endpoint (relative to API_BASE_URL)
   * @param {object} options - Fetch options (method, body, etc.)
   * @returns {Promise} Promise that resolves with the response
   */
  async apiRequest(endpoint, options = {}) {
    const url = `${this.API_BASE_URL}${endpoint}`;
    const config = {
      ...options,
      headers: this.getAuthHeaders(),
    };

    try {
      const response = await fetch(url, config);

      // If unauthorized, clear token and redirect to login
      if (response.status === 401) {
        this.clearToken();
        this.redirectToLogin();
        return null;
      }

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  },

  /**
   * Make an unauthenticated API request (for login, signup, etc.)
   * @param {string} endpoint - API endpoint
   * @param {object} options - Fetch options
   * @returns {Promise} Promise that resolves with the response
   */
  async publicApiRequest(endpoint, options = {}) {
    const url = `${this.API_BASE_URL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  },
};
