var truncate = function (elem, limit) {
    // Check if element and number of items is provided
    if (!elem || !limit) return;

    // Get the content of the element
    var content = elem.textContent.trim();

    // Covert the string into array of words
    content = content.split(' ').slice(0, limit);
    
    // Convert the array back to string
    content = content.join(' ');
    elem.textContent = content;
};

