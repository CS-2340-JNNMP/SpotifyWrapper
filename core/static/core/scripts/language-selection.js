// Define available languages and their options
const languages = {
  English: {
    options: ['Espagnol', 'Française']
  },
  Espagnol: {
    options: ['English', 'Française']
  },
  Française: {
    options: ['English', 'Espagnol']
  }
};

// Function to handle language selection
function handleLanguageSelection() {
  const dropdown = document.getElementById('lang-dropdown');
  const button = document.getElementById('languageDropdown');
  const menu = dropdown.querySelector('.dropdown-menu');

  // Add click event listeners to dropdown items
  menu.addEventListener('click', (e) => {
    if (e.target.classList.contains('dropdown-item')) {
      const selectedLang = e.target.textContent;

      // Update button text
      button.textContent = selectedLang;

      // Clear existing dropdown items
      menu.innerHTML = '';

      // Add new dropdown items based on selected language
      languages[selectedLang].options.forEach(lang => {
        const item = document.createElement('a');
        item.classList.add('dropdown-item');
        item.href = '#';
        item.textContent = lang;
        menu.appendChild(item);
      });
    }
  });
}

// Initialize the language switcher when the document loads
document.addEventListener('DOMContentLoaded', handleLanguageSelection);