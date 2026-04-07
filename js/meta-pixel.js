/**
 * Meta (Facebook) Pixel — loaded synchronously so init runs before paint.
 * Pixel ID: 3033942923462161
 */
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '3033942923462161');
fbq('track', 'PageView');

/** After successful GHL webhook: Lead event + short delay so the pixel can send before navigation. */
window.RichviewMetaPixel = window.RichviewMetaPixel || {};
window.RichviewMetaPixel.trackLeadAndRedirect = function (opts) {
    opts = opts || {};
    var contentName = opts.content_name || 'Book a Free Consultation';
    if (typeof fbq === 'function') {
        fbq('track', 'Lead', {
            content_name: contentName,
            content_category: 'consultation'
        });
    }
    var delayMs = typeof fbq === 'function' ? 200 : 0;
    setTimeout(function () {
        window.location.href = '/thank-you/';
    }, delayMs);
};
