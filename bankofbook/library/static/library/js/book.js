'use strict';
var BOOK = {
	tableSite : $("#table-site")
};

BOOK.name = 'book';
BOOK.version = 1.0;

//make bookcover slides be center when screen <= 768 
var bookCoverBeCenter = function () {
	if(screen.width <= 768){
		BOOK.tableSite.addClass('table-site');
	}else{
		BOOK.tableSite.removeClass('table-site');
	}
};
bookCoverBeCenter();

//click heart,change the background color
// var changeHeartBackgroundColor = function () {
// 	var clickNumber = 1;
// 	$("span[id^=heart]").click(function(){
// 		if(clickNumber % 2 != 0){
// 			$("span[id^=heart]").addClass('glyphicon-heart-bk-click');
// 		}else{
// 			$("span[id^=heart]").removeClass('glyphicon-heart-bk-click');
// 		}
// 		clickNumber ++;
// 	});
// };