/*JS file for TD main screen*/

$(".hud")[0].style.width = window.innerWidth * 0.73;
$(".hud")[0].style.height = window.innerHeight * 0.65;

$(".textbox")[0].style.width = window.innerWidth * 0.73;
$(".textbox")[0].style.height = window.innerHeight * 0.33;

$(".sidebar")[0].style.width = window.innerWidth * 0.25;
$(".sidebar")[0].style.height = window.innerHeight * 0.97;

document.getElementById("Yes").onclick = function(){
    console.log("Entering...");
    $("#start").css("display", "none");
    $(".main").css("display", "grid");
    setTimeout(enterTheDungeon, 1000)
};
 
document.getElementById("No").onclick = function(){
    enterTheOverWorld();
};

var playerSelection = false;

class GameState {
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

    pause(waitFunction=playerSelectionMade){
        if (!this.paused){
            console.log("pausing!")
            pauseSidebar();
            this.paused = true;
            waitFor(waitFunction)
                .then(_ => {
                    console.log("unpausing!")
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

class Menu {
    constructor(title, addFunction){
        this.title = title;
        this.addFunction = addFunction
        this.options = {};
    }

    addOption(newOption){
        this.options[newOption[0]] = newOption[1];
    }
}

class Option {
    constructor(name, run, flag){
        this.name = name;
        this.run = run;
        this.flag = flag;
    }
}

const actions = new Menu("Your Actions", addSidebarButton);
actions.options = {
    "attack": new Option("attack", dummyAttack, nothingLeftToType),
    "combat tricks": new Option(
        "combat tricks", 
        function() { loadSidebarMenu(combatTricks); },
        function() { return gameState.currentMenu == combatTricks; }),
    "status effects": null,
    "inventory": null,
    "wait": null,
    "flee": null,
}

function dummyAttack(){
    playerSelection = true;
    type("You attack nothing, with your sword!", nothingLeftToType);
    type("You missed.", nothingLeftToType);
    type("Who could have guessed...", nothingLeftToType);
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

function enterTheDungeon(){
    type("This is a test, I repeat, this is a test.", playerSelectionMade);
    gameState.pause(nothingLeftToType);
    loadSidebarMenu(actions);
};

function enterTheOverWorld(){
    console.log("Exiting....");
};

function addSidebarButton(menu, button_name){
    const back = document.createElement("div");
    back.className = "sidebar-button-back";
    back.id = button_name + "-back";

    const div = document.createElement("div");
    div.className = "sidebar-button-front";
    div.id = button_name;
    div.innerHTML = getNameAsInnerHTML(button_name);

    const button = document.createElement("div");
    button.className = "sidebar-button";

    back.addEventListener("click", () => {
        menu.options[button_name].run();
        gameState.pause(menu.options[button_name].flag);
    });

    back.appendChild(button)
    button.appendChild(div)
    document.getElementById("sidebar-button-holder").appendChild(back);
}

function playerSelectionMade(){
    if (playerSelection){
        playerSelection = false;
        return true
    }
    return false;
}

function pauseSidebar(){
    document.getElementById("sidebar").classList.add("paused");
}

function unpauseSidebar(){
    document.getElementById("sidebar").classList.remove("paused");
}

function addSideBarIconButton(menu, icon_name){
    const words = icon_name.split(" ");
    var id_str = "";
    var inner_text = "";
    for (let i = 0; i < words.length; i++){
        id_str = id_str + words[i] + "-";
        inner_text = inner_text + capitalize(words[i]) + "<br>";
    }
    id_str = id_str.substring(0, id_str.length-1);
    inner_text = inner_text.substring(0, inner_text.length-"<br>".length);
    const icon_image = id_str + ".png";

    const div = document.createElement("div");
    div.className = "sidebar-icon-button";
    div.id = icon_name;

    const shadow = document.createElement("img");
    shadow.className = "sidebar-icon-button-shadow";
    shadow.src = icon_image;
    shadow.id = id_str + "-shadow";

    const icon_bottom = document.createElement("img");
    icon_bottom.className = "sidebar-icon-button-img-bottom";
    icon_bottom.src = icon_image;
    icon_bottom.id = id_str + "-img-bottom";

    const icon = document.createElement("img");
    icon.className = "sidebar-icon-button-img";
    icon.src = icon_image;
    icon.id = id_str +"-img";

    const text = document.createElement("span");
    text.className = "sidebar-icon-button-text";
    text.innerHTML = inner_text;

    div.onclick = menu.options[icon_name];

    div.appendChild(shadow);
    div.appendChild(icon_bottom);
    div.appendChild(icon);
    div.appendChild(text);

    document.getElementById("sidebar-button-holder").appendChild(div);
}
