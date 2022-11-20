//Indicate current page on navbar
$('.nav-item > a[href$="' + location.pathname + '"]')
  .addClass('nav-current')
  .siblings().removeClass('nav-active');

//Add blur/transparency to navbar if not at page top
$(window).scroll(function() {
  if($(window).scrollTop() >= 50) {
    $('nav').addClass('navbar-scrolling');
  } else {
    $('nav').removeClass('navbar-scrolling');
  }
});

//Close Flash messages after 10 seconds
function closeFlashMsg() {
  $('.btn-close').each(function() {
    $(this).trigger('click');
  });
}

if($('#flash-msg-list').length) {
  setTimeout(() => {
    closeFlashMsg();
  }, 10000);
}
