/* ============================================
   OMNEXA AI - Global JavaScript
   ============================================ */

// Immediate execution: Move the particles-js container to body root if it exists
// This prevents ancestor CSS transitions/transforms (e.g., AOS) from breaking position: fixed
(function () {
  const particlesContainer = document.getElementById('particles-js');
  if (particlesContainer && particlesContainer.parentElement !== document.body) {
    document.body.insertBefore(particlesContainer, document.body.firstChild);
  }
})();

// Initialize AOS
AOS.init({
  duration: 800,
  once: true,
  offset: 80,
  easing: 'ease-out-cubic'
});

// ============================================
// Ripple Effect for Buttons
// ============================================
function createRipple(event) {
  const button = event.currentTarget;
  const circle = document.createElement('span');
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  circle.style.width = circle.style.height = `${diameter}px`;
  circle.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`;
  circle.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`;
  circle.classList.add('ripple');

  const ripple = button.getElementsByClassName('ripple')[0];
  if (ripple) {
    ripple.remove();
  }

  button.appendChild(circle);
}

// Add ripple effect to all buttons with .btn-ripple class
document.querySelectorAll('.btn-ripple').forEach(button => {
  button.addEventListener('click', createRipple);
});

// ============================================
// Scroll Reveal Animations
// ============================================
const scrollRevealElements = document.querySelectorAll('.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .stagger-item');

const scrollRevealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

scrollRevealElements.forEach(element => {
  scrollRevealObserver.observe(element);
});

// ============================================
// Parallax Effect
// ============================================
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  document.documentElement.style.setProperty('--scroll', scrolled);

  // Parallax for hero section
  const hero = document.querySelector('.hero-section');
  if (hero) {
    const heroContent = hero.querySelector('.hero-content');
    if (heroContent) {
      heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
  }

  // Parallax for floating elements
  document.querySelectorAll('.parallax-slow').forEach(el => {
    el.style.transform = `translateY(${scrolled * 0.2}px)`;
  });

  document.querySelectorAll('.parallax-medium').forEach(el => {
    el.style.transform = `translateY(${scrolled * 0.4}px)`;
  });

  document.querySelectorAll('.parallax-fast').forEach(el => {
    el.style.transform = `translateY(${scrolled * 0.6}px)`;
  });
});

// ============================================
// Mouse Move Effect for Hero
// ============================================
document.querySelector('.hero-section')?.addEventListener('mousemove', (e) => {
  const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
  const moveY = (e.clientY - window.innerHeight / 2) * 0.01;

  const heroContent = document.querySelector('.hero-content');
  if (heroContent) {
    heroContent.style.transform = `translate(${moveX}px, ${moveY}px)`;
  }

  // Move background orbs
  const orbs = document.querySelectorAll('.hero-section::before, .hero-section::after');
  orbs.forEach((orb, index) => {
    const factor = index === 0 ? 0.02 : -0.02;
    orb.style.transform = `translate(${moveX * factor * 100}px, ${moveY * factor * 100}px)`;
  });
});

// ============================================
// 3D Card Tilt Effect
// ============================================
document.querySelectorAll('.card-3d').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
  });
});

// ============================================
// Magnetic Button Effect
// ============================================
document.querySelectorAll('.btn-magnetic').forEach(button => {
  button.addEventListener('mousemove', (e) => {
    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });

  button.addEventListener('mouseleave', () => {
    button.style.transform = 'translate(0, 0)';
  });
});

// ============================================
// Text Gradient Animation on Scroll
// ============================================
const gradientTextElements = document.querySelectorAll('.gradient-text-shimmer');

const gradientTextObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
    } else {
      entry.target.style.animationPlayState = 'paused';
    }
  });
}, { threshold: 0.5 });

gradientTextElements.forEach(element => {
  element.style.animationPlayState = 'paused';
  gradientTextObserver.observe(element);
});

// ============================================
// Counter Animation with Enhanced Effects
// ============================================
function animateCounter(element, target, duration = 2000) {
  let start = 0;
  const increment = target / (duration / 16);
  const timer = setInterval(() => {
    start += increment;
    if (start >= target) {
      element.textContent = target + (element.dataset.suffix || '');
      clearInterval(timer);
      // Add completion animation
      element.style.animation = 'elasticBounce 0.6s ease';
    } else {
      element.textContent = Math.floor(start) + (element.dataset.suffix || '');
    }
  }, 16);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const counter = entry.target;
      const target = parseInt(counter.dataset.target);
      animateCounter(counter, target);
      counterObserver.unobserve(counter);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-number[data-target]').forEach(counter => {
  counterObserver.observe(counter);
});

// ============================================
// Navbar scroll effect
// ============================================
window.addEventListener('scroll', function () {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// ============================================
// Chatbot functionality
// ============================================
const chatbotButton = document.querySelector('.chatbot-button');
const chatbotPopup = document.querySelector('.chatbot-popup');
const chatbotInput = document.querySelector('.chatbot-input-group input');
const chatbotSendBtn = document.querySelector('.chatbot-input-group button');
const chatbotMessages = document.querySelector('.chatbot-messages');

if (chatbotButton) {
  chatbotButton.addEventListener('click', () => {
    chatbotPopup.classList.toggle('active');
  });

  // Close chatbot when clicking outside
  document.addEventListener('click', (e) => {
    if (!chatbotButton.contains(e.target) && !chatbotPopup.contains(e.target)) {
      chatbotPopup.classList.remove('active');
    }
  });
}

// Helper to parse Markdown safely into formatted HTML
function formatMarkdown(text) {
  if (!text) return '';
  if (typeof marked !== 'undefined' && (marked.parse || typeof marked === 'function')) {
    try {
      const parseFn = marked.parse || marked;
      return parseFn(text, { breaks: true, gfm: true });
    } catch (e) {
      console.error('Marked parsing error:', e);
    }
  }

  // Robust fallback markdown parser
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Code blocks (```lang ... ```)
  html = html.replace(/```(?:[a-zA-Z0-9]+)?\n?([\s\S]*?)```/g, function(match, code) {
    return '<pre class="chatbot-code-block"><code>' + code.trim() + '</code></pre>';
  });

  // Inline code (`code`)
  html = html.replace(/`([^`]+)`/g, '<code class="chatbot-inline-code">$1</code>');

  // Bold (**text**)
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Italics (*text*)
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Bullet points
  html = html.replace(/^\s*[-*+]\s+(.*)$/gm, '• $1');

  // Newlines
  html = html.replace(/\n/g, '<br>');

  return html;
}

// Chatbot message handling
function addChatbotMessage(message, isUser = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'chatbot-message';
  if (isUser) {
    messageDiv.style.background = 'var(--gradient-primary)';
    messageDiv.style.color = 'white';
    messageDiv.style.marginLeft = 'auto';
    messageDiv.style.maxWidth = '80%';
    messageDiv.textContent = message;
  } else {
    messageDiv.style.maxWidth = '92%';
    messageDiv.innerHTML = formatMarkdown(message);
  }
  chatbotMessages.appendChild(messageDiv);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

function handleChatbotSubmit() {
  const message = chatbotInput.value.trim();
  if (message) {
    addChatbotMessage(message, true);
    chatbotInput.value = '';

    // Add loading indicator
    const loadingId = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.id = loadingId;
    loadingDiv.className = 'chatbot-message';
    loadingDiv.style.background = '#f1f1f1';
    loadingDiv.style.color = '#333';
    loadingDiv.textContent = 'Typing...';
    chatbotMessages.appendChild(loadingDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    // Get or create session key
    let sessionKey = localStorage.getItem('omnexa_chat_session');
    if (!sessionKey) {
      sessionKey = 'sess_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('omnexa_chat_session', sessionKey);
    }

    // Call actual Django backend API
    fetch('/api/v1/chatbot/message/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_key: sessionKey,
        message: message,
        page_url: window.location.href
      })
    })
    .then(response => response.json())
    .then(data => {
      // Remove loading indicator
      const loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.remove();
      }
      addChatbotMessage(data.reply);
    })
    .catch(error => {
      console.error('Chatbot API Error:', error);
      // Remove loading indicator
      const loadingEl = document.getElementById(loadingId);
      if (loadingEl) {
        loadingEl.remove();
      }
      addChatbotMessage("Sorry, I'm having trouble connecting right now. Please try again later or contact us directly!");
    });
  }
}

if (chatbotSendBtn) {
  chatbotSendBtn.addEventListener('click', handleChatbotSubmit);
}

if (chatbotInput) {
  chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      handleChatbotSubmit();
    }
  });
}

// ============================================
// Smooth scroll for anchor links
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
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

// ============================================
// Form validation and submission
// ============================================
function validateForm(form) {
  let isValid = true;
  const fields = form.querySelectorAll('input, select, textarea');

  // Clear existing errors
  form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
  form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

  fields.forEach(field => {
    let fieldValid = true;
    let errorMsg = '';
    const val = field.value.trim();

    // Check required
    if (field.hasAttribute('required') && !val) {
      fieldValid = false;
      errorMsg = 'This field is required.';
    }

    // Email validation
    if (fieldValid && field.type === 'email' && val) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(val)) {
        fieldValid = false;
        errorMsg = 'Please enter a valid email address.';
      }
    }

    // Phone validation
    if (fieldValid && field.type === 'tel' && val) {
      const digits = val.replace(/\D/g, '');
      const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$/;
      if (!phoneRegex.test(val)) {
        fieldValid = false;
        errorMsg = 'Please enter a valid phone number.';
      } else if (digits.length < 10) {
        fieldValid = false;
        errorMsg = 'Phone number must be at least 10 digits.';
      }
    }

    if (!fieldValid) {
      isValid = false;
      field.classList.add('is-invalid');
      
      const feedback = document.createElement('div');
      feedback.className = 'invalid-feedback';
      feedback.textContent = errorMsg;
      field.after(feedback);
    }
  });

  return isValid;
}

function showFieldErrors(form, errors) {
  // Clear any existing errors first
  form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
  form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

  for (const [field, messages] of Object.entries(errors)) {
    const inputField = form.querySelector(`[name="${field}"]`);
    if (inputField) {
      inputField.classList.add('is-invalid');
      
      const feedback = document.createElement('div');
      feedback.className = 'invalid-feedback';
      feedback.textContent = messages.join(' ');
      inputField.after(feedback);
    }
  }
}

// ============================================
// Contact Form Submission
// ============================================
const bookingForm = document.getElementById('bookingForm');
if (bookingForm) {
  bookingForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (validateForm(this)) {
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
      submitBtn.disabled = true;

      // Get CSRF token
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

      // Prepare form data
      const formData = new FormData(this);
      const data = {};
      formData.forEach((value, key) => {
        data[key] = value;
      });

      try {
        const response = await fetch('/api/v1/contact/book/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.success) {
          submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Booking Confirmed!';
          submitBtn.style.background = 'var(--accent-green)';
          this.reset();

          // Clear any remaining errors
          this.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
          this.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

          setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.style.background = '';
            submitBtn.disabled = false;
          }, 3000);
        } else {
          if (result.errors) {
            showFieldErrors(this, result.errors);
          }
          throw new Error(result.message || 'Submission failed');
        }
      } catch (error) {
        submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Error! Try Again';
        submitBtn.style.background = 'var(--accent-red)';
        console.error('Form submission error:', error);

        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.style.background = '';
          submitBtn.disabled = false;
        }, 3000);
      }
    }
  });
}

// ============================================
// Careers Form Submission
// ============================================
const candidateForm = document.getElementById('candidateForm');
if (candidateForm) {
  candidateForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (validateForm(this)) {
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
      submitBtn.disabled = true;

      // Get CSRF token
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

      // Prepare form data with file
      const formData = new FormData(this);

      try {
        const response = await fetch('/api/v1/careers/apply/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
          submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Application Submitted!';
          submitBtn.style.background = 'var(--accent-green)';
          this.reset();

          // Clear any remaining errors
          this.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
          this.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

          setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.style.background = '';
            submitBtn.disabled = false;
          }, 3000);
        } else {
          if (result.errors) {
            showFieldErrors(this, result.errors);
          }
          throw new Error(result.message || 'Submission failed');
        }
      } catch (error) {
        submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Error! Try Again';
        submitBtn.style.background = 'var(--accent-red)';
        console.error('Form submission error:', error);

        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.style.background = '';
          submitBtn.disabled = false;
        }, 3000);
      }
    }
  });
}

// Generic form submission handler for other forms
document.querySelectorAll('form:not(#bookingForm):not(#candidateForm)').forEach(form => {
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (validateForm(form)) {
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = 'Submitting...';
      submitBtn.disabled = true;

      setTimeout(() => {
        submitBtn.textContent = '✓ Submitted Successfully!';
        submitBtn.style.background = 'var(--accent-green)';
        form.reset();

        setTimeout(() => {
          submitBtn.textContent = originalText;
          submitBtn.style.background = '';
          submitBtn.disabled = false;
        }, 3000);
      }, 1500);
    }
  });
});

// ============================================
// Industry solution cards click handler & Hash activation
// ============================================
document.querySelectorAll('.industry-card').forEach(card => {
  card.addEventListener('click', function () {
    const targetId = this.dataset.target;
    if (targetId) {
      const tabId = '#v-pills-' + targetId.substring(1) + '-tab';
      const tabButton = document.querySelector(tabId);
      if (tabButton) {
        const tab = new bootstrap.Tab(tabButton);
        tab.show();
        const targetSection = document.querySelector('.solutions-tabs-section');
        if (targetSection) {
          targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      } else {
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
          targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    }
  });
});

// Auto-activate tab based on URL hash on load
window.addEventListener('DOMContentLoaded', () => {
  const hash = window.location.hash;
  if (hash) {
    const cleanHash = hash.substring(1);
    const tabButton = document.getElementById(`v-pills-${cleanHash}-tab`);
    if (tabButton) {
      const tab = new bootstrap.Tab(tabButton);
      tab.show();
      setTimeout(() => {
        const section = document.querySelector('.solutions-tabs-section');
        if (section) {
          section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 500);
    }
  }
});

// ============================================
// Blog category filter
// ============================================
document.querySelectorAll('.blog-filter-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    // Remove active class from all buttons
    document.querySelectorAll('.blog-filter-btn').forEach(b => {
      b.classList.remove('active');
      b.style.background = 'transparent';
      b.style.color = 'var(--primary-blue)';
    });

    // Add active class to clicked button
    this.classList.add('active');
    this.style.background = 'var(--gradient-primary)';
    this.style.color = 'white';

    const category = this.dataset.category;

    // Filter blog cards
    document.querySelectorAll('.blog-card').forEach(card => {
      if (category === 'all' || card.dataset.category === category) {
        card.style.display = 'block';
        card.style.animation = 'fadeInUp 0.5s ease forwards';
      } else {
        card.style.display = 'none';
      }
    });
  });
});

// ============================================
// Service accordion functionality
// ============================================
document.querySelectorAll('.service-accordion-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    const accordionContent = this.nextElementSibling;
    const icon = this.querySelector('.accordion-icon');

    // Close all other accordions
    document.querySelectorAll('.service-accordion-content').forEach(content => {
      if (content !== accordionContent) {
        content.style.maxHeight = '0';
        content.style.padding = '0 20px';
      }
    });

    document.querySelectorAll('.accordion-icon').forEach(i => {
      if (i !== icon) {
        i.style.transform = 'rotate(0deg)';
      }
    });

    // Toggle current accordion
    if (accordionContent.style.maxHeight && accordionContent.style.maxHeight !== '0px') {
      accordionContent.style.maxHeight = '0';
      accordionContent.style.padding = '0 20px';
      icon.style.transform = 'rotate(0deg)';
    } else {
      accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
      accordionContent.style.padding = '20px';
      icon.style.transform = 'rotate(180deg)';
    }
  });
});

// ============================================
// Lazy loading images
// ============================================
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.add('loaded');
        observer.unobserve(img);
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}

// ============================================
// Add loading animation to page
// ============================================
window.addEventListener('load', () => {
  document.body.classList.add('loaded');

  // Trigger initial animations
  setTimeout(() => {
    document.querySelectorAll('.hero-title').forEach(el => {
      el.style.animation = 'textReveal 1s ease forwards';
    });
  }, 100);
});

// ============================================
// Dynamic year in footer
// ============================================
const currentYear = new Date().getFullYear();
document.querySelectorAll('.current-year').forEach(el => {
  el.textContent = currentYear;
});

// ============================================
// Back to top button
// ============================================
const backToTopBtn = document.createElement('button');
backToTopBtn.className = 'back-to-top';
backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopBtn.style.cssText = `
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 50px;
  height: 50px;
  background: var(--gradient-primary);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 999;
  box-shadow: var(--shadow-lg);
`;

document.body.appendChild(backToTopBtn);

window.addEventListener('scroll', () => {
  if (window.scrollY > 500) {
    backToTopBtn.style.opacity = '1';
    backToTopBtn.style.visibility = 'visible';
  } else {
    backToTopBtn.style.opacity = '0';
    backToTopBtn.style.visibility = 'hidden';
  }
});

backToTopBtn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

// ============================================
// Prevent form resubmission on page refresh
// ============================================
if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

// ============================================
// Add hover effect to service cards
// ============================================
document.querySelectorAll('.service-card').forEach(card => {
  card.addEventListener('mouseenter', function () {
    this.style.transform = 'translateY(-10px) scale(1.02)';
  });

  card.addEventListener('mouseleave', function () {
    this.style.transform = 'translateY(0) scale(1)';
  });
});

// ============================================
// Add stagger animation to cards
// ============================================
function addStaggerAnimation(container, selector, delay = 100) {
  const cards = container.querySelectorAll(selector);
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * delay}ms`;
  });
}

// Initialize stagger animations
document.querySelectorAll('.services-grid, .blog-grid, .case-studies-grid').forEach(grid => {
  addStaggerAnimation(grid, '.glass-card', 100);
});

// ============================================
// Custom Cursor Effect (Optional)
// ============================================
const customCursor = document.querySelector('.custom-cursor');
const cursorDot = document.querySelector('.cursor-dot');

if (customCursor && cursorDot) {
  document.addEventListener('mousemove', (e) => {
    customCursor.style.left = e.clientX - 10 + 'px';
    customCursor.style.top = e.clientY - 10 + 'px';
    cursorDot.style.left = e.clientX - 4 + 'px';
    cursorDot.style.top = e.clientY - 4 + 'px';
  });

  document.querySelectorAll('a, button, .service-card, .glass-card').forEach(el => {
    el.addEventListener('mouseenter', () => {
      customCursor.classList.add('hover');
    });
    el.addEventListener('mouseleave', () => {
      customCursor.classList.remove('hover');
    });
  });
}

// ============================================
// Performance: Reduce animations on low-end devices
// ============================================
if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
  document.documentElement.style.setProperty('--animation-duration', '0.5s');
  document.querySelectorAll('*').forEach(el => {
    el.style.animationDuration = '0.5s';
  });
}

// ============================================
// Testimonials Slider
// ============================================
(function () {
  const slider = document.getElementById('testimonialsSlider');
  const prevBtn = document.querySelector('.testimonials-nav-btn.prev-btn');
  const nextBtn = document.querySelector('.testimonials-nav-btn.next-btn');
  const cards = document.querySelectorAll('.testimonial-card');

  if (!slider || !prevBtn || !nextBtn || cards.length === 0) return;

  let currentIndex = 0;
  let cardWidth = 0;
  let gap = 24;
  let autoPlayInterval = null;
  let isPaused = false;

  // Calculate card width based on viewport
  function calculateCardWidth() {
    const containerWidth = slider.parentElement.offsetWidth;
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth < 1200;

    if (isMobile) {
      cardWidth = containerWidth;
    } else if (isTablet) {
      cardWidth = containerWidth / 2 - gap / 2;
    } else {
      cardWidth = containerWidth / 3 - gap * 2 / 3;
    }
  }

  // Update slider position
  function updateSlider() {
    const translateX = -(currentIndex * (cardWidth + gap));
    slider.style.transform = `translateX(${translateX}px)`;

    // Update active card
    cards.forEach((card, index) => {
      card.classList.remove('active');
      if (index === currentIndex) {
        card.classList.add('active');
      }
    });
  }

  // Go to next slide
  function nextSlide() {
    currentIndex++;
    if (currentIndex >= cards.length) {
      currentIndex = 0;
    }
    updateSlider();
  }

  // Go to previous slide
  function prevSlide() {
    currentIndex--;
    if (currentIndex < 0) {
      currentIndex = cards.length - 1;
    }
    updateSlider();
  }

  // Start auto-play
  function startAutoPlay() {
    if (autoPlayInterval) clearInterval(autoPlayInterval);
    autoPlayInterval = setInterval(() => {
      if (!isPaused) {
        nextSlide();
      }
    }, 4000);
  }

  // Stop auto-play
  function stopAutoPlay() {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
      autoPlayInterval = null;
    }
  }

  // Event listeners for navigation buttons
  prevBtn.addEventListener('click', () => {
    prevSlide();
    stopAutoPlay();
    startAutoPlay();
  });

  nextBtn.addEventListener('click', () => {
    nextSlide();
    stopAutoPlay();
    startAutoPlay();
  });

  // Pause on hover
  slider.addEventListener('mouseenter', () => {
    isPaused = true;
  });

  slider.addEventListener('mouseleave', () => {
    isPaused = false;
  });

  // Touch swipe support
  let touchStartX = 0;
  let touchEndX = 0;

  slider.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  slider.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, { passive: true });

  function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
      if (diff > 0) {
        // Swipe left - next slide
        nextSlide();
      } else {
        // Swipe right - previous slide
        prevSlide();
      }
      stopAutoPlay();
      startAutoPlay();
    }
  }

  // Handle window resize
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      calculateCardWidth();
      updateSlider();
    }, 100);
  });

  // Initialize
  calculateCardWidth();
  updateSlider();
  startAutoPlay();

  // Pause auto-play when page is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopAutoPlay();
    } else {
      startAutoPlay();
    }
  });
})();

// ============================================
// Global Fixed Fullscreen Particles Initializer
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  let particlesContainer = document.getElementById('particles-js');

  // If the page doesn't have the particles-js container, create it dynamically
  if (!particlesContainer) {
    particlesContainer = document.createElement('div');
    particlesContainer.id = 'particles-js';
    document.body.insertBefore(particlesContainer, document.body.firstChild);
  }

  // Double check if canvas has already been initialized (e.g. by inline template scripts)
  // If not initialized, set up global particles
  setTimeout(() => {
    const canvas = particlesContainer.querySelector('.particles-js-canvas-el');
    if (!canvas) {
      if (!window.particlesJS) {
        // Dynamically load particles.js if not present
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js';
        script.onload = () => {
          initGlobalParticlesJS();
        };
        document.head.appendChild(script);
      } else {
        initGlobalParticlesJS();
      }
    }
  }, 100);
});

function initGlobalParticlesJS() {
  if (window.particlesJS) {
    particlesJS('particles-js', {
      'particles': {
        'number': {
          'value': 80,
          'density': {
            'enable': true,
            'value_area': 800
          }
        },
        'color': {
          'value': ['#282973', '#FDB81E']
        },
        'shape': {
          'type': 'circle'
        },
        'opacity': {
          'value': 0.6,
          'random': true,
          'anim': {
            'enable': true,
            'speed': 1,
            'opacity_min': 0.3,
            'sync': false
          }
        },
        'size': {
          'value': 6,
          'random': true,
          'anim': {
            'enable': true,
            'speed': 2,
            'size_min': 1.5,
            'sync': false
          }
        },
        'line_linked': {
          'enable': true,
          'distance': 150,
          'color': '#282973',
          'opacity': 0.35,
          'width': 1.5
        },
        'move': {
          'enable': true,
          'speed': 2,
          'direction': 'none',
          'random': false,
          'straight': false,
          'out_mode': 'out',
          'bounce': false
        }
      },
      'interactivity': {
        'detect_on': 'canvas',
        'events': {
          'onhover': {
            'enable': true,
            'mode': 'grab'
          },
          'onclick': {
            'enable': true,
            'mode': 'push'
          },
          'resize': true
        },
        'modes': {
          'grab': {
            'distance': 140,
            'line_linked': {
              'opacity': 0.5
            }
          },
          'push': {
            'particles_nb': 4
          }
        }
      },
      'retina_detect': true
    });
  }
}

// ============================================
// Typewriter Effect for Hero Title
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  const element = document.getElementById('typewriter-text');
  if (!element) return;

  const words = ["AI Marketing & Automation ", "AI Software Development", "AI Chatbots", "Meta Ads", "AEO", "Content Creation", "Lead Generation", "Blog Writing", "Image & Video Generation"];
  let wordIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingSpeed = 150;

  function type() {
    const currentWord = words[wordIndex];

    if (isDeleting) {
      // Deleting characters
      element.textContent = currentWord.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 50; // Deleting is faster
    } else {
      // Typing characters
      element.textContent = currentWord.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 150; // Typing speed
    }

    // If complete typing
    if (!isDeleting && charIndex === currentWord.length) {
      typingSpeed = 2500; // Pause at the end of the word
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      wordIndex = (wordIndex + 1) % words.length; // Next word
      typingSpeed = 500; // Pause before starting to type next word
    }

    setTimeout(type, typingSpeed);
  }

  // Start the typewriter
  type();
});

