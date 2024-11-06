const endChars = [".", "!", "?"]
const pauseChars = [",", ":", ";", "*"]

function dummyAttack()
{
    playerSelection = true;
    type("You attack nothing, with your sword!", nothingLeftToType);
    type("You missed.", nothingLeftToType);
    type("Who could have guessed...", nothingLeftToType);
}

function autoScrollNarrator()
{
    var narrator = $("#narrator");
    narrator.get(0).scrollIntoView(false, {behavior: 'smooth'});
}

function capitalize(s)
{
    return s && s[0].toUpperCase() + s.slice(1);
}

function erase(speed=gameState.defaultSpeed / 4, charIndex=gameState.currentTextboxHTML.length-1)
{
    if (gameState.blinking) { gameState.blinking = false; }
    var speed = speed;
    var charIndex = charIndex;
    if (gameState.currentTextboxHTML.charAt(charIndex-1) == "<")
    {
        console.log("skipping...");
    } 
    else
    { 
        $("#narrator").html(
            gameState.currentTextboxHTML.substring(0, charIndex) + gameState.cursorHTML
        );
    }

    if (charIndex > 0)
    {
        setTimeout(erase, speed, speed, charIndex-1);
    } 
    else 
    {
        gameState.currentTextboxHTML = "";
        gameState.stopTyping();
    };
};

function getNameAsInnerHTML(name)
{
    return name;
    const words = name.split(" ");
    var final = "";
    for (let i = 0; i < words.length; i++)
    {
        final = final + capitalize(words[i]) + "<br>";
    }
    return final.substring(0, final.length-"<br>".length)
}

function nothingLeftToType()
{
    return gameState.typingQueue.size == 0;
}

function doneTyping()
{
    return gameState.typingQueue.size == 0 && gameState.typing == false;
}

function notTyping()
{
    return !gameState.typing;
}

function setSidebarHeader(header_title){
    $("#sidebar-header").html(header_title)
    $("#sidebar-button-holder").html("");
}

function waitFor(conditionFunction)
{
    const poll = resolve => {
      if(conditionFunction()) resolve();
      else setTimeout(_ => poll(resolve), 900);
    }
    return new Promise(poll);
}

function type(text, waitFunction="nowait", speed=gameState.defaultSpeed, charIndex=0)
{
    gameState.typingQueue.add(text);
    if (gameState.typing && gameState.currentText != text)
    {
        waitFor(notTyping)
            .then(_ =>
                type(text, waitFunction, speed, charIndex));
    } else {
        var text = text;
        var speed = speed;
        var charIndex = charIndex;
        gameState.currentText = text;
        /*if there's text and we're about to start typing, add newlines*/
        if ($("#narrator").text() != "" && !gameState.typing)
        {
            $("#narrator").html(gameState.currentTextboxHTML + "<br /><br />");
            gameState.currentTextboxHTML = $("#narrator").html();
        }
        if (!gameState.typing) { gameState.typing = true; }
        if (gameState.blinking) { gameState.blinking = false; }
        $("#narrator").html(  // set element's text
            gameState.currentTextboxHTML + text.substring(0, charIndex+1) + gameState.cursorHTML
        );
        var waitTime = speed;

        // increases the wait time between specific chars
        if (pauseChars.includes(text.charAt(charIndex))){waitTime += 300};
        if (endChars.includes(text.charAt(charIndex))){waitTime += 400};
        autoScrollNarrator();

        if (charIndex < text.length)
        {
            setTimeout(type, waitTime, text, waitFunction, speed, charIndex+1);
        }
        else // no more text left
        {
            console.log(waitFunction);
            gameState.typingQueue.delete(text);
            gameState.blinking = true;
            gameState.currentTextboxHTML = $("#narrator").html().substring(
                0, 
                $("#narrator").html().length-gameState.cursorHTML.length
            );

            // if there's nothing behind me, decide what to do
            if (gameState.typingQueue.size == 0){
                // if no wait function, just clear, else wait*/
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

