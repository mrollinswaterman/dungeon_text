
const JUMPINITIALVELOCITY = 70
/* layout:
    speed, hp, jumpdist, damage, knockback, offset, slow percent, snowball attack
*/

DIMENSIONS = {
    "":{
        "small":[85, 75],
        "medium":[120, 100]//placeholder
    },
    "Ice":{
        "small":[75, 65],//placeholder
        "medium":[110, 90]
    }
}

PROPERTIES = {
    "":{
        "small":[50, 70, 350, 10, 0, {x:0,y:30}],
        "medium":[35, 100, 250, 15, 2, {x:0,y:30}],
        "large":[10, 130, 100, 25, 5,]
    },
    "Ice":{
        "small":[80, 50, 520, 5, 0, {x:0, y: 25}, .1, false],
        "medium":[35, 100, 250, 30, 2, {x:0,y:12}, .2, true]
    }
}

class Slime {
    constructor(distance, player, size, type = ""){
        this.distance = distance

        this.dead = false
        this.dying = false

        this.speed = PROPERTIES[type][size][0]
        this.hpVal = PROPERTIES[type][size][1]
        this.jumpDist = PROPERTIES[type][size][2]
        this.damage = PROPERTIES[type][size][3]
        this.knockback = PROPERTIES[type][size][4]
        this.baseY = 0
        this.offset = PROPERTIES[type][size][5]

        this.name = size+type+"Slime"

        this.path = false

        this.viewDistance = window.innerWidth

        //create slime body
        if(this.name != undefined){
            this.body = document.createElement('div')
            this.body.className = this.name
            this.body.id = this.name+this.distance
    
            this.img = document.createElement('img')
            this.img.className = this.name+'-img'
            this.img.id = this.name+this.distance+"-img"
            this.img.src = "images/Slimes/"+this.name+".png"
    
            this.hitboxDiv = document.createElement('div')
            this.hitboxDiv.className = this.name+"-hitbox"
    
            this.body.appendChild(this.img)
            this.body.appendChild(this.hitboxDiv)
    
            //position slime


            this.body.style.left = (1200+this.distance*2000)


           // console.log(1200+ this.distance * 2000, this)
    
            document.getElementsByClassName('dirtroad')[0].appendChild(this.body)
    
            this.healthbar = new HealthBar(this.hpVal, this)
    
            this.enemy = player
    
            this.width = DIMENSIONS[type][size][0]
            this.height = DIMENSIONS[type][size][1]

            this.pinned = false

            //initialize position variables
            this.y = this.baseY
            this.yVel = 0
    
            this.body.style.bottom = this.y + this.offset.y
    
            this.x = (1200+this.distance*2000)
            this.xVel = 0

            this.leftEdge = window.innerWidth - (1200+this.distance*2000)

            this.hitbox = {
                width: this.width,
                height: this.height,

                c1:{
                    x: this.x,
                    y: this.y
                },
                c2:{
                    x: this.x,
                    y: this.y + this.height
                },
                c3:{
                    x: this.x + this.width,
                    y: this.y + this.height
                },
                c4:{
                    x: this.x + this.width,
                    y: this.y
                }
            }

            this.center = this.x + (this.width/2)
    
        }

    }

    update() {

        this.hitbox = {
            width: this.width,
            height: this.height,

            c1:{
                x: this.x,
                y: this.y
            },
            c2:{
                x: this.x,
                y: this.y + this.height
            },
            c3:{
                x: this.x + this.width,
                y: this.y + this.height
            },
            c4:{
                x: this.x + this.width,
                y: this.y
            }
        }


        //gravity

        if(this.y >= this.baseY && this.yVel != 0){
            this.y += this.yVel * 30 / 100
            this.yVel -= 9 * 30 / 100
            this.body.style.bottom = this.y + this.offset.y
            if(this.y <= this.baseY){
                this.xVel = 0
                this.yVel = 0
                this.y = this.baseY
                this.body.style.bottom = this.y + this.offset.y
                this.path = false
            }
        }
        
        if(!this.dead){
            //move
            this.move()

            this.center = this.x + (this.width/2)

            //bouncy???
            if(this.pinned){
                if(this.x + this.width > this.enemy.rightEdge && distanceTo(this.enemy, this) < this.enemy.viewDistance){
                    this.xVel = 0
                    this.path = false
                    this.x = this.enemy.rightEdge - 10 - this.width
                }
                if(this.x < this.enemy.leftEdge){
                    this.xVel = 0
                    this.path = false
                    this.x = this.enemy.leftEdge + 10
                }
            }

            //pathfinding
            if(this.path === false && !this.dying){
                this.path = true
                this.pathfinding()
            }

            //collision
            if(!checkTouching(this.enemy, this) && !this.dying){
                this.checkCollision()
            }
        }

    }

    move(){

        if(distanceTo(this.enemy, this) < this.viewDistance){


            this.x += this.xVel * 10 / 100
            this.body.style.left = this.x

            if(this.y <= this.baseY && distanceTo(this.enemy, this) > this.jumpDist - 50 && distanceTo(this.enemy, this) < this.jumpDist && this.xVel != 0){
                if(this.center > this.enemy.center){
                    this.xVel = -this.speed * 1.25
                } else {
                    this.xVel = this.speed * 1.25
                }
                
                if (this.yVel == 0) {
                    this.yVel = JUMPINITIALVELOCITY
                }
            }
        }
    }

    pathfinding(){

            awesomeTimeout(() => {
                if(this.y <= this.baseY && this.yVel === 0 && this.xVel === 0){

                    if(distanceTo(this.enemy, this) < this.jumpDist - 50){
                        this.yVel = 0
                        if(this.center > this.enemy.center){
                            this.img.style.transform = "scaleX(1)"
                            this.xVel = this.speed
                        } else{
                            this.img.style.transform = "scaleX(-1)"
                            this.xVel = -this.speed            
                        }
                    } else {
                        if(this.center > this.enemy.center){
                            this.img.style.transform = "scaleX(1)"
                            this.xVel = -this.speed
                        } else{
                            this.img.style.transform = "scaleX(-1)"
                            this.xVel = this.speed            
                        }
                    }
    
                    if(this.dead){
                        this.yVel = 0
                        this.xVel = 0
                    }
                }
                console

                
            }, (10000 - (this.speed * 100))/6)
    }

    checkCollision(){
        awesomeTimeout(() =>{
            if(checkTouching(this.enemy, this)){
                if(!this.pinned){
                    this.pinned = true
                }
    
                this.enemy.getHit(this, this.damage, this.knockback)
    
                if(this.center > this.enemy.center){
                    this.xVel = this.speed * 3
                    if(this.yVel < JUMPINITIALVELOCITY){
                        this.yVel = JUMPINITIALVELOCITY
                    }
                } else{
                    this.xVel = -this.speed * 3
                    if(this.yVel < JUMPINITIALVELOCITY){
                        this.yVel = JUMPINITIALVELOCITY
                    }
                }
            }
        }, 10)
    }

    getHit(knockback, damage){

        if(!this.pinned){
            this.pinned = true
        }
        
        if(this.center > this.enemy.center){
            this.xVel = this.speed * knockback
        } else{
            this.xVel = -this.speed * knockback
        }

        this.healthbar.loseHealth(damage)

        if(this.healthbar.hp <= 0){
            
            if(this.y > this.baseY && this.yVel < JUMPINITIALVELOCITY){
            } else {
                this.yVel = 0
            }
        } else {
            if(this.yVel < JUMPINITIALVELOCITY){
                this.yVel = JUMPINITIALVELOCITY
            }
        }





    }

    die(){

        this.enemy.enemyCount -= 1
        this.dying = true

        awesomeTimeout(() => {

            this.img.src = "images/Slimes/"+this.name+"-death0.png"
            
        }, 200);

        awesomeTimeout(() => {

            this.img.src = "images/Slimes/"+this.name+"-death1.png"

        }, 600)


        awesomeTimeout(() =>{

            this.img.src = "images/Slimes/"+this.name+"-death2.png"            
            this.dead = true
        }, 1000)

        awesomeTimeout(() =>{

            this.img.src = "images/Slimes/"+this.name+"-death3.png"
            
        }, 1400)



        awesomeTimeout(() => {
            if(document.getElementsByClassName('dirtroad')[0].contains(this.body)){
                document.getElementsByClassName('dirtroad')[0].removeChild(this.body)
            }

            this.body.style.display = 'none'


        }, 1800);
    }
}

class IceSlime extends Slime{
    constructor(dist, player, size, type="Ice"){
        super(dist, player, size, "Ice")

        this.slowEffect = PROPERTIES[type][size][6]
        this.snowballAttack = PROPERTIES[type][size][7]

        this.pause = false

        if(this.snowballAttack){
            this.xVel = null
        } else {
            this.xVel = 0
        }

    }

    update(){
        //gravity
        if(this.y >= this.baseY && this.yVel != 0){
            this.y += this.yVel * 30 / 100
            this.yVel -= 9 * 30 / 100
            this.body.style.bottom = this.y + this.offset.y
            if(this.y <= this.baseY){
                this.xVel = 0
                this.yVel = 0
                this.y = this.baseY
                this.body.style.bottom = this.y + this.offset.y
                this.path = false
            }
        }

        //update hitbox
        this.hitbox = {
            width: this.width,
            height: this.height,

            c1:{
                x: this.x,
                y: this.y
            },
            c2:{
                x: this.x,
                y: this.y + this.height
            },
            c3:{
                x: this.x + this.width,
                y: this.y + this.height
            },
            c4:{
                x: this.x + this.width,
                y: this.y
            }
        }
        
        if(!this.dead){
            if(this.snowballAttack){
                this.throwTime = .5
            }
            this.center = this.x + (this.width/2)

            if(!checkTouching(this.enemy, this)){
                this.checkCollision()
            }

            if(this.path === false && !this.pause){
                this.path = true
                this.pathfinding()
            }
    
            if(!this.pause){
                this.move()
            }
    
            if(this.xVel === null && this.snowballAttack){
                this.chooseAttackPattern()
            }

            //bouncy
            if(this.pinned){
                if(this.x + this.width > this.enemy.rightEdge && distanceTo(this.enemy, this) < this.enemy.viewDistance){
                    this.xVel = 0
                    this.path = false
                    this.x = this.enemy.rightEdge - 10 - this.width
                }
                if(this.x < this.enemy.leftEdge){
                    this.xVel = 0
                    this.path = false
                    this.x = this.enemy.leftEdge + 10
                }
            }
        }
        
    }


    chooseAttackPattern(){
        if(this.xVel == null){
            this.xVel = 0
        }
        if(distanceTo(this.enemy, this) < this.jumpDist * 4 && distanceTo(this.enemy, this) > this.jumpDist * 1.5 && this.y <= this.baseY){
            if(this.snowball === undefined){
                if(!this.pinned){
                    this.pinned = true
                }
                this.throwSnowball()
            }
        } else {
            this.pause = false
        }
    }

    move(){
        if(distanceTo(this.enemy, this) < this.viewDistance){

            this.x += this.xVel * 10 / 100
            this.body.style.left = this.x

            if(this.y <= this.baseY && distanceTo(this.enemy, this) > this.jumpDist - 50 && distanceTo(this.enemy, this) < this.jumpDist && this.xVel != 0){
                console.log(distanceTo(this.enemy, this))
                if(this.center > this.enemy.center){
                    this.xVel = -this.speed * 1.25
                } else {
                    this.xVel = this.speed * 1.25
                }
                
                if (this.yVel == 0) {
                    this.yVel = JUMPINITIALVELOCITY
                }
            } else if(distanceTo(this.enemy, this) <= this.jumpDist * 4 && this.snowballAttack){
                this.pause = true
                this.chooseAttackPattern()
            }
        }

    }

    slow(){
        if(!this.pinned){
            this.pinned = true
        }
        this.enemy.speed = this.enemy.speed * (1-this.slowEffect)
        this.enemy.initialJumpVel = this.enemy.initialJumpVel * (1-this.slowEffect)
        this.enemy.weapon.swingTime = this.enemy.weapon.swingTime * (1+this.slowEffect)
        this.enemy.weapon.recoveryTime = this.enemy.weapon.recoveryTime * (1+this.slowEffect)
        this.enemy.weapon.windupTime = this.enemy.weapon.windupTime * (1+this.slowEffect)
        this.enemy.slowed++

        if(this.enemy.slowed <= 1){
            awesomeTimeout(()=>{

                if(this.enemy.slowed > 0){
                    this.enemy.speed = parseInt(this.enemy.speed/(1-this.slowEffect*this.enemy.slowed))
                    this.enemy.initialJumpVel = parseInt(this.enemy.initialJumpVel/(1-this.slowEffect*this.enemy.slowed))
                    this.enemy.weapon.swingTime = parseInt(this.enemy.weapon.swingTime / (1+this.slowEffect*this.enemy.slowed))
                    this.enemy.weapon.recoveryTime = parseInt(this.enemy.weapon.recoveryTime / (1+this.slowEffect*this.enemy.slowed))
                    this.enemy.weapon.windupTime = parseInt(this.enemy.weapon.windupTime / (1+this.slowEffect*this.enemy.slowed))
                    this.enemy.slowed = 0
                }
            }, 5000)
        }
    }

    throwSnowball(){  
        this.body.style.transition = "all .5s"
 
        if(this.center > this.enemy.center){
            this.body.style.transformOrigin = "bottom right"
            this.body.style.transform = "scaleX(1) rotate(3deg)"
        }else{
            this.body.style.transformOrigin = "bottom left"
            this.body.style.transform = "scaleX(-1) rotate(-3deg)"
        }
        
        awesomeTimeout(() =>{
            this.body.style.transform = "rotate(0deg)"
            this.body.style.transition = "none"
            if(this.center > this.enemy.center){
                this.snowball = new Snowball(this.slowEffect, this.x, this.y, this)
            } else{
                this.snowball = new Snowball(this.slowEffect, this.x+this.width, this.y, this)
            }
            awesomeTimeout(() =>{
                this.snowball.delete()
                this.snowball = undefined
                this.chooseAttackPattern()
            }, (10000 - (this.speed * 100))/2)
        }, this.throwTime*1000)
    }

    checkCollision(){
        awesomeTimeout(() =>{
            if(checkTouching(this.enemy, this)){
                if(!this.pinned){
                    this.pinned = true
                }
    
                this.enemy.getHit(this, this.damage, this.knockback)
    
                if(this.enemy.slowed < 3){
                    this.slow()
                }
    
                if(this.center > this.enemy.center){
                    this.xVel = this.speed 
                    if(this.yVel < JUMPINITIALVELOCITY/1.5){
                        this.yVel = JUMPINITIALVELOCITY/1.5
                    }
                } else{
                    this.xVel = -this.speed
                    if(this.yVel < JUMPINITIALVELOCITY/1.5){
                        this.yVel = JUMPINITIALVELOCITY/1.5
                    }
                }
            }
        },10)
    }

    getHit(knockback, damage){

        this.pause = false
        
        if(this.center > this.enemy.center){
            this.xVel = (this.speed) * knockback
        } else{
            this.xVel = (-this.speed) * knockback
        }

        if(this.yVel < JUMPINITIALVELOCITY/1.5){
            this.yVel = JUMPINITIALVELOCITY/1.5
        }

        this.healthbar.loseHealth(damage)

    }

}


class Snowball{
    constructor(slowEffect, x, y, thrower){
        this.speed = 12
        this.slowEffect = slowEffect
        this.thrower = thrower

        this.x = x
        this.y = y + 40

        this.yVel = 5

        if(this.thrower.center > this.thrower.enemy.center){
            this.xVel = -this.speed
        } else {
            this.xVel = this.speed
        }

        this.damage = 10
        this.knockback = 0

        this.width = 70
        this.height = 60

        this.body = document.createElement("div")
        this.body.className = "snowball"

        this.img = document.createElement("img")
        this.img.className = "snowball-img"
        this.img.src = "images/Slimes/snowball.png"
        
        this.body.appendChild(this.img)

        this.body.style.left = this.x
        this.body.style.bottom = this.y - this.thrower.offset.y

        this.collisionDetection = true

        this.done = false


        document.getElementsByClassName('dirtroad')[0].appendChild(this.body)
    }

    update(){

        this.center = this.x + (this.width/2)

        this.y += this.yVel * 10 / 100
        this.yVel -= 1 * 10 / 100
        this.body.style.bottom = this.y - this.thrower.offset.y

        this.move()

        if(this.collisionDetection === true){
            this.checkCollision()
        }
    }

    move(){
        this.x += this.xVel
        this.body.style.left = this.x
    }

    checkCollision(){
        if(this.center > this.thrower.enemy.x && this.center < (this.thrower.enemy.x +this.thrower.enemy.width)){
            this.collisonDetection = false
            if(this.y > this.thrower.enemy.y && this.y < (this.thrower.enemy.y + this.thrower.enemy.height)){
                this.done = true
                this.thrower.enemy.getHit(this.thrower, this.damage, this.knockback)
                this.thrower.slow()
                this.body.style.display = "none"

            }
        }
    }

    delete(){
        this.body.style.display = "none"
        if(this.body.parentNode.contains(this.body)){
            this.body.parentNode.removeChild(this.body)
        }
    }
}

class BigSnowball extends Snowball{
    constructor(slowEffect, x, y, thrower){
        super(slowEffect, x, y, thrower)

        this.speed = 24

        this.damage = 15
        this.knockback = 5

        this.width = 70
        this.height = 60

        this.img.src = "images/Bosses/BigSnowball.png"

        this.damage = this.thrower.snowballDamage

        this.knockback = this.thrower.snowballKnockback
    }

}


console.log("Initializing Enemies...")

awesomeTimeout((console.log("Enemies Initialized")), 1000)