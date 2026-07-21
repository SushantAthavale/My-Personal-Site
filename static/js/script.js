const toggleBtn = document.getElementById('toggleBtn');
const passwordInput = document.getElementById('password');
const form = document.getElementById('loginForm');
const errorText = document.getElementById('errorText');
const rateEls = document.querySelectorAll('.rate-val');
const introOverlay = document.getElementById('siteIntro');

window.addEventListener('load', () => {
  if (!introOverlay) return;
  introOverlay.addEventListener('animationend', (event) => {
    if (event.animationName !== 'intro-slide') return;
    introOverlay.classList.add('fade-out');
    setTimeout(() => {
      document.body.classList.add('intro-complete');
    }, 180);
    setTimeout(() => {
      if (introOverlay.parentNode) {
        introOverlay.parentNode.removeChild(introOverlay);
      }
    }, 360);
  }, { once: true });
});

toggleBtn.addEventListener('click', () => {
  const isHidden = passwordInput.type === 'password';
  passwordInput.type = isHidden ? 'text' : 'password';
  toggleBtn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
  toggleBtn.querySelector('.eye-icon').classList.toggle('hide', isHidden);
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const userId = document.getElementById('userId').value.trim();
  const password = passwordInput.value;
  const btn = form.querySelector('.btn-signin');

  if (!userId || !password) {
    errorText.style.color = 'var(--red)';
    errorText.textContent = 'Enter both your user ID and password to continue.';
    return;
  }

  if (password.length < 4) {
    errorText.style.color = 'var(--red)';
    errorText.textContent = 'That password looks too short — check and try again.';
    return;
  }

  errorText.textContent = '';
  const originalText = btn.innerHTML;
  btn.innerHTML = 'Checking…';
  btn.disabled = true;

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        userId,
        password,
        remember: document.getElementById('remember').checked ? 'on' : 'off',
      }),
    });

    const result = await response.json();

    if (result.success) {
      errorText.style.color = 'var(--green)';
      errorText.textContent = result.message || 'Login successful. Redirecting…';
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 800);
    } else {
      errorText.style.color = 'var(--red)';
      errorText.textContent = result.error || 'Unable to sign in. Please try again.';
    }
  } catch (error) {
    errorText.style.color = 'var(--red)';
    errorText.textContent = 'Server error. Try again after a moment.';
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
});

setInterval(() => {
  rateEls.forEach(el => {
    const base = parseFloat(el.dataset.base);
    const wiggle = base * (Math.random() * 0.006 - 0.003);
    const value = Math.round(base + wiggle);
    el.style.color = '#e08540';
    el.textContent = '₹' + value.toLocaleString('en-IN');
    setTimeout(() => { el.style.color = ''; }, 400);
  });
}, 3500);
