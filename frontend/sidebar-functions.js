
const sidebarScrollUp = [
    {opacity: 1, transform: `translateY(0)`},
    {opacity: 0, transform: `translateY(-${window.innerHeight*0.95 * 1.25}px)`},
    {opacity: 0, transform: `translateY(${window.innerHeight*0.95 * 1.25}px)`},
    {opacity: 1, transform: `translateY(0)`},
];

const sidebarScrollDown = [
    {opacity: 1, transform: `translateY(0)`},
    {opacity: 0, transform: `translateY(${window.innerHeight*0.95 * 1.25}px)`},
    {opacity: 0, transform: `translateY(-${window.innerHeight*0.95 * 1.25}px)`},
    {opacity: 1, transform: `translateY(0)`},
];

const sidebarScrollTiming = 
{
    duration: 500,
    iterations: 1,
};

function addSidebarButton(menu, button_name)
{
    const back = document.createElement("div");
    back.className = "sidebar-button-back";
    back.id = button_name + "-back";

    const front = document.createElement("div");
    front.className = "sidebar-button-front";
    front.classList.add("active-button");
    front.id = button_name + "-front";
    front.innerHTML = getNameAsInnerHTML(button_name);

    const button = document.createElement("div");
    button.className = "sidebar-button";
    button.id = button_name;

    if (menu.options[button_name] != null)
    {
        button.addEventListener("mouseup", menu.options[button_name].onClick);
    }

    back.appendChild(front)
    button.appendChild(back)
    document.getElementById("sidebar-button-holder").appendChild(button);
}

function loadSidebarMenu(menu)
{
    $("#sidebar").addClass("paused");
    $("#sidebar").css("animation", "");
    $("#sidebar").css("animation", "flip-in-Y 1s");
    setSidebarHeader(menu.title);
    if (menu.title != "Your Actions")
    {
        document.getElementById('sidebar').animate(sidebarScrollDown, sidebarScrollTiming);
    }
    else
    {
        document.getElementById('sidebar').animate(sidebarScrollUp, sidebarScrollTiming);
    }

    setTimeout(() =>
    {
        const buffer = 50;
        options = Object.keys(menu.options);
        for (let i = 0; i < options.length; i++)
        {
            setTimeout(menu.addFunction, i*buffer, menu, options[i]);
        }
        setTimeout(() => 
        {
            gameState.currentMenu = menu;
            $("#sidebar").removeClass("paused");
        }, buffer * options.length);
    }, sidebarScrollTiming.duration+100);
}

function pauseSidebar()
{
    console.log("Pausing...");
    var fronts = document.getElementsByClassName("sidebar-button-front");
    for (let front of fronts)
    {
        front.classList.remove("active-button");
    }

    var buttons = document.getElementsByClassName("sidebar-button");
    for (let button of buttons)
    {
        if (gameState.currentMenu.options[button.id] != null)
        {
            console.log("removing button functionality");
            button.removeEventListener("mouseup", gameState.currentMenu.options[button.id].onClick);
        }
    }
}

function unpauseSidebar()
{
    console.log("Unpausing...");
    var buttons = document.getElementsByClassName("sidebar-button-front");
    for (let button of buttons)
    {
        button.classList.add("active-button");
    }

    var buttons = document.getElementsByClassName("sidebar-button");
    for (let button of buttons)
    {
        if (gameState.currentMenu.options[button.id] != null)
        {
            console.log("adding button functionality");
            button.addEventListener("mouseup", gameState.currentMenu.options[button.id].onClick);
        }
    }
}

function setSidebarHeader(header_title)
{
    $("#sidebar-header").html(header_title);
    $("#sidebar-button-holder").html("");
}