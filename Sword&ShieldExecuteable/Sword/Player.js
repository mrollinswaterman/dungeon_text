// notes:

console.log("Initializing Player...")

awesomeTimeout((console.log("Player Initialized")), 1000)

DEATHNOTES = [
    'You Died',
    'Eat it',
    'Whoops',
    'Good Try',
    "Clearly, this game isn't meant for everyone",
    'Better luck next time',
    'That must have stung',
    "Fin",
    "Have you tried not getting hit?",
    "Wow, you're bad at this",
    "End of the line",
    'Nice job',
    "Hey, maybe the NPCs are just having a really good day. "

]



INITIALJUMPVELOCITY = 100
class Player {
    constructor(num, selectedWeapon, enemiesList){

        this.enemiesList = enemiesList

        this.cooldown = 0

        this.WEAPONS = {"sword": new Sword(this), "greatsword": new Greatsword(this)}

        //create player box
        this.player = document.createElement('div')
        this.player.className = "player"
        this.player.id = 'player'+num

        this.speed = 5
        this.initialJumpVel = INITIALJUMPVELOCITY
        this.x = 100
        this.xVel = this.speed
        this.baseY = 0
        this.y = this.baseY
        this.yVel = 0
        this.leftEdge = 10
        this.rightEdge = window.innerWidth -10

        this.viewDistance = this.rightEdge - this.x
        this.renderDistance = window.innerWidth

        this.attacking = false
        this.direction = null

        this.weapon = this.WEAPONS[selectedWeapon]

        //create hero
        this.herobody = document.createElement('div')
        this.herobody.className = 'herobody'
        
        this.bodyimg = document.createElement('img')
        this.bodyimg.src = "images/player.png"
        this.bodyimg.className = 'bodyimg'

        this.herobody.appendChild(this.bodyimg)

        this.handw = document.createElement('div')
        this.handw.className = 'handw'

        //da hand
        this.hand = document.createElement('img')
        this.hand.className = 'hand'
        this.hand.id = "herohand"
        this.hand.src = "images/hand4.png"

        this.hand2 = document.createElement('img')
        this.hand2.className = 'hand2'
        this.hand2.id = "herohand2"
        this.hand2.src = "images/hand4.png"

        //this.hand2.style.display = "none"

        //hitbox
        this.hitbox = document.createElement('div')
        this.hitbox.className = "player-hitbox"

        //hp bar
        this.healthbar = new PlayerHealthBar(100, this)

        //append everything
        this.handw.appendChild(this.hand)
        //this.handw.appendChild(this.hand2)
        this.handw.appendChild(this.weapon.body)

        this.herobody.appendChild(this.handw)

        this.player.appendChild(this.herobody)
        this.player.appendChild(this.hitbox)

        document.getElementsByClassName('dirtroad')[0].appendChild(this.player)

        //effects
        this.slowed = 0

        this.jumping = false
        this.scroll = false

        this.pause = false

        this.enemyCount = 0

        this.width = 79
        this.height = 60
        this.center = this.x + (this.width/2)

        this.offset ={
            x: 0,
            y: -15
        }

        this.player.style.bottom = this.y + this.offset.y

        this.hitbox = {
            width: this.width,
            height: this.height,
            c1: {
                x: this.x,
                y: this.y+25
            },
            c2:{
                x: this.x,
                y: this.y+this.height+25
            },
            c3:{
                x:this.x+this.width,
                y: this.y + this.height+25
            },
            c4:{
                x: this.x+this.width,
                y: this.y+25
            }
        }

        this.collisionDetection = true

        this.lastUpperTreeIndex = 0
        this.lastLowerTreeIndex = 0

        this.cutscene = false
        this.knockback = false

        this.newGame = true

        this.levelCounter = 1

        this.dead = false

        //this.pointer = document.createElement("div")

        //this.pointer.className = "pointer"

        // this.pointer2 = document.createElement("div")

        // this.pointer2.className = "pointer"

       // dirtroad.appendChild(this.pointer)
        // // dirtroad.appendChild(this.pointer2)

    }

    update() {

        this.center = this.x + (this.width/2) + 10

        //gravity
        if(this.y >=this.baseY && this.yVel != 0){
            this.y += this.yVel * 30 / 100
            this.yVel -= (0.2*this.initialJumpVel) * 30 / 100
            this.player.style.bottom = this.y + this.offset.y
           if(this.y <= this.baseY){
                this.jumping = false
                this.y = this.baseY
                this.yVel = 0
                this.knockback = false
                this.player.style.bottom = this.y + this.offset.y
           }
        }

        if(this.enemyCount === 0){
            this.scroll = true
        }
        if(this.enemyCount > 0){
            this.scroll = false
        }

        if(this.enemyCount < 0){
            this.enemeyCount = 0
        }
        
        if(this.cutscene){
            this.scroll = false
            this.stop()
            this.jumping = false
        }

        if(this.pause){
            this.scroll = false
            this.stop()
            this.jumping = false
        }

        //adjust hitbox
        this.hitbox = {
            width: this.width,
            height: this.height,
            c1: {
                x: this.x,
                y: this.y+25
            },
            c2:{
                x: this.x,
                y: this.y+this.height+25
            },
            c3:{
                x:this.x+this.width,
                y: this.y + this.height+25
            },
            c4:{
                x: this.x+this.width,
                y: this.y+25
            }
        }

        //scroll 
        if(this.scroll && this.direction != null){
            this.scrolling()
        }

        //are you jumping?
        if(this.jumping){
            if(this.yVel === 0){
                this.yVel = this.initialJumpVel
            }
        }

        //are you being knocked back?
        if(this.knockback){
            this.direction = null
            this.x += this.xVel
            this.player.style.left = this.x
        }


        //move stuff
        if(this.direction != null && this.x > this.leftEdge && this.x < this.rightEdge){

            this.handw.style.transition = "none"
            
            if(this.direction == "left"){
                this.xVel = -this.speed
                this.bodyimg.style.transform = "scaleX(1)"
                this.handw.style.transition = ""
                this.handw.style.left = 43

            } else if(this.direction == "right"){
                this.xVel = this.speed
                this.bodyimg.style.transform = "scaleX(-1)"
                this.handw.style.transition = ""
                this.handw.style.left = 43
        
            }

            if (!this.attacking)
            {
                this.x += this.xVel
            }
            this.player.style.left = this.x

        } else if(this.x <= this.leftEdge){
            this.xVel = 0
            this.x = this.leftEdge + 1
        } else if(this.x >= this.rightEdge){
            this.xVel = 0
            this.x = this.rightEdge - 1
        }

        //are there monsters nearby?
        if(this.enemiesList.length > 0 && this.enemyCount === 0){
            this.enemiesList.forEach(slime => {
                if(distanceTo(this, slime) < this.viewDistance && !slime.dying){
                        this.enemyCount++
                        this.scroll = false
                }
            })
        }

        //spawn trees
        for(var t = this.lastUpperTreeIndex; t < uTreeList.length; t++){
            var upperTree = uTreeList[t]

            if((upperTree.x - this.x) < this.renderDistance){
                upperTree.rendered = true
                this.lastUpperTreeIndex = t
            } else {
                break
            }
        }
        for(var t = this.lastLowerTreeIndex; t < lTreeList.length; t++){
            var lowerTree = lTreeList[t]

            if((lowerTree.x - this.x) < this.renderDistance){
                lowerTree.rendered = true
                this.lastLowerTreeIndex = t
            } else {
                break
            }
        }

        if(this.attacking && this.weapon.angle <= this.weapon.maxAngle){
            this.weapon.angle += this.weapon.swingTime
        }

        //collision + hit detection
        if(this.collisionDetection){
            this.checkCollision()
        }  

        //effects
        if(this.slowed > 0){
            var color = {
                r: 122,
                g: 208,
                b:255
            }
            color.r -= this.slowed * 20
            color.g -= this.slowed * 30
            this.bodyimg.style.filter = "drop-shadow(1px 1px "+this.slowed*10+"px rgb("+color.r+","+color.g+","+color.b+"))"
        } else if (this.slowed === 0){
            this.bodyimg.style.filter = "none"

        }
        
        //next Level
        // if(parseInt(sign.style.left) - this.x <= 670){
        //     this.enemyCount = 1
        //     this.scroll = false

        //     if((this.x >= this.rightEdge || this.x >= this.rightEdge - 20) && !this.cutscene){
        //         this.cutscene = true
        //         nextLevel(this.levelCounter)
                
        //     }
        // }

    }


    move(direction){
        this.direction = {'a': 'left', 'd': 'right'}[direction]
    }

    stop() {
        this.direction = null
    }

    attack(){
        this.cooldown = 1
        this.pause = true
        awesomeTimeout(() =>{
            
            this.pause = false

            awesomeTimeout(() =>{
                this.cooldown = 0
            }, this.weapon.cooldownTime*2)
        }, this.weapon.cooldownTime)

        this.weapon.attack()
    }

    checkCollision(){
        if(Object.values(this.enemiesList).length > 0){
            Object.values(this.enemiesList).forEach(slime => {
                if(slime.hitbox){
                    if(detectCollision(slime.hitbox,this.weapon.hitbox) && this.attacking === true && !slime.dead){
                        this.collisionDetection = false
                        slime.getHit(this.weapon.knockback, this.weapon.damage)
                        awesomeTimeout(() => {
                            this.collisionDetection = true
                        }, 600)
                    }
                }
            })
        }

        bossList.forEach(boss => {
            if(detectCollision(boss.hitbox,this.weapon.hitbox)&& this.attacking === true && !boss.dead){
                if(boss.hitbox){
                    this.collisionDetection = false
                    boss.getHit(this.weapon.damage)
                    awesomeTimeout(() => {
                        this.collisionDetection = true
                    }, 400)
                }
            }
        })
    }
    
    getHit(source, damage, knockback){

        this.healthbar.loseHealth(damage)

        if(knockback > 0){
            this.knockback = true
            this.yVel = knockback * 10
            if(this.center < source.center){
                this.xVel = -this.speed*knockback/2
            } else{
                this.xVel = this.speed*knockback/2
            }

        }
    }

    scrolling(){
        this.rightEdge = window.xScroll + window.innerWidth
        this.leftEdge = window.xScroll
        if ((this.x - window.xScroll) > 500) {
            if(this.x > 500){
                var target = this.x - 500
                var camSpeed = this.speed*3
                var mxOffset = window.xScroll + camSpeed
                var mnOffset = window.xScroll - camSpeed

                window.xScroll = Math.min(Math.max(mnOffset, target), mxOffset)

            } else{
                window.xScroll = this.x - 500
            }
            this.player.style.left = this.x - window.xScroll
            //debugger

            var brightness = ((1-window.xScroll/40000).toFixed(1))
            document.getElementsByClassName('sky')[0].style.left = 0 - window.xScroll/2.5
            document.getElementsByClassName('landscape')[0].style.left = 0 - window.xScroll/1.5
            document.getElementsByClassName('landscape')[0].style.filter = "brightness(" + brightness + ")"
            document.getElementsByClassName('landscape-2')[0].style.left = 0 - window.xScroll
            document.getElementsByClassName('landscape-2')[0].style.filter = "brightness("+((1-window.xScroll/40000).toFixed(1))+")"
            document.getElementsByClassName('dirtroad')[0].style.left = 0 - window.xScroll


            //sun movement
            sun.x = window.xScroll/2.5 + sun.xInitial
            sun.y += sun.vel
            if(sun.y > 300){
                sun.vel *= -1
            }
            if(sun.y < -50){
                sun.vel *= -1
            }

            //moon movement
            moon.x = window.xScroll/2.5 + moon.xInitial
            moon.y += -moon.vel
            if(moon.y < 0){
                moon.vel *= -1
            }
            if(moon.y > 300){
                moon.vel *= -1
            }

            //brightness for evironment objs
            Array.from(document.getElementsByClassName('cloud-holder')).forEach(cloud => {
                cloud.style.filter = "brightness("+brightness+")"
            })
            Array.from(document.getElementsByClassName('tree-holder')).forEach(tree => {
                tree.style.filter = "brightness("+brightness+")"
            })

        }
    }

    die(){
        this.dead = true
        mainPage2.style.background = "black"
        mainPage2.style.opacity = 1.0
        deathNote.innerHTML = DEATHNOTES[getRndInteger(0, DEATHNOTES.length)]

        setTimeout(() =>{
            resetAll(this.levelCounter, this.weapon.body.className)

            setTimeout(() =>{
                mainPage2.style.background = "none"
                mainPage2.style.opacity = 0

                setTimeout(() =>{
                    currentLevel.initializeEverything()
                },10)
            },2000)
        },4000)

    }
}

