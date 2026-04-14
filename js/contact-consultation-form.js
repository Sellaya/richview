(function richviewGhlPostInit() {
    var RICHVIEW_GHL_WEBHOOK_URL = 'https://services.leadconnectorhq.com/hooks/6nNoIJcrYfqxWyIeR9xc/webhook-trigger/cc5524bb-cf46-4c3f-b7a9-ab502924fbe3';
    window.RichviewPostGhl = function (payload) {
        return fetch(RICHVIEW_GHL_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify(payload)
        });
    };
    window.RichviewGhlPayload = {
        leadCategory: function (code) {
            if (code === 'borrowing') return 'Borrower';
            if (code === 'investing') return 'Investor';
            if (code === 'brokering') return 'Broker';
            return String(code || '').trim();
        },
        selectLabel: function (el) {
            if (!el || el.nodeName !== 'SELECT') return '';
            var opt = el.options[el.selectedIndex];
            return opt ? String(opt.textContent || '').trim() : '';
        }
    };
})();

(function consultPhoneTitleInit() {
            var p = document.getElementById('consultPhone');
            if (p && !p.getAttribute('title')) {
                p.setAttribute('title', 'Enter a 10-digit Canadian phone number');
            }
        })();

        (function consultBorrowerLoanTypeInit() {
            var interest = document.getElementById('consultInterest');
            var wrap = document.getElementById('consultBorrowerLoanTypeWrap');
            var loanSel = document.getElementById('consultBorrowerLoanType');
            if (!interest || !wrap || !loanSel) return;
            function sync() {
                var borrowing = interest.value === 'borrowing';
                if (borrowing) {
                    wrap.classList.add('is-visible');
                    wrap.setAttribute('aria-hidden', 'false');
                    loanSel.removeAttribute('tabindex');
                    loanSel.setAttribute('required', 'required');
                } else {
                    wrap.classList.remove('is-visible');
                    wrap.setAttribute('aria-hidden', 'true');
                    loanSel.setAttribute('tabindex', '-1');
                    loanSel.removeAttribute('required');
                    loanSel.selectedIndex = 0;
                }
            }
            interest.addEventListener('change', sync);
            sync();
        })();

        (function() {
            var form = document.getElementById('consultationForm');
            if (!form) return;
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                var submitBtn = document.getElementById('consultSubmitBtn');
                var boxBody   = document.getElementById('ctaBoxBody');
                var successEl = document.getElementById('ctaFormSuccess');
                var spinnerHandle = null;
                if (submitBtn && window.RichviewLottie) {
                    spinnerHandle = window.RichviewLottie.showButtonSpinner(submitBtn, { size: window.innerWidth < 640 ? 18 : 20 });
                } else if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.textContent = 'Sending...';
                }
                var fd = new FormData(form);
                var H = window.RichviewGhlPayload || {};
                var _fn = String(fd.get('consultFirstName') || '').trim();
                var _ln = String(fd.get('consultLastName') || '').trim();
                var _phoneDigits = String(fd.get('consultPhone') || '').replace(/\D/g, '');
                if (_phoneDigits.length !== 10) {
                    alert('Please enter a valid 10-digit phone number.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                    var telEl = document.getElementById('consultPhone');
                    if (telEl && telEl.focus) telEl.focus();
                    return;
                }
                var interestEl = form.querySelector('[name="consultInterest"]');
                var loanEl = form.querySelector('[name="consultBorrowerLoanType"]');
                var _interest = String(fd.get('consultInterest') || (interestEl && interestEl.value) || '').trim();
                var _loanType = String(fd.get('consultBorrowerLoanType') || (loanEl && loanEl.value) || '').trim();
                var _msgRaw = String(fd.get('consultMessage') || '').trim();
                if (_interest === 'borrowing' && !_loanType) {
                    alert('Please select a financing type.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                    return;
                }
                var _date = String(fd.get('consultDate') || '').trim();
                var _time = String(fd.get('consultTime') || '').trim();

                if (!_date || !_time) {
                    alert('Please select both date and time for your consultation.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                    return;
                }

                var pad = function(n) { return (n < 10 ? '0' : '') + n; };
                var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
                var formatTime = function(d) {
                    var h = d.getHours(), min = d.getMinutes(), ampm = h >= 12 ? 'PM' : 'AM';
                    h = h % 12 || 12;
                    return pad(h) + ':' + pad(min) + ' ' + ampm;
                };
                var dtStr = _time.length === 5 ? _date + 'T' + _time + ':00' : _date + 'T' + _time;
                var d = new Date(dtStr);
                var timeStr = !isNaN(d.getTime()) ? formatTime(d) : '';

                var schedule_mm_dd_yyyy = '';
                var schedule_dd_mmm_yyyy = '';
                var schedule_yyyy_mm_dd = '';
                if (!isNaN(d.getTime()) && timeStr) {
                    schedule_mm_dd_yyyy = pad(d.getMonth()+1) + '-' + pad(d.getDate()) + '-' + d.getFullYear() + ' ' + timeStr;
                    schedule_dd_mmm_yyyy = pad(d.getDate()) + '-' + months[d.getMonth()] + '-' + d.getFullYear() + ' ' + timeStr;
                    schedule_yyyy_mm_dd = d.getFullYear() + '-' + pad(d.getMonth()+1) + '-' + pad(d.getDate()) + ' ' + timeStr;
                }
                var schedule_call = [schedule_mm_dd_yyyy, schedule_dd_mmm_yyyy, schedule_yyyy_mm_dd].filter(Boolean).join(', ');
                var interestLabel = H.selectLabel ? H.selectLabel(interestEl) : '';
                var loanLabel = _interest === 'borrowing' && H.selectLabel ? H.selectLabel(loanEl) : '';
                var leadCat = H.leadCategory ? H.leadCategory(_interest) : '';
                var messageForGhl = _msgRaw;
                if (_interest === 'borrowing' && _loanType) {
                    messageForGhl = 'Financing type: ' + _loanType + (_msgRaw ? '\n\n' + _msgRaw : '');
                }
                var _email = String(fd.get('consultEmail') || '').trim();
                var _phone = String(fd.get('consultPhone') || '').trim();
                var payload = {
                    form_name:    'Book a Free Consultation',
                    first_name:   _fn,
                    last_name:    _ln,
                    firstName:    _fn,
                    lastName:     _ln,
                    name:         (_fn + ' ' + _ln).trim(),
                    email:        _email,
                    phone:        _phone,
                    service:      _interest,
                    interest:     _interest,
                    interest_label: interestLabel,
                    service_label: interestLabel,
                    financing_type: _interest === 'borrowing' ? _loanType : '',
                    financing_type_label: loanLabel,
                    lead_category: leadCat,
                    contact_type: leadCat,
                    borrower_loan_type: _interest === 'borrowing' ? _loanType : '',
                    borrower_financing_type: _interest === 'borrowing' ? _loanType : '',
                    borrower_loan_type_label: _interest === 'borrowing' ? loanLabel : '',
                    message:      messageForGhl,
                    message_user: _msgRaw,
                    consultation_date: _date,
                    consultation_time: _time,
                    schedule_call: schedule_call,
                    schedule_mm_dd_yyyy: schedule_mm_dd_yyyy,
                    schedule_dd_mmm_yyyy: schedule_dd_mmm_yyyy,
                    schedule_yyyy_mm_dd: schedule_yyyy_mm_dd,
                    source_url:   window.location.href,
                    page_url:     window.location.href,
                    submitted_at: new Date().toISOString(),
                    user_agent:   navigator.userAgent
                };
                console.log('[GHL] Form submit triggered');
                console.log('[GHL] Payload:', JSON.stringify(payload, null, 2));
                try {
                    var response = await window.RichviewPostGhl(payload);
                    console.log('[GHL] Response status:', response.status, '| ok:', response.ok);
                    if (!response.ok) { throw new Error('Webhook responded with status ' + response.status); }
                    form.reset();
                    if (window.RichviewGoogle && window.RichviewGoogle.trackConsultationLead) {
                        window.RichviewGoogle.trackConsultationLead({ form_name: payload.form_name });
                    }
                    if (window.RichviewMetaPixel && window.RichviewMetaPixel.trackLeadAndRedirect) {
                        window.RichviewMetaPixel.trackLeadAndRedirect({ content_name: payload.form_name });
                    } else {
                        window.location.href = '/thank-you/';
                    }
                } catch (err) {
                    console.error('[GHL] Webhook submission failed:', err);
                    alert('Something went wrong. Please try again or call us directly.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                }
            });
        })();

        (function heroConsultationGhlInit() {
            var form = document.getElementById('heroConsultationForm');
            if (!form) return;
            form.addEventListener('submit', async function (e) {
                e.preventDefault();
                var submitBtn = document.getElementById('heroConsultSubmitBtn');
                var spinnerHandle = null;
                if (submitBtn && window.RichviewLottie) {
                    spinnerHandle = window.RichviewLottie.showButtonSpinner(submitBtn, { size: window.innerWidth < 640 ? 18 : 20 });
                } else if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.textContent = 'Sending...';
                }
                var fd = new FormData(form);
                var H = window.RichviewGhlPayload || {};
                var _fn = String(fd.get('heroConsultFirstName') || '').trim();
                var _ln = String(fd.get('heroConsultLastName') || '').trim();
                var _phoneDigits = String(fd.get('heroConsultPhone') || '').replace(/\D/g, '');
                if (_phoneDigits.length !== 10) {
                    alert('Please enter a valid 10-digit phone number.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                    var telEl = document.getElementById('heroConsultPhone');
                    if (telEl && telEl.focus) telEl.focus();
                    return;
                }
                var interestEl = form.querySelector('[name="heroConsultInterest"]');
                var loanEl = form.querySelector('[name="heroBorrowerLoanType"]');
                var _interest = String(fd.get('heroConsultInterest') || (interestEl && interestEl.value) || '').trim();
                var _loanType = String(fd.get('heroBorrowerLoanType') || (loanEl && loanEl.value) || '').trim();
                var _msgRaw = String(fd.get('heroConsultMessage') || '').trim();
                if (_interest === 'borrowing' && !_loanType) {
                    alert('Please select a financing type.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                    return;
                }
                var _date = String(fd.get('heroConsultDate') || '').trim();
                var _time = String(fd.get('heroConsultTime') || '').trim();
                if (!_date || !_time) {
                    alert('Please select both date and time for your consultation.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                    return;
                }
                var pad = function (n) { return (n < 10 ? '0' : '') + n; };
                var months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
                var formatTime = function (d) {
                    var h = d.getHours(), min = d.getMinutes(), ampm = h >= 12 ? 'PM' : 'AM';
                    h = h % 12 || 12;
                    return pad(h) + ':' + pad(min) + ' ' + ampm;
                };
                var dtStr = _time.length === 5 ? _date + 'T' + _time + ':00' : _date + 'T' + _time;
                var d = new Date(dtStr);
                var timeStr = !isNaN(d.getTime()) ? formatTime(d) : '';
                var schedule_mm_dd_yyyy = '';
                var schedule_dd_mmm_yyyy = '';
                var schedule_yyyy_mm_dd = '';
                if (!isNaN(d.getTime()) && timeStr) {
                    schedule_mm_dd_yyyy = pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + '-' + d.getFullYear() + ' ' + timeStr;
                    schedule_dd_mmm_yyyy = pad(d.getDate()) + '-' + months[d.getMonth()] + '-' + d.getFullYear() + ' ' + timeStr;
                    schedule_yyyy_mm_dd = d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + ' ' + timeStr;
                }
                var schedule_call = [schedule_mm_dd_yyyy, schedule_dd_mmm_yyyy, schedule_yyyy_mm_dd].filter(Boolean).join(', ');
                var interestLabel = H.selectLabel ? H.selectLabel(interestEl) : '';
                var loanLabel = _interest === 'borrowing' && H.selectLabel ? H.selectLabel(loanEl) : '';
                var leadCat = H.leadCategory ? H.leadCategory(_interest) : '';
                var messageForGhl = _msgRaw;
                if (_interest === 'borrowing' && _loanType) {
                    messageForGhl = 'Financing type: ' + _loanType + (_msgRaw ? '\n\n' + _msgRaw : '');
                }
                var _email = String(fd.get('heroConsultEmail') || '').trim();
                var _phone = String(fd.get('heroConsultPhone') || '').trim();
                var payload = {
                    form_name: 'Hero Consultation (Schedule)',
                    first_name: _fn,
                    last_name: _ln,
                    firstName: _fn,
                    lastName: _ln,
                    name: (_fn + ' ' + _ln).trim(),
                    email: _email,
                    phone: _phone,
                    service: _interest,
                    interest: _interest,
                    interest_label: interestLabel,
                    service_label: interestLabel,
                    financing_type: _interest === 'borrowing' ? _loanType : '',
                    financing_type_label: loanLabel,
                    lead_category: leadCat,
                    contact_type: leadCat,
                    borrower_loan_type: _interest === 'borrowing' ? _loanType : '',
                    borrower_financing_type: _interest === 'borrowing' ? _loanType : '',
                    borrower_loan_type_label: _interest === 'borrowing' ? loanLabel : '',
                    message: messageForGhl,
                    message_user: _msgRaw,
                    consultation_date: _date,
                    consultation_time: _time,
                    schedule_call: schedule_call,
                    schedule_mm_dd_yyyy: schedule_mm_dd_yyyy,
                    schedule_dd_mmm_yyyy: schedule_dd_mmm_yyyy,
                    schedule_yyyy_mm_dd: schedule_yyyy_mm_dd,
                    source_url: window.location.href,
                    page_url: window.location.href,
                    submitted_at: new Date().toISOString(),
                    user_agent: navigator.userAgent
                };
                console.log('[GHL] Hero form submit triggered');
                console.log('[GHL] Payload:', JSON.stringify(payload, null, 2));
                try {
                    var response = await window.RichviewPostGhl(payload);
                    console.log('[GHL] Response status:', response.status, '| ok:', response.ok);
                    if (!response.ok) { throw new Error('Webhook responded with status ' + response.status); }
                    form.reset();
                    if (window.RichviewGoogle && window.RichviewGoogle.trackConsultationLead) {
                        window.RichviewGoogle.trackConsultationLead({ form_name: payload.form_name });
                    }
                    if (window.RichviewMetaPixel && window.RichviewMetaPixel.trackLeadAndRedirect) {
                        window.RichviewMetaPixel.trackLeadAndRedirect({ content_name: payload.form_name });
                    } else {
                        window.location.href = '/thank-you/';
                    }
                } catch (err) {
                    console.error('[GHL] Webhook submission failed:', err);
                    alert('Something went wrong. Please try again or call us directly.');
                    if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore();
                    else if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Schedule Consultation'; }
                }
            });
        })();

        (function consultPickerInit() {
            var dateTrigger = document.getElementById('consultDateTrigger');
            var timeTrigger = document.getElementById('consultTimeTrigger');
            var dateDropdown = document.getElementById('consultDateDropdown');
            var timeDropdown = document.getElementById('consultTimeDropdown');
            var dateValueEl = document.getElementById('consultDateValue');
            var timeValueEl = document.getElementById('consultTimeValue');
            var calendarDays = document.getElementById('consultCalendarDays');
            var calendarMonthYear = document.getElementById('consultCalendarMonthYear');
            var timeGrid = document.getElementById('consultTimeGrid');
            var dateInput = document.getElementById('consultDate');
            var timeInput = document.getElementById('consultTime');

            if (!dateTrigger || !timeTrigger || !dateDropdown || !timeDropdown || !calendarDays || !timeGrid || !dateInput || !timeInput) return;

            var selectedDate = null;
            var selectedTime = null;
            var viewYear = new Date().getFullYear();
            var viewMonth = new Date().getMonth();

            function pad(n) { return (n < 10 ? '0' : '') + n; }
            function isWorkingDay(dateObj) {
                var day = dateObj.getDay();
                return day >= 1 && day <= 5; // Mon-Fri only
            }
            function nextWorkingDay(fromDate) {
                var d = new Date(fromDate);
                d.setHours(0, 0, 0, 0);
                while (!isWorkingDay(d)) d.setDate(d.getDate() + 1);
                return d;
            }

            function formatDateDisplay(ymd) {
                if (!ymd) return '';
                var p = ymd.split('-');
                if (p.length !== 3) return ymd;
                var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                return months[parseInt(p[1], 10) - 1] + ' ' + parseInt(p[2], 10) + ', ' + p[0];
            }

            function closeDropdown(dd) { if (dd) dd.classList.remove('is-open'); }
            function openDropdown(dd, trigger) {
                closeDropdown(dateDropdown);
                closeDropdown(timeDropdown);
                dateTrigger.setAttribute('aria-expanded', 'false');
                timeTrigger.setAttribute('aria-expanded', 'false');
                if (dd) dd.classList.add('is-open');
                if (trigger) trigger.setAttribute('aria-expanded', 'true');
            }

            function dayClick(e) {
                var btn = e.currentTarget;
                if (btn.classList.contains('disabled') || btn.classList.contains('other-month')) return;
                selectedDate = btn.dataset.ymd;
                dateInput.value = selectedDate;
                if (dateValueEl) {
                    dateValueEl.textContent = formatDateDisplay(selectedDate);
                    dateValueEl.classList.remove('placeholder');
                }
                renderCalendar();
                setTimeout(function() {
                    closeDropdown(dateDropdown);
                    dateTrigger.setAttribute('aria-expanded', 'false');
                }, 150);
            }

            function renderCalendar() {
                var first = new Date(viewYear, viewMonth, 1);
                var last = new Date(viewYear, viewMonth + 1, 0);
                var startOffset = first.getDay();

                var today = new Date();
                today.setHours(0, 0, 0, 0);

                calendarDays.innerHTML = '';

                for (var i = 0; i < startOffset; i++) {
                    var d = new Date(viewYear, viewMonth, 1 - (startOffset - i));
                    var isPast = d < today;
                    var isWeekend = !isWorkingDay(d);
                    var cell = document.createElement('button');
                    cell.type = 'button';
                    cell.className = 'cta-calendar-day other-month' + ((isPast || isWeekend) ? ' disabled' : '');
                    cell.textContent = d.getDate();
                    cell.dataset.ymd = d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
                    cell.setAttribute('aria-label', d.toLocaleDateString());
                    calendarDays.appendChild(cell);
                }

                for (var day = 1; day <= last.getDate(); day++) {
                    var date = new Date(viewYear, viewMonth, day);
                    var isPast = date < today;
                    var isWeekend = !isWorkingDay(date);
                    var isToday = date.getTime() === today.getTime();
                    var ymd = viewYear + '-' + pad(viewMonth + 1) + '-' + pad(day);
                    var isSelected = selectedDate === ymd;

                    var cell = document.createElement('button');
                    cell.type = 'button';
                    cell.className =
                        'cta-calendar-day' +
                        (isSelected ? ' selected' : '') +
                        (isToday ? ' today' : '') +
                        ((isPast || isWeekend) ? ' disabled' : '');
                    cell.textContent = day;
                    cell.dataset.ymd = ymd;
                    cell.setAttribute('aria-label', date.toLocaleDateString());
                    if (!isPast && !isWeekend) cell.addEventListener('click', dayClick);
                    calendarDays.appendChild(cell);
                }

                var remaining = 42 - calendarDays.children.length;
                for (var j = 0; j < remaining; j++) {
                    var nd = new Date(viewYear, viewMonth + 1, j + 1);
                    var isPast2 = nd < today;
                    var isWeekend2 = !isWorkingDay(nd);
                    var cell = document.createElement('button');
                    cell.type = 'button';
                    cell.className = 'cta-calendar-day other-month' + ((isPast2 || isWeekend2) ? ' disabled' : '');
                    cell.textContent = nd.getDate();
                    cell.dataset.ymd = nd.getFullYear() + '-' + pad(nd.getMonth() + 1) + '-' + pad(nd.getDate());
                    calendarDays.appendChild(cell);
                }

                if (calendarMonthYear) {
                    var monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
                    calendarMonthYear.textContent = monthNames[viewMonth] + ' ' + viewYear;
                }
            }

            function timeClick(e) {
                var btn = e.currentTarget;
                selectedTime = btn.dataset.value;
                timeInput.value = selectedTime;
                if (timeValueEl) {
                    timeValueEl.textContent = btn.dataset.display;
                    timeValueEl.classList.remove('placeholder');
                }
                renderTimeSlots();
                setTimeout(function() {
                    closeDropdown(timeDropdown);
                    timeTrigger.setAttribute('aria-expanded', 'false');
                }, 150);
            }

            function renderTimeSlots() {
                timeGrid.innerHTML = '';
                for (var h = 9; h <= 18; h++) {
                    for (var m = 0; m < 60; m += 30) {
                        if (h === 18 && m > 0) break;
                        var hour = h, min = m;
                        var h12 = hour % 12 || 12;
                        var ampm = hour < 12 ? 'AM' : 'PM';
                        var display = pad(h12) + ':' + pad(min) + ' ' + ampm;
                        var value24 = pad(hour) + ':' + pad(min);

                        var btn = document.createElement('button');
                        btn.type = 'button';
                        btn.className = 'cta-time-slot' + (selectedTime === value24 ? ' selected' : '');
                        btn.textContent = display;
                        btn.dataset.value = value24;
                        btn.dataset.display = display;
                        btn.setAttribute('aria-label', display);
                        btn.addEventListener('click', timeClick);
                        timeGrid.appendChild(btn);
                    }
                }
            }

            dateTrigger.addEventListener('click', function(ev) {
                ev.stopPropagation();
                var isOpen = dateDropdown.classList.contains('is-open');
                if (isOpen) {
                    closeDropdown(dateDropdown);
                    dateTrigger.setAttribute('aria-expanded', 'false');
                    return;
                }

                if (selectedDate) {
                    var parts = selectedDate.split('-');
                    viewYear = parseInt(parts[0], 10);
                    viewMonth = parseInt(parts[1], 10) - 1;
                } else {
                    var t = new Date();
                    viewYear = t.getFullYear();
                    viewMonth = t.getMonth();
                }
                renderCalendar();
                openDropdown(dateDropdown, dateTrigger);
            });

            timeTrigger.addEventListener('click', function(ev) {
                ev.stopPropagation();
                var isOpen = timeDropdown.classList.contains('is-open');
                if (isOpen) {
                    closeDropdown(timeDropdown);
                    timeTrigger.setAttribute('aria-expanded', 'false');
                    return;
                }
                var dateVal = (dateInput.value && dateInput.value.trim()) || '';
                if (dateVal) {
                    selectedDate = dateVal;
                }
                if (!dateVal) {
                    try { dateTrigger.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (err) {}
                    dateTrigger.focus();
                    renderCalendar();
                    openDropdown(dateDropdown, dateTrigger);
                    return;
                }
                renderTimeSlots();
                openDropdown(timeDropdown, timeTrigger);
            });

            var prevBtn = dateDropdown.querySelector('.cta-calendar-prev');
            var nextBtn = dateDropdown.querySelector('.cta-calendar-next');
            if (prevBtn) prevBtn.addEventListener('click', function(ev) {
                ev.stopPropagation();
                viewMonth--;
                if (viewMonth < 0) { viewMonth = 11; viewYear--; }
                renderCalendar();
            });
            if (nextBtn) nextBtn.addEventListener('click', function(ev) {
                ev.stopPropagation();
                viewMonth++;
                if (viewMonth > 11) { viewMonth = 0; viewYear++; }
                renderCalendar();
            });

            var todayBtn = dateDropdown.querySelector('[data-today]');
            if (todayBtn) todayBtn.addEventListener('click', function(ev) {
                ev.stopPropagation();
                var t = nextWorkingDay(new Date());
                selectedDate = t.getFullYear() + '-' + pad(t.getMonth() + 1) + '-' + pad(t.getDate());
                viewYear = t.getFullYear();
                viewMonth = t.getMonth();
                dateInput.value = selectedDate;
                if (dateValueEl) {
                    dateValueEl.textContent = formatDateDisplay(selectedDate);
                    dateValueEl.classList.remove('placeholder');
                }
                renderCalendar();
            });

            document.addEventListener('click', function(e) {
                var t = e.target;
                if (!t || t.nodeType !== 1) return;
                if (dateTrigger.contains(t) || dateDropdown.contains(t) ||
                    timeTrigger.contains(t) || timeDropdown.contains(t)) return;
                if (t.closest && t.closest('label[for="consultDateTrigger"], label[for="consultTimeTrigger"]')) return;
                closeDropdown(dateDropdown);
                closeDropdown(timeDropdown);
                dateTrigger.setAttribute('aria-expanded', 'false');
                timeTrigger.setAttribute('aria-expanded', 'false');
            }, true);

            document.addEventListener('keydown', function(e) {
                if (e.key !== 'Escape') return;
                closeDropdown(dateDropdown);
                closeDropdown(timeDropdown);
                dateTrigger.setAttribute('aria-expanded', 'false');
                timeTrigger.setAttribute('aria-expanded', 'false');
            });

        })();

        (function consultMultistepInit() {
            var form = document.getElementById('consultationForm');
            var steps = form && form.querySelectorAll('.hero-form-step');
            var stepDots = form && form.querySelectorAll('.hero-step-dot');
            var backBtn = document.getElementById('consultFormBackBtn');
            var nextBtn = document.getElementById('consultFormNextBtn');
            var submitBtn = document.getElementById('consultSubmitBtn');
            if (!form || !steps.length || !backBtn || !nextBtn || !submitBtn) return;

            var currentStep = 1;
            var totalSteps = steps.length;

            function goToStep(step) {
                step = Math.max(1, Math.min(step, totalSteps));
                currentStep = step;
                steps.forEach(function(s) {
                    var n = parseInt(s.dataset.step, 10);
                    s.classList.toggle('active', n === step);
                    s.setAttribute('aria-hidden', n !== step);
                });
                stepDots.forEach(function(d) {
                    var n = parseInt(d.dataset.step, 10);
                    d.classList.toggle('active', n === step);
                    d.setAttribute('aria-current', n === step ? 'step' : null);
                });
                backBtn.style.display = step === 1 ? 'none' : '';
                nextBtn.style.display = step === totalSteps ? 'none' : '';
                submitBtn.style.display = step === totalSteps ? 'inline-flex' : 'none';
            }

            function phoneHasTenDigits(el) {
                if (!el || el.type !== 'tel') return true;
                var digits = (el.value || '').replace(/\D/g, '');
                return digits.length === 10;
            }

            function validateStep(step) {
                var panel = form.querySelector('.hero-form-step[data-step="' + step + '"]');
                if (!panel) return true;
                var inputs = panel.querySelectorAll('input[required], select[required], textarea[required]');
                for (var i = 0; i < inputs.length; i++) {
                    var el = inputs[i];
                    if (el.type === 'hidden' ? false : el.offsetParent === null) continue;
                    if (!el.value || (typeof el.value === 'string' && !el.value.trim())) {
                        if (el.type !== 'hidden') el.reportValidity && el.reportValidity();
                        else alert('Please select date and time.');
                        return false;
                    }
                }
                if (step === 1) {
                    var tel = document.getElementById('consultPhone');
                    var telInStep = tel && tel.closest && tel.closest('.hero-form-step.active');
                    if (telInStep && !phoneHasTenDigits(tel)) {
                        tel.setCustomValidity('Please enter a 10-digit phone number.');
                        if (tel.reportValidity) tel.reportValidity();
                        tel.setCustomValidity('');
                        return false;
                    }
                }
                return true;
            }

            backBtn.addEventListener('click', function() { goToStep(currentStep - 1); });
            nextBtn.addEventListener('click', function() {
                if (validateStep(currentStep)) goToStep(currentStep + 1);
            });
            stepDots.forEach(function(dot) {
                dot.addEventListener('click', function() {
                    var step = parseInt(this.dataset.step, 10);
                    if (step < currentStep) goToStep(step);
                    else if (step > currentStep && validateStep(currentStep)) goToStep(step);
                });
            });
            goToStep(1);
        })();

        (function () {
            function fmtCA(el) {
                var d = el.value.replace(/\D/g, '').slice(0, 10);
                var out = '';
                if      (d.length === 0) out = '';
                else if (d.length <= 3)  out = '(' + d;
                else if (d.length <= 6)  out = '(' + d.slice(0,3) + ') ' + d.slice(3);
                else                     out = '(' + d.slice(0,3) + ') ' + d.slice(3,6) + '-' + d.slice(6);
                if (out !== el.value) {
                    el.value = out;
                    try { el.setSelectionRange(out.length, out.length); } catch(e) {}
                }
            }
            document.querySelectorAll('input[type="tel"]').forEach(function (el) {
                el.setAttribute('maxlength', '14');
                el.setAttribute('inputmode', 'numeric');
                el.setAttribute('autocomplete', 'tel-national');
                el.addEventListener('input', function () {
                    fmtCA(this);
                    this.setCustomValidity('');
                });
                el.addEventListener('keydown', function (e) {
                    // Allow: backspace(8), delete(46), tab(9), enter(13), esc(27),
                    //        arrows(35-40), and ctrl/cmd shortcuts
                    var navKeys = [8, 9, 13, 27, 35, 36, 37, 38, 39, 40, 46];
                    if (navKeys.indexOf(e.keyCode) !== -1) return;
                    if ((e.ctrlKey || e.metaKey) && [65, 67, 86, 88].indexOf(e.keyCode) !== -1) return;
                    if (e.key && !/^\d$/.test(e.key)) e.preventDefault();
                });
                el.addEventListener('paste', function (e) {
                    e.preventDefault();
                    var pasted = (e.clipboardData || window.clipboardData).getData('text');
                    this.value = pasted.replace(/\D/g, '').slice(0, 10);
                    fmtCA(this);
                });
            });
        })();

        (function contactCtaRevealInit() {
    if (!document.getElementById('contact')) return;
    var els = document.querySelectorAll('#contact .reveal');
    if (!els.length) return;
    if (!window.IntersectionObserver) {
        els.forEach(function (el) { el.classList.add('visible'); });
        return;
    }
    var o = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
    els.forEach(function (el) { o.observe(el); });
})();
