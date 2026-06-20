/* ============================================================
   LOYA MEDIA — INTERACTIONS
   ============================================================ */

// ── Custom Cursor ────────────────────────────
const dot  = document.createElement('div');
const ring = document.createElement('div');
dot.className  = 'cursor-dot';
ring.className = 'cursor-ring';
document.body.appendChild(dot);
document.body.appendChild(ring);

let mouseX = 0, mouseY = 0;
let ringX  = 0, ringY  = 0;

document.addEventListener('mousemove', e => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  dot.style.left = mouseX + 'px';
  dot.style.top  = mouseY + 'px';
});

(function animateRing() {
  ringX += (mouseX - ringX) * 0.12;
  ringY += (mouseY - ringY) * 0.12;
  ring.style.left = ringX + 'px';
  ring.style.top  = ringY + 'px';
  requestAnimationFrame(animateRing);
})();

document.querySelectorAll('a, button, [data-hover]').forEach(el => {
  el.addEventListener('mouseenter', () => { dot.classList.add('hover'); ring.classList.add('hover'); });
  el.addEventListener('mouseleave', () => { dot.classList.remove('hover'); ring.classList.remove('hover'); });
});

// ── Nav Scroll ───────────────────────────────
const nav = document.querySelector('nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });
}

// ── Mobile Menu ──────────────────────────────
const toggle   = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
const navCta   = document.querySelector('.nav-cta');

if (toggle) {
  toggle.addEventListener('click', () => {
    const open = toggle.classList.toggle('open');
    navLinks.classList.toggle('open', open);
    if (navCta) navCta.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    toggle.classList.remove('open');
    navLinks.classList.remove('open');
    if (navCta) navCta.classList.remove('open');
    document.body.style.overflow = '';
  }));
}

// ── Scroll Reveal ─────────────────────────────
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      revealObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Active Nav Link ───────────────────────────
const page = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === page) a.classList.add('active');
});

// ── Contact Form ──────────────────────────────
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('.cta-pill');
    const origText = btn.innerHTML;
    btn.innerHTML = 'Sending… <span>⋯</span>';
    btn.style.opacity = '0.7';
    btn.style.pointerEvents = 'none';

    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      if (res.ok) {
        form.style.display = 'none';
        document.getElementById('form-success').style.display = 'block';
      } else {
        throw new Error();
      }
    } catch {
      btn.innerHTML = origText;
      btn.style.opacity = '';
      btn.style.pointerEvents = '';
      alert('Something went wrong. Please try again.');
    }
  });
}

// ── Line animation for statement sections ─────
const lineObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const lines = e.target.querySelectorAll('.statement-line');
      lines.forEach((l, i) => {
        l.style.transitionDelay = (i * 0.12) + 's';
        l.classList.add('visible');
      });
      lineObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll('.statement-text').forEach(el => {
  el.querySelectorAll('.statement-line').forEach(l => {
    l.style.opacity = '0';
    l.style.transform = 'translateY(40px)';
    l.style.transition = 'opacity 0.8s cubic-bezier(0.16,1,0.3,1), transform 0.8s cubic-bezier(0.16,1,0.3,1)';
  });
  lineObserver.observe(el);
});

document.querySelectorAll('.statement-line.visible').forEach(l => {
  l.style.opacity = '1';
  l.style.transform = 'none';
});

// ── FAQ Accordion ─────────────────────────────
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
