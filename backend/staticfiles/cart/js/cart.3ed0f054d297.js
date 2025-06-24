// change quantity in cart

document.body.addEventListener('cartUpdated', function(e) {
    const count = e.detail.count;
    updateCartCount(`(${count})`);
});

function updateCartCount(countText) {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.innerHTML = countText;
    }
    const cartItemsCount = document.getElementById('cart-items-count');
    if (cartItemsCount) {
        const count = countText.replace(/[()]/g, '');
        cartItemsCount.textContent = `${count} item${count != '1' ? 's' : ''}`;
    }
}