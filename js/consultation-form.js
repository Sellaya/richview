const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

class ConsultationForm {
  constructor() {
    this.form = document.getElementById('consultationForm');
    this.scheduleSection = document.getElementById('consultScheduleSection');
    this.nextBtn = document.getElementById('consultFormNextBtn');
    this.backBtn = document.getElementById('consultFormBackBtn');
    this.submitBtn = document.getElementById('consultSubmitBtn');
    this.nextWrap = document.getElementById('consultNextWrap');
    this.backWrap = document.getElementById('consultBackWrap');
    this.submitWrap = document.getElementById('consultSubmitWrap');
    this.formFields = document.querySelector('.cta-form-fields');
    this.successMessage = document.getElementById('ctaFormSuccess');

    this.currentStep = 1;
    this.selectedDate = null;
    this.selectedTime = null;

    this.init();
  }

  init() {
    if (!this.form) return;

    this.scheduleSection.style.display = 'none';
    this.backWrap.style.display = 'none';
    this.submitWrap.style.display = 'none';

    this.initCalendar();
    this.initTimePicker();
    this.attachEventListeners();
  }

  attachEventListeners() {
    this.nextBtn?.addEventListener('click', () => this.goToStep2());
    this.backBtn?.addEventListener('click', () => this.goToStep1());
    this.form?.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  validateStep1() {
    const firstName = document.getElementById('consultFirstName').value.trim();
    const lastName = document.getElementById('consultLastName').value.trim();
    const email = document.getElementById('consultEmail').value.trim();
    const phone = document.getElementById('consultPhone').value.trim();
    const interest = document.getElementById('consultInterest').value;
    const message = document.getElementById('consultMessage').value.trim();

    if (!firstName || !lastName || !email || !phone || !interest || !message) {
      this.showError('Please fill out all required fields');
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      this.showError('Please enter a valid email address');
      return false;
    }

    return true;
  }

  validateStep2() {
    if (!this.selectedDate || !this.selectedTime) {
      this.showError('Please select both a date and time for your consultation');
      return false;
    }
    return true;
  }

  goToStep2() {
    if (!this.validateStep1()) return;

    this.currentStep = 2;
    this.scheduleSection.style.display = 'block';
    this.nextWrap.style.display = 'none';
    this.backWrap.style.display = 'block';
    this.submitWrap.style.display = 'block';

    this.scheduleSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  goToStep1() {
    this.currentStep = 1;
    this.scheduleSection.style.display = 'none';
    this.nextWrap.style.display = 'block';
    this.backWrap.style.display = 'none';
    this.submitWrap.style.display = 'none';
  }

  async handleSubmit(e) {
    e.preventDefault();

    if (!this.validateStep2()) return;

    this.setSubmitButtonLoading(true);

    const formData = {
      first_name: document.getElementById('consultFirstName').value.trim(),
      last_name: document.getElementById('consultLastName').value.trim(),
      email: document.getElementById('consultEmail').value.trim(),
      phone: document.getElementById('consultPhone').value.trim(),
      interest: document.getElementById('consultInterest').value,
      message: document.getElementById('consultMessage').value.trim(),
      consultation_date: this.selectedDate,
      consultation_time: this.selectedTime,
      user_agent: navigator.userAgent,
    };

    try {
      const apiUrl = `${SUPABASE_URL}/functions/v1/submit-consultation`;

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Failed to submit consultation request');
      }

      this.showSuccess();
      this.form.reset();
      this.selectedDate = null;
      this.selectedTime = null;

      setTimeout(() => {
        window.location.href = '/thank-you.html';
      }, 2000);

    } catch (error) {
      console.error('Form submission error:', error);
      this.showError('Unable to submit your request. Please try again or call us at (416) 300-4448.');
    } finally {
      this.setSubmitButtonLoading(false);
    }
  }

  setSubmitButtonLoading(loading) {
    if (loading) {
      this.submitBtn.disabled = true;
      this.submitBtn.textContent = 'Submitting...';
    } else {
      this.submitBtn.disabled = false;
      this.submitBtn.textContent = 'Schedule Consultation';
    }
  }

  showSuccess() {
    this.formFields.style.display = 'none';
    this.successMessage.style.display = 'block';
  }

  showError(message) {
    const existingError = document.querySelector('.form-error-message');
    if (existingError) {
      existingError.remove();
    }

    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error-message';
    errorDiv.style.cssText = 'background: #fee; border: 1px solid #fcc; color: #c33; padding: 12px; border-radius: 6px; margin: 16px 0; font-size: 14px;';
    errorDiv.textContent = message;

    if (this.currentStep === 1) {
      this.nextWrap.parentNode.insertBefore(errorDiv, this.nextWrap);
    } else {
      this.submitWrap.parentNode.insertBefore(errorDiv, this.submitWrap);
    }

    setTimeout(() => errorDiv.remove(), 5000);
  }

  initCalendar() {
    const dateTrigger = document.getElementById('consultDateTrigger');
    const dateDropdown = document.getElementById('consultDateDropdown');
    const dateValue = document.getElementById('consultDateValue');
    const dateInput = document.getElementById('consultDate');
    const calendarDays = document.getElementById('consultCalendarDays');
    const monthYear = document.getElementById('consultCalendarMonthYear');
    const prevBtn = dateDropdown?.querySelector('.cta-calendar-prev');
    const nextBtn = dateDropdown?.querySelector('.cta-calendar-next');
    const todayBtn = dateDropdown?.querySelector('[data-today]');

    let currentDate = new Date();
    let displayMonth = currentDate.getMonth();
    let displayYear = currentDate.getFullYear();

    const renderCalendar = () => {
      const firstDay = new Date(displayYear, displayMonth, 1);
      const lastDay = new Date(displayYear, displayMonth + 1, 0);
      const prevLastDay = new Date(displayYear, displayMonth, 0);
      const firstDayIndex = firstDay.getDay();
      const lastDayDate = lastDay.getDate();
      const prevLastDayDate = prevLastDay.getDate();

      monthYear.textContent = firstDay.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

      let daysHTML = '';

      for (let i = firstDayIndex; i > 0; i--) {
        daysHTML += `<button type="button" class="cta-calendar-day disabled" disabled>${prevLastDayDate - i + 1}</button>`;
      }

      for (let day = 1; day <= lastDayDate; day++) {
        const date = new Date(displayYear, displayMonth, day);
        const dateString = date.toISOString().split('T')[0];
        const isToday = dateString === new Date().toISOString().split('T')[0];
        const isPast = date < new Date(new Date().setHours(0, 0, 0, 0));
        const isSelected = dateString === this.selectedDate;

        let className = 'cta-calendar-day';
        if (isToday) className += ' today';
        if (isPast) className += ' disabled';
        if (isSelected) className += ' selected';

        daysHTML += `<button type="button" class="${className}" data-date="${dateString}" ${isPast ? 'disabled' : ''}>${day}</button>`;
      }

      calendarDays.innerHTML = daysHTML;

      calendarDays.querySelectorAll('.cta-calendar-day:not(.disabled)').forEach(btn => {
        btn.addEventListener('click', () => {
          const dateString = btn.dataset.date;
          this.selectedDate = dateString;
          dateInput.value = dateString;

          const date = new Date(dateString);
          dateValue.textContent = date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
          dateValue.classList.remove('placeholder');

          dateDropdown.classList.remove('open');
          dateTrigger.setAttribute('aria-expanded', 'false');
        });
      });
    };

    dateTrigger?.addEventListener('click', () => {
      const isOpen = dateDropdown.classList.contains('open');
      dateDropdown.classList.toggle('open');
      dateTrigger.setAttribute('aria-expanded', !isOpen);

      document.getElementById('consultTimeDropdown')?.classList.remove('open');
    });

    prevBtn?.addEventListener('click', () => {
      displayMonth--;
      if (displayMonth < 0) {
        displayMonth = 11;
        displayYear--;
      }
      renderCalendar();
    });

    nextBtn?.addEventListener('click', () => {
      displayMonth++;
      if (displayMonth > 11) {
        displayMonth = 0;
        displayYear++;
      }
      renderCalendar();
    });

    todayBtn?.addEventListener('click', () => {
      displayMonth = currentDate.getMonth();
      displayYear = currentDate.getFullYear();
      renderCalendar();
    });

    document.addEventListener('click', (e) => {
      if (!dateTrigger?.contains(e.target) && !dateDropdown?.contains(e.target)) {
        dateDropdown?.classList.remove('open');
        dateTrigger?.setAttribute('aria-expanded', 'false');
      }
    });

    renderCalendar();
  }

  initTimePicker() {
    const timeTrigger = document.getElementById('consultTimeTrigger');
    const timeDropdown = document.getElementById('consultTimeDropdown');
    const timeValue = document.getElementById('consultTimeValue');
    const timeInput = document.getElementById('consultTime');
    const timeGrid = document.getElementById('consultTimeGrid');

    const timeSlots = [
      '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM',
      '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM',
      '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM',
      '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM',
      '5:00 PM'
    ];

    let timeSlotsHTML = '';
    timeSlots.forEach(slot => {
      timeSlotsHTML += `<button type="button" class="cta-time-slot" data-time="${slot}">${slot}</button>`;
    });
    timeGrid.innerHTML = timeSlotsHTML;

    timeGrid.querySelectorAll('.cta-time-slot').forEach(btn => {
      btn.addEventListener('click', () => {
        this.selectedTime = btn.dataset.time;
        timeInput.value = btn.dataset.time;
        timeValue.textContent = btn.dataset.time;
        timeValue.classList.remove('placeholder');

        timeGrid.querySelectorAll('.cta-time-slot').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');

        timeDropdown.classList.remove('open');
        timeTrigger.setAttribute('aria-expanded', 'false');
      });
    });

    timeTrigger?.addEventListener('click', () => {
      const isOpen = timeDropdown.classList.contains('open');
      timeDropdown.classList.toggle('open');
      timeTrigger.setAttribute('aria-expanded', !isOpen);

      document.getElementById('consultDateDropdown')?.classList.remove('open');
    });

    document.addEventListener('click', (e) => {
      if (!timeTrigger?.contains(e.target) && !timeDropdown?.contains(e.target)) {
        timeDropdown?.classList.remove('open');
        timeTrigger?.setAttribute('aria-expanded', 'false');
      }
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new ConsultationForm());
} else {
  new ConsultationForm();
}
