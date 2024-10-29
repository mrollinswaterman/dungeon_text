
const endChars = [".", "!", "?"]
const pauseChars = [",", ":", ";", "*"]

function autoScrollNarrator(){
    var narrator = $("#narrator");
    narrator.get(0).scrollIntoView(false, {behavior: 'smooth'});
}

function capitalize(s){
    return s && s[0].toUpperCase() + s.slice(1);
}

function erase(speed=gameState.defaultSpeed / 2.5, charIndex=gameState.currentTextboxHTML.length-1){
    if (gameState.blinking) { gameState.blinking = false; }
    var speed = speed;
    var charIndex = charIndex;
    if (gameState.currentTextboxHTML.charAt(charIndex-1) == "<"){
        console.log("skipping...");
    } else{ 
        $("#narrator").html(
            gameState.currentTextboxHTML.substring(0, charIndex) + gameState.cursorHTML
        );
    }

    if (charIndex > 0){
        setTimeout(erase, speed, speed, charIndex-1);
    } else {
        gameState.currentTextboxHTML = "";
        gameState.stopTyping();
    };
};

function getNameAsInnerHTML(name){
    const words = name.split(" ");
    var final = "";
    for (let i = 0; i < words.length; i++){
        final = final + capitalize(words[i]) + "<br>";
    }
    return final.substring(0, final.length-"<br>".length)
}

function getStyle(el,styleProp)
{
    if (el.currentStyle)
        return el.currentStyle[styleProp];
    return document.defaultView.getComputedStyle(el,null)[styleProp];
}

function loadSidebarMenu(menu){
    $("#sidebar").css("animation", "");
    $("#sidebar").css("animation", "flip-in-Y 1s");
    setSidebarHeader(menu.title);
    const buffer = 150;
    options = Object.keys(menu.options);
    for (let i = 0; i < options.length; i++){
        setTimeout(menu.addFunction, i*buffer, menu, options[i]);
    }
    setTimeout(() => {
        gameState.currentMenu = menu;
    }, buffer * options.length);
}

function nothingLeftToType(){
    console.log(gameState.typingQueue.size);
    return gameState.typingQueue.size == 0;
}

function notTyping(){
    return !gameState.typing;
}

function setSidebarHeader(header_title){
    $("#sidebar-header").html(header_title)
    $("#sidebar-button-holder").html("");
}

function wait(seconds) {
    return new Promise(resolve => {
       setTimeout(resolve, seconds * 1000);
    });
} 

function waitFor(conditionFunction) {
    const poll = resolve => {
      if(conditionFunction()) resolve();
      else setTimeout(_ => poll(resolve), 900);
    }
    return new Promise(poll);
}

function type(text, waitFunction="nowait", speed=gameState.defaultSpeed, charIndex=0){
    gameState.typingQueue.add(text);
    if (gameState.typing && gameState.currentText != text){
        waitFor(notTyping)
            .then(_ =>
                type(text, waitFunction, speed, charIndex));
    } else {
        var text = text;
        var speed = speed;
        var charIndex = charIndex;
        gameState.currentText = text;
        /*if there's text and we're about to start typing, add newlines*/
        if ($("#narrator").text() != "" && !gameState.typing){
            $("#narrator").html(gameState.currentTextboxHTML + "<br /><br />");
            gameState.currentTextboxHTML = $("#narrator").html();
        }
        if (!gameState.typing) { gameState.typing = true; }
        if (gameState.blinking) { gameState.blinking = false; }
        /*set the element's text*/
        $("#narrator").html(
            gameState.currentTextboxHTML + text.substring(0, charIndex+1) + gameState.cursorHTML
        );
        var waitTime = speed;
        /*increases the wait time between specific chars*/
        if (pauseChars.includes(text.charAt(charIndex))){waitTime += 300};
        if (endChars.includes(text.charAt(charIndex))){waitTime += 400};
        autoScrollNarrator();
        if (charIndex < text.length) {
            setTimeout(type, waitTime, text, waitFunction, speed, charIndex+1);
        }else {
            console.log(waitFunction);
            gameState.typingQueue.delete(text);
            gameState.blinking = true;
            gameState.currentTextboxHTML = $("#narrator").html().substring(
                0, 
                $("#narrator").html().length-gameState.cursorHTML.length
            );

            /* if there's nothing behind me, decide what to do */
            if (gameState.typingQueue.size == 0){
                /*if no wait function, just clear, else wait*/
                if (waitFunction == "nowait"){
                    console.log("not waiting")
                    setTimeout(erase, 900);
                } else {
                    console.log("waiting...")
                    waitFor(waitFunction)
                        .then(_ => 
                            setTimeout(erase, 900));
                }
            } else{
                gameState.stopTyping();
            }
        };
    }; 
};

