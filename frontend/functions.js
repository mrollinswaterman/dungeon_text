
const endChars = [".", "!", "?"]
const pauseChars = [",", ":", ";", "*"]

function getStyle(el,styleProp)
{
    if (el.currentStyle)
        return el.currentStyle[styleProp];
    return document.defaultView.getComputedStyle(el,null)[styleProp];
}

function capitalize(s){
    return s && s[0].toUpperCase() + s.slice(1);
}

function setSidebarHeader(header_title){
    $("#sidebar-header").html(header_title)
    $("#sidebar-button-holder").html("");
}

function getNameAsInnerHTML(name){
    const words = name.split(" ");
    var final = "";
    for (let i = 0; i < words.length; i++){
        final = final + capitalize(words[i]) + "<br>";
    }
    return final.substring(0, final.length-"<br>".length)
}

function waitFor(conditionFunction) {
    const poll = resolve => {
      if(conditionFunction()) resolve();
      else setTimeout(_ => poll(resolve), 900);
    }
    return new Promise(poll);
}

function wait(seconds) {
    return new Promise(resolve => {
       setTimeout(resolve, seconds * 1000);
    });
} 

function notTyping(){
    return !CurrentState.typing;
}

function type(text, waitFunction="nowait", speed=CurrentState.defaultSpeed, charIndex=0){
    CurrentState.typingQueue.add(text);
    if (CurrentState.typing && CurrentState.currentText != text){
        waitFor(notTyping)
            .then(_ =>
                type(text, waitFunction, speed, charIndex));
    } else {
        var text = text;
        var speed = speed;
        var charIndex = charIndex;
        CurrentState.currentText = text;
        /*if there's text and we're about to start typing, add newlines*/
        if ($("#narrator").text() != "" && !CurrentState.typing){
            $("#narrator").html(CurrentState.currentTextboxHTML + "<br /><br />");
            CurrentState.currentTextboxHTML = $("#narrator").html();
        }
        if (!CurrentState.typing) { CurrentState.typing = true; }
        if (CurrentState.blinking) { CurrentState.blinking = false; }
        /*set the element's text*/
        $("#narrator").html(
            CurrentState.currentTextboxHTML + text.substring(0, charIndex+1) + CurrentState.cursorHTML
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
            CurrentState.typingQueue.delete(text);
            CurrentState.blinking = true;
            CurrentState.currentTextboxHTML = $("#narrator").html().substring(
                0, 
                $("#narrator").html().length-CurrentState.cursorHTML.length
            );

            /* if there's nothing behind me, decide what to do */
            if (CurrentState.typingQueue.size == 0){
                alert("END");
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
                CurrentState.stopTyping();
            }
        };
    }; 
};

function erase(speed=CurrentState.defaultSpeed / 2.5, charIndex=CurrentState.currentTextboxHTML.length-1){
    if (CurrentState.blinking) { CurrentState.blinking = false; }
    var speed = speed;
    var charIndex = charIndex;
    if (CurrentState.currentTextboxHTML.charAt(charIndex-1) == "<"){
        console.log("skipping...");
    } else{ 
        $("#narrator").html(
            CurrentState.currentTextboxHTML.substring(0, charIndex) + CurrentState.cursorHTML
        );
    }

    if (charIndex > 0){
        setTimeout(erase, speed, speed, charIndex-1);
    } else {
        CurrentState.currentTextboxHTML = "";
        /*if nothing after me*/
        CurrentState.stopTyping();
    };
};

function autoScrollNarrator(){
    var narrator = $("#narrator");
    narrator.get(0).scrollIntoView(false, {behavior: 'smooth'});
}