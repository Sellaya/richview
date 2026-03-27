/**
 * Lottie animation utilities - Richview Capital
 * Mobile-first, prefers-reduced-motion compliant
 * CSS fallbacks when Lottie unavailable
 */

(function (global) {
  'use strict';

  var LOTTIE_VERSION = '5.12.2';
  var LOTTIE_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/lottie-web/' + LOTTIE_VERSION + '/lottie.min.js';
  var SPINNER_URL = 'lottie/forms/spinner-loading.json';
  var SUCCESS_URL = 'lottie/forms/success-check.json';
  /* Fallback CDN URLs - minimal, fintech-appropriate (LottieFiles) */
  var SPINNER_CDN = 'https://assets10.lottiefiles.com/packages/lf20_sz1efvkm.json';
  var SUCCESS_CDN = 'https://assets10.lottiefiles.com/packages/lf20_zk3c2dlm.json';

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function loadScript(url) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = url;
      s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function loadLottie() {
    if (global.lottie) return Promise.resolve(global.lottie);
    return loadScript(LOTTIE_CDN).then(function () { return global.lottie; });
  }

  function tryUrl(base, fallback) {
    return base.indexOf('/') === 0 || base.indexOf('http') === 0 ? base : (document.location.pathname.replace(/\/[^/]*$/, '/') + base);
  }

  function createSpinnerFallback(size) {
    var wrap = document.createElement('span');
    wrap.className = 'lottie-spinner-fallback';
    wrap.setAttribute('aria-hidden', 'true');
    wrap.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;width:' + (size || 20) + 'px;height:' + (size || 20) + 'px;';
    wrap.innerHTML = '<svg width="' + (size || 20) + '" height="' + (size || 20) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10" opacity="0.25"/><path d="M12 2a10 10 0 0 1 10 10" class="lottie-spinner-arc"/></svg>';
    return wrap;
  }

  function createSuccessFallback(size) {
    var wrap = document.createElement('span');
    wrap.className = 'lottie-success-fallback';
    wrap.setAttribute('aria-hidden', 'true');
    wrap.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;width:' + (size || 48) + 'px;height:' + (size || 48) + 'px;';
    wrap.innerHTML = '<svg width="' + (size || 48) + '" height="' + (size || 48) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path class="lottie-success-path" d="M5 13l4 4L19 7"/></svg>';
    return wrap;
  }

  /**
   * Show loading spinner in button (or container)
   * @param {HTMLElement} el - Button or container
   * @param {Object} opts - { size: number, useLottie: boolean }
   * @returns {{ destroy: function, restore: function }}
   */
  function showButtonSpinner(el, opts) {
    opts = opts || {};
    var size = opts.size || 20;
    /* CSS-only by default for reliability; set useLottie: true when JSON files exist */
    var useLottie = opts.useLottie === true && !prefersReducedMotion();
    var originalHTML = el.innerHTML;
    var originalDisabled = el.disabled;
    var container = document.createElement('span');
    container.className = 'lottie-spinner-wrap';
    container.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;';
    el.disabled = true;
    el.classList.add('btn-loading');

    function restore() {
      el.disabled = originalDisabled;
      el.classList.remove('btn-loading');
      el.innerHTML = originalHTML;
    }

    function tryLottie() {
      loadLottie().then(function (lottie) {
        var div = document.createElement('div');
        div.style.cssText = 'width:' + size + 'px;height:' + size + 'px;';
        container.appendChild(div);
        var inst = lottie.loadAnimation({
          container: div,
          renderer: 'svg',
          loop: true,
          autoplay: true,
          path: tryUrl(SPINNER_URL) + '?' + Date.now()
        });
        inst.addEventListener('data_failed', function () {
          tryFallback();
        });
        container._lottie = inst;
      }).catch(tryFallback);
    }

    function tryFallback() {
      if (container.querySelector('.lottie-spinner-fallback')) return;
      var fallback = createSpinnerFallback(size);
      container.innerHTML = '';
      container.appendChild(fallback);
    }

    container.appendChild(createSpinnerFallback(size));
    el.innerHTML = '';
    el.appendChild(container);
    if (useLottie) {
      fetch(tryUrl(SPINNER_URL)).then(function (r) { return r.ok ? r.json() : Promise.reject(); })
        .then(function () {
          container.innerHTML = '';
          var div = document.createElement('div');
          div.style.cssText = 'width:' + size + 'px;height:' + size + 'px;';
          container.appendChild(div);
          loadLottie().then(function (lottie) {
            container._lottie = lottie.loadAnimation({
              container: div,
              renderer: 'svg',
              loop: true,
              autoplay: true,
              path: tryUrl(SPINNER_URL)
            });
          }).catch(function () {});
        }).catch(function () {
          tryLottie();
        });
    }

    return { destroy: restore, restore: restore };
  }

  /**
   * Show success checkmark (play once)
   * @param {HTMLElement} container
   * @param {Object} opts - { size: number, useLottie: boolean, onComplete: function }
   */
  function showSuccessCheck(container, opts) {
    opts = opts || {};
    var size = opts.size || 48;
    var useLottie = opts.useLottie === true && !prefersReducedMotion();
    var inner = document.createElement('div');
    inner.className = 'lottie-success-wrap';
    inner.style.cssText = 'width:' + size + 'px;height:' + size + 'px;display:flex;align-items:center;justify-content:center;';
    container.innerHTML = '';
    container.appendChild(inner);

    var fallback = createSuccessFallback(size);
    inner.appendChild(fallback);
    fallback.querySelector('.lottie-success-path').style.animation = 'lottieSuccessDraw 0.6s cubic-bezier(0.16,1,0.3,1) 0.15s forwards';
    fallback.querySelector('.lottie-success-path').style.strokeDasharray = '24';
    fallback.querySelector('.lottie-success-path').style.strokeDashoffset = '24';

    if (opts.onComplete) setTimeout(opts.onComplete, 800);

    if (useLottie) {
      fetch(tryUrl(SUCCESS_URL)).then(function (r) { return r.ok ? r.json() : Promise.reject(); })
        .then(function () {
          inner.innerHTML = '';
          var div = document.createElement('div');
          div.style.cssText = 'width:' + size + 'px;height:' + size + 'px;';
          inner.appendChild(div);
          loadLottie().then(function (lottie) {
            var inst = lottie.loadAnimation({
              container: div,
              renderer: 'svg',
              loop: false,
              autoplay: true,
              path: tryUrl(SUCCESS_URL)
            });
            inst.addEventListener('complete', function () {
              if (opts.onComplete) opts.onComplete();
            });
          });
        }).catch(function () {});
    }
  }

  global.RichviewLottie = {
    showButtonSpinner: showButtonSpinner,
    showSuccessCheck: showSuccessCheck,
    prefersReducedMotion: prefersReducedMotion
  };
})(typeof window !== 'undefined' ? window : this);
