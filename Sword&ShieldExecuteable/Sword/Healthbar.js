console.log("Initializing Healthbars...")

setTimeout((console.log("Healthbars Initialized")), 1000)


class HealthBar{
    constructor(size, owner){

        this.owner = owner

        this.size = size

        this.hp = this.size

        //create bar
        this.bar = document.createElement('div')
        this.bar.className = 'healthbar'
        this.bar.id = owner+'healthbar'

        //fill bar
        this.health = document.createElement('div')
        this.health.className = 'health'
        this.health.id = owner+'health'

        this.bar.style.width = size*1.5
        this.health.style.width = size*1.5

        this.bar.appendChild(this.health)
        
        this.owner.body.appendChild(this.bar)

    }

    loseHealth(damage){

        this.hp -= damage

        if(this.hp <= 0){
            this.health.style.width = "0px"
            if(!this.owner.dead){
                //this.owner.dead = true
                this.owner.die()
            }
        } else if (this.hp > 0){
            this.health.style.width = this.hp*1.5
        }

    }

    delete(){
        this.bar.parentNode.removeChild(this.bar)
    }
}

class PlayerHealthBar{
    constructor(size, owner){
        this.owner = owner 

        this.size = size

        this.hp = this.size

        //create bar
        this.bar = document.createElement('div')
        this.bar.className = 'playerhealthbar'
        this.bar.id = owner.player.id+'healthbar'

        this.number = document.createElement("div")
        this.number.className = "hp-number"
        this.number.innerHTML = "HP: "+this.hp+"/"+this.size

        //fill bar
        this.health = document.createElement('div')
        this.health.className = 'health'
        this.health.id = owner.player.id+'health'

        this.health.style.width = this.size*3
        this.bar.style.width = this.size*3

        this.bar.appendChild(this.health)

        this.number.appendChild(this.bar)
        
        document.getElementById("main").appendChild(this.number)

    }

    loseHealth(damage){
        this.hp -= damage

        if(this.hp <= 0){
            this.health.style.width = "0px"
            this.number.innerHTML = "HP: 0/"+this.size
            this.owner.dead = true
            this.owner.die()
        } else if (this.hp > 0){
            this.health.style.width = this.hp*3
            this.number.innerHTML = "HP: "+this.hp+"/"+this.size
            this.number.appendChild(this.bar)
        }
    }
}

class BossHealthBar{
    constructor(size, owner){
        this.owner = owner 

        this.size = size

        this.hp = this.size

        //create bar
        this.bar = document.createElement('div')
        this.bar.className = 'bosshealthbar'
        this.bar.id = owner.name+'healthbar'

        //fill bar
        this.health = document.createElement('div')
        this.health.className = 'health'
        this.health.id = owner.name+'health'

        //boss name
        this.title = document.createElement('div')
        this.title.className = "bosstitle"
        this.title.id = owner.name+"title"
        this.title.innerHTML = owner.title.full

        this.multiplier = (window.innerWidth - 100) / this.size

        this.health.style.width = this.size*this.multiplier
        this.bar.style.width = this.size*this.multiplier

        this.bar.appendChild(this.health)
        this.bar.appendChild(this.title)

        
        document.getElementById("main").appendChild(this.bar)
    }

    loseHealth(damage){
        this.hp -= damage

        if(this.hp <= 0){
            this.health.style.width = "0px"
            this.owner.dead = true
            this.owner.die()
        } else if (this.hp > 0){
            this.health.style.width = this.hp*this.multiplier
        }
    }

}

