class Environment_Object{
    constructor(type, x, y, src, parent, rendered=true){
        this.x = x
        this.y = y
        this.src = src
        this.parent = parent
        this.vel = .25
        this.rendered = rendered
        this.xInitial = x
        this.yInitial = y

        //make img
        this.img = document.createElement('img')
        this.img.src = src
        this.img.className = `${type}-img`

        //make container
        this.container = document.createElement('div')
        this.container.className = `${type}-holder`
        this.container.style.transform = "translate("+this.x+"px, "+this.y+"px)"
        this.container.appendChild(this.img)

        if(this.rendered){
            this.parent.appendChild(this.container)
        }
    }

    update(){
        if(this.rendered && !this.parent.contains(this.container)){
            this.parent.appendChild(this.container)
        } else if(this.rendered === false && this.parent.contains(this.container)){
            this.parent.removeChild(this.container)
        }
        // this.container.style.left =  this.x
        // this.container.style.top = this.y
    }
}

class Cloud extends Environment_Object{
    constructor(x, y, src, parent, driftSpeed){
        super('cloud', x, y, src, parent)

        this.driftSpeed = driftSpeed
    }

    update(){
        this.x -= this.driftSpeed
        this.container.style.left = this.x
    }
}

class Sun extends Environment_Object{
    constructor(x, y, src, parent){
        super('sun', x, y, src, parent)

    }

    update(){
        this.container.style.transform = "translate("+this.x+"px, "+this.y+"px)"   
    }
}

class Moon extends Environment_Object{
    constructor(x, y, src, parent){
        super('moon', x, y, src, parent)

    }

    update(){
        this.container.style.transform = "translate("+this.x+"px, "+this.y+"px)"   
    }
}

class Tree extends Environment_Object{
    constructor(x, y, src, parent, rendered){
        super('tree', x, y, src, parent, rendered)
    }
}