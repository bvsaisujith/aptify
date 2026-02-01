/**
 * Dashboard Page Logic
 * Handles authenticated user interactions and data display
 */

document.addEventListener('DOMContentLoaded', function() {
  // Guard: ensure user is authenticated
  AuthGuard.requireAuth();

  const token = AuthGuard.getToken();
  const userDisplay = document.getElementById('userDisplay');
  const welcomeMessage = document.getElementById('welcomeMessage');
  const tokenDisplay = document.getElementById('tokenDisplay');
  const logoutBtn = document.getElementById('logoutBtn');
  const copyTokenBtn = document.getElementById('copyTokenBtn');

  /**
   * Initialize dashboard with user data
   */
  function initializeDashboard() {
    // Parse token to extract user info (if using JWT)
    // For mock token, show generic welcome message
    const userInfo = parseToken(token);

    // Display user greeting
    if (userInfo && userInfo.email) {
      userDisplay.textContent = `👤 ${userInfo.email}`;
      welcomeMessage.textContent = `You're logged in as ${userInfo.email}. Ready to showcase your skills?`;
    } else {
      userDisplay.textContent = '👤 User';
      welcomeMessage.textContent = 'Welcome back! Ready to showcase your skills?';
    }

    // Display token (for debugging purposes)
    const displayToken = token.length > 50 
      ? token.substring(0, 30) + '...' + token.substring(token.length - 10)
      : token;
    tokenDisplay.textContent = displayToken;
  }

  /**
   * Simple JWT token parser (basic implementation)
   * In production, verify token on backend and fetch user data from API
   * @param {string} token - JWT token
   * @returns {object} Decoded token payload or null
   */
  function parseToken(token) {
    try {
      // If token is a mock token, extract basic info
      if (token.startsWith('mock-jwt-token-')) {
        return {
          email: 'user@aptify.com',
          type: 'mock',
        };
      }

      // For real JWT tokens
      const parts = token.split('.');
      if (parts.length !== 3) {
        return null;
      }

      // Decode JWT payload (second part)
      const payload = parts[1];
      const decoded = JSON.parse(atob(payload));
      return decoded;
    } catch (error) {
      console.error('Error parsing token:', error);
      return null;
    }
  }

  /**
   * Handle logout
   */
  logoutBtn.addEventListener('click', function() {
    // Clear authentication token
    AuthGuard.clearToken();

    // Redirect to login
    AuthGuard.redirectToLogin();
  });

  /**
   * Handle token copy to clipboard
   */
  copyTokenBtn.addEventListener('click', function() {
    try {
      navigator.clipboard.writeText(token);
      const originalText = copyTokenBtn.textContent;
      copyTokenBtn.textContent = '✓ Copied!';
      setTimeout(() => {
        copyTokenBtn.textContent = originalText;
      }, 2000);
    } catch (error) {
      console.error('Failed to copy token:', error);
      alert('Failed to copy token');
    }
  });

  /**
   * Fetch user data from API (when backend is ready)
   * Uncomment and modify endpoint when backend provides user API
   */
  async function fetchUserData() {
    try {
      // Example: const userData = await AuthGuard.apiRequest('/users/me/');
      // console.log('User data:', userData);
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      // If 401, user will be redirected by AuthGuard.apiRequest()
    }
  }

  // Initialize dashboard
  initializeDashboard();
  fetchUserData();
});
