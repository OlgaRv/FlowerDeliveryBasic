function updateFlowerImage() {
    var flowerSelect = document.getElementById('id_flower');
    var selectedOption = flowerSelect.options[flowerSelect.selectedIndex];
    var imageUrl = selectedOption.getAttribute('data-image-url');
    document.getElementById('flower-image').src = imageUrl;
}

// Initialize the image when the page loads
updateFlowerImage();
