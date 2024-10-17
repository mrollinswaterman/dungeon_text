/*JS file for TD main screen*/
const defaultSpeed = 80;
var cursor = true;
var typing = false;
var cursorHTML = $("#narrator").html();
var blinking = true;
var currentText = "";
var currentTextboxHTML = "";

const endChars = [".", "!", "?"]
const pauseChars = [",", ":", ";", "*"]

function waitFor(conditionFunction) {
    const poll = resolve => {
      if(conditionFunction()) resolve();
      else setTimeout(_ => poll(resolve), 900);
    }
    return new Promise(poll);
};

function notTyping() {
    return !typing
};

function stopTyping(){
    typing = false;
}

function autoScrollNarrator(){
    var narrator = $("#narrator");
    narrator.get(0).scrollIntoView(false, {behavior: 'smooth'});
}

function type(text, clear=true, speed=defaultSpeed, charIndex=0){
    if (typing && currentText != text){
        waitFor(notTyping)
            .then(_ => type(text, clear, speed, charIndex));
    } else {
        var text = text;
        var speed = speed;
        var charIndex = charIndex;
        currentText = text;
        /*if there's text and we're about to start typing, add newlines*/
        if ($("#narrator").text() != "" && !typing){
            $("#narrator").html(currentTextboxHTML + "<br /><br />");
            currentTextboxHTML = $("#narrator").html();
        }
        if (!typing) {typing = true;}
        /*increases the wait time between specific chars*/
        var waitTime = speed;
        if (text.charAt(charIndex) in endChars) {waitTime += 50};
        if (text.charAt(charIndex) in pauseChars) {waitTime += 25};
        /*set the element's text*/
        $("#narrator").html(currentTextboxHTML + text.substring(0, charIndex+1) + cursorHTML);
        autoScrollNarrator();
        if (charIndex < text.length) {
            setTimeout(type, waitTime, text, clear, speed, charIndex+1);
        }else {
            currentTextboxHTML = $("#narrator").html().substring(0, $("#narrator").html().length-cursorHTML.length);
            if (clear){
                setTimeout(erase, 800);
            } else {
                stopTyping();
            };
        };
    }; 
};

function erase(speed=defaultSpeed / 2.5, charIndex=currentTextboxHTML.length-1){
    var speed = speed;
    var charIndex = charIndex;
    console.log(currentTextboxHTML.substring(0, charIndex));
    if (currentTextboxHTML.charAt(charIndex-1) == "<"){
        console.log("skip me!\n")
    } else{ 
        $("#narrator").html(currentTextboxHTML.substring(0, charIndex) + cursorHTML);
    }

    if (charIndex > 0){
        setTimeout(erase, speed, speed, charIndex-1);
    } else {
        currentTextboxHTML = "";
        setTimeout(stopTyping, 800);
    };
};

$(".text-box")[0].style.width = window.innerWidth * 0.70;
$(".text-box")[0].style.height = window.innerHeight * 0.30;

$(".side-bar")[0].style.width = window.innerWidth * 0.25;
$(".side-bar")[0].style.height = window.innerHeight * 0.95;

setInterval(() => {
    if (!typing){
        blinking = true;
    } else {
        $("#cursor").css("opacity", 0);
    };
}, 10);

setInterval(() => {
    if (blinking){
        if (cursor){
            $("#cursor").css("opacity", 0);
            cursor = false;
        } else {
            $("#cursor").css("opacity", 1);
            cursor = true;
        };
    };
}, 600);

document.getElementById("Yes").onclick = function(){
    console.log("Entering...");
    $("#start").css("display", "none");
    $(".main").css("display", "flex");
    setTimeout(enterTheDungeon, 1000)
};
 
document.getElementById("No").onclick = function(){
    enterTheOverWorld();
};

function enterTheDungeon(){
    type("First.", false);
    /*type("Second.", false);
    type("Third.");*/
};

function enterTheOverWorld(){
    console.log("Exiting....");
};
