//notes:

//asmorel tree needs more green

//see if theres a good way to change snow speed

console.log("Initializing variables...")

setTimeout(() => {
    console.log("Variables Initialized")
}, 1000)


const mainPage = document.getElementById("main")
const mainPage2 = document.getElementsByClassName("main2")[0]

console.log(window.innerHeight)

mainPage2.style.height = window.innerHeight + 100
mainPage2.style.width = window.innerWidth

const deathNote = document.createElement('div')
deathNote.className = "death-note"
mainPage2.appendChild(deathNote)

const defeatMessage = document.createElement("div")
defeatMessage.className = "defeat-message"
mainPage2.appendChild(defeatMessage)

const messageDiv = document.createElement("div")
messageDiv.className = "message-div"
mainPage2.appendChild(messageDiv)

const sky = document.getElementsByClassName('sky')[0]
const landscape = document.getElementsByClassName('landscape')[0]
const dirtroad = document.getElementsByClassName('dirtroad')[0]
const landscape2 = document.getElementsByClassName('landscape-2')[0]

sky.style.width = window.innerWidth * 4 
landscape.style.width = window.innerWidth * 5

dirtroad.style.width = window.innerWidth * 7
landscape2.style.width = window.innerWidth * 10

const sign = document.createElement('img')
sign.className = 'sign'
sign.src = "images/continue.png"

dirtroad.appendChild(sign)

document.body.addEventListener("keydown", function(event){
    if(event.key === " "){
        event.preventDefault()
    }
})

//initialize all variables
window.xScroll = 0

var healthBars = []

var clouds = []

var weapon = null

var player1 = null

var enviroment = null

var cloudList = []
var sun = null
var moon = null
var uTreeList = []
var lTreeList = []

var encounterDist = null

var boss = null

var gerald = null

var bossList = []


document.addEventListener('keydown', function (e) {

    if(e.key === " "){
        if(player1.cooldown === 0 && !player1.cutscene){
            player1.attack()
        }
    }

    if(e.key === "u"){
        loadCathedral2()
    }

    if(e.key == "a" || e.key === "d"){
        player1.move(e.key)
    } 

    if(e.key === "c"){
        player1.jumping = true
    }


    if(e.key == 'q'){
        debugger
    }
})

document.addEventListener('keyup', function (e) {
    if(e.key === "d" || e.key === "a"){
        player1.stop()
    }
})

window.gameTime = 0
let time = Date.now()

main = () => {

}

//var currentLevel = new Level(2, "greatsword")
var currentLevel = new Level(1, "sword")

currentLevel.initializeEverything()
