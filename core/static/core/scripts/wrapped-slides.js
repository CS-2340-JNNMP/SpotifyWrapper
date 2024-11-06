// Keep track of which slide we're on
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');
const dots = document.querySelectorAll('.dot');

// Function to update which slide is showing
function showSlide(n) {
    // Hide all slides first
    slides.forEach(slide => {
        slide.style.display = 'none';
    });

    // Remove active class from all dots
    dots.forEach(dot => {
        dot.classList.remove('active');
    });

    // Show the specified slide
    slides[n].style.display = 'flex';

    // Add active class to the corresponding dot
    dots[n].classList.add('active');
}

// Function to go to a specific slide (called when dots are clicked)
function goToSlide(n) {
    currentSlide = n;
    showSlide(currentSlide);
}

// Function to move slides (for prev/next buttons)
function moveSlide(n) {
    currentSlide += n;

    // Handle wrapping around at the ends
    if (currentSlide >= slides.length) {
        currentSlide = 0;
    }
    if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }

    showSlide(currentSlide);
}

// Initialize the first slide
document.addEventListener('DOMContentLoaded', () => {
    showSlide(currentSlide);
});