/**
 * OMNEXA AI - Brand Theme Modern JavaScript
 * Galaxy Dots, Text Scramble, Spotlight Cards, Magnetic Buttons, Galaxy Particles
 */

document.addEventListener('DOMContentLoaded', () => {
  initTextScramble();
  initSpotlightCards();
  initMagneticButtons();
  initScrollProgress();
  initScrollReveal();
  initFloatingElements();
  initCosmicEffects();
});

/* ============================================
   1. Text Scramble Effect (ReactBits inspired)
   ============================================ */
function initTextScramble() {
  const chars = '!<>-_\\/[]{}=+*#?@~';
  const elements = document.querySelectorAll('.text-scramble');

  elements.forEach(el => {
    const originalText = el.dataset.text || el.innerText;
    el.dataset.text = originalText;
    let frame = 0;
    let queue = [];

    for (let i = 0; i < originalText.length; i++) {
      queue.push({
        from: chars[Math.floor(Math.random() * chars.length)],
        to: originalText[i],
        start: Math.floor(Math.random() * 30),
        end: Math.floor(Math.random() * 30) + 30
      });
    }

    const update = () => {
      let output = '';
      let complete = 0;

      for (let i = 0; i < queue.length; i++) {
        const { from, to, start, end } = queue[i];
        let char = from;

        if (frame >= end) {
          complete++;
          char = to;
        } else if (frame >= start) {
          if (Math.random() < 0.2) {
            char = chars[Math.floor(Math.random() * chars.length)];
          } else {
            char = Math.random() < 0.5 ? from : chars[Math.floor(Math.random() * chars.length)];
          }
          char = char;
        }

        output += char;
      }

      el.innerText = output;

      if (complete === queue.length) {
        return;
      }

      frame++;
      requestAnimationFrame(update);
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          frame = 0;
          update();
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    observer.observe(el);
  });
}

/* ============================================
   2. Spotlight Card Effect (ReactBits inspired)
   ============================================ */
function initSpotlightCards() {
  const cards = document.querySelectorAll('.spotlight-card');

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      card.style.setProperty('--mouse-x', x + '%');
      card.style.setProperty('--mouse-y', y + '%');
    });
  });
}

/* ============================================
   3. Magnetic Button Effect (Enhanced)
   ============================================ */
function initMagneticButtons() {
  const buttons = document.querySelectorAll('.btn-magnetic-enhanced, .btn-gradient, .btn-outline-gradient');

  buttons.forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0, 0)';
    });
  });
}

/* ============================================
   4. Scroll Progress Bar
   ============================================ */
function initScrollProgress() {
  const progressBar = document.createElement('div');
  progressBar.className = 'scroll-progress-indicator';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #282973, #FDB81E, #282973);
    z-index: 9999;
    width: 0%;
    transition: width 0.1s linear;
    box-shadow: 0 0 8px rgba(253, 184, 30, 0.5);
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = scrollPercent + '%';
  });
}

/* ============================================
   6. Scroll Reveal Animations
   ============================================ */
function initScrollReveal() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Blur-in reveal
  document.querySelectorAll('.blur-reveal').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.filter = 'blur(8px)';
    el.style.transition = 'all 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
    observer.observe(el);
  });

  // Scale reveal
  document.querySelectorAll('.scale-reveal').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'scale(0.9)';
    el.style.transition = 'all 0.7s cubic-bezier(0.16, 1, 0.3, 1)';
    observer.observe(el);
  });

  // Word by word reveal
  document.querySelectorAll('.word-reveal-trigger').forEach(el => {
    const words = el.innerText.split(' ');
    el.innerHTML = words.map((word, i) =>
      `<span class="word" style="display:inline-block;opacity:0;transform:translateY(10px);transition:all 0.5s cubic-bezier(0.16,1,0.3,1) ${i * 0.08}s">${word}</span>`
    ).join(' ');
    observer.observe(el);
  });
}

// Handle revealed class (scoped to avoid re-injection)
(function () {
  const revealStyle = document.createElement('style');
  revealStyle.textContent = `
    .revealed.blur-reveal { opacity: 1 !important; transform: translateY(0) !important; filter: blur(0) !important; }
    .revealed.scale-reveal { opacity: 1 !important; transform: scale(1) !important; }
    .revealed .word { opacity: 1 !important; transform: translateY(0) !important; }
  `;
  document.head.appendChild(revealStyle);
})();

/* ============================================
   7. Floating Elements
   ============================================ */
function initFloatingElements() {
  const elements = document.querySelectorAll('.float-chaos');

  elements.forEach((el, index) => {
    let mouseX = 0, mouseY = 0;
    let currentX = 0, currentY = 0;
    let rotation = 0;

    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      mouseX = (e.clientX - rect.left - rect.width / 2) * 0.1;
      mouseY = (e.clientY - rect.top - rect.height / 2) * 0.1;
    });

    el.addEventListener('mouseleave', () => {
      mouseX = 0;
      mouseY = 0;
    });

    function update() {
      currentX += (mouseX - currentX) * 0.1;
      currentY += (mouseY - currentY) * 0.1;
      rotation = Math.sin(Date.now() / 1000 + index) * 3;

      el.style.transform = `translate(${currentX}px, ${currentY}px) rotate(${rotation}deg)`;
      requestAnimationFrame(update);
    }

    update();
  });
}

/* ============================================
   8. Cosmic Effects
   ============================================ */
function initCosmicEffects() {
  // Glitch effect on hover for specific elements
  const glitchElements = document.querySelectorAll('.glitch-hover');

  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&*';

  glitchElements.forEach(el => {
    const originalText = el.innerText;

    el.addEventListener('mouseenter', () => {
      let iterations = 0;
      const interval = setInterval(() => {
        el.innerText = originalText.split('').map((char, i) => {
          if (i < iterations) return originalText[i];
          if (char === ' ') return ' ';
          return chars[Math.floor(Math.random() * chars.length)];
        }).join('');

        iterations += 1;
        if (iterations > originalText.length) {
          clearInterval(interval);
        }
      }, 40);
    });
  });

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Custom cursor glow effect (desktop only)
  if (window.matchMedia('(pointer: fine)').matches) {
    const cursor = document.createElement('div');
    cursor.style.cssText = `
      position: fixed;
      width: 300px;
      height: 300px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(253, 184, 30, 0.08) 0%, transparent 70%);
      pointer-events: none;
      z-index: 9998;
      transform: translate(-50%, -50%);
      opacity: 0;
      transition: opacity 0.3s ease;
    `;
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
      cursor.style.opacity = '1';
    });

    document.addEventListener('mouseleave', () => {
      cursor.style.opacity = '0';
    });
  }
}

/* ============================================
   9. Navbar Enhanced Behavior
   ============================================ */
(function () {
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const currentScroll = window.scrollY;
      if (currentScroll > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
      lastScroll = currentScroll;
    });

    // Make navbar hidden on scroll down, visible on scroll up
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const currentScroll = window.scrollY;
          if (currentScroll > lastScroll && currentScroll > 200) {
            navbar.style.transform = 'translateY(-100%)';
          } else {
            navbar.style.transform = 'translateY(0)';
          }
          lastScroll = currentScroll;
          ticking = false;
        });
        ticking = true;
      }
    });
  }
})();

/* ============================================
   10. Enhanced Counter Animation
   ============================================ */
function enhancedCountUp(el, target, duration = 2000) {
  const suffix = el.dataset.suffix || '';
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const easeProgress = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(easeProgress * target);

    el.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.style.animation = 'elasticBounce 0.5s ease';
    }
  }

  requestAnimationFrame(update);
}

// Use enhanced counter (renamed to avoid conflict with main.js counterObserver)
(function () {
  const brandCounterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counter = entry.target;
        const target = parseInt(counter.dataset.target);
        const suffix = counter.dataset.suffix || '';
        counter.textContent = '0' + suffix;
        enhancedCountUp(counter, target);
        brandCounterObserver.unobserve(counter);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-number[data-target]').forEach(counter => {
    brandCounterObserver.observe(counter);
  });
})();

/* ============================================
   11. Performance: Reduce motion for slow devices
   ============================================ */
if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
  document.documentElement.classList.add('reduce-motion');
}
