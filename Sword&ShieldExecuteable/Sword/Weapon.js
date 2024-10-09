



class Weapon{
    constructor(owner){
        this.owner = owner

        this.body = document.createElement('div')
 
        this.weaponimg = document.createElement('img')

        this.hitboxDiv = document.createElement('div')

        this.body.appendChild(this.weaponimg)
        this.body.appendChild(this.hitboxDiv)
    }

    update(){

        this.initialHitbox = {
            width: this.boxWidth,
            height: this.boxHeight,
            c1:{
                x: this.xInitial,
                y: this.yInitial,
            },
            c2 :{
                x: this.xInitial,
                y: this.yInitial + this.boxHeight
            },
            c3:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial + this.boxHeight
            },
            c4:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial
            },
        }


    }
}

class Sword extends Weapon{
    constructor(owner) {
        super(owner)

        this.body.className = "sword"
        this.weaponimg.className = "sword-img"

        this.origin = {
            x: this.owner.x +32,
            y: this.y + 25
        }

        this.xInitial = this.owner.x + 13
        this.yInitial = this.owner.y + 95

        this.boxHeight = 190
        this.boxWidth = 38

        this.height = 70

        this.initialHitbox = {
            width: this.boxWidth,
            height: this.boxHeight,

            c1:{
                x: this.xInitial,
                y: this.yInitial,
            },
            c2 :{
                x: this.xInitial,
                y: this.yInitial + this.boxHeight
            },
            c3:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial + this.boxHeight
            },
            c4:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial
            },
            rotated: false
        }
        
        this.angle = 0

        this.direction = "right"

        this.weaponimg.src = "images/Weapons/TrustySword.png"
        this.windupTime = .2
        this.swingTime = 10
        this.recoveryTime = 0.4
        this.damage = 30
        this.knockback = 2.0
        this.cooldownTime = this.windupTime*1.4*1000 + this.swingTime*10
        
        this.maxAngle = 90

        this.hitboxDiv.className = "sword-hitbox"



    }

    update(){

        //update origin
        if(this.direction === "left"){
            this.origin = {
                x: this.owner.x + 44,
                y: this.owner.y + 25
            }
        }else {
            this.origin = {
                x: this.owner.x + 32,
                y: this.owner.y + 25
            }
        }

        //update x & y
        this.xInitial = this.owner.x + 13
        this.yInitial = this.owner.y + 95

        super.update()

        this.hitbox = this.getRotatedRect2()

        if(this.owner.direction != null){
            this.direction = this.owner.direction
        }

        //unswing sword
        if(this.angle >= this.maxAngle){
            this.angle = this.maxAngle

            awesomeTimeout(() => {
                this.owner.handw.style.transition = "all "+this.recoveryTime+"s"
                this.owner.handw.style.bottom = 55

                this.owner.attacking = false
                
                this.angle = 0
            }, this.recoveryTime/2 * 1000)
        }

        if(this.direction === "left"){
            this.body.parentNode.style.transform = "scaleX(-1) rotate("+this.angle+"deg)"
        } else if (this.direction === "right"){
            this.body.parentNode.style.transform = "scaleX(1) rotate("+this.angle+"deg)"
        }



    }

    attack(){
        this.owner.herobody.style.transition = "all " + this.windupTime/2+"s"
        this.owner.handw.style.transition = "all "+this.windupTime+"s"

        if(this.owner.xVel > 0){
            this.owner.herobody.style.transformOrigin = "bottom left"
            this.owner.herobody.style.transform = "rotate(-5deg)"
        } else{
            this.owner.herobody.style.transformOrigin = "bottom right"
            this.owner.herobody.style.transform = "rotate(5deg)"

        }

        this.owner.handw.style.bottom = 75
        this.owner.handw.style.transformOrigin = "bottom left"
        this.angle = -45


        awesomeTimeout(() => {

            this.owner.herobody.style.transition = "all "+this.recoveryTime/2+"s"
            this.owner.herobody.style.transform = "rotate(0deg)"

            this.owner.handw.style.transition = "none"
            this.owner.handw.style.transition = "bottom .4s"
            this.owner.handw.style.bottom = 35


            this.owner.attacking = true

        }, this.windupTime*1.4*1000)
    }

    adjust(){
        this.owner.hand.style.bottom = 0
        this.owner.hand.style.left = -20.6//-23.5
    }

    getRotatedRect(){
        if(this.direction === "left"){
            return {    
                c1: {
                    x: this.origin.x + cos(90 + 13 + this.angle) * this.height * 1.1,
                    y: this.origin.y + sin(90 + 13 + this.angle) * this.height * 1.1,
                },
                c2: {
                    x: this.origin.x + cos(90 + 3 + this.angle) * this.height * 3.7,
                    y: this.origin.y + sin(90 + 3 + this.angle) * this.height * 3.7,
                },
                c3: {
                    x: this.origin.x  + cos(90 - 3 + this.angle) * this.height * 3.7,
                    y: this.origin.y + sin(90 - 3 + this.angle) * this.height * 3.7,
                },
                c4: {
                    x: this.origin.x + cos(90 - 13 + this.angle) * this.height * 1.1,
                    y: this.origin.y + sin(90 - 13 + this.angle) * this.height * 1.1,
                },
            }
        } else {

            return {    
                c1: {
                    x: this.origin.x + cos(90 + 13 + this.angle * -1) * this.height * 1.1,
                    y: this.origin.y + sin(90 + 13 + this.angle * -1) * this.height * 1.1,
                },
                c2: {
                    x: this.origin.x + cos(90 + 3 + this.angle * -1) * this.height * 3.7,
                    y: this.origin.y + sin(90 + 3 + this.angle * -1) * this.height * 3.7,
                },
                c3: {
                    x: this.origin.x  + cos(90 - 3 + this.angle * -1) * this.height * 3.7,
                    y: this.origin.y + sin(90 - 3 + this.angle * -1) * this.height * 3.7,
                },
                c4: {
                    x: this.origin.x + cos(90 - 13 + this.angle * -1) * this.height * 1.1,
                    y: this.origin.y + sin(90 - 13 + this.angle * -1) * this.height * 1.1,
                },
            }
        }
    }

    getRotatedRect2(){
        if(this.direction === "left"){
            return {    
                c1: {
                    x: this.origin.x + cos(90 + 13 + this.angle) * this.height * 1.1,
                    y: this.origin.y + sin(90 + 13 + this.angle) * this.height * 1.1,
                },
                c2: {
                    x: this.origin.x + cos(90 + 3 + this.angle) * this.height * 3.7,
                    y: this.origin.y + sin(90 + 3 + this.angle) * this.height * 3.7,
                },
                c3: {
                    x: this.origin.x  + cos(90 - 3 + this.angle) * this.height * 3.7,
                    y: this.origin.y + sin(90 - 3 + this.angle) * this.height * 3.7,
                },
                c4: {
                    x: this.origin.x + cos(90 - 13 + this.angle) * this.height * 1.1,
                    y: this.origin.y + sin(90 - 13 + this.angle) * this.height * 1.1,
                },
            }
        } else {

            return {    
                c1: {
                    x: this.origin.x + cos(90 + 13 + this.angle * -1) * this.height * 1.1,
                    y: this.origin.y + sin(90 + 13 + this.angle * -1) * this.height * 1.1,
                },
                c2: {
                    x: this.origin.x + cos(90 + 3 + this.angle * -1) * this.height * 3.4,
                    y: this.origin.y + sin(90 + 3 + this.angle * -1) * this.height * 3.4,
                },
                c3: {
                    x: this.origin.x  + cos(90 - 3 + this.angle * -1) * this.height * 3.4,
                    y: this.origin.y + sin(90 - 3 + this.angle * -1) * this.height * 3.4,
                },
                c4: {
                    x: this.origin.x + cos(90 - 13 + this.angle * -1) * this.height * 1.1,
                    y: this.origin.y + sin(90 - 13 + this.angle * -1) * this.height * 1.1,
                },
            }
        }
    }
}



class Greatsword extends Weapon{
    constructor(owner){
        super(owner)

        this.origin = {
            x: this.owner.x + 35,
            y: this.owner.y + 27
        }

        this.xInitial = this.owner.x + 2
        this.yInitial = this.owner.y + 145

        this.boxWidth = 68
        this.boxHeight = 340

        this.height = 117
        
        this.initialHitbox = {
            width: this.boxWidth,
            height: this.boxHeight,

            c1:{
                x: this.xInitial,
                y: this.yInitial,
            },
            c2 :{
                x: this.xInitial,
                y: this.yInitial + this.boxHeight
            },
            c3:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial + this.boxHeight
            },
            c4:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial
            },
            rotated: false
        }

        this.body.className = "greatsword"
        this.weaponimg.className = "greatsword-img"

        
        this.angle = 0

        this.direction = "right"

        this.weaponimg.src = "images/Weapons/ReginaldJr.png"//"images/Weapons/Reginald-Jr.png"
        this.swingTime = 20
        this.windupTime = 1.0
        this.recoveryTime = 1.5
        this.damage = 70
        this.knockback = 4.0
        this.cooldownTime = (this.windupTime*1000+this.swingTime*10)

        this.maxAngle = 90

        this.shake = false
        this.hitboxDiv.className = "greatsword-hitbox"
        

    }

    update(){

        //update origin
        if(this.direction === "left"){
            this.origin = {
                x: this.owner.x + 44,
                y: this.owner.y + 27
            }
        }else{
            this.origin = {
                x: this.owner.x + 35,
                y: this.owner.y + 27
            }
        }

        //update x + y
        this.xInitial = this.owner.x + 2
        this.yInitial = this.owner.y + 145

        super.update()

        this.hitbox = this.getRotatedRect()

       // console.log(this.hitbox)

        //unswing sword
        if(this.angle >= this.maxAngle){
            this.angle = this.maxAngle

            awesomeTimeout(() => {
                this.owner.handw.style.transition = "all "+this.recoveryTime+"s"

                this.owner.attacking = false
                this.owner.handw.style.bottom = 55

                
                this.angle = 0
            }, this.recoveryTime/2 * 1000)
        }

        //set direction
        if(this.owner.direction != null){
            this.direction = this.owner.direction
        }

        //flip visuals
        if(this.direction === "left"){
            this.body.parentNode.style.transform = "scaleX(-1) rotate("+this.angle+"deg)"
        } else if (this.direction === "right"){
            this.body.parentNode.style.transform = "scaleX(1) rotate("+this.angle+"deg)"
        }

    }

    attack(){
        this.owner.herobody.style.transition = "all " + this.windupTime/2+"s"
        this.owner.handw.style.transition = "all "+ this.windupTime+"s"

        if(this.direction === "right"){
            this.owner.herobody.style.transformOrigin = "bottom left"
            this.owner.herobody.style.transform = "rotate(-20deg)"
        } else{
            this.owner.herobody.style.transformOrigin = "bottom right"
            this.owner.herobody.style.transform = "rotate(20deg)"

        }

        this.owner.handw.style.transformOrigin = "bottom left"
        
        this.owner.handw.style.bottom = 120
        this.angle = -45


        awesomeTimeout(() => {
            
            this.owner.herobody.style.transition = "all "+this.recoveryTime/2+"s"
            this.owner.herobody.style.transform = "rotate(0deg)"
            
            
            this.owner.handw.style.transition = "none"
            this.owner.handw.style.transition = "bottom .2s"
            this.owner.handw.style.bottom = 30

            this.owner.attacking = true

            awesomeTimeout(() =>{
                if(this.shake){
                    shake2()
                }
            }, this.swingTime*10)

        }, this.windupTime*1000)
    }

    getRotatedRect(){
        if(this.direction === "left"){
            return {    
                c1: {
                    x: this.origin.x + cos(90 + 13 + this.angle) * this.height * 1.3,
                    y: this.origin.y + sin(90 + 13 + this.angle) * this.height * 1.3,
                },
                c2: {
                    x: this.origin.x + cos(90 + 3+ this.angle) * this.height * 3.8,
                    y: this.origin.y + sin(90 + 3+ this.angle) * this.height * 3.8,
                },
                c3: {
                    x: this.origin.x  + cos(90 - 3+ this.angle) * this.height * 3.8,
                    y: this.origin.y + sin(90 - 3+ this.angle) * this.height * 3.8,
                },
                c4: {
                    x: this.origin.x + cos(90 - 13 + this.angle) * this.height * 1.3,
                    y: this.origin.y + sin(90 - 13 + this.angle) * this.height * 1.3,
                },
            }
        } else {

            return {    
                c1: {
                    x: this.origin.x + cos(90 + 13 + this.angle * -1) * this.height * 1.3,
                    y: this.origin.y + sin(90 + 13 + this.angle * -1) * this.height * 1.3,
                },
                c2: {
                    x: this.origin.x + cos(90 + 3+ this.angle * -1) * this.height * 3.8,
                    y: this.origin.y + sin(90 + 3+ this.angle * -1) * this.height * 3.8,
                },
                c3: {
                    x: this.origin.x  + cos(90 - 3+ this.angle * -1) * this.height * 3.8,
                    y: this.origin.y + sin(90 - 3+ this.angle * -1) * this.height * 3.8,
                },
                c4: {
                    x: this.origin.x + cos(90 - 13 + this.angle * -1) * this.height * 1.3,
                    y: this.origin.y + sin(90 - 13 + this.angle * -1) * this.height * 1.3,
                },
            }
        }
    }

    adjust(){
        this.owner.hand.style.left = -19
        this.owner.hand.style.bottom = -7
    }
 
}

class AmeliasMace extends Weapon{
    constructor(owner){
        super(owner)

        this.body.className = "Amelia-mace"
        this.weaponimg.className = "Amelia-mace-img"

        this.xInitial = 5 + this.owner.x
        this.yInitial = 262 + this.owner.y

        this.origin = {
            x: 127 + this.owner.x,
            y: 43 + this.owner.y
        }

        this.boxHeight = 110
        this.boxWidth = 230

        this.height = 220

        this.lowerAngle = 20//60//20
        this.upperAngle = 10//10//15

        this.lowerHeightMultiplier = .5//.2//1.2
        this.upperHeightMultiplier = 1.5//1.6//1.5

        this.initialHitbox = {
            width: this.boxWidth,
            height: this.boxHeight,
            c1:{
                x: this.xInitial,
                y: this.yInitial,
            },
            c2 :{
                x: this.xInitial,
                y: this.yInitial + this.boxHeight
            },
            c3:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial + this.boxHeight
            },
            c4:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial
            },
            rotated: false
        }
        
        this.angle = 0

        this.direction = "left"

        this.weaponimg.src = "images/Weapons/Amelia'sMace.png"
        this.windupTime = .4
        this.swingTime = .9
        this.recoveryTime = 1.0
        this.damage = 20
        this.knockback = 5.0
        this.cooldownTime = (this.windupTime+this.recoveryTime + this.swingTime)*1500
        
        this.maxAngle = 80

        this.shake = false

    }


    update(){


        if(this.direction === "left"){
            this.origin = {
                x: 127 + this.owner.x,
                y: 43 + this.owner.y
            }
        }else{
            this.origin = {
                x: 127 - 70 + this.owner.x,
                y: 43 + this.owner.y
            }
        }

        this.xInitial = 5 + this.owner.x
        this.yInitial = 262 + this.owner.y


        this.initialHitbox = {
            width: this.boxWidth,
            height: this.boxHeight,
            c1:{
                x: this.xInitial,
                y: this.yInitial,
            },
            c2 :{
                x: this.xInitial,
                y: this.yInitial + this.boxHeight
            },
            c3:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial + this.boxHeight
            },
            c4:{
                x: this.xInitial + this.boxWidth,
                y: this.yInitial
            },
            rotated: false
        }

        if(this.angle < this.maxAngle*-1){
            this.angle = this.maxAngle*-1
        }

        if(this.owner.direction != null){
            this.direction = this.owner.direction
        }

        if(this.direction === "left"){
            this.body.parentNode.style.transform = "scaleX(1) rotate("+this.angle+"deg)"

        } else if (this.direction === "right"){
            this.body.parentNode.style.transform = "scaleX(-1) rotate("+this.angle+"deg)"
        }

        this.hitbox = this.getRotatedRect()

    }
    
    attack(special = false){

       // console.log(this.windupTime)
        
        this.owner.body.style.transition = "all " + this.windupTime/2+"s"

        if(this.direction === "right"){
            this.owner.body.style.transformOrigin = "bottom left"
            this.owner.body.style.transform = "rotate(-10deg)"
        } else{
            this.owner.body.style.transformOrigin = "bottom right"
            this.owner.body.style.transform = "rotate(10deg)"

        }

        this.owner.hand.style.transition = "all " + this.windupTime + "s"
        this.owner.hand.style.transformOrigin = "bottom right"
        this.angle = 45

        if(special === true){
            this.glow()
        }


        awesomeTimeout(() => {

            this.owner.hand.style.transition = "none"
            this.owner.body.style.transition = "all "+this.swingTime/5+"s ease-in"
            this.owner.body.style.transform = "rotate(0deg)"

            this.owner.attacking = true


            if(special){
                awesomeTimeout(() =>{
                    shake2()

                }, this.swingTime * 800)
            }
           

            awesomeTimeout(() => {
                if(this.angle <= this.maxAngle*-1){
                    this.owner.hand.style.transition = "all "+this.recoveryTime+"s"
                    this.owner.body.style.transition = "none"
                    this.owner.attacking = false


    
                    this.angle = 0
                } else {
                    awesomeTimeout(() =>{
                        if(this.angle <= this.maxAngle*-1){
                            this.owner.hand.style.transition = "all "+this.recoveryTime+"s"
                            this.owner.body.style.transition = "none"
                            this.owner.attacking = false


                           this.angle = 0
                        }
                    }, 1000)
                }

            }, this.recoveryTime*1500)

        }, this.windupTime*1000)
    }

    powerAttack(){
        this.damage *= 2
        this.knockback *= 1.5
        this.windupTime *= 2.5
        this.swingTime /= 2
        this.recoveryTime *= 2

        this.lowerAngle *= 3
        
        this.lowerHeightMultiplier /= 2
        this.upperHeightMultiplier += .2

        //this.glow()
        this.attack(true)

        awesomeTimeout(() =>{
            this.damage /= 2
            this.knockback /= 1.5
            this.windupTime /= 2.5
            this.swingTime *= 2
            this.recoveryTime /= 2

            this.lowerAngle /= 3
        
            this.lowerHeightMultiplier *= 2
            this.upperHeightMultiplier -= .2

        },this.cooldownTime)

    }

    glow(){

        this.weaponimg.src = "images/Weapons/Amelia'sMacePowerAttack.png"
        this.body.style.filter = "drop-shadow(1px 1px 1px yellow)"

        awesomeTimeout(() =>{
            this.body.style.filter = "drop-shadow(1px 1px 5px yellow)"

            awesomeTimeout(() =>{
                this.body.style.filter = "drop-shadow(1px 1px 10px yellow)"
            }, 200)
        }, 200)

        awesomeTimeout(() =>{
            this.weaponimg.src = "images/Weapons/Amelia'sMace.png"
            this.body.style.filter = "none"

        }, this.cooldownTime)
        
    }

    getRotatedRect(){
        if(this.direction === "left"){
            return {    
                c1: {
                    x: this.origin.x + cos(90 + this.lowerAngle + this.angle * -1) * this.height * this.lowerHeightMultiplier,
                    y: this.origin.y + sin(90 + this.lowerAngle + this.angle * -1) * this.height * this.lowerHeightMultiplier,
                },
                c2: {
                    x: this.origin.x + cos(90 + this.upperAngle + this.angle * -1) * this.height * this.upperHeightMultiplier,
                    y: this.origin.y + sin(90 + this.upperAngle + this.angle * -1) * this.height * this.upperHeightMultiplier,
                },
                c3: {
                    x: this.origin.x  + cos(90 -this.upperAngle + this.angle * -1) * this.height * this.upperHeightMultiplier,
                    y: this.origin.y + sin(90 -this.upperAngle + this.angle * -1) * this.height * this.upperHeightMultiplier,
                },
                c4: {
                    x: this.origin.x + cos(90 - this.lowerAngle + this.angle * -1) * this.height * this.lowerHeightMultiplier,
                    y: this.origin.y + sin(90 - this.lowerAngle + this.angle * -1) * this.height * this.lowerHeightMultiplier,
                },
            }
        } else {
            return {    
                c1: {
                    x: this.origin.x + cos(90 + this.lowerAngle + this.angle) * this.height * this.lowerHeightMultiplier,
                    y: this.origin.y + sin(90 + this.lowerAngle + this.angle) * this.height * this.lowerHeightMultiplier,
                },
                c2: {
                    x: this.origin.x + cos(90 + this.upperAngle + this.angle) * this.height * this.upperHeightMultiplier,
                    y: this.origin.y + sin(90 + this.upperAngle + this.angle) * this.height * this.upperHeightMultiplier,
                },
                c3: {
                    x: this.origin.x  + cos(90 -this.upperAngle + this.angle) * this.height * this.upperHeightMultiplier,
                    y: this.origin.y + sin(90 -this.upperAngle + this.angle) * this.height * this.upperHeightMultiplier,
                },
                c4: {
                    x: this.origin.x + cos(90 - this.lowerAngle + this.angle) * this.height * this.lowerHeightMultiplier,
                    y: this.origin.y + sin(90 - this.lowerAngle + this.angle) * this.height * this.lowerHeightMultiplier,
                },
            }
        }
    }
}
