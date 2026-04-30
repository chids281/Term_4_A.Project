// Keeps track of the current slide index
let currentSlide = 0;

// Select all slides and dots from the DOM
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");

// Get Next and Back buttons
const nextBtn = document.getElementById("nextBtn");
const backBtn = document.getElementById("backBtn");


// ======================
// SHOW SLIDE FUNCTION
// ======================
function showSlide(index) {

    // Remove active class from all slides
    slides.forEach(slide => slide.classList.remove("active"));

    // Remove active style from all dots
    dots.forEach(dot => dot.classList.remove("active-dot"));

    // Activate the selected slide
    slides[index].classList.add("active");

    // Activate corresponding dot
    dots[index].classList.add("active-dot");


    // ======================
    // NEXT BUTTON TEXT
    // ======================

    // If last slide → change button to "Get Started"
    if (index === slides.length - 1) {
        nextBtn.innerText = "Get Started";
    } else {
        nextBtn.innerText = "Next";
    }


    // ======================
    // BACK BUTTON VISIBILITY
    // ======================

    // Hide back button on first slide
    if (index === 0) {
        backBtn.style.display = "none";
    } else {
        backBtn.style.display = "block";
    }
}


// ======================
// NEXT SLIDE FUNCTION
// ======================
function nextSlide() {

    // If not on last slide → move forward
    if (currentSlide < slides.length - 1) {
        currentSlide++;
        showSlide(currentSlide);

    } else {
        // If last slide → redirect to auth page
        window.location.href = "/auth/";
    }
}


// ======================
// PREVIOUS SLIDE FUNCTION
// ======================
function prevSlide() {

    // Move back only if not on first slide
    if (currentSlide > 0) {
        currentSlide--;
        showSlide(currentSlide);
    }
}


// ======================
// SKIP FUNCTION
// ======================
function skipOnboarding() {

    // Skip onboarding completely
    window.location.href = "/auth/";
}


// ======================
// INITIALIZATION
// ======================

// Show the first slide when page loads
showSlide(currentSlide);