function addToCart(itemId) {
    const quantity = document.getElementById(`quantity-${itemId}`).value;
    const url = "/add_to_cart/" + itemId + `?quantity=${quantity}`;
    window.location.href = url;
}
