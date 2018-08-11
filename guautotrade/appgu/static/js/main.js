(function($) {
	"use strict";
	
	// Preloader
	$(window).on('load', function() {
		$("#preloader").delay(10).fadeOut();
	});

	// Mobile Toggle Btn
	$('.navbar-toggle').on('click',function(){
		$('#header').toggleClass('nav-collapse')
	});
	
})(jQuery);