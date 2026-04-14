/**
 * Google marketing: Tag Manager and/or gtag (GA4 + Google Ads).
 *
 * Configure in ONE of these ways:
 * 1) Edit the defaults below (replace placeholders with real IDs from Google).
 * 2) Or define window.RICHVIEW_GOOGLE_CONFIG before this script loads:
 *    RICHVIEW_GOOGLE_CONFIG = { gtmId, ga4Id, googleAdsId, adsLeadSendTo }
 *
 * In Google Ads, create a "Submit lead form" (or Website) conversion, then either:
 * - set adsLeadSendTo to the full "send_to" value shown in the tag (AW-xxx/yyyy), or
 * - set googleAdsId + adsLeadConversionLabel separately.
 *
 * GTM: if gtmId is set, only GTM loads here — configure GA4, Google Ads, and
 * Conversion Linker inside the GTM container. This script still pushes
 * dataLayer events (e.g. generate_lead) for your triggers.
 */
(function () {
    var defaults = {
        gtmId: '',
        ga4Id: 'G-YNXH166YHG',
        googleAdsId: 'AW-18038380140',
        adsLeadConversionLabel: '',
        adsLeadSendTo: ''
    };
    var cfg = window.RICHVIEW_GOOGLE_CONFIG || {};
    var GTM_ID = cfg.gtmId != null ? cfg.gtmId : defaults.gtmId;
    var GA4_ID = cfg.ga4Id != null ? cfg.ga4Id : defaults.ga4Id;
    var GOOGLE_ADS_ID = cfg.googleAdsId != null ? cfg.googleAdsId : defaults.googleAdsId;
    var ADS_LEAD_LABEL = cfg.adsLeadConversionLabel != null ? cfg.adsLeadConversionLabel : defaults.adsLeadConversionLabel;
    var ADS_LEAD_SEND_TO = cfg.adsLeadSendTo != null ? cfg.adsLeadSendTo : defaults.adsLeadSendTo;

    function looksLikeGtm(id) {
        return typeof id === 'string' && /^GTM-[A-Z0-9]+$/i.test(id.trim());
    }
    function looksLikeGa4(id) {
        return typeof id === 'string' && /^G-[A-Z0-9]+$/i.test(id.trim());
    }
    function looksLikeAds(id) {
        return typeof id === 'string' && /^AW-[0-9]+$/i.test(id.trim());
    }
    function isPlaceholder(id) {
        if (!id || typeof id !== 'string') return true;
        var t = id.trim();
        return /X{3,}/i.test(t) || /^G-XXXXXXXXXX$/i.test(t) || /^AW-XXXXXXXXXX$/i.test(t) || /^GTM-XXXXXXX$/i.test(t);
    }

    window.dataLayer = window.dataLayer || [];

    function injectGTM(id) {
        (function (w, d, s, l, i) {
            w[l] = w[l] || [];
            w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
            var f = d.getElementsByTagName(s)[0];
            var j = d.createElement(s);
            var dl = l !== 'dataLayer' ? '&l=' + l : '';
            j.async = true;
            j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
            f.parentNode.insertBefore(j, f);
        })(window, document, 'script', 'dataLayer', id);
    }

    function loadGtagAndConfig() {
        var bootId = '';
        if (looksLikeGa4(GA4_ID) && !isPlaceholder(GA4_ID)) bootId = GA4_ID.trim();
        else if (looksLikeAds(GOOGLE_ADS_ID) && !isPlaceholder(GOOGLE_ADS_ID)) bootId = GOOGLE_ADS_ID.trim();
        if (!bootId) return;

        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(bootId);
        document.head.appendChild(s);
        s.onload = function () {
            window.dataLayer = window.dataLayer || [];
            function gtag() {
                window.dataLayer.push(arguments);
            }
            window.gtag = window.gtag || gtag;
            gtag('js', new Date());
            if (looksLikeGa4(GA4_ID) && !isPlaceholder(GA4_ID)) {
                gtag('config', GA4_ID.trim(), { send_page_view: true });
            }
            if (looksLikeAds(GOOGLE_ADS_ID) && !isPlaceholder(GOOGLE_ADS_ID)) {
                gtag('config', GOOGLE_ADS_ID.trim());
            }
        };
    }

    if (looksLikeGtm(GTM_ID) && !isPlaceholder(GTM_ID)) {
        injectGTM(GTM_ID.trim());
    } else if (
        (looksLikeGa4(GA4_ID) && !isPlaceholder(GA4_ID)) ||
        (looksLikeAds(GOOGLE_ADS_ID) && !isPlaceholder(GOOGLE_ADS_ID))
    ) {
        loadGtagAndConfig();
    }

    function buildAdsSendTo() {
        if (ADS_LEAD_SEND_TO && String(ADS_LEAD_SEND_TO).indexOf('/') !== -1) {
            return String(ADS_LEAD_SEND_TO).trim();
        }
        if (looksLikeAds(GOOGLE_ADS_ID) && ADS_LEAD_LABEL && String(ADS_LEAD_LABEL).trim()) {
            return GOOGLE_ADS_ID.trim() + '/' + String(ADS_LEAD_LABEL).trim();
        }
        return '';
    }

    window.RichviewGoogle = window.RichviewGoogle || {};

    /**
     * Call after a successful consultation form submission (before redirect).
     * Pushes dataLayer for GTM; fires GA4 generate_lead + Google Ads conversion when gtag is available.
     */
    window.RichviewGoogle.trackConsultationLead = function (opts) {
        opts = opts || {};
        var formName = opts.form_name || 'Book a Free Consultation';
        var payload = {
            event: 'generate_lead',
            lead_source: 'consultation_form',
            form_name: formName,
            currency: 'CAD'
        };
        window.dataLayer.push(payload);

        if (typeof window.gtag === 'function') {
            window.gtag('event', 'generate_lead', {
                currency: 'CAD',
                value: typeof opts.value === 'number' ? opts.value : 1,
                form_name: formName
            });
            var sendTo = buildAdsSendTo();
            if (sendTo) {
                window.gtag('event', 'conversion', { send_to: sendTo });
            }
        }
    };
})();
