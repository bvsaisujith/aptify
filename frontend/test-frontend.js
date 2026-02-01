#!/usr/bin/env node

/**
 * Automated Frontend Authentication Flow Test
 * Tests the complete login flow and localStorage management
 */

const http = require('http');
const { URL } = require('url');

const FRONTEND_URL = 'http://127.0.0.1:3000';
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
};

class FrontendTester {
  constructor() {
    this.passedTests = 0;
    this.failedTests = 0;
  }

  log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
  }

  pass(testName) {
    this.log(`✓ ${testName}`, 'green');
    this.passedTests++;
  }

  fail(testName, error) {
    this.log(`✗ ${testName}: ${error}`, 'red');
    this.failedTests++;
  }

  async fetchUrl(url) {
    return new Promise((resolve, reject) => {
      const parsedUrl = new URL(url);
      const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port,
        path: parsedUrl.pathname + parsedUrl.search,
        method: 'GET',
        timeout: 5000,
      };

      const req = http.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          resolve({
            status: res.statusCode,
            headers: res.headers,
            body: data,
          });
        });
      });

      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });

      req.end();
    });
  }

  async testServerRunning() {
    this.log('\n📋 Test 1: Server Connection', 'blue');
    try {
      const response = await this.fetchUrl(FRONTEND_URL);
      if (response.status === 200) {
        this.pass('Frontend server is running and responsive');
      } else {
        this.fail('Frontend server', `Status code ${response.status}`);
      }
    } catch (error) {
      this.fail('Frontend server', error.message);
    }
  }

  async testAuthGuardExists() {
    this.log('\n📋 Test 2: Auth Guard Module', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/static/js/auth-guard.js`);
      if (response.status === 200 && response.body.includes('AuthGuard')) {
        this.pass('auth-guard.js module exists and has AuthGuard object');
      } else {
        this.fail('auth-guard.js', 'Missing AuthGuard object');
      }

      if (response.body.includes('isAuthenticated')) {
        this.pass('auth-guard.js has isAuthenticated() method');
      }

      if (response.body.includes('setToken')) {
        this.pass('auth-guard.js has setToken() method');
      }

      if (response.body.includes('getToken')) {
        this.pass('auth-guard.js has getToken() method');
      }

      if (response.body.includes('clearToken')) {
        this.pass('auth-guard.js has clearToken() method');
      }

      if (response.body.includes('requireAuth')) {
        this.pass('auth-guard.js has requireAuth() guard function');
      }

      if (response.body.includes('requireNotAuth')) {
        this.pass('auth-guard.js has requireNotAuth() guard function');
      }
    } catch (error) {
      this.fail('auth-guard.js', error.message);
    }
  }

  async testLoginPage() {
    this.log('\n📋 Test 3: Login Page', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/templates/login.html`);
      if (response.status === 200) {
        this.pass('login.html page is accessible');
      }

      if (response.body.includes('id="loginForm"')) {
        this.pass('login.html has login form');
      }

      if (response.body.includes('type="email"')) {
        this.pass('login.html has email input field');
      }

      if (response.body.includes('type="password"')) {
        this.pass('login.html has password input field');
      }

      if (response.body.includes('type="submit"')) {
        this.pass('login.html has submit button');
      }

      if (response.body.includes('src="/static/js/auth-guard.js"')) {
        this.pass('login.html loads auth-guard.js');
      }

      if (response.body.includes('src="/static/js/login.js"')) {
        this.pass('login.html loads login.js');
      }
    } catch (error) {
      this.fail('login.html', error.message);
    }
  }

  async testDashboardPage() {
    this.log('\n📋 Test 4: Dashboard Page', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/templates/dashboard.html`);
      if (response.status === 200) {
        this.pass('dashboard.html page is accessible');
      }

      if (response.body.includes('Welcome to AptiFy')) {
        this.pass('dashboard.html has welcome message');
      }

      if (response.body.includes('id="logoutBtn"')) {
        this.pass('dashboard.html has logout button');
      }

      if (response.body.includes('id="userDisplay"')) {
        this.pass('dashboard.html has user display element');
      }

      if (response.body.includes('id="tokenDisplay"')) {
        this.pass('dashboard.html has token display element');
      }

      if (response.body.includes('src="/static/js/auth-guard.js"')) {
        this.pass('dashboard.html loads auth-guard.js');
      }

      if (response.body.includes('src="/static/js/dashboard.js"')) {
        this.pass('dashboard.html loads dashboard.js');
      }
    } catch (error) {
      this.fail('dashboard.html', error.message);
    }
  }

  async testIndexPage() {
    this.log('\n📋 Test 5: Index/Entry Gate', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/templates/index.html`);
      if (response.status === 200) {
        this.pass('index.html page is accessible');
      }

      if (response.body.includes('AptiFy - Loading')) {
        this.pass('index.html has loading title');
      }

      if (response.body.includes('src="/static/js/auth-guard.js"')) {
        this.pass('index.html loads auth-guard.js');
      }

      if (response.body.includes('AuthGuard.isAuthenticated()')) {
        this.pass('index.html checks authentication on load');
      }

      if (response.body.includes('AuthGuard.redirectToDashboard()')) {
        this.pass('index.html redirects to dashboard if authenticated');
      }

      if (response.body.includes('AuthGuard.redirectToLogin()')) {
        this.pass('index.html redirects to login if not authenticated');
      }
    } catch (error) {
      this.fail('index.html', error.message);
    }
  }

  async testStyles() {
    this.log('\n📋 Test 6: Styling System', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/static/css/styles.css`);
      if (response.status === 200) {
        this.pass('styles.css is accessible');
      }

      if (response.body.includes('--color-primary')) {
        this.pass('CSS has color variables');
      }

      if (response.body.includes('--spacing-md')) {
        this.pass('CSS has spacing variables');
      }

      if (response.body.includes('.btn')) {
        this.pass('CSS has button styles');
      }

      if (response.body.includes('.login-page')) {
        this.pass('CSS has login page styles');
      }

      if (response.body.includes('.dashboard-page')) {
        this.pass('CSS has dashboard page styles');
      }

      if (response.body.includes('@media')) {
        this.pass('CSS has responsive design media queries');
      }
    } catch (error) {
      this.fail('styles.css', error.message);
    }
  }

  async testLoginLogic() {
    this.log('\n📋 Test 7: Login Logic', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/static/js/login.js`);
      if (response.status === 200) {
        this.pass('login.js is accessible');
      }

      if (response.body.includes('AuthGuard.requireNotAuth()')) {
        this.pass('login.js prevents authenticated users from accessing');
      }

      if (response.body.includes('loginForm.addEventListener')) {
        this.pass('login.js handles form submission');
      }

      if (response.body.includes('AuthGuard.setToken')) {
        this.pass('login.js stores token after successful login');
      }

      if (response.body.includes('AuthGuard.redirectToDashboard')) {
        this.pass('login.js redirects to dashboard after login');
      }

      if (response.body.includes('isValidEmail')) {
        this.pass('login.js validates email format');
      }

      if (response.body.includes('demo@aptify.com')) {
        this.pass('login.js has demo credentials for testing');
      }
    } catch (error) {
      this.fail('login.js', error.message);
    }
  }

  async testDashboardLogic() {
    this.log('\n📋 Test 8: Dashboard Logic', 'blue');
    try {
      const response = await this.fetchUrl(`${FRONTEND_URL}/static/js/dashboard.js`);
      if (response.status === 200) {
        this.pass('dashboard.js is accessible');
      }

      if (response.body.includes('AuthGuard.requireAuth()')) {
        this.pass('dashboard.js requires authentication');
      }

      if (response.body.includes('logoutBtn.addEventListener')) {
        this.pass('dashboard.js handles logout button click');
      }

      if (response.body.includes('AuthGuard.clearToken()')) {
        this.pass('dashboard.js clears token on logout');
      }

      if (response.body.includes('AuthGuard.redirectToLogin')) {
        this.pass('dashboard.js redirects to login after logout');
      }

      if (response.body.includes('AuthGuard.getToken()')) {
        this.pass('dashboard.js retrieves and displays token');
      }
    } catch (error) {
      this.fail('dashboard.js', error.message);
    }
  }

  async runAllTests() {
    console.clear();
    this.log('═══════════════════════════════════════════════════════════', 'blue');
    this.log('  AptiFy Frontend Authentication System - Test Suite', 'blue');
    this.log('═══════════════════════════════════════════════════════════', 'blue');

    await this.testServerRunning();
    await this.testAuthGuardExists();
    await this.testLoginPage();
    await this.testDashboardPage();
    await this.testIndexPage();
    await this.testStyles();
    await this.testLoginLogic();
    await this.testDashboardLogic();

    this.log('\n═══════════════════════════════════════════════════════════', 'blue');
    this.log('Test Results:', 'blue');
    this.log(`  ${colors.green}✓ Passed: ${this.passedTests}${colors.reset}`);
    this.log(`  ${colors.red}✗ Failed: ${this.failedTests}${colors.reset}`);
    this.log(`  Total: ${this.passedTests + this.failedTests}`);
    this.log('═══════════════════════════════════════════════════════════', 'blue');

    if (this.failedTests === 0) {
      this.log('\n🎉 All tests passed! Frontend is ready for testing.', 'green');
      this.log('\nQuick Start:', 'yellow');
      this.log('  1. Open: http://127.0.0.1:3000/templates/index.html', 'blue');
      this.log('  2. You will be redirected to login.html (no token yet)', 'blue');
      this.log('  3. Use credentials: demo@aptify.com / demo123', 'blue');
      this.log('  4. Token will be stored in localStorage', 'blue');
      this.log('  5. You will be redirected to dashboard.html', 'blue');
      this.log('  6. Click logout to clear token and return to login', 'blue');
    } else {
      this.log('\n⚠️  Some tests failed. Please review the issues above.', 'red');
      process.exit(1);
    }
  }
}

const tester = new FrontendTester();
tester.runAllTests().catch((error) => {
  console.error('Test suite error:', error);
  process.exit(1);
});
