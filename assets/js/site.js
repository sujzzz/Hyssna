// Hyssna International — shared page behaviour
(function () {
  document.documentElement.classList.add('js');
  var body = document.body;

  // Flyout menu
  var flyout = document.querySelector('[data-flyout]');
  var openBtn = document.querySelector('[data-menu-open]');
  var closeBtn = document.querySelector('[data-menu-close]');
  var flyImg = document.querySelector('[data-fly-img]');
  function setMenu(open) {
    if (open) {
      flyout.hidden = false;
      requestAnimationFrame(function () { flyout.classList.add('open'); });
      closeBtn.focus();
    } else {
      flyout.classList.remove('open');
      setTimeout(function () { flyout.hidden = true; }, 350);
      openBtn.focus();
    }
    body.classList.toggle('no-scroll', open);
    openBtn.setAttribute('aria-expanded', String(open));
  }
  openBtn.addEventListener('click', function () { setMenu(true); });
  closeBtn.addEventListener('click', function () { setMenu(false); });

  // Hovering a menu item opens its submenu and swaps the picture
  flyout.querySelectorAll('.fly-list > li').forEach(function (li) {
    li.addEventListener('mouseenter', function () {
      flyout.querySelectorAll('.fly-list > li.show').forEach(function (o) { if (o !== li) o.classList.remove('show'); });
      if (li.querySelector('.fly-sub')) li.classList.add('show');
    });
  });
  flyout.querySelectorAll('[data-image]').forEach(function (a) {
    var swap = function () {
      var src = a.getAttribute('data-image');
      if (!flyImg || flyImg.getAttribute('src') === src) return;
      flyImg.classList.add('fading');
      setTimeout(function () { flyImg.src = src; flyImg.classList.remove('fading'); }, 200);
    };
    a.addEventListener('mouseenter', swap);
    a.addEventListener('focus', swap);
  });

  // Floating "Talk to us" button and panel
  var fab = document.querySelector('[data-talk]');
  var sheet = document.querySelector('[data-talk-sheet]');
  var scrim = document.querySelector('[data-talk-close]');
  var fabLabel = fab.querySelector('[data-talk-label]');
  function setTalk(open) {
    sheet.classList.toggle('open', open);
    scrim.classList.toggle('open', open);
    fab.setAttribute('aria-expanded', String(open));
    fabLabel.textContent = open ? 'Close' : 'Talk to us';
    body.classList.toggle('no-scroll', open);
    if (open) setTimeout(function () { sheet.focus({ preventScroll: true }); }, 400);
  }
  fab.addEventListener('click', function () { setTalk(fab.getAttribute('aria-expanded') !== 'true'); });
  scrim.addEventListener('click', function () { setTalk(false); });
  function onScroll() { fab.classList.toggle('show', window.scrollY > 500); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!flyout.hidden) setMenu(false);
    if (sheet.classList.contains('open')) { setTalk(false); fab.focus(); }
  });

  // Hero video (home only)
  var video = document.getElementById('hero-video');
  var toggle = document.querySelector('[data-video-toggle]');
  if (video && toggle) {
    var label = toggle.querySelector('span');
    var icon = toggle.querySelector('svg');
    var pauseIcon = icon.innerHTML;
    var setPaused = function (paused) {
      if (paused) video.pause(); else video.play().catch(function () {});
      toggle.setAttribute('aria-pressed', String(paused));
      label.textContent = paused ? 'Play video' : 'Pause video';
      icon.innerHTML = paused ? '<path d="M2 1l9 5-9 5z"/>' : pauseIcon;
    };
    toggle.addEventListener('click', function () { setPaused(!video.paused); });
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) setPaused(true);
  }

  // Lightbox
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

  // Enquiry forms: validated in the page; the live site connects them to email
  document.querySelectorAll('[data-enquiry]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var flag = function (input, bad) {
      var err = document.getElementById(input.id + '-err');
      input.setAttribute('aria-invalid', String(bad));
      if (bad) input.setAttribute('aria-describedby', err.id); else input.removeAttribute('aria-describedby');
      err.hidden = !bad;
      return bad;
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = form.elements.first;
      var email = form.elements.email;
      var badName = flag(first, !first.value.trim());
      var badEmail = flag(email, !/^\S+@\S+\.\S+$/.test(email.value.trim()));
      if (badName || badEmail) { (badName ? first : email).focus(); status.textContent = ''; return; }
      status.textContent = 'Thank you, ' + first.value.trim() + '. Our team will be in touch shortly.';
      form.reset();
    });
  });

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
