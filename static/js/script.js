const toggleBtn = document.getElementById('toggleBtn');
const passwordInput = document.getElementById('password');
const form = document.getElementById('loginForm');
const errorText = document.getElementById('errorText');
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
  const password = passwordInput.value.trim();
  const btn = form.querySelector('.btn-signin');

  if (!userId || !password) {
    errorText.style.color = 'var(--red)';
    errorText.textContent = 'Enter both your email and password to continue.';
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

    // If login is successful, the server redirects. `response.redirected` will be true.
    if (response.redirected) {
      window.location.href = response.url; // Follow the redirect to the dashboard
      return;
    }

    // If there was no redirect, it means login failed and we got a JSON error.
    if (!response.ok) {
      try {
        const result = await response.json();
        errorText.style.color = 'var(--red)';
        errorText.textContent = result.error || 'Unable to sign in. Please try again.';
      } catch (e) {
        // This can happen if the server returns a non-JSON error (e.g., an HTML error page).
        // This is a more specific error message that helps with debugging.
        errorText.style.color = 'var(--red)';
        errorText.textContent = 'An unexpected server response was received.';
        // Log the actual response for debugging.
        console.error('Login failed. The server response was not valid JSON.');
        response.text().then(text => console.error('Server response body:', text));
      }
    }

    // Reset button state on failure
    btn.innerHTML = originalText;
    btn.disabled = false;
  } catch (error) {
    errorText.style.color = 'var(--red)';
    errorText.textContent = 'Server error. Try again after a moment.';
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
});
