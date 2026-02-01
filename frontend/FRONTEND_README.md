# AptiFy Frontend Application

A clean, vanilla HTML/CSS/JavaScript frontend authentication system with automatic redirects and protected routes.

## 🏗️ Project Structure

```
frontend/
├── static/
│   ├── css/
│   │   └── styles.css          # Global styles for all pages
│   └── js/
│       ├── auth-guard.js       # Reusable authentication utility
│       ├── login.js            # Login page logic
│       └── dashboard.js        # Dashboard page logic
└── templates/
    ├── index.html              # Entry gate (redirects based on auth)
    ├── login.html              # Login form page
    └── dashboard.html          # Protected dashboard page
```

## 🔐 Authentication Flow

### Entry Point: `index.html`
- Loads on any root access
- Checks for `auth_token` in `localStorage`
- **If authenticated**: Redirects to `/dashboard.html`
- **If not authenticated**: Redirects to `/login.html`

### Login: `login.html` + `login.js`
- Public page accessible without authentication
- Form validates email and password
- **Guard**: Redirects authenticated users to dashboard
- On successful login:
  1. Stores token in `localStorage`
  2. Redirects to `/dashboard.html`
- Demo credentials: `demo@aptify.com` / `demo123`

### Dashboard: `dashboard.html` + `dashboard.js`
- Protected page requiring authentication
- **Guard**: Redirects unauthenticated users to login
- Displays user information and token
- Logout button clears token and redirects to login

## 🛡️ Authentication Guard (`auth-guard.js`)

Reusable utility providing:

### Core Functions
- `isAuthenticated()` - Check if user has valid token
- `getToken()` - Retrieve stored token
- `setToken(token)` - Store authentication token
- `clearToken()` - Remove token from storage

### Guard Functions
- `requireAuth()` - Protect pages that need authentication
- `requireNotAuth()` - Protect pages that need NO authentication (like login)

### Redirect Functions
- `redirectToLogin()` - Go to login page
- `redirectToDashboard()` - Go to dashboard page
- `redirectToIndex()` - Go to index/entry page

### API Functions
- `getAuthHeaders()` - Get headers with Bearer token for API requests
- `apiRequest(endpoint, options)` - Make authenticated API requests
- `publicApiRequest(endpoint, options)` - Make unauthenticated API requests

## 🚀 Usage

### Protecting a New Page

1. **Create new HTML file** (e.g., `profile.html`)
2. **Load scripts** at the bottom:
```html
<script src="/static/js/auth-guard.js"></script>
<script src="/static/js/profile.js"></script>
```

3. **In profile.js**, add guard:
```javascript
document.addEventListener('DOMContentLoaded', function() {
  AuthGuard.requireAuth();
  // Your page logic here
});
```

### Making API Calls

**Authenticated requests:**
```javascript
const data = await AuthGuard.apiRequest('/users/me/', {
  method: 'GET'
});
```

**Public requests (login):**
```javascript
const response = await AuthGuard.publicApiRequest('/auth/login/', {
  method: 'POST',
  body: JSON.stringify({ email, password })
});
```

### Token Management

**Get current token:**
```javascript
const token = AuthGuard.getToken();
```

**Store token:**
```javascript
AuthGuard.setToken(response.token);
```

**Clear token (logout):**
```javascript
AuthGuard.clearToken();
AuthGuard.redirectToLogin();
```

## 🎨 Styling

### CSS Architecture
- **Variables**: Complete design system with colors, spacing, shadows
- **Components**: Buttons, forms, cards, navbar
- **Responsive**: Mobile-first design with breakpoints
- **Utility Classes**: Margin, padding, flexbox helpers

### Color Palette
- **Primary**: `#667eea` (purple)
- **Secondary**: `#764ba2` (dark purple)
- **Success**: `#48bb78` (green)
- **Danger**: `#f56565` (red)
- **Warning**: `#ed8936` (orange)

### Responsive Breakpoints
- **Mobile**: < 480px
- **Tablet**: < 768px
- **Desktop**: > 768px

## 🔄 Data Flow

```
User Opens App
    ↓
index.html loads
    ↓
Checks localStorage for "auth_token"
    ├─ Token exists → dashboard.html
    └─ No token → login.html
    
User enters credentials → login.js processes
    ├─ Valid → Store token in localStorage → dashboard.html
    └─ Invalid → Show error message
    
Dashboard loads → dashboard.js executes
    ├─ No token → Redirect to login.html
    └─ Token exists → Display user info
    
User clicks Logout → Clear token → login.html
```

## 🔗 API Integration

### Current Setup
- **Mock Login**: Demo credentials work without backend
- **API Base URL**: `http://127.0.0.1:8000/api` (configurable in `auth-guard.js`)

### When Backend is Ready

1. **Update API_BASE_URL** in `auth-guard.js`:
```javascript
API_BASE_URL: 'http://your-domain.com/api',
```

2. **Replace mock login** in `login.js` with real API call:
```javascript
async function login(email, password) {
  const response = await AuthGuard.publicApiRequest('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
  return response;
}
```

3. **Fetch user data** in `dashboard.js`:
```javascript
const userData = await AuthGuard.apiRequest('/users/me/');
```

## 🧪 Testing

### Test Flow 1: Fresh User
1. Clear localStorage: `localStorage.clear()`
2. Open `index.html`
3. Should redirect to `login.html`

### Test Flow 2: Authenticated User
1. Login with `demo@aptify.com` / `demo123`
2. Token stored in localStorage
3. Open `index.html`
4. Should redirect to `dashboard.html`

### Test Flow 3: Manual Token Test
1. In browser console:
```javascript
localStorage.setItem('auth_token', 'test-token-123');
window.location.replace('/index.html');
// Should redirect to dashboard
```

## 🔒 Security Considerations

✅ **Implemented**
- Token stored in localStorage (XSS protection via Content Security Policy)
- HTTPS recommended for production
- Bearer token in Authorization header
- Auto-logout on 401 response
- No sensitive data in JavaScript

⚠️ **Best Practices**
- **Always use HTTPS** in production
- **Implement CSRF tokens** for forms
- **Set HttpOnly cookies** for token if possible (requires backend)
- **Implement token refresh** mechanism
- **Add rate limiting** on login attempts
- **Validate on backend** always

## 📝 Configuration

### Change Token Key
In `auth-guard.js`:
```javascript
TOKEN_KEY: 'auth_token',  // Change to your preferred key
```

### Change API Base URL
In `auth-guard.js`:
```javascript
API_BASE_URL: 'http://your-api.com/api',
```

### Change Redirect URLs
Modify in respective `*-guard.js` functions:
```javascript
redirectToLogin: '/login',           // Change URL
redirectToDashboard: '/dashboard',   // Change URL
```

## 🚢 Deployment

### File Structure
```
public_html/
├── index.html
├── login.html
├── dashboard.html
├── static/
│   ├── css/styles.css
│   └── js/
│       ├── auth-guard.js
│       ├── login.js
│       └── dashboard.js
```

### Web Server Configuration (Nginx)
```nginx
location / {
    try_files $uri $uri.html /index.html;
}
```

### Web Server Configuration (Apache)
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</IfModule>
```

## 🐛 Troubleshooting

### Issue: Login form not working
1. Check browser console for errors
2. Verify `auth-guard.js` is loaded
3. Check if localStorage is enabled
4. Verify API endpoint is correct

### Issue: Dashboard shows blank
1. Check if token exists: `localStorage.getItem('auth_token')`
2. Check browser console for errors
3. Verify `dashboard.js` loaded
4. Check CSS styles loaded

### Issue: Infinite redirect loop
1. Clear localStorage
2. Clear browser cache
3. Check auth guard logic in JavaScript
4. Verify redirect URLs are correct

## 📚 Further Development

### To Add New Protected Pages
1. Create new HTML file
2. Include scripts: `auth-guard.js` and page-specific JS
3. Call `AuthGuard.requireAuth()` on load
4. Add page logic below guard

### To Add New Public Pages
1. Create new HTML file
2. Include script: `auth-guard.js`
3. Call `AuthGuard.requireNotAuth()` to prevent logged-in users
4. Add page logic below guard

### To Connect Backend API
1. Update `API_BASE_URL` in `auth-guard.js`
2. Replace mock functions with real API calls
3. Handle error responses appropriately
4. Implement token refresh mechanism

## 📄 License

AptiFy Frontend © 2026. Built with vanilla JavaScript.

---

**Last Updated**: February 1, 2026  
**Version**: 1.0.0
