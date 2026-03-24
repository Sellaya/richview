/**
 * Expandable mortgage-style cards — click to expand/collapse (card body or chevron).
 * No hover-to-open (CSS must not reveal .product-card children on :hover).
 * Grids: .products-grid or .expandable-card-grid (same markup). Accordion per grid.
 */
(function () {
    var GRID_SELECTORS = ['.products-grid', '.expandable-card-grid'];

    function collectGrids() {
        var seen = new Set();
        var list = [];
        GRID_SELECTORS.forEach(function (sel) {
            document.querySelectorAll(sel).forEach(function (el) {
                if (!seen.has(el)) {
                    seen.add(el);
                    list.push(el);
                }
            });
        });
        return list;
    }

    function init() {
        var grids = collectGrids();
        if (!grids.length) return;

        grids.forEach(function (grid) {
            var cards = grid.querySelectorAll('.product-card');
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
                card.setAttribute('tabindex', '0');

                function toggle() {
                    var isOpen = !card.classList.contains('expanded');
                    cards.forEach(function (c) {
                        if (c !== card) {
                            c.classList.remove('expanded');
                            c.setAttribute('aria-expanded', 'false');
                            var ch = c.querySelector('.product-card-chevron');
                            if (ch) ch.setAttribute('aria-expanded', 'false');
                        }
                    });
                    card.classList.toggle('expanded', isOpen);
                    card.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                    chevron.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                    chevron.setAttribute('aria-label', isOpen ? 'Collapse details' : 'Expand details');
                }

                function handleChevronToggle(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    toggle();
                }

                chevron.addEventListener('click', handleChevronToggle);
                chevron.addEventListener('keydown', function (e) {
                    if (e.key === 'Enter' || e.key === ' ') {
                        handleChevronToggle(e);
                    }
                });

                card.addEventListener('click', function (e) {
                    if (e.target.closest('.product-card-chevron')) return;
                    if (e.target.closest('a')) return;
                    toggle();
                });

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
