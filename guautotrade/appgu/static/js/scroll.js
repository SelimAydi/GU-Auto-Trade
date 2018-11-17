var scrollLink = $('.scroll');
  
// Smooth scrolling
scrollLink.click(function(e) {
  console.log("SCROLLING");
  e.preventDefault();
  $('body,html').animate({
    scrollTop: $(this.hash).offset().top - 150
  }, 1000 );
});