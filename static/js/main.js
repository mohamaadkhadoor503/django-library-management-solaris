"use strict";

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const hasFinePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

/* ---------- Navbar, scroll progress & back-to-top ---------- */

function initScrollEffects() {
    const nav = document.querySelector(".site-nav");
    const progress = document.querySelector(".scroll-progress");
    const backToTop = document.querySelector(".back-to-top");
    let ticking = false;

    const update = () => {
        const scrollY = window.scrollY;
        const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

        nav?.classList.toggle("scrolled", scrollY > 20);
        backToTop?.classList.toggle("show", scrollY > 500);
        progress?.style.setProperty("--progress", maxScroll > 0 ? scrollY / maxScroll : 0);
        ticking = false;
    };

    window.addEventListener("scroll", () => {
        if (!ticking) {
            requestAnimationFrame(update);
            ticking = true;
        }
    }, { passive: true });

    backToTop?.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });

    update();
}

/* ---------- Animated counters ---------- */

function animateCounter(el) {
    const target = Number(el.dataset.count) || 0;

    if (prefersReducedMotion || target === 0) {
        el.textContent = target;
        return;
    }

    const duration = 1600;
    const start = performance.now();

    const step = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);
        el.textContent = Math.round(target * eased);

        if (progress < 1) {
            requestAnimationFrame(step);
        }
    };

    el.textContent = "0";
    requestAnimationFrame(step);
}

/* ---------- Scroll reveal ---------- */

function initReveal() {
    const items = document.querySelectorAll(".reveal");

    // Stagger book cards row by row.
    document.querySelectorAll(".book-col").forEach((col, index) => {
        col.style.setProperty("--d", index % 3);
    });

    if (!("IntersectionObserver" in window)) {
        items.forEach((el) => el.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) {
                return;
            }

            entry.target.classList.add("is-visible");
            entry.target.querySelectorAll("[data-count]").forEach(animateCounter);
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    items.forEach((el) => observer.observe(el));
}

/* ---------- 3D tilt on cards ---------- */

function initTilt() {
    if (prefersReducedMotion || !hasFinePointer) {
        return;
    }

    document.querySelectorAll(".tilt").forEach((card) => {
        card.addEventListener("pointermove", (event) => {
            const rect = card.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;

            card.classList.add("is-tilting");
            card.style.setProperty("--ry", `${x * 10}deg`);
            card.style.setProperty("--rx", `${y * -10}deg`);
        });

        card.addEventListener("pointerleave", () => {
            card.classList.remove("is-tilting");
            card.style.setProperty("--ry", "0deg");
            card.style.setProperty("--rx", "0deg");
        });
    });
}

/* ---------- Magnetic buttons ---------- */

function initMagnetic() {
    if (prefersReducedMotion || !hasFinePointer) {
        return;
    }

    document.querySelectorAll(".magnetic").forEach((btn) => {
        btn.addEventListener("pointermove", (event) => {
            const rect = btn.getBoundingClientRect();
            const x = event.clientX - rect.left - rect.width / 2;
            const y = event.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.2}px, ${y * 0.3}px)`;
        });

        btn.addEventListener("pointerleave", () => {
            btn.style.transform = "";
        });
    });
}

/* ---------- Live book search & category filter ---------- */

function initBookFilter() {
    const grid = document.getElementById("bookGrid");
    const search = document.getElementById("bookSearch");

    if (!grid || !search) {
        return;
    }

    const cards = grid.querySelectorAll(".book-col");
    const chips = document.querySelectorAll(".chip");
    const noResults = document.getElementById("noResults");
    let activeCategory = "all";

    const apply = () => {
        const query = search.value.trim().toLowerCase();
        let visibleCount = 0;

        cards.forEach((card) => {
            const matchesText = card.dataset.search.includes(query);
            const matchesCategory = activeCategory === "all"
                || card.dataset.categories.split("|").includes(activeCategory);
            const visible = matchesText && matchesCategory;
            const wasHidden = card.classList.contains("is-hidden");

            card.classList.toggle("is-hidden", !visible);

            if (visible) {
                visibleCount += 1;
                card.classList.add("is-visible");

                if (wasHidden) {
                    card.classList.remove("is-entering");
                    void card.offsetWidth; // restart the pop-in animation
                    card.classList.add("is-entering");
                }
            }
        });

        noResults?.classList.toggle("d-none", visibleCount > 0);
    };

    search.addEventListener("input", apply);

    // Pre-fill the search from ?q= (e.g. coming from the 404 page).
    const initialQuery = new URLSearchParams(window.location.search).get("q");
    if (initialQuery) {
        search.value = initialQuery;
        apply();
    }

    chips.forEach((chip) => {
        chip.addEventListener("click", () => {
            chips.forEach((c) => c.classList.remove("active"));
            chip.classList.add("active");
            activeCategory = chip.dataset.filter;
            apply();
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initScrollEffects();
    initReveal();
    initTilt();
    initMagnetic();
    initBookFilter();
});
