$('#swiper-container').height($('#swiper-container').width()*0.5+'px');
$('.row').children().height($('.row').width()/6+'px');
$('.row').find('img').height('100%');
$(document).ready(function(){
  $('.move-div').mouseenter(function(){
    $(this).find(".hide-box").slideDown("300");
    $(this).find('img').css(  'filter','blur(3px) brightness(0.6)');
  });
   $('.move-div').mouseleave(function(){
    $(this).find(".hide-box").slideUp("300");
    $(this).find('img').css('filter','blur(0px) brightness(1)');
  });
});
