(function () {
  var btn = document.getElementById('menu-toggle');
  var drawer = document.getElementById('mobile-drawer');
  var backdrop = document.getElementById('drawer-backdrop');
  if (!btn || !drawer || !backdrop) return;

  function toggle(open) {
    var willOpen = typeof open === 'boolean' ? open : !drawer.classList.contains('open');
    drawer.classList.toggle('open', willOpen);
    backdrop.classList.toggle('open', willOpen);
    btn.classList.toggle('open', willOpen);
    btn.setAttribute('aria-expanded', String(willOpen));
    btn.setAttribute('aria-label', willOpen ? '메뉴 닫기' : '메뉴 열기');
  }

  btn.addEventListener('click', function () { toggle(); });
  backdrop.addEventListener('click', function () { toggle(false); });
  drawer.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { toggle(false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') toggle(false);
  });

  // 카드 상시 부유 — reduced-motion 이면 CSS 가 정지시킴
  document.querySelectorAll('.about-card, .product-card').forEach(function (card) {
    card.classList.add('floatable');
  });
})();
