class Rectangle{
    constructor(x, y, width, height, angle){
        this.x = x
        this.y = y
        this.width = width
        this.height = height
        this.angle = angle

        

        this.c1 ={
            x: this.x,
            y: this.y
        }

        this.c2 = {
            x: this.x,
            y: this.y + this.height
        }

        this.c3 = {
            x: this.x + this.width,
            y: this.y + this.height
        }

        this.c4 = {
            x: this.x + this.width,
            y: this.y
        }


        this.body = document.createElement('div')
        this.body.className = "rect"

        this.body.style.left = this.x
        this.body.style.bottom = this.y
        this.body.style.width = this.width
        this.body.style.height = this.height

        if(this.angle > 0){
            this.body.style.transition = "all 2s"
            this.body.style.transformOrigin = "bottom right"
        } else{
            this.body.style.transformOrigin = "bottom left"

        }

        this.body.style.transform = "rotate("+this.angle+")deg"

        document.body.appendChild(this.body)
    }

    update(){
        this.body.style.transform = "rotate("+this.angle+"deg)"

        this.body.style.left = this.x
        this.body.style.bottom = this.y
        this.body.style.width = this.width
        this.body.style.height = this.height

        if(this.angle != 0){
            var newHB = getRotatedRect({x: this.x, y:this.y},this.height, this, this.angle)
            this.c1 = newHB.c1
            this.c3 = newHB.c3
            this.c3 = newHB.c3
            this.c4 = newHB.c4
        }

    }
}


const rect1 = new Rectangle (100, 100, 90, 60, 0)

const rect2 = new Rectangle(140, 100, 90, 60 ,45)


setInterval(() =>{
    rect1.update()
    rect2.update()
})





function getRotatedRect(origin, height, hitbox, angle){
    // angle *= -1
    console.log(angle)
    if(angle === 0){
        //console.log("fuck off")
        return hitbox


    } else if (angle > 0){
        const newX0 = origin.x + (height * cos(90-angle)) 
        const newY0 = origin.y + (height * sin(90-angle))

        const c1 = {
            x: newX0 - ((origin.x - hitbox.c1.x) * cos(45)),
            y: newY0 + ((origin.x - hitbox.c1.x) * sin(45))
        }

        const c2 = {
            x: c1.x + ((hitbox.c2.y - hitbox.c1.y) * cos(45)),
            y: c1.y + ((hitbox.c2.y - hitbox.c1.y) * sin(45))
        }

        const c3 = {
            x: c2.x + ((hitbox.c3.x - hitbox.c2.x) * cos(45)),
            y: c2.y -  ((hitbox.c3.x - hitbox.c2.x) * sin(45))
        }

        const c4 = {
            x: c3.x - ((hitbox.c3.y - hitbox.c4.y) * cos(45)),
            y: c3.y - ((hitbox.c3.y - hitbox.c4.y) * sin(45))
        }

        const newHitbox = {
            width: hitbox.width,
            height: hitbox.height,
            c1: c1,
            c2: c2,
            c3: c3,
            c4: c4,
            rotated: true
        }

        return newHitbox
    } else {
        const newX0 = origin.x - (height * cos(90+angle)) 
        const newY0 = origin.y + (height * sin(90+angle))

        const c1 = {
            x: newX0 - ((origin.x - hitbox.c1.x) * cos(45)),
            y: newY0 - ((origin.x - hitbox.c1.x) * sin(45))
        }

        const c2 = {
            x: c1.x - ((hitbox.c2.y - hitbox.c1.y) * cos(45)),
            y: c1.y + ((hitbox.c2.y - hitbox.c1.y) * sin(45))
        }

        const c3 = {
            x: c2.x + ((hitbox.c3.x - hitbox.c2.x) * cos(45)),
            y: c2.y +  ((hitbox.c3.x - hitbox.c2.x) * sin(45))
        }

        const c4 = {
            x: c3.x + ((hitbox.c3.y - hitbox.c4.y) * cos(45)),
            y: c3.y - ((hitbox.c3.y - hitbox.c4.y) * sin(45))
        }

        const newHitbox = {
            width: hitbox.width,
            height: hitbox.height,
            c1: c1,
            c2: c2,
            c3: c3,
            c4: c4,
            rotated: true
        }

        return newHitbox
    }

}
