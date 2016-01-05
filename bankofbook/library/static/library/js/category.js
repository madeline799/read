'use strict';
var CATEGORY = {
	btnNav : $("#btn-nav"),
	leftCategory : $("#bs-example-navbar-collapse-left-category")
};

CATEGORY.name = 'category';
CATEGORY.version = 1.0;

//once navigation show,library contents hide
var navigationShowLibraryContentsHide = function () {
	CATEGORY.btnNav.click(function(){
		var left_category = CATEGORY.leftCategory.hasClass("in");
		if(left_category){
			CATEGORY.leftCategory.removeClass("in");
		}
	});
};
navigationShowLibraryContentsHide();

//make the pagination be right when they are two columns
var adjustPaginationHeight = function () {
	var pagination_height = $("div[name='pagination']").height();
	if(pagination_height > 42){
		$("ul[name='pagination-ul']").addClass("pagination-items-ul");
	}
};
adjustPaginationHeight();