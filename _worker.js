const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function addSecurityHeaders(response) {
  const newResponse = new Response(response.body, response);
  newResponse.headers.set('X-Frame-Options', 'SAMEORIGIN');
  newResponse.headers.set('X-Content-Type-Options', 'nosniff');
  newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  newResponse.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  newResponse.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  return newResponse;
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

async function handleSubscribe(request, env) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }
  if (request.method !== 'POST') {
    return addSecurityHeaders(json({ error: 'Method not allowed.' }, 405));
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return addSecurityHeaders(json({ error: 'Invalid request body.' }, 400));
  }

  const email = (body.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return addSecurityHeaders(json({ error: 'Invalid email address.' }, 400));
  }

  /* ── Beehiiv ─────────────────────────────────────────────────────────── */
  if (env.BEEHIIV_API_KEY && env.BEEHIIV_PUBLICATION_ID) {
    try {
      const res = await fetch(
        `https://api.beehiiv.com/v2/publications/${env.BEEHIIV_PUBLICATION_ID}/subscriptions`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${env.BEEHIIV_API_KEY}`,
          },
          body: JSON.stringify({
            email,
            reactivate_existing: true,
            send_welcome_email: true,
          }),
        }
      );
      if (!res.ok) {
        const err = await res.text().catch(() => '');
        console.error('Beehiiv error', res.status, err);
      }
    } catch (err) {
      console.error('Beehiiv fetch failed', err);
    }
    return addSecurityHeaders(json({ success: true }));
  }

  /* ── Fallback: KV + console log ──────────────────────────────────────── */
  console.log('EMAIL_CAPTURE:', email);
  if (env.EMAIL_CAPTURE_KV) {
    try {
      const key = `email:${Date.now()}:${email}`;
      await env.EMAIL_CAPTURE_KV.put(key, email, { expirationTtl: 60 * 60 * 24 * 365 });
    } catch (err) {
      console.error('KV write failed', err);
    }
  }

  return addSecurityHeaders(json({ success: true }));
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === '/subscribe') {
      return handleSubscribe(request, env);
    }

    /* Pass everything else through to static assets */
    return addSecurityHeaders(await env.ASSETS.fetch(request));
  },
};
