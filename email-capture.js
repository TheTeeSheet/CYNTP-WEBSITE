/* ─── CYNTP Email Capture ────────────────────────────────────────────────── */

(function () {
  const COOKIE     = 'cyntp_modal';
  const COOKIE_DAYS = 7;
  const FALLBACK_MS = 25000;
  const WORKER_URL  = '/subscribe';

  /* ── Cookie helpers ────────────────────────────────────────────────────── */
  function setCookie(name, value, days) {
    const exp = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value};expires=${exp};path=/;SameSite=Lax`;
  }
  function getCookie(name) {
    return document.cookie.split(';').some(c => c.trim().startsWith(name + '='));
  }

  /* ── Shared success inner HTML ─────────────────────────────────────────── */
  function successHTML() {
    return `
      <div class="cem-success-check">&#10003;</div>
      <h2 class="cem-headline">You're in.</h2>
      <p class="cem-sub">Every Thursday we send curated golf trips, course reviews, and travel intel to your inbox. While you wait for the first one, here are three places to start:</p>
      <div class="cem-success-links">
        <a href="/cyntp-trips.html" class="cem-success-link">Browse Stay &amp; Play Trips &rarr;</a>
        <a href="/cyntp-turn.html" class="cem-success-link">Read The Turn &rarr;</a>
        <a href="https://instagram.com/coursesyouneedtoplay" class="cem-success-link" target="_blank" rel="noopener">Follow on Instagram &rarr;</a>
      </div>
      <p class="cem-success-signoff">See you Thursday,<br>— Cameron, Noah &amp; Beau</p>`;
  }

  /* ── Modal HTML ────────────────────────────────────────────────────────── */
  const MODAL_HTML = `
<div id="ceModal" role="dialog" aria-modal="true" aria-labelledby="cemHeadline">
  <div class="cem-backdrop" id="cemBackdrop"></div>
  <div class="cem-box">
    <div class="cem-img-col">
      <img src="https://res.cloudinary.com/dak67vton/image/upload/f_auto,q_auto,w_900/v1779161086/IMG_9979_fgjlqk.heic" alt="Golf trip" loading="lazy">
    </div>
    <div class="cem-copy">
      <button class="cem-close" id="cemClose" aria-label="Close">&times;</button>
      <div id="cemContent">
        <p class="cem-eyebrow">CYNTP Community</p>
        <h2 class="cem-headline" id="cemHeadline">Get our Top 6 Golf Trips.</h2>
        <p class="cem-sub">Drop your email and we'll send it over right away. Six trips we've actually taken, the must-play courses, and where to book each one. Plus trips, course reviews, and gear straight to your inbox.</p>
        <form class="cem-form" id="cemForm" novalidate>
          <input class="cem-input" id="cemEmail" type="email" placeholder="Your email address" autocomplete="email" required>
          <p class="cem-error" id="cemError">Please enter a valid email address.</p>
          <button class="cem-btn" id="cemSubmit" type="submit">Get the Free Guide</button>
          <p class="cem-legal">Unsubscribe anytime. We'll never share your email.</p>
        </form>
      </div>
      <div id="cemSuccess" class="cem-success" style="display:none"></div>
    </div>
  </div>
</div>`;

  /* ── Inject modal ──────────────────────────────────────────────────────── */
  document.body.insertAdjacentHTML('beforeend', MODAL_HTML);

  const modal     = document.getElementById('ceModal');
  const backdrop  = document.getElementById('cemBackdrop');
  const closeBtn  = document.getElementById('cemClose');
  const form      = document.getElementById('cemForm');
  const emailIn   = document.getElementById('cemEmail');
  const errorMsg  = document.getElementById('cemError');
  const submitBtn = document.getElementById('cemSubmit');
  const content   = document.getElementById('cemContent');
  const successEl = document.getElementById('cemSuccess');

  /* ── Open / close ──────────────────────────────────────────────────────── */
  function openModal() {
    modal.classList.add('cem-visible');
    document.body.style.overflow = 'hidden';
    setTimeout(() => emailIn && emailIn.focus(), 350);
  }

  function closeModal() {
    modal.classList.remove('cem-visible');
    document.body.style.overflow = '';
  }

  /* ── Gate: only show once per 7 days ──────────────────────────────────── */
  function maybeOpenModal() {
    if (!getCookie(COOKIE)) {
      setCookie(COOKIE, '1', COOKIE_DAYS);
      openModal();
    }
  }

  /* ── Exit intent ───────────────────────────────────────────────────────── */
  let triggered = false;
  document.addEventListener('mouseleave', function (e) {
    if (!triggered && e.clientY < 20) {
      triggered = true;
      maybeOpenModal();
    }
  });

  /* ── 25-second fallback ────────────────────────────────────────────────── */
  setTimeout(function () {
    if (!triggered) {
      triggered = true;
      maybeOpenModal();
    }
  }, FALLBACK_MS);

  /* ── Close handlers ────────────────────────────────────────────────────── */
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', closeModal);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  /* ── Form submit ───────────────────────────────────────────────────────── */
  function isValidEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
  }

  async function handleSubmit(emailValue) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Joining…';
    errorMsg.style.display = 'none';

    try {
      const res = await fetch(WORKER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailValue.trim() }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok && data.error) throw new Error(data.error);
    } catch (err) {
      /* silently succeed for network errors — don't block the user */
    }

    /* Show success — user closes manually */
    content.style.display = 'none';
    successEl.innerHTML = successHTML();
    successEl.style.display = 'flex';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const val = emailIn.value;
    if (!isValidEmail(val)) {
      errorMsg.style.display = 'block';
      emailIn.focus();
      return;
    }
    handleSubmit(val);
  });

  /* ── Reset modal state on close so it's reusable ──────────────────────── */
  modal.addEventListener('transitionend', function () {
    if (!modal.classList.contains('cem-visible')) {
      content.style.display = '';
      successEl.style.display = 'none';
      successEl.innerHTML = '';
      form.reset();
      submitBtn.disabled = false;
      submitBtn.textContent = 'Get the Free Guide';
      errorMsg.style.display = 'none';
    }
  });

  /* ── Global opener ─────────────────────────────────────────────────────── */
  window.openEmailModal = openModal;

  /* ── Post CTA builder (used by blog-post.html) ─────────────────────────── */
  window.buildPostCTA = function () {
    return `
<div class="post-email-cta" id="postEmailCta">
  <p class="cem-eyebrow">CYNTP Community</p>
  <h3 class="cem-headline">Liked this? You'll love what we send on Thursdays.</h3>
  <p class="cem-sub">Curated golf trips and course reviews from CYNTP. No spam, just the good stuff.</p>
  <form class="cem-form" id="postCtaForm" novalidate>
    <input class="cem-input" id="postCtaEmail" type="email" placeholder="Your email address" autocomplete="email" required>
    <button class="cem-btn" id="postCtaSubmit" type="submit">Join the Community</button>
  </form>
  <p class="cem-legal" id="postCtaLegal">Unsubscribe anytime. We'll never share your email.</p>
</div>`;
  };

  window.wirePostCTA = function () {
    const postForm   = document.getElementById('postCtaForm');
    const postEmail  = document.getElementById('postCtaEmail');
    const postSubmit = document.getElementById('postCtaSubmit');
    if (!postForm) return;

    postForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      const val = postEmail ? postEmail.value : '';
      if (!isValidEmail(val)) {
        postEmail && postEmail.focus();
        return;
      }
      postSubmit.disabled = true;
      postSubmit.textContent = 'Joining…';

      try {
        await fetch(WORKER_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: val.trim() }),
        });
      } catch (err) { /* silent */ }

      /* Replace entire CTA block with success content */
      const cta = document.getElementById('postEmailCta');
      if (cta) {
        cta.innerHTML = `<div class="cem-success post-cta-success">${successHTML()}</div>`;
      }
    });
  };
})();
