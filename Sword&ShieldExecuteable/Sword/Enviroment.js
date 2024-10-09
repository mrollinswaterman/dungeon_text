

class Enviroment_Object{
    constructor(x, y, type, src, parent){
        this.x = x
        this.y = y
        this.src = src
        this.parent = parent
        this.type = type

        //make container
        

        //make img
        this.img = document.createElement('img')
        this.img.src = src

        if(type ==="cloud"){
            this.cloud = document.createElement('div')
            this.cloud.style.top = this.y
            this.cloud.style.left = this.x
            this.cloud.appendChild(this.img)
            this.parent.appendChild(this.cloud)
        } else if (type ==="sun"){
            this.sun = document.createElement('div')
            this.sun.style.top = this.y
            this.sun.style.left = this.x
            this.sun.appendChild(this.img)
            this.parent.appendChild(this.sun)
        } else if(type==="tree"){
            this.tree = document.createElement('div')
            this.tree.style.top = this.y
            this.tree.style.left = this.x
            this.tree.appendChild(this.img)
            this.parent.appendChild(this.tree)
        }


    }

    update(){
        if(this.type === "cloud"){
            this.cloud.style.left = this.x
        } else if (this.type === "sun"){
            this.sun.style.left = this.x
        } else if(this.type=== "tree"){
            this.tree.style.left = this.x
        }
    }
}

class Cloud extends Enviroment_Object{
    constructor(x, y, type = "cloud", src, parent, driftSpeed){
        super(x, y, type, src, parent)
        this.driftSpeed = driftSpeed

        //make container
        // this.cloud = document.createElement('div')
        this.cloud.className = "cloud-holder"
        // this.cloud.style.top = this.y
        // this.cloud.style.left = this.x
        this.cloud.style.position = "absolute"
        this.cloud.style.height = "fit-content"
        this.cloud.style.width = "fit-content"

        //make img
       // this.img = document.createElement('img')
        // this.img.src = "cloud.png"
        this.img.className = 'pixel-cloud'




        //this.cloud.appendChild(this.img)
        //document.getElementsByClassName('sky')[0].appendChild(this.cloud)
    }

    update(){
        this.x -= this.driftSpeed
        this.cloud.style.left = this.x
    }
}

class Sun extends Enviroment_Object{
    constructor(x, y, type = "sun", src, parent){
        super(x, y, type, src, parent)

        //make holder
        // this.sun = document.createElement('div')
        this.sun.className = "sun"

        //make img
        //this.img = document.createElement("img")
        this.img.className = "sun-img"
        // this.img.src = "sun.png"

        // this.sun.appendChild(this.img)

        // document.getElementsByClassName('sky')[0].appendChild(this.sun)

    }

    update(){
        this.sun.style.top = this.y
    }
}

class Tree extends Enviroment_Object{
    constructor(x, y, type = "tree", src, parent){
        super(x, y, type, src, parent)

        this.tree.className = "tree-holder"

        this.img.className = "pixel-tree"

        this.tree.style.position = 'absolute'
        this.tree.style.height = "fit-content"
        this.tree.style.width = "fit-content"
    }
}