function addToCart(itemId) {
    // Get the quantity from the input field
    const quantityInput = document.querySelector(`input[type="text"][data-item-id="${itemId}"]`);
    const quantity = quantityInput ? quantityInput.value : 1; // Default to 1 if not found

    // Construct the URL for adding to cart
    const url = `/add_to_cart/${itemId}/?quantity=${quantity}`;
    
    // Redirect to the URL
    window.location.href = url;
}
