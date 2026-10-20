// Hyssna International — page behaviour
(function () {
  // Mobile menu
  var menuBtn = document.querySelector('.menu-btn');
  var links = document.getElementById('nav-links');
  function closeMenu() {
    links.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.textContent = 'Menu';
  }
  menuBtn.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.textContent = open ? 'Close' : 'Menu';
  });
  links.addEventListener('click', function (e) { if (e.target.closest('a')) closeMenu(); });

  // Hero video pause control; paused by default for reduced motion
  var video = document.getElementById('hero-video');
  var toggle = document.querySelector('[data-video-toggle]');
  var label = toggle.querySelector('span');
  var icon = toggle.querySelector('svg');
  var pauseIcon = icon.innerHTML;
  function setPaused(paused) {
    if (paused) video.pause(); else video.play().catch(function () {});
    toggle.setAttribute('aria-pressed', String(paused));
    label.textContent = paused ? 'Play video' : 'Pause video';
    icon.innerHTML = paused ? '<path d="M2 1l9 5-9 5z"/>' : pauseIcon;
  }
  toggle.addEventListener('click', function () { setPaused(!video.paused); });
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) setPaused(true);

  // Client marquee: duplicate the row so the loop is seamless
  document.querySelectorAll('[data-marquee]').forEach(function (ul) {
    Array.prototype.slice.call(ul.children).forEach(function (li) {
      var copy = li.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true');
      ul.appendChild(copy);
    });
  });

  // Lightbox for projects and certificates
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lb-img');
  var lbTitle = document.getElementById('lb-title');
  document.querySelectorAll('[data-lightbox]').forEach(function (el) {
    el.addEventListener('click', function () {
      lbImg.src = el.getAttribute('data-lightbox');
      lbImg.alt = el.getAttribute('data-title') || '';
      lbTitle.textContent = el.getAttribute('data-title') || '';
      if (typeof lb.showModal === 'function') lb.showModal();
    });
  });
  lb.querySelector('[data-close]').addEventListener('click', function () { lb.close(); });
  lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });

  // Gentle reveal as sections enter the viewport (content stays visible without JS)
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-reveal');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) {
      // anything already on screen shows immediately
      if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in');
      io.observe(el);
    });
  }

  // Enquiry form: validates in the page; the live site connects it to email
  var form = document.getElementById('enquiry');
  var status = document.getElementById('form-status');
  function flag(input, errId, bad) {
    input.setAttribute('aria-invalid', String(bad));
    if (bad) input.setAttribute('aria-describedby', errId); else input.removeAttribute('aria-describedby');
    document.getElementById(errId).hidden = !bad;
    return bad;
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements.name;
    var email = form.elements.email;
    var badName = flag(name, 'f-name-err', !name.value.trim());
    var badEmail = flag(email, 'f-email-err', !/^\S+@\S+\.\S+$/.test(email.value.trim()));
    if (badName || badEmail) { (badName ? name : email).focus(); status.textContent = ''; return; }
    status.textContent = 'Thank you, ' + name.value.trim().split(' ')[0] + '. Our team will be in touch shortly.';
    form.reset();
  });

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
