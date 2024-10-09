BOSS_DIMENSIONS = {
    "Reginald" : [159,140],
    "Gerald" : [85, 75],
    "Amelia": [159, 140],
}

TITLES = {
    "Player" : ["? ? ?","? ? ?"],
    "Reginald": ["Sir Reginald, Head Accountant to the High King", "? ? ?"],
    "Gerald": ["Gerald","Gerald"],
    "Amelia": ["Lady Amelia, Archbishop to the High King", "Lady Amelia"]
}

class Boss{
    constructor(name, x, player){
        this.name = name

        this.x = x
        this.y = 0
        this.baseY = 0

        this.xVel = 0
        this.yVel = 0

        this.body = document.createElement('div')
        this.body.className = `${name}`
        this.body.style.left = this.x

        this.img = document.createElement('img')
        this.img.className = `${name}-img`
        this.img.src = "images/Bosses/"+`${name}.png`

        this.hitbox = document.createElement('div')
        this.hitbox.className = `${name}-hitbox`

        this.body.appendChild(this.img)
        this.body.appendChild(this.hitbox)

        document.getElementsByClassName('dirtroad')[0].appendChild(this.body)

        this.enemy = player

        this.title = {
            full: TITLES[this.name][0],
            short: TITLES[this.name][1]
        }

        this.width = BOSS_DIMENSIONS[name][0]
        this.height = BOSS_DIMENSIONS[name][1]

        this.pause = false
        this.checkCollision = true

        this.center = this.x + (this.width/2)

        this.viewDistance = window.innerWidth

        this.hitbox = {
            width: this.width,
            height: this.height,

            c1: {
                x: this.x,
                y: this.y
            }, 
            c2: {
                x: this.x,
                y: this.y + this.height
            },
            c3: {
                x: this.x + this.width,
                y: this.y + this.height
            },
            c4: {
                x: this.x + this.width,
                y: this.y
            }
        }

    }

    update(){
        this.center = this.x + (this.width/2)

        this.hitbox = {
            width: this.width,
            height: this.height,

            c1: {
                x: this.x,
                y: this.y
            }, 
            c2: {
                x: this.x,
                y: this.y + this.height
            },
            c3: {
                x: this.x + this.width,
                y: this.y + this.height
            },
            c4: {
                x: this.x + this.width,
                y: this.y
            }
        }
    }

    move(){
        if(distanceTo(this, this.enemy) < this.viewDistance){
            this.x += this.xVel * 10 / 100
            this.body.style.left = this.x
        }
    }
}



class Reginald extends Boss{
    constructor(x, player){
        super("Reginald", x, player)

        this.speed = 40
        this.hpVal = 600
        this.baseY = 5
        this.y = 5

        this.healthbar = ""

        this.textbox = undefined

        this.attackCounter = -1

        this.img.src = "images/Bosses/Reginald.png"

        this.dashDistance = 400
        this.dashWindup = 900
        this.dashRecovery = 2000
        this.dashDamage = 15
        this.dashKnockback = 5

        this.jumpDistance = 400
        this.jumpWindup = 800
        this.jumpRecovery = 1500
        this.jumpDamage = 30
        this.jumpKnockback = 10

        this.pause = false
        this.cutscene = true

        this.tracking = false 
    
        this.secondPhase = false

        this.c = null
        this.script = null

        this.shadow = document.createElement('div')
        this.shadow.className = "Reginald-shadow"

        this.body.appendChild(this.shadow)


    }

    update(){

        super.update()

        if(this.dead){
            this.yVel = 0
            this.xVel = 0
        }

        if(this.cutscene && this.enemy.cutscene && !this.pause){
            this.move()
            this.xVel = -this.speed


            if(this.x < this.enemy.rightEdge - 400 && !this.pause){
                this.pause = true
                this.c = 0
                if(this.enemy.newGame){
                    this.script = Reginald_Alt_Speech[getRndInteger(0, Reginald_Alt_Speech.length)]
                    TITLES[this.name][1] = "Sir Reginald S. Slime"
                } else{
                    this.script = Reginald_Speech

                    
                }
            }
        }

        if(this.c != null){

            if(this.c < this.script.length){

                if(this.textbox === undefined){
                    this.textbox = new Textbox()
                }

                if(this.textbox.text === ""){
                    if(this.c <= this.script.length - 1){
                        this.c++
                    }
                }

                
                if(this.script[this.c + 1]){
                    if(this.script[this.c + 1].speaker === "Gerald"){
                        gerald.pause = false
                        gerald.cutscene = true
                        this.img.style.transform = "scaleX(1)"
                    } else if(this.script[this.c+1].speaker === "Player"){

                    }
                }

                if(this.c <= this.script.length - 1){
                    if((this.textbox.text === "" || this.textbox.text == undefined)){
                        this.textbox.speaker = this.script[this.c].speaker
                        this.textbox.text = this.script[this.c].text
                        this.textbox.write()
                        
                    }
                    if(this.script[this.c].delete && !this.textbox.deleting && !this.textbox.deleted && this.c < this.script.length){
                        this.textbox.deleting = true
                    } else if (this.textbox.deleted){
                        this.textbox = undefined
                    }
                }

            } else {
                if(this.textbox != undefined && this.textbox.text === ""){
                    this.textbox.delete()
                    this.textbox = undefined
                    if(gerald.cutscene){
                        gerald.pause = false
                        gerald.cutscene = false
                    }
                    if(!gerald.cutscene){
                        gerald.pause = false
                    }
                    this.img.style.transform = "scaleX(-1)"
                    this.healthbar = new BossHealthBar(this.hpVal, this)
                    awesomeTimeout(()=>{
                        this.pause = false
                        this.cutscene = false
                        this.enemy.cutscene = false
                        this.rightBound = this.x
                    }, 500)
                }
            }
        }

        if(this.y >= this.baseY && this.yVel != 0){
            this.shadow.style.display = 'block'
            if(this.yVel > 0){
                this.y += this.yVel * 30 / 100
                this.yVel -= 9 * 30 / 100
            }else if(this.yVel <= 0 && this.tracking){
                if(this.center - this.enemy.center > 15){
                    this.xVel = -this.speed 
                } else if (this.center - this.enemy.center < 0){
                    this.xVel = this.speed
                }  else if (this.center - this.enemy.center <= 5){
                    this.xVel = 0
                    awesomeTimeout(() => {
                        this.tracking = false
                    }, this.jumpWindup)
                }
            } else{
                this.y += this.yVel * 30 / 100
                this.yVel -= 100 * 30 / 100
            } 
            this.img.style.bottom = this.y


            if(this.y < this.baseY){
                this.shadow.style.display = 'none'
                this.y = this.baseY
                this.yVel = 0

                this.img.style.bottom = this.y
            }
        }
        // if(this.y >= this.baseY && this.yVel != 0){
        //     this.shadow.style.display = 'block'
        //     this.y += this.yVel * 30 / 100
        //     if(this.yVel > 20){
        //         this.yVel -= 9 * 30 / 100
        //     } else if (this.tracking && this.yVel < 20){
        //         console.log('floating')
        //         this.yVel -= 0.01
        //         this.xVel = 0
        //         if(this.center - this.enemy.center > 15){
        //             this.xVel = -this.speed /2 
        //         } else if (this.center - this.enemy.center < 0){
        //             this.xVel = this.speed / 2
        //         } else if (this.center - this.enemy.center <= 15){
        //             this.xVel = 0
        //             awesomeTimeout(() => {
        //                 if(this.tracking && this.yVel < 20){
        //                     this.tracking = false
        //                 }
        //             }, this.jumpWindup)
        //         }
        //     }
        //     else{
        //         this.yVel -= 100 * 30 / 100
        //     }
        //     this.img.style.bottom = this.y

        //     if(this.y < this.baseY){
        //         this.shadow.style.display = 'none'
        //         this.pause = true
        //         this.xVel = 0
        //         this.yVel = 0
        //         this.y = this.baseY
        //         this.img.style.bottom = this.y
        //         awesomeTimeout(() => {
        //             this.pause = false
        //         }, this.jumpRecovery)
        //     }
        // }

        //collision dectection
        if(this.checkCollision){
            if(checkTouching(this.enemy, this)){
                this.checkCollision = false
                this.xVel = 0
                this.pause = true
                if(this.attackCounter >= 0){
                    this.enemy.getHit(this, this.dashDamage, this.dashKnockback)
                    awesomeTimeout(()=> {
                        this.pause = false 
                        this.checkCollision = true
                    },this.dashRecovery)
                } else if (this.attackCounter === 3 || this.attackCounter < 0){
                    this.enemy.getHit(this, this.jumpDamage, this.jumpKnockback)
                    awesomeTimeout(()=> {
                        this.pause = false
                        this.checkCollision = true 
                    },this.jumpRecovery)
                } else{
                    debugger
                }
    
            }
        }

        if(!this.pause && !this.cutscene){
            this.move()

            if(this.dead){
                return
            }

            this.dash()

            this.groundPound()

            //don't go out of bounds
            if(this.center - (this.width/4) < this.enemy.leftEdge){
                this.xVel = 0
                this.pause = true
                this.x = this.enemy.leftEdge + 2

                if(this.secondPhase && this.dashRecovery === 0){
                    this.pause = false
                } else {
                    awesomeTimeout(() => {
                        this.xVel = this.speed * 5
                        this.pause = false
                        awesomeTimeout(() => {
                            this.pause = true
    
                            awesomeTimeout(() =>{
                                this.pause = false
                                this.xVel = 0
                            }, 500)
                        }, 80)
                    }, this.dashRecovery*2)
                }
            } 
            if (this.x + this.width > this.enemy.rightEdge){
                this.xVel = 0
                this.pause = true
                this.x = this.enemy.rightEdge - this.width

                if(this.secondPhase && this.dashRecovery === 0){
                    this.pause = false
                } else {
                    awesomeTimeout(() => {
                        this.xVel = -this.speed * 5
                        this.pause = false
                        awesomeTimeout(() => {
                            this.pause = true
    
                            awesomeTimeout(() =>{
                                this.pause = false
                                this.xVel = 0
                            }, 500)
                        }, 80)
                    }, this.dashRecovery*2)
                }
            }

            //patfinding
            if(this.y <= this.baseY && this.xVel === 0 && this.x != this.enemy.leftEdge && this.x != this.enemy.rightEdge && !this.pause){
                this.pathfinding()
    
            } 

        }
    }

    //distanceTo(this.enemy, this) < this.dashDistance - 50

    pathfinding(){

        if(this.attackCounter === 0){
            this.attackCounter = -1
        }
        this.body.style.transition = "none"

        if(this.center > this.enemy.center){
            this.img.style.transform = "scaleX(-1)"
            this.xVel = -this.speed * 2
        } else{
            this.img.style.transform = "scaleX(1)"
            this.xVel = this.speed * 2   
        }
    }

    move(){
        this.x += this.xVel * 10 / 100
        this.body.style.left = this.x 
    }

    telegraphDash(direction){
        this.body.style.opacity = 0.2
        this.body.style.transition = "all .2s"
        if(direction === "left"){
            this.body.style.transformOrigin = "bottom right"
            this.body.style.transform = "rotate(5deg)"
        } else {
            this.body.style.transformOrigin = "bottom left"
            this.body.style.transform = "rotate(-5deg)"
        }
        awesomeTimeout(() => {
            this.body.style.opacity = .9

            awesomeTimeout(() => {
                this.body.style.opacity = 0.2

                awesomeTimeout(() => {
                    this.body.style.opacity = .9
                    this.body.style.transform = "rotate(0deg)"
                    this.body.style.transition = "none"
                }, 200)
            }, 200)
        }, 200)
    }

    groundPound(){
        
        if(this.attackCounter < 0 && this.attackCounter > -12 && this.y == this.baseY){

            if(distanceTo(this.enemy, this) > 0 && distanceTo(this.enemy, this) < this.jumpDistance){
                console.log("jump!")
                this.tracking = true
                this.pause = true
                this.attackCounter -= 1
                console.log(this.attackCounter) 

                // if(this.secondPhase){
                //     this.attackCounter -= 1 
                // }

                //check orientation
                if(this.center > this.enemy.center){
                    this.img.style.transform = "scaleX(-1)"
                    this.xVel = -this.speed
                } else{
                    this.img.style.transform = "scaleX(1)"
                    this.xVel = this.speed
                }

                awesomeTimeout(() => {
                    this.pause = false
                    this.yVel = 130
                },this.jumpWindup)
            }
        } else if(this.attackCounter <= -12){
            awesomeTimeout(() => {
                this.attackCounter = 3
            }, 2000)
        }
    }

    //distanceTo(this.enemy, this) > (this.dashDistance - 50) && distanceTo(this.enemy, this) < this.dashDistance

    dash(){
        
 
        if(this.y <= this.baseY && this.yVel == 0 && Math.abs(this.xVel) < this.speed * 5){


            if(this.attackCounter > 0){

                if(distanceTo(this.enemy, this) > 0 && distanceTo(this.enemy, this) < this.dashDistance){
                    console.log("dashing")
                    if(this.secondPhase && this.attackCounter === 3 && getRndInteger(0, 10) < 20){
                        this.dashRecovery = 0

                        this.dashDistance = 1440
                    }

                    if(this.center > this.enemy.center){
                        this.pause = true
                        this.xVel = -this.speed * 8
                        this.attackCounter -= 1
                        console.log(this.attackCounter)
                        this.img.style.transform = "scaleX(-1)"
                        
                        this.telegraphDash("left")
    
                        awesomeTimeout(() => {
                            this.pause = false
                            this.body.style.transition = "none"
                        }, this.dashWindup)
    
                    } else{
                        this.pause = true
                        this.attackCounter -= 1
                        console.log(this.attackCounter)
                        this.img.style.transform = "scaleX(1)"
                        this.xVel = this.speed * 8
    
                        this.telegraphDash("right")
                        
                        awesomeTimeout(() => {
                            this.pause = false
                            this.body.style.transition = "none"
                        }, this.dashWindup)
                        
                    }
                }
            }
        }
    }

    getHit(damage, knockback){
        this.healthbar.loseHealth(damage)
    }

    die(){
        this.dead = true
        this.enemy.pause = true
        awesomeTimeout(() =>{
            this.img.src = "images/Bosses/Reginald-death0.png"
            awesomeTimeout(()=>{
                this.img.src = "images/Bosses/Reginald-death1.png"
                awesomeTimeout(() =>{
                    this.img.src = "images/Bosses/Reginald-death2.png"
                    awesomeTimeout(() =>{
                        this.img.src = "images/Bosses/Reginald-death3.png"
                    },900)
                },900)
            }, 900)
        }, 900)
        this.body.style.transition = "all 4s"
        this.body.style.opacity = 0.7
        this.item = new Item("ReginaldJr", this.enemy, this.x, this.y)
        awesomeTimeout(() => {
            defeatMessage.innerHTML = "Vassal Defeated"
            mainPage2.style.opacity = 1.0
            this.enemy.pause = false
            awesomeTimeout(() => {
                mainPage2.style.opacity = 0
                awesomeTimeout(() =>{
                    defeatMessage.innerHTML = ""
                    this.item.body.style.display = "block"
                    this.enemy.levelCounter++
                    this.enemy.enemyCount = 0
                    this.healthbar.bar.style.display = "none"
                }, 3000)
            }, 4000)
        }, 3600)
    }
}


class Gerald extends Boss{
    constructor(x){
        super("Gerald", x)

        this.img.src = "images/Slimes/smallSlime.png"

        this.speed = 40

        this.hpVal = 5000

        this.cutscene = false

        this.pause = true

        this.dead = false

        this.textbox = undefined
    }

    update(){
        if(this.cutscene){
            this.img.style.transform = "scaleX(1)"
            this.xVel = -this.speed / 2

            if(this.x < boss.x+boss.width + 100 && !this.pause){
                this.pause = true

            }
        } else{
            this.img.style.transform = "scaleX(-1)"
            this.xVel = this.speed 

            if(this.x > boss.x + boss.width + 500 && !this.pause){
                this.body.parentNode.removeChild(this.body)
                this.dead = true
            }

        }

        if(!this.pause){
            this.move()
        }
    } 
    
    move(){
        this.x += this.xVel * 10 / 100
        this.body.style.left = this.x 
    }
}

class Amelia extends Boss{
    constructor(x, player){
        super("Amelia", x, player)

        this.speed = 35
        this.hpVal = 500
        this.baseY = 0
        this.y = this.baseY

        this.healthbar = ""

        this.textbox = undefined

        this.weapon = new AmeliasMace(this)

        this.weapon.body.style.display = "none"

        this.attacking = false

        this.attackCounter = -1

        this.strikingDistance = this.weapon.height

        this.offset ={
            x:0,
            y:0
        }

        this.width = 165
        this.height = 160

        this.snowballDistance = 650
        this.snowballsize = 10
        this.snowballWindup = .8
        this.snowballRecovery = 4000
        this.snowballDamage = 15
        this.snowballKnockback = 5

        this.slowEffect = .35

        this.img.src = "images/Bosses/Amelia.png"

        this.hatImg = document.createElement('img')
        this.hatImg.className = 'Amelia-hat'
        this.hatImg.src = "images/Bosses/Amelia-hat.png"

        this.hand = document.createElement('div')
        this.hand.className = "Amelia-hand"

        this.hand.appendChild(this.weapon.body)
        this.body.appendChild(this.hatImg)
        this.body.appendChild(this.hand)


        this.pause = false
        this.cutscene = true

        this.collisionDetection = true 

        this.secondPhase = false

        this.direction = null

        this.c = null
        this.script = null

    }

    update(){

        if(this.collisionDetection){
            this.collision()
        }

        this.center = this.x +(this.width/2)

        if(!this.pause && !this.cutscene){
            this.move()

            if(this.dead){
                return
            }
        }

        //swing
        if(this.attacking && this.weapon.angle >= (-1*this.weapon.maxAngle)-15){
            this.weapon.angle -= 10
        }

        //patfinding
        if(this.xVel === 0 && !this.pause && !this.cutscene){
            this.pathfinding()
        }

        //default update
        super.update()

        //CUTSCENE STUFF

        if(this.cutscene && this.enemy.cutscene && !this.pause){
            this.move()
            this.xVel = -this.speed

            if(this.x < this.enemy.rightEdge - 400 && !this.pause){
                this.pause = true
                this.c = 0
                if(this.enemy.newGame){
                    this.script = Amelia_Alt_Speech[getRndInteger(0, Amelia_Alt_Speech.length)]
                } else{
                    this.script = Amelia_Speech
                }
            }
        }

        
        if(this.c != null){

            if(this.c < this.script.length){

                if(this.textbox === undefined){
                    this.textbox = new Textbox()
                    this.textbox.box.style.height = 260
                    this.textbox.textContainer.style.bottom = "85%"
                    
                }

                if(this.textbox.text === ""){
                    if(this.c <= this.script.length - 1){
                        this.c++
                    }
                }

                if(this.c <= this.script.length - 1){
                    if((this.textbox.text === "" || this.textbox.text == undefined)){
                        this.textbox.speaker = this.script[this.c].speaker
                        this.textbox.text = this.script[this.c].text
                        this.textbox.write()
                        
                    }
                    if(this.script[this.c].delete && !this.textbox.deleting && !this.textbox.deleted && this.c < this.script.length){
                        this.textbox.deleting = true
                    } else if (this.textbox.deleted){
                        this.textbox = undefined
                    }
                }

            } else {
                if(this.textbox != undefined && this.textbox.text === ""){
                    this.textbox.delete()
                    this.textbox = undefined
                    this.healthbar = new BossHealthBar(this.hpVal, this)
                    this.weapon.body.style.display = "block"
                    this.xVel = 0
                    awesomeTimeout(()=>{
                        this.pause = false
                        this.cutscene = false
                        this.enemy.cutscene = false
                    }, 500)
                }
            }
        }
        

    }

    move(){
        this.x += this.xVel * 10 / 100
        this.body.style.left = this.x 

        if(!this.cutscene){
            if(distanceTo(this.enemy, this) < this.strikingDistance && distanceTo(this.enemy, this) > this.strikingDistance-20){
                this.xVel = 0
                this.pause = true
    
                if(this.attackCounter != 0){
                    awesomeTimeout(() =>{
                        this.weapon.attack()
    
                        awesomeTimeout(() =>{
                            if(this.pause){
                                this.pause = false
                            }
                        }, this.weapon.cooldownTime)
                    }, 300)
                } else {
                    awesomeTimeout(() =>{
                        this.weapon.powerAttack()
    
                        awesomeTimeout(() =>{
                            if(this.pause){
                                this.pause = false
                            }
                        }, this.weapon.cooldownTime*1.6)
                    }, 300)
                }
            }
        }
    }

    collision(){
            if(detectCollision(this.enemy.hitbox, this.weapon.hitbox) && this.attacking){
                this.collisionDetection = false
                this.enemy.getHit(this, this.weapon.damage, this.weapon.knockback)
    
                if(this.enemy.slowed < 3){
                    this.slow()
                }

                awesomeTimeout(() =>{
                    if(!this.collisionDetection){
                        this.collisionDetection = true
                    }
                }, this.weapon.cooldownTime)
            }
    }

    pathfinding(){

        this.img.style.transition = "none"
        if(this.center > this.enemy.center){
            this.img.style.transform = "scaleX(-1)"
        }else{
            this.img.style.transform = "scaleX(1)"
        }
        if(distanceTo(this.enemy, this) < this.snowballDistance - 300){
            //smack em
            this.hammerStrike()
            
        }else{
            //throw a snowball at him
            if(this.attackCounter < 0){
                this.pause = true
                this.throwSnowball()
            } else {
                this.hammerStrike()
            }
        }

    }

    hammerStrike(){
        if(this.attackCounter < 0){
            this.attackCounter = 3
        }
        this.attackCounter -= 1
        this.hand.style.transition = "none"
        if(distanceTo(this.enemy,this) > this.strikingDistance){
            if(this.center > this.enemy.center){
                this.img.style.transform = "scaleX(-1)"
                this.hatImg.style.transform = "scaleX(-1)"
                this.hand.style.left = -25
                this.direction = "left"
                this.xVel = -this.speed
            } else {
                this.img.style.transform = "scaleX(1)"
                this.hatImg.style.transform = "scaleX(1)"
                this.hand.style.left = -100
                this.direction = "right"
                this.xVel = this.speed
            }
        } else if(distanceTo(this.enemy, this) < this.strikingDistance && distanceTo(this.enemy, this) < this.strikingDistance - 20){
            if(this.center > this.enemy.center){
                this.img.style.transform = "scaleX(-1)"
                this.hatImg.style.transform = "scaleX(-1)"
                this.hand.style.left = -25
                this.direction = "left"
                this.xVel = this.speed
            } else {
                this.img.style.transform = "scaleX(1)"
                this.hatImg.style.transform = "scaleX(1)"
                this.hand.style.left = -100
                this.direction = "right"
                this.xVel = -this.speed
            }
        }
    }

    throwSnowball(){  
        this.body.style.transition = "all "+this.snowballWindup+"s"
 
        if(this.center > this.enemy.center){
            this.body.style.transformOrigin = "bottom right"
            this.body.style.transform = "rotate(7deg)"
        }else{
            this.body.style.transformOrigin = "bottom left"
            this.body.style.transform = "rotate(-7deg)"
        }
        
        awesomeTimeout(() =>{
            this.body.style.transform = "rotate(0deg)"
            this.body.style.transition = "none"
            if(this.center > this.enemy.center){
                this.snowball = new BigSnowball(this.slowEffect, this.x, this.y, this)
            } else{
                this.snowball = new BigSnowball(this.slowEffect, this.x+this.width, this.y, this)
            }
            awesomeTimeout(() =>{
                this.snowball.delete()
                this.snowball = undefined
                this.pause = false
            }, this.snowballRecovery)
        }, this.snowballWindup * 1000)
    }

    slow(){
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
            }, 8000)
        }
    }


    getHit(damage){
        if(damage > 50){
            damage /= 2
        }
        this.healthbar.loseHealth(damage)
    }

    die(){

    }
}

