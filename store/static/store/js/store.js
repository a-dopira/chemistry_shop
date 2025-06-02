 document.body.addEventListener('htmx:afterSwap', function(e) {
    if (e.target.id === 'cart-count') {
        const successMsg = document.getElementById('add-success');
        successMsg.style.display = 'flex';
        
        const btnText = document.querySelector('.btn-text');
        const originalText = btnText.textContent;
        btnText.textContent = 'Added!';
        
        setTimeout(() => {
            successMsg.style.display = 'none';
            btnText.textContent = originalText;
        }, 2000);
    }
});

document.body.addEventListener('htmx:responseError', function(e) {
    alert('Error adding item to cart. Please try again.');
});