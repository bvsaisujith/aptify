/**
 * Login Page Logic
 * Handles user authentication and token storage
 */

document.addEventListener('DOMContentLoaded', function() {
  // Guard: redirect authenticated users away from login
  AuthGuard.requireNotAuth();

  const loginForm = document.getElementById('loginForm');
  const errorMessageDiv = document.getElementById('errorMessage');
  const btnText = document.querySelector('.btn-text');
  const btnLoader = document.querySelector('.btn-loader');
  const submitBtn = loginForm.querySelector('button[type="submit"]');

  /**
   * Show error message to user
   * @param {string} message - Error message to display
   */
  function showError(message) {
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = 'block';
  }

  /**
   * Hide error message
   */
  function hideError() {
    errorMessageDiv.style.display = 'none';
    errorMessageDiv.textContent = '';
  }

  /**
   * Show loading state on submit button
   */
  function setLoading(isLoading) {
    if (isLoading) {
      submitBtn.disabled = true;
      btnText.style.display = 'none';
      btnLoader.style.display = 'block';
    } else {
      submitBtn.disabled = false;
      btnText.style.display = 'inline';
      btnLoader.style.display = 'none';
    }
  }

  /**
   * Handle login form submission
   */
  loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    hideError();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    // Validate inputs
    if (!email || !password) {
      showError('Please enter both email and password.');
      return;
    }

    if (!isValidEmail(email)) {
      showError('Please enter a valid email address.');
      return;
    }

    setLoading(true);

    try {
      /**
       * Mock Login - Replace with actual backend API call
       * In production, this would call: POST /api/auth/login/
       */
      const response = await mockLogin(email, password);

      if (response.success) {
        // Store the authentication token
        AuthGuard.setToken(response.token);

        // Small delay for UX - show success before redirect
        await new Promise(resolve => setTimeout(resolve, 300));

        // Redirect to dashboard
        AuthGuard.redirectToDashboard();
      } else {
        showError(response.message || 'Login failed. Please try again.');
      }
    } catch (error) {
      console.error('Login error:', error);
      showError('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  });

  /**
   * Mock Login Function - Replace with real backend call
   * In production: POST to /api/auth/login/
   */
  async function mockLogin(email, password) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Mock credentials for demo
    if (email === 'demo@aptify.com' && password === 'demo123') {
      return {
        success: true,
        token: 'mock-jwt-token-' + Date.now(),
        user: {
          id: 1,
          email: email,
          username: 'demo_user',
          role: 'candidate',
        },
      };
    }

    // For any other credentials, show error
    return {
      success: false,
      message: 'Invalid email or password. Try demo@aptify.com / demo123',
    };
  }

  /**
   * Simple email validation
   * @param {string} email - Email to validate
   * @returns {boolean} True if valid email format
   */
  function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
});
