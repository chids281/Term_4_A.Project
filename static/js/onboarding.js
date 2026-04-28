let currentSlide = 0;

const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");
const nextBtn = document.getElementById("nextBtn");
const backBtn = document.getElementById("backBtn");

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active-dot"));

    slides[index].classList.add("active");
    dots[index].classList.add("active-dot");

    // Handle Next button text
    if (index === slides.length - 1) {
        nextBtn.innerText = "Get Started";
    } else {
        nextBtn.innerText = "Next";
    }

    // Handle Back button visibility
    if (index === 0) {
        backBtn.style.display = "none";
    } else {
        backBtn.style.display = "block";
    }
}

function nextSlide() {
    if (currentSlide < slides.length - 1) {
        currentSlide++;
        showSlide(currentSlide);
    } else {
        window.location.href = "/auth/";
    }
}

function prevSlide() {
    if (currentSlide > 0) {
        currentSlide--;
        showSlide(currentSlide);
    }
}

function skipOnboarding() {
    window.location.href = "/auth/";
}

// Initialize
showSlide(currentSlide);