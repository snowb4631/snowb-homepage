(function () {
  var root = document.getElementById('hero-carousel');
  if (!root) return;
  var track = root.querySelector('.hero-track');
  var slides = track.querySelectorAll('.hero-slide');
  var dots = root.querySelectorAll('.hero-dots button');
  var prev = root.querySelector('.hero-nav.prev');
  var next = root.querySelector('.hero-nav.next');

  function current() { return Math.round(track.scrollLeft / track.clientWidth); }
  function go(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    track.scrollTo({ left: i * track.clientWidth });
  }
  function sync() {
    var i = current();
    dots.forEach(function (d, k) { d.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
  }

  prev.addEventListener('click', function () { go(current() - 1); });
  next.addEventListener('click', function () { go(current() + 1); });
  dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); }); });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(current() - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(current() + 1); }
  });
  var t;
  track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(sync, 60); }, { passive: true });
  window.addEventListener('resize', sync);
  sync();
})();
