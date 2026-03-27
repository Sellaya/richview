/**
 * Minimalistic Testimonials Slider
 * Mobile-first touch-enabled slider with keyboard support
 */

class TestimonialsSlider {
  constructor(container) {
    this.container = container;
    this.track = container.querySelector('.testimonials-slider-track');
    this.slides = Array.from(container.querySelectorAll('.testimonial-slide'));
    this.prevBtn = container.querySelector('.testimonials-nav-btn--prev');
    this.nextBtn = container.querySelector('.testimonials-nav-btn--next');
    this.dotsContainer = container.querySelector('.testimonials-dots');

    this.currentIndex = 0;
    this.touchStartX = 0;
    this.touchEndX = 0;
    this.isDragging = false;

    this.init();
  }

  init() {
    if (this.slides.length === 0) return;

    this.createDots();
    this.bindEvents();
    this.updateSlider();
  }

  createDots() {
    if (!this.dotsContainer) return;

    this.slides.forEach((_, index) => {
      const dot = document.createElement('button');
      dot.className = 'testimonials-dot';
      dot.setAttribute('aria-label', `Go to testimonial ${index + 1}`);
      if (index === 0) dot.classList.add('active');

      dot.addEventListener('click', () => {
        this.goToSlide(index);
      });

      this.dotsContainer.appendChild(dot);
    });

    this.dots = Array.from(this.dotsContainer.querySelectorAll('.testimonials-dot'));
  }

  bindEvents() {
    // Navigation buttons
    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.prev());
    }
    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.next());
    }

    // Touch events
    this.track.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: true });
    this.track.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: true });
    this.track.addEventListener('touchend', () => this.handleTouchEnd());

    // Mouse drag events
    this.track.addEventListener('mousedown', (e) => this.handleMouseDown(e));
    this.track.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.track.addEventListener('mouseup', () => this.handleMouseUp());
    this.track.addEventListener('mouseleave', () => this.handleMouseUp());

    // Keyboard navigation
    this.container.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        this.prev();
      } else if (e.key === 'ArrowRight') {
        this.next();
      }
    });

    // Auto-advance (optional)
    // this.startAutoPlay();
  }

  handleTouchStart(e) {
    this.touchStartX = e.touches[0].clientX;
  }

  handleTouchMove(e) {
    this.touchEndX = e.touches[0].clientX;
  }

  handleTouchEnd() {
    const diff = this.touchStartX - this.touchEndX;
    const threshold = 50;

    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        this.next();
      } else {
        this.prev();
      }
    }

    this.touchStartX = 0;
    this.touchEndX = 0;
  }

  handleMouseDown(e) {
    this.isDragging = true;
    this.touchStartX = e.clientX;
    this.track.style.cursor = 'grabbing';
  }

  handleMouseMove(e) {
    if (!this.isDragging) return;
    this.touchEndX = e.clientX;
  }

  handleMouseUp() {
    if (!this.isDragging) return;

    const diff = this.touchStartX - this.touchEndX;
    const threshold = 50;

    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        this.next();
      } else {
        this.prev();
      }
    }

    this.isDragging = false;
    this.touchStartX = 0;
    this.touchEndX = 0;
    this.track.style.cursor = 'grab';
  }

  prev() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.updateSlider();
    }
  }

  next() {
    if (this.currentIndex < this.slides.length - 1) {
      this.currentIndex++;
      this.updateSlider();
    }
  }

  goToSlide(index) {
    if (index >= 0 && index < this.slides.length) {
      this.currentIndex = index;
      this.updateSlider();
    }
  }

  updateSlider() {
    // Move track
    const offset = -this.currentIndex * 100;
    this.track.style.transform = `translateX(${offset}%)`;

    // Update buttons
    if (this.prevBtn) {
      this.prevBtn.disabled = this.currentIndex === 0;
    }
    if (this.nextBtn) {
      this.nextBtn.disabled = this.currentIndex === this.slides.length - 1;
    }

    // Update dots
    if (this.dots) {
      this.dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === this.currentIndex);
      });
    }
  }

  startAutoPlay(interval = 5000) {
    this.autoPlayInterval = setInterval(() => {
      if (this.currentIndex < this.slides.length - 1) {
        this.next();
      } else {
        this.goToSlide(0);
      }
    }, interval);

    // Pause on hover
    this.container.addEventListener('mouseenter', () => {
      clearInterval(this.autoPlayInterval);
    });

    this.container.addEventListener('mouseleave', () => {
      this.startAutoPlay(interval);
    });
  }
}

// Initialize all sliders on page load
document.addEventListener('DOMContentLoaded', () => {
  const sliderContainers = document.querySelectorAll('.testimonials-slider-container');
  sliderContainers.forEach(container => {
    new TestimonialsSlider(container);
  });
});
