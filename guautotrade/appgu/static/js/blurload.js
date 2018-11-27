// This is "probably" IE9 compatible but will need some fallbacks for IE8
// - (event listeners, forEach loop)

// wait for the entire page to finish loading

$(".intro_section").delay(100).animate({"opacity": "1"}, 1000);

window.addEventListener('load', function() {


	// setTimeout to simulate the delay from a real page load
	setTimeout(lazyLoad, 1000);

});

function showImages() {
	var bgimages = document.getElementsByClassName("bg-image--hidden");
    var bgimages_length = bgimages.length;
    for (var i = 0; i < bgimages_length; i++){
        bgimages[0].classList.remove("bg-image--hidden");
    }
}

function lazyLoad() {
    var card_images = document.querySelectorAll('.card-image');

	console.log(card_images);
	// loop over each card image
	card_images.forEach(function(card_image) {
        var image_url = card_image.getAttribute('data-image-full');
        console.log(image_url);
        var content_image = card_image.querySelector('img');
        console.log(content_image);
		
		// change the src of the content image to load the new high res photo
		content_image.src = image_url;
		
		// listen for load event when the new photo is finished loading
		content_image.addEventListener('load', function() {
			// swap out the visible background image with the new fully downloaded photo
			card_image.style.backgroundImage = 'url(' + image_url + ')';
			// add a class to remove the blur filter to smoothly transition the image change
			card_image.className = card_image.className + ' is-loaded';
		});
		
	});
	var card_img = document.getElementsByClassName("card-image")[0];
	card_img.classList.add('slideshow-image');
	setTimeout(showImages, 700);

}

