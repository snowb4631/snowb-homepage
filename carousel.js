(function () {
  var root = document.getElementById('hero-carousel');
  if (!root) return;
  var track = root.querySelector('.hero-track');
  var slides = track.querySelectorAll('.hero-slide');
  var n = slides.length;
  var dots = root.querySelectorAll('.hero-dots button[role="tab"]');
  var prev = root.querySelector('.hero-nav.prev');
  var next = root.querySelector('.hero-nav.next');
  var play = root.querySelector('.hero-play');
  var DELAY = 5000;

  // 원형 큐: [마지막 복제본, 1 … n, 첫 장 복제본] — 양 끝 복제본에 닿으면 반대쪽 실제 장으로 조용히 옮겨,
  // 마지막 장 다음은 첫 장, 첫 장 이전은 마지막 장이 된다. 실제 i번째 장은 트랙 위치 i + 1 에 있다.
  function cloneOf(slide) {
    var c = slide.cloneNode(true);
    c.setAttribute('aria-hidden', 'true');
    c.querySelectorAll('img').forEach(function (img) { img.alt = ''; img.loading = 'eager'; });
    return c;
  }
  track.insertBefore(cloneOf(slides[n - 1]), slides[0]);
  track.appendChild(cloneOf(slides[0]));

  function pos() { return Math.round(track.scrollLeft / track.clientWidth); }
  function current() { return (pos() - 1 + n) % n; }
  function jump(p) {
    track.style.scrollBehavior = 'auto';
    track.scrollLeft = p * track.clientWidth;
    track.style.scrollBehavior = '';
  }
  function goPos(p) { track.scrollTo({ left: Math.max(0, Math.min(n + 1, p)) * track.clientWidth }); }
  function go(i) { goPos(i + 1); }
  function sync() {
    var p = pos();
    if (dragging) return;
    if (p === 0) jump(n);
    else if (p === n + 1) jump(1);
    var i = current();
    dots.forEach(function (d, k) { d.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
  }

  // 자동 넘김 — 마우스가 올라가 있거나, 포커스가 안에 있거나, 화면 밖이거나, 탭이 숨겨졌으면 쉰다.
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stopped = reduced, hovering = false, focused = false, visible = true, dragging = false, timer;
  function schedule() {
    clearTimeout(timer);
    if (stopped || hovering || focused || dragging || !visible || document.hidden) return;
    timer = setTimeout(function () { go(current() + 1); schedule(); }, DELAY);
  }
  function setStopped(v) {
    stopped = v;
    play.classList.toggle('paused', v);
    play.setAttribute('aria-label', v ? '자동 넘김 시작' : '자동 넘김 정지');
    schedule();
  }

  prev.addEventListener('click', function () { go(current() - 1); schedule(); });
  next.addEventListener('click', function () { go(current() + 1); schedule(); });
  dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); schedule(); }); });
  play.addEventListener('click', function () { setStopped(!stopped); });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(current() - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(current() + 1); }
  });

  // 마우스 드래그로 좌우 넘기기 (터치·트랙패드는 브라우저 기본 스크롤을 그대로 쓴다)
  var startX = 0, startLeft = 0, moved = 0;
  track.addEventListener('pointerdown', function (e) {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    dragging = true; moved = 0; startX = e.clientX; startLeft = track.scrollLeft;
    track.classList.add('dragging');
    try { track.setPointerCapture(e.pointerId); } catch (err) { /* 합성 이벤트 등 캡처 불가 시 무시 */ }
    schedule();
  });
  track.addEventListener('pointermove', function (e) {
    if (!dragging) return;
    moved = e.clientX - startX;
    track.scrollLeft = startLeft - moved;
  });
  function endDrag() {
    if (!dragging) return;
    dragging = false;
    track.classList.remove('dragging');
    var base = Math.round(startLeft / track.clientWidth);
    goPos(Math.abs(moved) > 50 ? base + (moved < 0 ? 1 : -1) : base);
    schedule();
  }
  track.addEventListener('pointerup', endDrag);
  track.addEventListener('pointercancel', endDrag);
  track.addEventListener('click', function (e) { if (Math.abs(moved) > 5) e.preventDefault(); }, true);

  root.addEventListener('mouseenter', function () { hovering = true; schedule(); });
  root.addEventListener('mouseleave', function () { hovering = false; schedule(); });
  root.addEventListener('focusin', function (e) { focused = e.target !== play; schedule(); });
  root.addEventListener('focusout', function () { focused = false; schedule(); });
  document.addEventListener('visibilitychange', schedule);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; schedule(); }, { threshold: 0.4 }).observe(track);
  }

  var t;
  track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(function () { sync(); schedule(); }, 80); }, { passive: true });
  window.addEventListener('resize', function () { jump(current() + 1); sync(); });
  jump(1);
  setStopped(stopped);
  sync();
})();
