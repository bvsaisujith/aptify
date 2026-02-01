/**
 * Landing Page JavaScript
 * Handles navigation, animations, and interactions
 */

document.addEventListener('DOMContentLoaded', function() {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add scroll animation to feature cards
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe all feature cards and benefit items
  document.querySelectorAll('.feature-card, .benefit-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
  });

  // Handle navbar scroll effect
  let lastScrollTop = 0;
  const navbar = document.querySelector('.landing-navbar');

  window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > 50) {
      navbar.style.boxShadow = '0 5px 20px rgba(102, 126, 234, 0.3)';
    } else {
      navbar.style.boxShadow = '0 2px 10px rgba(102, 126, 234, 0.2)';
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  });

  // Mobile menu toggle (if needed for responsive nav)
  handleMobileNav();
});

/**
 * Handle mobile navigation
 */
function handleMobileNav() {
  const viewport = window.innerWidth;

  if (viewport <= 768) {
    const navbarLinks = document.querySelector('.navbar-links');
    if (navbarLinks) {
      // Adjust for mobile if needed
      navbarLinks.style.maxHeight = 'calc(100vh - 60px)';
    }
  }
}

/**
 * Track user interactions
 */
function trackEvent(eventName, eventData = {}) {
  console.log(`Event: ${eventName}`, eventData);
  // Can be integrated with analytics service later
  // Example: Google Analytics, Mixpanel, etc.
}

/**
 * Log CTA clicks
 */
document.querySelectorAll('a[href="/login/"]').forEach(link => {
  link.addEventListener('click', () => {
    trackEvent('cta_click', {
      location: link.parentElement.className,
      text: link.textContent
    });
  });
});

/**
 * Handle feature card hover effects
 */
document.querySelectorAll('.feature-card').forEach(card => {
  card.addEventListener('mouseenter', function() {
    this.style.zIndex = '10';
  });

  card.addEventListener('mouseleave', function() {
    this.style.zIndex = '1';
  });
});

/**
 * Responsive navbar adjustments
 */
window.addEventListener('resize', handleMobileNav);

console.log('Landing page initialized successfully');
