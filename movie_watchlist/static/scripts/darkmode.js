let darkMode = localStorage.getItem('darkMode');
const docBody = document.body;
const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
const darkModeToggle = document.querySelector('#toggle-theme');
const themeColor = document.querySelector('meta[name="theme-color"]');

const enableDarkMode = () => {
  docBody.classList.add('dark-mode');
  themeColor.setAttribute('content', '#1c2023');
};

const disableDarkMode = () => {
  docBody.classList.remove('dark-mode');
  themeColor.setAttribute('content', '#fafafa');
};

if (darkMode === 'enabled') {
  darkModeToggle.checked = true
  enableDarkMode();
} else if (darkMode === 'disabled') {
  darkModeToggle.checked = false
  disableDarkMode();
}

darkModeMediaQuery.addEventListener('change', (e) => {
  const darkModeOn = e.matches;
  if (!darkMode) {
    if (darkModeOn) {
      darkModeToggle.checked = true
      enableDarkMode();
    } else {
      darkModeToggle.checked = false
      disableDarkMode();
    }
  }
});

darkModeToggle.addEventListener('change', function() {
  if (!this.checked) {
    disableDarkMode();
    darkMode = localStorage.setItem('darkMode', 'disabled');
  } else {
    enableDarkMode();
    darkMode = localStorage.setItem('darkMode', 'enabled');
  }
});
