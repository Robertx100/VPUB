// Theme toggle and state management for vpublication
(function () {
  function getPreferredTheme() {
    const stored = localStorage.getItem('vpub-theme');
    if (stored) {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('vpub-theme', theme);
    updateToggleIcons(theme);
  }

  function updateToggleIcons(theme) {
    const sunIcons = document.querySelectorAll('.theme-icon-sun');
    const moonIcons = document.querySelectorAll('.theme-icon-moon');
    
    sunIcons.forEach(el => {
      if (theme === 'dark') {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    });

    moonIcons.forEach(el => {
      if (theme === 'dark') {
        el.classList.add('hidden');
      } else {
        el.classList.remove('hidden');
      }
    });
  }

  // Initial application
  const initialTheme = getPreferredTheme();
  applyTheme(initialTheme);

  // Global toggle function accessible to DOM
  window.toggleTheme = function () {
    const isDark = document.documentElement.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';
    applyTheme(newTheme);
  };

  // Listen for system changes if user hasn't overridden
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('vpub-theme')) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // DOMContentLoaded update
  document.addEventListener('DOMContentLoaded', () => {
    updateToggleIcons(document.documentElement.classList.contains('dark') ? 'dark' : 'light');
  });
})();
