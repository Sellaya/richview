/**
 * Testimonials Read more / Show less
 * Expands to show full review on click.
 * Uses event delegation so duplicated cards in slider work.
 */
(function () {
  'use strict';
  function init() {
    document.body.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('.testimonial-read-more');
      if (!btn) return;
      e.preventDefault();
      e.stopPropagation();
      var card = btn.closest('.testimonial-card');
      if (!card) return;
      var expanded = card.classList.toggle('is-expanded');
      btn.setAttribute('aria-expanded', expanded);
      var span = btn.querySelector('span');
      if (span) {
        span.textContent = expanded ? 'Show less' : 'Read more';
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
