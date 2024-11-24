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
    console.log("Entering...");
    $("#start").css("display", "none");
    $(".main").css("display", "grid");
    setTimeout(enterTheOverworld, 1000)
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
        if (waitFunction == "nowait"){
            waitFunction = nothingLeftToType;
        }
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
    constructor(title, addFunction=addSidebarButton){
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
            const front = document.getElementById(`${name}-front`);
            if (front.classList.contains("active-button"))
            {
                setTimeout(() => // function to run
                {
                    onClick();
                    gameState.pauseUntil(flag);
                }, 300); 
            }

        } 
        this.flag = flag;  // flag to check if the function has completed
    }
}

const overworldMenu = new Menu("Your Actions");
overworldMenu.options = {
    "enter the dungeon": new Option("enter the dungeon", enterTheDungeon,
        function () {return gameState.currentMenu == actions; }
    ),
    "visit the shopkeeper": new Option("visit the shopkeeper", enterTheShop,
        function() { return gameState.currentMenu == shopMenu; }
    ),
    "inventory": null,
    "rest":null
}

const shopMenu = new Menu("Your Actions");
shopMenu.options = {
    "buy":null,
    "sell":null,
    "invetory":null,
    "leave":null,
}

const actions = new Menu("Your Actions");
actions.options = {
    "attack": new Option("attack", dummyAttack, doneTyping),
    "combat tricks": new Option(
        "combat tricks", 
        function() { loadSidebarMenu(combatTricks); },
        function() { return gameState.currentMenu == combatTricks; }),
    "inventory": null,
    "status effects": null,
    "wait": null,
    "flee": null,
}

const combatTricks = new Menu("Combat Tricks");
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
        function() { 
            console.log(gameState.currentMenu.title);
            return gameState.currentMenu == actions; 
        }
    ),
}

function enterTheDungeon()
{
    type(`This is a test! I repeat, this is a test!`, playerSelectionMade);
    loadSidebarMenu(actions);
};

function enterTheOverworld()
{
    type("You clamber out of the darkness...");
    type("Where to now?", playerSelectionMade);
    loadSidebarMenu(overworldMenu);
};

function enterTheShop()
{
    type("The Shopkeep glances at you...");
    type("What would you like to do?", playerSelectionMade);
    loadSidebarMenu(shopMenu);
};
