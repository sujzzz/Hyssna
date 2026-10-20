// Hyssna International — landing page behaviour
(function () {
  var header = document.querySelector('.site-header');

  // Header turns solid once the page scrolls past the top of the hero
  function onScroll() {
    header.classList.toggle('solid', window.scrollY > 24);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var menuBtn = document.querySelector('.menu-btn');
  var links = document.getElementById('nav-links');
  menuBtn.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.textContent = open ? 'Close' : 'Menu';
  });
  links.addEventListener('click', function (e) {
    if (e.target.closest('a')) {
      links.classList.remove('open');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.textContent = 'Menu';
    }
  });

  // Logo: show the uploaded logo when it loads, otherwise the wordmark
  var brand = document.querySelector('.brand');
  var logo = document.querySelector('[data-logo]');
  function logoReady() { if (logo.naturalWidth > 0) brand.classList.add('has-logo'); }
  if (logo.complete) logoReady(); else logo.addEventListener('load', logoReady);

  // Media slots: mark any image that fails to load so its placeholder shows
  document.querySelectorAll('[data-media]').forEach(function (slot) {
    var img = slot.querySelector('img');
    if (!img) return;
    function check() { if (!img.naturalWidth) slot.classList.add('is-missing'); }
    img.addEventListener('error', function () { slot.classList.add('is-missing'); });
    img.addEventListener('load', function () { slot.classList.remove('is-missing'); });
    if (img.complete) check();
  });

  // Hero video: pause control, and respect reduced motion
  var video = document.getElementById('hero-video');
  var toggle = document.querySelector('[data-video-toggle]');
  var label = toggle.querySelector('span');
  var icon = toggle.querySelector('svg');
  var pauseIcon = icon.innerHTML;
  var playIcon = '<path d="M2 1l9 5-9 5z"/>';

  function setPaused(paused) {
    if (paused) video.pause(); else video.play().catch(function () {});
    toggle.setAttribute('aria-pressed', String(paused));
    label.textContent = paused ? 'Play video' : 'Pause video';
    icon.innerHTML = paused ? playIcon : pauseIcon;
  }
  toggle.addEventListener('click', function () { setPaused(!video.paused); });
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) setPaused(true);
  video.addEventListener('error', function () { toggle.hidden = true; }, true);
  var source = video.querySelector('source');
  if (source) source.addEventListener('error', function () { toggle.hidden = true; });

  // Certificate viewer
  var dialog = document.getElementById('cert-viewer');
  var vTitle = document.getElementById('viewer-title');
  var vImg = document.getElementById('viewer-img');
  var vMissing = document.getElementById('viewer-missing');
  document.querySelectorAll('[data-cert]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var missing = btn.querySelector('.is-missing');
      vTitle.textContent = btn.getAttribute('data-cert-title');
      vImg.hidden = !!missing;
      vMissing.hidden = !missing;
      if (!missing) {
        vImg.src = btn.getAttribute('data-cert');
        vImg.alt = btn.getAttribute('data-cert-title') + ' certificate';
      }
      if (typeof dialog.showModal === 'function') dialog.showModal();
    });
  });
  dialog.querySelector('[data-close]').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });

  // Enquiry form: validates in the page; the live site will connect it to email
  var form = document.getElementById('enquiry');
  var status = document.getElementById('form-status');
  function flag(input, errId, bad) {
    input.setAttribute('aria-invalid', String(bad));
    input.setAttribute('aria-describedby', bad ? errId : '');
    document.getElementById(errId).hidden = !bad;
    return bad;
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements.name;
    var email = form.elements.email;
    var badName = flag(name, 'f-name-err', !name.value.trim());
    var badEmail = flag(email, 'f-email-err', !/^\S+@\S+\.\S+$/.test(email.value.trim()));
    if (badName || badEmail) {
      (badName ? name : email).focus();
      status.textContent = '';
      return;
    }
    status.textContent = 'Thank you, ' + name.value.trim().split(' ')[0] +
      '. This preview does not send messages yet; on the live site your enquiry goes to info@hyssnauae.com.';
    form.reset();
  });

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
