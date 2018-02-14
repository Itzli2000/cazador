jQuery(document).ready(function() {

	

});


// Privacy modal
// Get the modal
var modalPromo = document.getElementById('privacy');

// Get the button that opens the modal
var btnPromo = document.getElementById("promoBtn");

// Get the <span> element that closes the modal
var spanPromo = document.getElementsByClassName("closepromo")[0];

// When the user clicks on the button, open the modal 
btnPromo.onclick = function() {
    modalPromo.style.display = "block";
}


// When the user clicks on <span> (x), close the modal
spanPromo.onclick = function() {
  modalPromo.style.display = "none";
}



// Promotions modal
// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("closemodal")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
  else if (event.target == modalPromo) {
    modalPromo.style.display = "none";
  }
}
