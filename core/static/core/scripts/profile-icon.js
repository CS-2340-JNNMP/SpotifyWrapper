// Check if user is logged in (you'll need to modify this based on your authentication system)
const isLoggedIn = true

function handleProfileClick() {
    alert("clicked");
    if (!isLoggedIn) {
        window.location.href = '/login';
        return;
    }

    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('show');

    // Close dropdown when clicking outside
    document.addEventListener('click', function closeDropdown(e) {
        if (!e.target.closest('.nav-buttons')) {
            dropdown.classList.remove('show');
            document.removeEventListener('click', closeDropdown);
        }
    });
}

function handleDeleteAccount() {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
    // Add your delete account logic here
        console.log('Account deletion requested');
    }
}

// Close dropdown when pressing escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.getElementById('profileDropdown').classList.remove('show');
    }
});