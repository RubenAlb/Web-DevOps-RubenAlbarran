// Racing World - JavaScript

// ===== DARK MODE =====
// Inicializar tema desde localStorage
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

// Actualizar icono del botón de tema
function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// Toggle del tema
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tema
    initTheme();
    
    // Event listener para el botón de cambio de tema
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Efecto de transición suave
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg)';
            }, 300);
        });
    }
    
    // Agregar animación a los elementos cuando aparecen
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });

    // Observar todas las cards
    const cards = document.querySelectorAll('.card, .carrera-card, .curiosidad-card');
    cards.forEach(card => observer.observe(card));
});

// ===== ANIMACIONES Y EFECTOS =====

// Efecto de hover mejorado para las cards
document.querySelectorAll('.card, .carrera-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transition = 'all 0.3s ease';
    });
});

// Scroll suave para los enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Función para resaltar el enlace activo en la navegación
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Ejecutar al cargar la página
highlightActiveNavLink();

// Agregar efecto de carga mejorado
window.addEventListener('load', function() {
    // Fade in inicial de la página
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
    
    // Animar cards con delay
    const allCards = document.querySelectorAll('.card, .carrera-card, .curiosidad-card');
    allCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 50));
    });
});

// Efecto parallax en el scroll
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const header = document.querySelector('header');
    
    if (header) {
        header.style.transform = `translateY(${scrolled * 0.3}px)`;
        header.style.opacity = 1 - (scrolled / 500);
    }
    
    // Mostrar/ocultar botón scroll to top
    const scrollToTopBtn = document.getElementById('scroll-to-top');
    if (scrollToTopBtn) {
        if (scrolled > 300) {
            scrollToTopBtn.classList.add('visible');
        } else {
            scrollToTopBtn.classList.remove('visible');
        }
    }
});

// Scroll to top button functionality
const scrollToTopBtn = document.getElementById('scroll-to-top');
if (scrollToTopBtn) {
    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Animación de números contador (para estadísticas)
function animateCounter(element, target, duration = 1000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(function() {
        start += increment;
        if (start >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(start);
        }
    }, 16);
}

// Activar contadores en estadísticas si existen
const counters = document.querySelectorAll('.stat-value');
if (counters.length > 0) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const target = parseInt(entry.target.dataset.target || entry.target.textContent);
                animateCounter(entry.target, target);
                entry.target.dataset.animated = 'true';
            }
        });
    });
    
    counters.forEach(counter => observer.observe(counter));
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️'
    };
    
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close">×</button>
    `;
    
    container.appendChild(toast);
    
    // Close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.style.animation = 'slideInFromRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    });
    
    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideInFromRight 0.3s ease reverse';
                setTimeout(() => toast.remove(), 300);
            }
        }, duration);
    }
}

// Exponer función globalmente
window.showToast = showToast;

console.log('🏁 Racing World cargado correctamente');
