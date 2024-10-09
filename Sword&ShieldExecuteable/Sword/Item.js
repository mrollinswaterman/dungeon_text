
class Item{
    constructor(name,target, x, y){
        this.name = name
        this.target = target

        this.x = x
        this.baseY = y + 50
        this.y = this.baseY

        this.yVel = 0

        this.body = document.createElement("div")
        this.body.className = "item"
        console.log(' hi', x)
        this.body.style.left = x
        this.body.style.bottom = y + 50

        this.img = document.createElement("img")
        this.img.className = "item-img"
        this.img.src = "images/Weapons/"+this.name+".png"

        this.body.appendChild(this.img)

        dirtroad.appendChild(this.body)
        
        this.width = 50
        this.height = 154

        this.center = this.x + (this.width/2)

        this.pickedUp = false
    }

    update(){
        this.center = this.x + (this.width/2)

        //gravity
        if(this.y >= this.baseY && this.yVel != 0){
            this.yVel -= 9.8 * 10 / 100

            
        }

        if(this.yVel === 0){
            this.yVel = 25
        }

        this.y += this.yVel * 10 / 100
        this.body.style.bottom = this.y

        if(this.y < this.baseY){
            this.yVel = 0
        }
        
        if(distanceTo(this.target, this) < 5){
            this.pickUp()
        }
    }

    pickUp(){
        this.pickedUp = true
        this.body.style.display = "none"
        acquireNewItem(this)
        this.target.enemyCount = []
    }
}
