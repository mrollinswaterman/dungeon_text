/*JS file for TD main screen*/
var defaultSpeed = 80
var cursor = true
var typing = false

$(".text-box")[0].style.width = window.innerWidth * 0.70
$(".text-box")[0].style.height = window.innerHeight * 0.30

$(".side-bar")[0].style.width = window.innerWidth * 0.25
$(".side-bar")[0].style.height = window.innerHeight * 0.95

setInterval(() => {
    console.log("blinking...")
    if (cursor && !typing){
        $("#cursor").css("opacity", 0);
        cursor = false;
    } else {
        $("#cursor").css("opacity", 1);
        cursor = true;
    };
}, 600);

document.getElementById("Yes").onclick = function(){
    enterTheDungeon();
};
 
document.getElementById("No").onclick = function(){
    enterTheOverWorld();
};

function enterTheDungeon(){
    console.log("Entering...")
    $("#start").css("display", "none")
    $(".main").css("display", "flex")

    type("You encounter a Level 13 Hellhound.")
};

function enterTheOverWorld(){
    console.log("Exiting....")
};

function type(text, speed=defaultSpeed, charIndex=0){
    var text = text
    var speed = speed
    var charIndex = charIndex
    if (!typing){
        typing = true
    }
    document.getElementById("narrator").innerText += text.charAt(charIndex);
    if (charIndex < text.length) {
        setTimeout(type, speed, text, speed, charIndex+1);
    } else {
        document.getElementById("narrator").innerText += "\n"
        $("#cursor").css("margin-left", "10")
        typing = false
    }
};
