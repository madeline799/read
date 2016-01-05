'use strict';
var BOOKHTML = {
	slider : $("#slider"),
	sidebar : $("#sidebar"),
	main : $("#main"),
	opener : $("#opener")
};

BOOKHTML.name = 'bookhtml';
BOOKHTML.version = 1.0;

//make left bar open and closed
var contentsOpenClosed = function () {
	BOOKHTML.slider.on("click",function(){
		if(BOOKHTML.sidebar.hasClass("open") && BOOKHTML.main.hasClass("closed")){
			BOOKHTML.sidebar.removeClass("open");
			BOOKHTML.main.removeClass("closed");
			BOOKHTML.opener.removeClass("opener");
		}else{
			BOOKHTML.sidebar.addClass("open");
			BOOKHTML.main.addClass("closed");
			BOOKHTML.opener.addClass("opener");
		}
	});
};
contentsOpenClosed();

//once user click the main area,the contents sidebar will hide
var mainClickClosedContents = function () {
	BOOKHTML.main.click( function () {
		if(BOOKHTML.sidebar.hasClass("open") && BOOKHTML.main.hasClass("closed"))
		{
			BOOKHTML.sidebar.removeClass("open");
			BOOKHTML.main.removeClass("closed");
			BOOKHTML.opener.removeClass("opener");
		}
	});
};
mainClickClosedContents();

//add an another text color for current chapter
var currentChapterAddRemove = function () {
	$(".list_item").on("click",function(){
		$(".list_item").removeClass("currentChapter");
		$(this).addClass("currentChapter");
	});
};
currentChapterAddRemove();

//make left contents height is the screen height
var getContentsHeight = function () {
	var clientHeight;
	if(screen.width <= 768){
		clientHeight = document.documentElement.clientHeight - 50;
	}else{
		clientHeight = document.documentElement.clientHeight - 102;
	}
	document.getElementById("tocView").style.height = clientHeight + "px";
	document.getElementById("rectangle").style.height = clientHeight + "px";
};
getContentsHeight();