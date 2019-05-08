var modal = document.querySelector('.modal')
var trigger = document.querySelector('.btn-danger')
var closeButton = document.querySelector('.close-button')

// Toggle the modal css property.
function toggleModal() {
    modal.classList.toggle('show-modal');
}

// Close the modal when clicked off the window
function windowOnClick(event) {
    if (event.target === modal) {
        toggleModal()
    }
}

trigger.addEventListener('click', toggleModal);
closeButton.addEventListener('click', toggleModal);
window.addEventListener('click', windowOnClick);