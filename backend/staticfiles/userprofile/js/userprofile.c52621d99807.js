function openProfileModal() {
    const modal = document.getElementById('profile-modal');
    const wrapper = document.querySelector('.wrapper');
    modal.style.display = 'flex';
    wrapper.classList.add('modal-open');
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    htmx.ajax('GET', '/profile/update/', {
        target: '#modal-form-container',
        swap: 'innerHTML'
    });
    console.log('Profile modal opened');
}

function closeProfileModal() {
    const modal = document.getElementById('profile-modal');
    const wrapper = document.querySelector('.wrapper');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = 'none';
        wrapper.classList.remove('modal-open');
        document.getElementById('modal-form-container').innerHTML = '';
    }, 300);
}

function showSuccessMessage() {
    const message = document.getElementById('success-message');
    message.classList.add('show');
    setTimeout(() => {
        message.classList.remove('show');
    }, 3000);
}

document.getElementById('profile-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeProfileModal();
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modal = document.getElementById('profile-modal');
        if (modal.style.display === 'flex') {
            closeProfileModal();
        }
    }
});

document.addEventListener('htmx:afterRequest', function(e) {
    if (e.detail.xhr.status === 200 && e.detail.requestConfig.path.includes('profile/update/')) {
        if (e.detail.xhr.getResponseHeader('HX-Trigger') === 'profileUpdated') {
            closeProfileModal();
            showSuccessMessage();
            
            htmx.ajax('GET', '/account/?section=profile', {
                target: '#profile-section',
                swap: 'outerHTML'
            });
        }
    }
});