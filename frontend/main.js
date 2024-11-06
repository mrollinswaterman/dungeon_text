/*JS file for TD main screen*/

$(".hud")[0].style.width = window.innerWidth * 0.73;
$(".hud")[0].style.height = window.innerHeight * 0.65;

$(".textbox")[0].style.width = window.innerWidth * 0.73;
$(".textbox")[0].style.height = window.innerHeight * 0.33;

$(".sidebar")[0].style.width = window.innerWidth * 0.25;
$(".sidebar")[0].style.height = window.innerHeight * 0.97;

document.getElementById("Yes").onclick = function()
{
    console.log("Entering...");
    $("#start").css("display", "none");
    $(".main").css("display", "grid");
    setTimeout(enterTheDungeon, 1000)
};
 
document.getElementById("No").onclick = function()
{
    enterTheOverWorld();
};

var playerSelection = false;

class GameState 
{
    constructor(){
        this.typing = false;
        this.blinking = true;
        this.cursor = true;
        this.paused = false;
        this.currentText = "";
        this.currentTextboxHTML = "";
        this.cursorHTML = $("#narrator").html();
        this.defaultSpeed = 60;

        this.currentMenu = null;

        this.typingQueue = new Set();

        /*blink the cursor*/
        setInterval(() => {
            if (this.blinking){
                if (this.cursor){
                    $("#cursor").css("opacity", 0);
                    this.cursor = false;
                } else {
                    $("#cursor").css("opacity", 1);
                    this.cursor = true;
                };
            } else{
                $("#cursor").css("opacity", 0);
                this.cursor = false;
            }
        }, 600);
    }

    pauseUntil(waitFunction=playerSelectionMade){
        if (!this.paused){
            pauseSidebar();
            this.paused = true;
            waitFor(waitFunction)
                .then(_ => {
                    unpauseSidebar();
                    this.paused = false;
                });
        }
    }

    stopTyping(){
        this.blinking = true;
        setTimeout(() =>{
            this.typing = false;
        }, 900);
    }
}

const gameState = new GameState();

class Menu
{
    constructor(title, addFunction){
        this.title = title;
        this.addFunction = addFunction
        this.options = {};
    }

    addOption(newOption){
        this.options[newOption[0]] = newOption[1];
    }
}

class Option 
{
    constructor(name, onClick, flag){
        this.name = name;
        this.onClick = () => 
        {
            setTimeout(() => // function to run
            {
                onClick();
                gameState.pauseUntil(flag);
            }, 300); 
        } 
        this.flag = flag;  // flag to check if the function has completed
    }
}

const actions = new Menu("Your Actions", addSidebarButton);
actions.options = {
    "attack": new Option("attack", dummyAttack, doneTyping),
    "combat tricks": new Option(
        "combat tricks", 
        function() { loadSidebarMenu(combatTricks); },
        function() { return gameState.currentMenu == combatTricks; }),
    "status effects": null,
    "inventory": null,
    "wait": null,
    "flee": null,
}

const combatTricks = new Menu("Combat Tricks", addSidebarButton);
combatTricks.options = {
    "power attack": null,
    "feint": null,
    "riposte": null,
    "total defense": null,
    "all-out": null,
    "study weakness": null,
    "back": new Option(
        "back", 
        function(){ loadSidebarMenu(actions); },
        function() { return gameState.currentMenu = actions; }
    ),
}

function enterTheDungeon()
{
    type(`test`, playerSelectionMade);
    loadSidebarMenu(actions);
    //gameState.pauseUntil(nothingLeftToType);

};

function enterTheOverWorld()
{
    console.log("Exiting....");
};

function playerSelectionMade()
{
    if (playerSelection){
        playerSelection = false;
        return true
    }
    return false;
}
