'use strict';
var STYLE = {
};

STYLE.name = 'style';
STYLE.version = 1.0;

//click the icon,the page will turn to top
var turnToTop = function () {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 1000){
			$('div.go-top').show();
		}else{
			$('div.go-top').hide();
		}
	});
	$("div.go-top").click(function() {
		$('html, body').animate({scrollTop: 0}, 200);
	});
};
turnToTop();