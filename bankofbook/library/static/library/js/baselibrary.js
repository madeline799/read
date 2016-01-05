'use strict';
var BASELIBRARY = {
	footerSite : $("#footer-site")
};

BASELIBRARY.name = 'baselibrary';
BASELIBRARY.version = 1.0;

$(document).ready(function(){
	var scroll;
	if(document.documentElement.clientHeight < document.documentElement.offsetHeight){
		scroll = true;
	}else{
		scroll = false;
	}
	if(!scroll){
		BASELIBRARY.footerSite.addClass("footer-site");
	}
});
