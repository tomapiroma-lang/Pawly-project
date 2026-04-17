/* PAWLY — main.js */

// ---- Scroll animations ----
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const delay = entry.target.dataset.aosDelay || 0;
        setTimeout(() => {
          entry.target.style.animationPlayState = "running";
          entry.target.classList.add("animated");
        }, parseInt(delay));
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll("[data-aos]").forEach((el) => {
  el.style.animationPlayState = "paused";
  observer.observe(el);
});

// ---- Smooth scroll for anchor links ----
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

// ---- Navbar shrink on scroll ----
const nav = document.querySelector(".pawly-nav");
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    nav?.classList.add("scrolled");
  } else {
    nav?.classList.remove("scrolled");
  }
});

// ---- Prefill contact subject from URL param ----
const urlParams = new URLSearchParams(window.location.search);
const subjectParam = urlParams.get("subject");
if (subjectParam) {
  const sel = document.getElementById("subject");
  if (sel) {
    [...sel.options].forEach((opt) => {
      if (opt.text.includes(subjectParam) || opt.value === subjectParam) {
        opt.selected = true;
      }
    });
  }
}
