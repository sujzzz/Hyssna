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

  // Company film (home): plays muted, inside the page, while it is on screen. A local
  // MP4 loops on its own. The YouTube player is sent back to its start just before the
  // end, so YouTube's end screen of other videos never appears.
  var film = document.querySelector('[data-film]');
  if (film) {
    var filmStart = Number(film.getAttribute('data-start')) || 0;
    var playBtn = film.querySelector('[data-film-play]');
    var soundBtn = film.querySelector('[data-film-sound]');
    var filmPauseIcon = playBtn.querySelector('svg').innerHTML;
    var clip = film.querySelector('video');
    var ctl = null, inView = false, requested = false, guard = null;
    var userPaused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var showPlaying = function (playing) {
      film.classList.toggle('is-playing', playing);
      playBtn.setAttribute('aria-pressed', String(!playing));
      playBtn.querySelector('span').textContent = playing ? 'Pause' : 'Play';
      playBtn.querySelector('svg').innerHTML = playing ? filmPauseIcon : '<path d="M2 1l9 5-9 5z"/>';
    };
    var ready = function (c) {
      ctl = c;
      c.mute();
      film.classList.remove('is-fallback');
      film.classList.add('is-ready');
      if (inView && !userPaused) c.play(); else if (c.playing()) c.pause();
    };
    var fail = function () { if (!ctl) film.classList.add('is-fallback'); };

    var useClip = function () {
      clip.addEventListener('playing', function () { showPlaying(true); });
      clip.addEventListener('pause', function () { showPlaying(false); });
      clip.addEventListener('error', fail, true);
      ready({
        play: function () { var pr = clip.play(); if (pr && pr.catch) pr.catch(function () {}); },
        pause: function () { clip.pause(); },
        playing: function () { return !clip.paused; },
        mute: function () { clip.muted = true; },
        unMute: function () { clip.muted = false; },
        muted: function () { return clip.muted; }
      });
    };

    var useYouTube = function () {
      var player = new YT.Player('film-player', {
        videoId: film.getAttribute('data-film'),
        playerVars: { autoplay: 0, mute: 1, controls: 0, rel: 0, playsinline: 1, modestbranding: 1, disablekb: 1, fs: 0, iv_load_policy: 3, start: filmStart },
        events: {
          onReady: function () {
            ready({
              play: function () { player.playVideo(); },
              pause: function () { player.pauseVideo(); },
              playing: function () { return player.getPlayerState() === YT.PlayerState.PLAYING; },
              mute: function () { player.mute(); },
              unMute: function () { player.unMute(); },
              muted: function () { return player.isMuted(); }
            });
          },
          onStateChange: function (e) {
            if (e.data === YT.PlayerState.PLAYING) {
              showPlaying(true);
              clearInterval(guard);
              guard = setInterval(function () {
                var d = player.getDuration();
                if (d && player.getCurrentTime() > d - 1.2) player.seekTo(filmStart, true);
              }, 250);
            } else if (e.data === YT.PlayerState.PAUSED) {
              showPlaying(false);
              clearInterval(guard);
            } else if (e.data === YT.PlayerState.ENDED) {
              player.seekTo(filmStart, true);
              player.playVideo();
            }
          },
          onError: function () { ctl = null; film.classList.remove('is-ready', 'is-playing'); fail(); }
        }
      });
    };

    var load = function () {
      if (requested) return;
      requested = true;
      if (clip) { useClip(); return; }
      if (window.YT && window.YT.Player) { useYouTube(); return; }
      var prev = window.onYouTubeIframeAPIReady;
      window.onYouTubeIframeAPIReady = function () { if (prev) prev(); useYouTube(); };
      var s = document.createElement('script');
      s.src = 'https://www.youtube.com/iframe_api';
      s.onerror = fail;
      document.head.appendChild(s);
      setTimeout(fail, 10000);
    };
    var toggle = function () {
      if (ctl.playing()) { userPaused = true; ctl.pause(); }
      else { userPaused = false; ctl.play(); }
    };

    playBtn.addEventListener('click', function () { if (ctl) toggle(); });
    soundBtn.addEventListener('click', function () {
      if (!ctl) return;
      var on = ctl.muted();
      if (on) ctl.unMute(); else ctl.mute();
      soundBtn.setAttribute('aria-pressed', String(on));
      soundBtn.querySelector('span').textContent = on ? 'Sound off' : 'Sound on';
    });
    film.addEventListener('click', function (e) { if (ctl && !e.target.closest('button')) toggle(); });

    if ('IntersectionObserver' in window) {
      // load the player a little before the section arrives, play only while it is on screen
      new IntersectionObserver(function (entries, obs) {
        if (entries[0].isIntersecting) { load(); obs.disconnect(); }
      }, { rootMargin: '400px 0px' }).observe(film);
      new IntersectionObserver(function (entries) {
        inView = entries[0].intersectionRatio >= 0.35;
        if (!ctl) return;
        if (inView && !userPaused) ctl.play();
        else if (!inView && ctl.playing()) ctl.pause();
      }, { threshold: [0, 0.35] }).observe(film);
    } else {
      inView = true;
      load();
    }
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
