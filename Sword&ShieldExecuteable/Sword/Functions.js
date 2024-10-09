console.log("Loading World...")

setTimeout(() => {
    console.log("World Loaded.")
}, 1000);

function shake() {
    document.body.classList.add("apply-shake")

    setTimeout(() =>{
        document.body.classList.remove("apply-shake") 
    }, 1000)
}

function shake2() {
    document.body.classList.add("apply-shake2")

    setTimeout(() =>{
        document.body.classList.remove("apply-shake2") 
    }, 1000)
}


window.foo = false

function detectCollision(hitbox1, hitbox2){

    if(hitbox2){
        // if(window.foo === false){
        //     window.foo = true

        //     window.h1c1 = document.createElement("div")
        //     window.h1c2 = document.createElement("div")
        //     window.h1c3 = document.createElement("div")
        //     window.h1c4 = document.createElement("div")
        //     window.h2c1 = document.createElement("div")
        //     window.h2c2 = document.createElement("div")
        //     window.h2c3 = document.createElement("div")
        //     window.h2c4 = document.createElement("div")


        //     window.h1c1.className = "pointer"
        //     window.h1c2.className = "pointer"
        //     window.h1c3.className = "pointer"
        //     window.h1c4.className = "pointer"
        //     window.h2c1.className = "pointer"
        //     window.h2c2.className = "pointer"
        //     window.h2c3.className = "pointer"
        //     window.h2c4.className = "pointer"


        //     dirtroad.appendChild(window.h1c1)
        //     dirtroad.appendChild(window.h1c2)
        //     dirtroad.appendChild(window.h1c3)
        //     dirtroad.appendChild(window.h1c4)
        //     dirtroad.appendChild(window.h2c1)
        //     dirtroad.appendChild(window.h2c2)
        //     dirtroad.appendChild(window.h2c3)
        //     dirtroad.appendChild(window.h2c4)
        // }


        // window.h1c1.style.bottom = hitbox1.c1.y
        // window.h1c1.style.left = hitbox1.c1.x
        // window.h1c2.style.bottom = hitbox1.c2.y
        // window.h1c2.style.left = hitbox1.c2.x
        // window.h1c3.style.bottom = hitbox1.c3.y
        // window.h1c3.style.left = hitbox1.c3.x
        // window.h1c4.style.bottom = hitbox1.c4.y
        // window.h1c4.style.left = hitbox1.c4.x
        // window.h2c1.style.bottom = hitbox2.c1.y
        // window.h2c1.style.left = hitbox2.c1.x
        // window.h2c2.style.bottom = hitbox2.c2.y
        // window.h2c2.style.left = hitbox2.c2.x
        // window.h2c3.style.bottom = hitbox2.c3.y
        // window.h2c3.style.left = hitbox2.c3.x
        // window.h2c4.style.bottom = hitbox2.c4.y
        // window.h2c4.style.left = hitbox2.c4.x


        const newHitbox1 = {
            line1: findSlopeIntercept(hitbox1.c1, hitbox1.c2), //y = m * X + b
            line2: findSlopeIntercept(hitbox1.c2, hitbox1.c3),
            line3: findSlopeIntercept(hitbox1.c3, hitbox1.c4),
            line4: findSlopeIntercept(hitbox1.c4, hitbox1.c1)
        }

        const newHitbox2 = {
            line1: findSlopeIntercept(hitbox2.c1, hitbox2.c2), //y = m * X + b
            line2: findSlopeIntercept(hitbox2.c2, hitbox2.c3),
            line3: findSlopeIntercept(hitbox2.c3, hitbox2.c4),
            line4: findSlopeIntercept(hitbox2.c4, hitbox2.c1)
        }


        for(var L1 of Object.values(newHitbox1)){
            for(var L2 of Object.values(newHitbox2)){

                if(findIntersection(L1, L2)){
                    return true
                }
            }
        }

    }
}


function findSlopeIntercept(p1, p2){
    var tweakedX = p1.x - .001
    var slope = (p2.y - p1.y) / (p2.x - tweakedX)

    var intercept = p1.y - (slope*tweakedX)

    return {
        m: slope,
        b: intercept,
        x1: tweakedX,
        x2: p2.x
    }
}


function findIntersection(line1, line2){

    const xIntercept = (line1.b - line2.b) / (line2.m - line1.m)//+0.0015

    //console.log(xIntercept)

    const onLine1 = xIntercept > line1.x1 ? xIntercept <= line1.x2 : xIntercept > line1.x2
    const onLine2 = xIntercept > line2.x1 ? xIntercept <= line2.x2 : xIntercept > line2.x2

    return onLine1 && onLine2
}

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min
}

function sin(x) {
    return Math.sin(x / 180 * Math.PI);
}
 
function cos(x) {
    return Math.cos(x / 180 * Math.PI);
}

function aSin(x) {
    return Math.asin(x / 180 * Math.PI);
}
 
function aCos(x) {
    return Math.acos(x / 180 * Math.PI);
}

function aTan(x){
    return Math.atan(x / 180 * Math.PI)
}


function nextLevel(level){
    console.log("Next Level", level)
    player1.dead = true
    mainPage2.style.background = "black"
    mainPage2.style.opacity = 1.0
    const exposition = new Storybox(Plot[level], level)
    exposition.findSentences()
    window.exposition = exposition
    setTimeout(() =>{
        exposition.write()
        //chooseYourWeapon(level)
    }, 2800)

}

WEAPONS = {
    1: ["TrustySword"],
    2: ["TrustySword", "ReginaldJr"]
}


function chooseYourWeapon(level){
    const chooseYourWeapon = document.createElement("div")
    chooseYourWeapon.className = "choose-your-weapon"
    const titleDiv = document.createElement('div')
    titleDiv.className = "choose-your-weapon-title"
    chooseYourWeapon.appendChild(titleDiv)
    mainPage2.appendChild(chooseYourWeapon)
    titleDiv.innerHTML = "Choose Your Weapon: "

    for(var i = 0; i< WEAPONS[level].length; i++){
        const weaponSelection = document.createElement("div")
        weaponSelection.className = "weapon-selection"
        weaponSelection.id = "weapon-selection-"+WEAPONS[level][i]

        const weaponName = document.createElement("div")
        weaponName.className = "weapon-name"
        weaponName.innerHTML = WeaponInfo[WEAPONS[level][i]].name
        weaponSelection.appendChild(weaponName)

        const weaponSelectionImg = document.createElement("img")
        weaponSelectionImg.className = "weapon-selection-img"
        weaponSelectionImg.src = "images/Weapons/"+WEAPONS[level][i]+".png"

        const weaponInfoDiv = document.createElement("div")
        weaponInfoDiv.className = "weapon-info-"+WEAPONS[level][i]

        weaponInfoDiv.innerHTML = WeaponInfo[WEAPONS[level][i]].info
        
        weaponSelection.appendChild(weaponSelectionImg)
        chooseYourWeapon.appendChild(weaponSelection)
        weaponSelection.appendChild(weaponInfoDiv)

        document.getElementById("weapon-selection-"+WEAPONS[level][i]).addEventListener('click', function(event){
            var selection = event.path[1].id.split("-")[2]

            var name = WeaponInfo[selection].type

            resetAll(level, name)

            for(var i; i < document.getElementsByClassName("weapon-selection").length; i++){
                document.getElementsByClassName("weapon-selection")[i].removeEventListener("click")
            }

            chooseYourWeapon.style.opacity = "0.0"

            setTimeout(() =>{
                mainPage2.style.opacity = 0
                currentLevel.initializeEverything()
                setTimeout(() =>{
                    mainPage2.style.background = "none"
                    mainPage2.removeChild(chooseYourWeapon)
                }, 200)
            }, 2800)
        })
    }


    setTimeout(() =>{
        chooseYourWeapon.style.opacity = 1
    },500)

}

function loadCathedral(){
    sky.style.display = "none"
    landscape.style.display = "none"
    landscape2.style.display = "none"
    dirtroad.style.background = "none"
    dirtroad.style.bottom = "0%"

    mainPage.style.backgroundImage = "url(images/cathedral5.png)"

    mainPage.style.height = window.innerHeight +20
    mainPage.style.width = window.innerWidth
    mainPage2.style.bottom = window.innerHeight

    player1.healthbar.bar.style.zIndex = 10
    player1.scroll = false
    player1.enemyCount += 1
}

function loadCathedral2(){
    const church = document.createElement('div')
    const churchImg = document.createElement("img")

    church.className = "church"
    churchImg.src = "images/sideCathedral9.png"

    church.appendChild(churchImg)

    dirtroad.appendChild(church)
}


function checkTouching(obj1, obj2){

    return !(
        obj1.x + 20 + obj1.width < obj2.x + 20 ||
        obj1.x + 20 > obj2.x + 20 + obj2.width ||
        obj1.y + obj1.height < obj2.y || obj1.y > obj2.y + obj2.height
    )

    // return(
    //     obj1.x + 20 > obj2.x + 20 &&
    //     obj1.x + 20 < obj2.x + 20 + obj2.width &&
    //     obj1.y > obj2. y && obj1.y < obj2.y + obj2.height
    // )
} 

function distanceTo(obj1, obj2){
    return Math.abs((obj1.center - obj2.center))
}

function acquireNewItem(item){

    messageDiv.innerHTML = `New Item Aquired: `+ item.name

    item.body.style.display = "block"
    item.body.style.left = "50%"
    item.body.style.bottom = "10%"
    
    messageDiv.style.marginBottom = "20%"
    messageDiv.style.width = 800
    messageDiv.appendChild(item.body)
    mainPage2.style.opacity = 1.0

    awesomeTimeout(() => {
        mainPage2.style.opacity = 0.0
        messageDiv.removeChild(messageDiv.firstChild)
        messageDiv.innerHTML = ""
        messageDiv.style.marginBottom = "none"
        messageDiv.style.width = "auto"
    }, 4000)

}

function resetAll(level, weapon){
    mainPage.style.display = "none"
    console.log(weapon)
    if(sky.firstChild){
        sky.removeChild(sky.firstChild)
        resetAll(level, weapon)
    } else if(landscape.firstChild){
        landscape.removeChild(landscape.firstChild)
        resetAll(level, weapon)
    } else if(dirtroad.firstChild){
        dirtroad.removeChild(dirtroad.firstChild)
        resetAll(level, weapon)
    } else if(landscape2.firstChild){
        landscape2.removeChild(landscape2.firstChild)
        resetAll(level, weapon)
    }else if(document.getElementsByClassName('hp-number')[0]){
        mainPage.removeChild(document.getElementsByClassName('hp-number')[0])
        resetAll(level, weapon)
    }else if(document.getElementsByClassName('bosshealthbar')[0]){
        mainPage.removeChild(document.getElementsByClassName('bosshealthbar')[0])
        resetAll(level, weapon)
    }else {
        console.log("LEVEL", level, weapon)
        currentLevel = new Level(level, weapon)
        mainPage.style.display = "block"
    }
}

function generateForest(viewDist){

    console.log(viewDist)

    var renderDistance = parseInt(viewDist/270 * 2 * 4)

    const sun = new Sun(200, -50, "images/Enviroment/sun.png", document.getElementsByClassName('sky')[0])

    const moon = new Moon(1000, 300, "images/Enviroment/moon.png", document.getElementsByClassName('sky')[0])

    var cloudList = []
    var upperTreeList = []
    var lowerTreeList = []

    for(var i = 0; i < 19; i++){
    
        if(i%2 === 0){
            var T = getRndInteger(-20, 10) + 20
        } else{
            var T = getRndInteger(-10, 30) - 20
        }
    
        var L = i*350 + getRndInteger(0, 20)

        var drift = getRndInteger(1, 2) / 10
    
        const newCloud = new Cloud(L, T, "images/Enviroment/cloud.png", document.getElementsByClassName('sky')[0], drift)

        cloudList.push(newCloud)
    }
    
    for(var i = 0; i < renderDistance; i++){
        if(i%2 === 0){
            var T = getRndInteger(-85, -110) - 100
        } else{
            var T = getRndInteger(-110, -160) + 100
        }

        var L = i * 150 + getRndInteger(0, 50)

        if(T > -85){
            T = -85
        }
        if(T < -160){
            T = -160
        }

        const newUpperTree = new Tree(L, T, "images/Enviroment/newTree.png", document.getElementsByClassName('landscape')[0], true)
        newUpperTree.container.id = "UT"+i

        newUpperTree.rendered = false

        if(i%2 != 0){
            newUpperTree.container.style.zIndex = 1
        }

        upperTreeList.push(newUpperTree)
    }
    
    for(var i = 0; i < renderDistance*2; i++){
        if(i%2 === 0){
            var T = getRndInteger(0, -30) - 100
        } else{
            var T = getRndInteger(-30, -60) + 100
        }
    
        var L = i * 150 + getRndInteger(0, 50)

        if(T > 0){
            T = 0
        }
        if(T < -60){
            T = -60
        }

        const newLowerTree = new Tree(L, T, "images/Enviroment/newTree.png", document.getElementsByClassName('landscape-2')[0], true)
        newLowerTree.container.id = "LT"+i

        if(i%2 === 0){
            newLowerTree.container.style.zIndex = 3
        } else {
            newLowerTree.container.style.zIndex = 4
        }

        newLowerTree.rendered = false

        lowerTreeList.push(newLowerTree)
    }

    return {cloudList: cloudList, sun: sun, moon: moon, upperTreeList: upperTreeList, lowerTreeList: lowerTreeList}
    
}



function generateWinterWonderland(viewDist){

    document.getElementsByClassName('landscape')[0].style.background = "white"
    document.getElementsByClassName('landscape-2')[0].style.background = "white"

    console.log(viewDist)

    var renderDistance = parseInt(viewDist/270 * 2 * 4)

    const sun = new Sun(200, -50, "images/Enviroment/sun.png", document.getElementsByClassName('sky')[0])

    const moon = new Moon(1000, 300, "images/Enviroment/moon.png", document.getElementsByClassName('sky')[0])

    var cloudList = []
    var upperTreeList = []
    var lowerTreeList = []

    for(var i = 0; i < 19; i++){
    
        if(i%2 === 0){
            var T = getRndInteger(-20, 10) + 20
        } else{
            var T = getRndInteger(-10, 30) - 20
        }
    
        var L = i*350 + getRndInteger(0, 20)

        var drift = getRndInteger(1, 2) / 10
    
        const newCloud = new Cloud(L, T, "images/Enviroment/cloud.png", document.getElementsByClassName('sky')[0], drift)

        cloudList.push(newCloud)
    }

    for(var i = 0; i < renderDistance; i++){
        if(i%2 === 0){
            var T = getRndInteger(-50, -110) - 100
        } else{
            var T = getRndInteger(-110, -160) + 100
        }

        var L = i * 250 + getRndInteger(0, 50)

        if(T > -50){
            T = -50
        }
        if(T < -160){
            T = -160
        }

        const newUpperTree = new Tree(L, T, "images/Enviroment/snowTree.png", document.getElementsByClassName('landscape')[0], true)
        newUpperTree.container.id = "UT"+i

        newUpperTree.rendered = false

        if(i%2 != 0){
            newUpperTree.container.style.zIndex = 1
        }

        upperTreeList.push(newUpperTree)
    }
    
    for(var i = 0; i < renderDistance*2; i++){
        if(i%2 === 0){
            var T = getRndInteger(0, -30) - 100
        } else{
            var T = getRndInteger(-30, -60) + 100
        }
    
        var L = i * 250 + getRndInteger(0, 50)

        if(T > 0){
            T = 0
        }
        if(T < -60){
            T = -60
        }

        const newLowerTree = new Tree(L, T, "images/Enviroment/snowTree.png", document.getElementsByClassName('landscape-2')[0], true)
        newLowerTree.container.id = "LT"+i

        if(i%2 === 0){
            newLowerTree.container.style.zIndex = 3
        } else {
            newLowerTree.container.style.zIndex = 4
        }

        newLowerTree.rendered = false

        lowerTreeList.push(newLowerTree)
    }

    const snowDiv = document.createElement('div')
    snowDiv.id = "snow"

    mainPage.appendChild(snowDiv)

    toggle_snow()
    
    
    return {cloudList: cloudList, sun: sun, moon: moon, upperTreeList: upperTreeList, lowerTreeList: lowerTreeList}
}






