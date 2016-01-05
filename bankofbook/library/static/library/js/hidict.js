function getSelectionText() {
    var b;
    if (window.getSelection) {
        b = window.getSelection();
    } else {
        if (document.getSelection) {
            b = document.getSelection();
        } else {
            if (document.selection) {
                b = document.selection.createRange().text;
            } else {
                b = "";
            }
        }
    }
    return b.toString().trim();
}
function chkTextReady(f) {
    console.log("chkTextReady");
    var e, g;
    if (f.target == dictIcon) {
        return;
    }
    $("#dictIcon").css("display", "none");
    $("#dictContent").css("display", "none");
    $("#annotationIconCover").css("display", "none");
    try {
        if (f.type.indexOf("touchstart") == 0) {
            dictIconTop = f.touches[0].pageY;
            dictIconLeft = f.touches[0].pageX;
            return
        } else {
            if (f.type.indexOf("touchend") == 0) {} else {
                if (f.type.indexOf("touchcancel") == 0) {} else {
                    if (f.type.indexOf("mouseup") == 0) {
                        dictIconTop = f.pageY;
                        dictIconLeft = f.pageX;
                    }
                }
            }
        }
        dictWord = getSelectionText();
        if (dictWord.length > 0) {
            if (document.documentElement && document.documentElement.scrollTop) {
                e = document.documentElement.scrollTop;
                g = document.documentElement.scrollLeft;
            } else {
                if (document.body) {
                    e = document.body.scrollTop;
                    g = document.body.scrollLeft
                }
            }
            if ((dictIconTop - e) < screen.height / 4) {
                dictIconTop += $("#dictIcon").height()
            } else {
                dictIconTop -= 2 * $("#dictIcon").height()
            }
            dictIconLeft -= $("#dictIcon").width();
            if (dictIconLeft < $("#dictIcon").width()) {
                dictIconLeft = $("#dictIcon").width();
            }
            $("#dictIcon").css("display", "block");
            $("#dictIcon").css("top", dictIconTop);
            $("#dictIcon").css("left", dictIconLeft);

            $("#annotationIconCover").css("display", "block");
            $("#annotationIconCover").css("top", dictIconTop - 100);
            $("#annotationIconCover").css("left", dictIconLeft + 45);
        } else {
            $("#dictIcon").css("display", "none");
            $("#annotationIconCover").css("display", "none");
        }
    } catch(h) {
        console.log(f.type);
        console.log("chkTextReady, err:" + h.message);
    }
}
function showTextExplanation(b) {
    console.log("showTextExplanation");
    dictWord = getSelectionText();
    console.log("b========="+b);
    console.log("dictWord========="+dictWord);
    if (dictWord.length > 0) {
        if (b.type.indexOf("touchstart") == 0) {
            dictContentTop = b.touches[0].pageY;
            dictContentLeft = 0
        } else {
            if (b.type.indexOf("mouseover") == 0) {
                dictContentTop = b.pageY;
                dictContentLeft = b.pageX
            }
        }
        $.ajax({
            url: "http://www.hidict.cn/dictionary/hidict_service_lookup/?term=" + dictWord,
            dataType: "jsonp",
            success: function(e) {
                console.log("showTextExplanation, success!");
                if (e == null) {
                    $("#dictWord").html(dictWord);
                    $("#briefExplanation").html("jiandandejianshi");
                    $("#detailExplanationLink").attr("href", "http://www.hidict.cn/dictionary/")
                } else {
                    var a = "";
                    for (var f = 0; f < e.expl.definition[0].length; f++) {
                        if (e.expl.definition[0][f]) {
                            a += e.expl.definition[0][f] + "; "
                        }
                    }
                    $("#dictWord").html(dictWord);
                    $("#briefExplanation").html(a);
                    $("#detailExplanationLink").attr("href", "http://www.hidict.cn/dictionary/" + dictWord)
                }
                $("#dictContent").css("display", "block");
                $("#dictContent").css("top", dictContentTop);
                $("#dictContent").css("left", dictContentLeft)
            },
            error: function(a) {
                console.log("showTextExplanation, err!")
            },
        })
    }
}

var hidict = document.getElementById("hidict");

var dictIcon, dictIconTop, dictIconLeft;
var dictContent, dictContentTop, dictContentLeft;
var dictWord;
dictIcon = document.createElement("img");
dictIcon.id = "dictIcon";
dictContent = document.createElement("div");
dictContent.id = "dictContent";
document.body.appendChild(dictIcon);
document.body.appendChild(dictContent);

$("#dictIcon").css("display", "none");
$("#dictIcon").css("position", "absolute");
$("#dictIcon").css("left", "100px");
$("#dictIcon").css("top", "100px");
$("#dictIcon").css("z-index", "9999");
$("#dictIcon").attr("src", "../../../static/library/img/annotation-icon.png");
$("#dictIcon").attr("usemap", "#annotator-plugin");
$("#dictContent").css("display", "none");
$("#dictContent").css("position", "absolute");
$("#dictContent").css("left", "100px");
$("#dictContent").css("top", "100px");
$("#dictContent").css("z-index", "99999999999");
$("#dictContent").css("background-color", "white");
$("#dictContent").css("border", "medium solid rgb(112,186,224)");
$("#dictContent").css("border-radius", "0.5em");
$("#dictContent").css("padding", "0.5em");
$("#dictContent").append("<div id='dictWord'></div>");
$("#dictContent").append("<div id='dictExplanation'></div>");
$("#dictWord").css("font-size", "1.2em");
$("#dictWord").css("font-weight", "500");
$("#dictExplanation").css("padding-left", "1em");
$("#dictExplanation").append("<div id='briefExplanation'></div>");
$("#dictExplanation").append("<div id='detailExplanation'></div>");
$("#detailExplanation").css("padding-top", "1em");
$("#dictWord").html("dictWord");
$("#briefExplanation").html("briefExplanation");
$("#detailExplanation").append("<a id='detailExplanationLink'>HiDict.cn</a>");
$("#detailExplanationLink").attr("title", "HiDict");
$("#detailExplanationLink").attr("href", "http://www.hidict.cn/");
$("#detailExplanationLink").attr("target", "_blank");

$(document).ready(function() {
    try {
        document.createEvent("TouchEvent");
        document.addEventListener("touchstart", chkTextReady, false);
        document.addEventListener("touchend", chkTextReady, false);
        document.addEventListener("touchcancel", chkTextReady, false);
        hidict.addEventListener("touchstart", showTextExplanation, false)
    } catch(b) {
        console.log("Fail to bind TouchEvent");
        try {
            document.createEvent("MouseEvent");
            document.addEventListener("mouseup", chkTextReady, false);
            hidict.addEventListener("mouseover", showTextExplanation, false)
        } catch(b) {
            console.log("Fail to bind MouseEvent")
        }
    }
});