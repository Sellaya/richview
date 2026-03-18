/**
 * Product cards — hover (desktop) / chevron click (mobile, accordion)
 * Desktop: hover to expand, no click needed
 * Mobile: click chevron only to expand; opening one closes others
 */
(function () {
    function init() {
        var grids = document.querySelectorAll('.products-grid');
        if (!grids.length) return;

        grids.forEach(function (grid) {
            var cards = grid.querySelectorAll('.product-card');
            var isTouchLike = window.matchMedia('(hover: none), (pointer: coarse)').matches;
        cards.forEach(function (card) {
            if (card.hasAttribute('data-expand-inited')) return;
            card.setAttribute('data-expand-inited', 'true');

            var top = card.querySelector('.product-card-top');
            if (!top) return;

            var chevron = top.querySelector('.product-card-chevron');
            if (!chevron) {
                chevron = document.createElement('button');
                chevron.className = 'product-card-chevron';
                chevron.type = 'button';
                chevron.setAttribute('aria-label', 'Expand details');
                chevron.setAttribute('aria-expanded', 'false');
                top.appendChild(chevron);
            }

            card.setAttribute('aria-expanded', 'false');

            function closeOthers() {
                cards.forEach(function (c) {
                    if (c !== card) {
                        c.classList.remove('expanded');
                        c.setAttribute('aria-expanded', 'false');
                        var ch = c.querySelector('.product-card-chevron');
                        if (ch) ch.setAttribute('aria-expanded', 'false');
                    }
                });
            }

            function toggle() {
                var isOpen = !card.classList.contains('expanded');
                closeOthers();
                card.classList.toggle('expanded', isOpen);
                card.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                chevron.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                chevron.setAttribute('aria-label', isOpen ? 'Collapse details' : 'Expand details');
            }

            // Chevron click: accordion behavior (mobile + desktop)
            chevron.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                toggle();
            });

            // Mobile/touch: allow tapping anywhere on the card to toggle.
            if (isTouchLike) {
                card.addEventListener('click', function (e) {
                    if (e.target.closest('.product-card-chevron')) return;
                    toggle();
                });
            }

            // Keyboard accessibility for focused card container.
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggle();
                }
            });
        });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
