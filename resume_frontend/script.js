window.onload = function() {
    // Send an HTTP request to the Azure Function when the webpage loads
    fetch('https://azrappresume.azurewebsites.net')
        .then(response => response.text())
        .then(data => {
            // Update the webpage with the new visitor count
            console.log(data)
            document.getElementById('counter').textContent = '#' + data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
};
