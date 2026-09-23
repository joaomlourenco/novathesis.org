// Two states, as the platform guidance prescribes: follow the system, or pin
// the opposite of it. Pinning is exact -- pin dark while the system is light,
// and the page stays dark when the system later turns dark. Clicking back to
// whatever the system currently is means "follow the system" again, so the
// preference is dropped rather than pinned to the same value.
(function () {
  var KEY = 'color-scheme';
  var mq = matchMedia('(prefers-color-scheme: dark)');
  var meta = function () { return document.querySelector('meta[name="color-scheme"]'); };
  var sys = function () { return mq.matches ? 'dark' : 'light'; };

  function store(v) {
    try { v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); } catch (e) {}
  }
  function read() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function apply(v) {                       // v: 'light dark' | 'light' | 'dark'
    var r = document.documentElement, m = meta();
    if (m) m.content = v;
    r.classList.toggle('theme-dark', v === 'dark');
    r.classList.toggle('theme-light', v === 'light');
    label(v === 'light dark' ? sys() : v);
  }

  function label(effective) {
    var to = effective === 'dark' ? 'light' : 'dark';
    var txt = document.documentElement.lang === 'pt'
      ? (to === 'dark' ? 'Mudar para o tema escuro' : 'Mudar para o tema claro')
      : (to === 'dark' ? 'Switch to dark theme' : 'Switch to light theme');
    var bs = document.querySelectorAll('.theme-btn');
    for (var i = 0; i < bs.length; i++) {
      bs[i].setAttribute('aria-label', txt);
      bs[i].setAttribute('title', txt);
    }
  }

  apply(read() || 'light dark');
  document.addEventListener('DOMContentLoaded', function () { apply(meta() ? meta().content : 'light dark'); });

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.theme-btn');
    if (!b) return;
    var cur = meta() ? meta().content : 'light dark';
    var next = (cur === 'light dark' ? sys() : cur) === 'dark' ? 'light' : 'dark';
    var v = next === sys() ? 'light dark' : next;
    store(v === 'light dark' ? null : v);
    apply(v);
  });

  // The system setting can change while the page is open; follow it unless pinned.
  mq.addEventListener('change', function () { if (!read()) apply('light dark'); });
})();
