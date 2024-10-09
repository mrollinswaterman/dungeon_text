PUNCT_SPEED = 800
DEFAULT_WRITESPEED = 50
DEFAULT_CLEARSPEED = 10

class Textbox{
    constructor(text, speaker){ 
        if(text){
            this.text = text
        } else {
            this.text = undefined
        }

        this.speaker = speaker

        this.writeSpeed = DEFAULT_WRITESPEED

        this.letterCount = 0

        this.deleting = false 
        this.deleted = false

        //make the box
        this.box = document.createElement('div')
        this.box.className = "text-box"

        this.textContainer = document.createElement("div")
        this.textContainer.className = "text"
        this.textContainer.innerHTML = ""

        this.titleBox = document.createElement('div')
        this.titleBox.className = "title-box"

        this.speakerBox = document.createElement("div")
        this.speakerBox.className = "speaker-box"

        this.speakerImg = document.createElement('img')
        this.speakerImg.className = "speaker-img"
        
        this.speakerBox.appendChild(this.speakerImg)
        this.box.appendChild(this.speakerBox)
        this.box.appendChild(this.titleBox)
        this.box.appendChild(this.textContainer)

        document.getElementById("main").appendChild(this.box)
    }

    write(){
        this.speakerImg.src = "images/Speakers/"+this.speaker+".png"
        this.titleBox.innerHTML = TITLES[this.speaker][1]
        if(this.letterCount < this.text.length){
            this.textContainer.innerHTML += this.text.charAt(this.letterCount)
            if(punctuation.indexOf(this.text.charAt(this.letterCount)) > -1){
                this.speed = PUNCT_SPEED
            } else{
                this.speed = DEFAULT_WRITESPEED
            }
            this.letterCount++
            setTimeout(() => this.write(), this.speed)
        } else {
            setTimeout(this.clear(), 3000)
        }
    }

    clear(){
        if(this.letterCount >= 0){
            this.textContainer.innerHTML = this.textContainer.innerHTML.slice(0, -1)
            this.letterCount --
            setTimeout(() => this.clear(), DEFAULT_CLEARSPEED)
        } else {
            this.text = ""
            if(this.deleting === true){
                this.delete()
                //debugger
            }
        }
    }

    delete(){
        if(this.box.parentNode != null){
            this.box.parentNode.removeChild(this.box)
        }
        setTimeout(() => {
            this.deleted = true
        }, 1000)
    }

}



class Storybox{
    constructor(text, level){
        this.text = text
        this.level = level

        this.sentenceList = []

        this.count = -1

        this.deleting = false 
        this.deleted = false

        this.box = document.createElement('div')
        this.box.className = "story-box"

        document.getElementById("main2").appendChild(this.box)

    }

    findSentences(){
        this.text = this.text.split(/\r?\n/)
        this.text.shift()
        this.text.pop()
        
        this.text.forEach(item =>{
            this.container = document.createElement("p")
            this.container.className = "sentence-box"
            this.container.innerHTML = item
            this.box.appendChild(this.container)
        })
    }

    write(){   
        const list = Array.from(document.getElementsByClassName("sentence-box"))
        list.forEach(sentence =>{
            this.count++
            setTimeout(() =>{
                sentence.style.opacity = 1.0


                if(list.indexOf(sentence) === list.length-1){
                    //console.log("found ya!")
                    setTimeout(()=>{
                        this.clear()
                    }, 3000)
                }

            }, 3500 * this.count)


        })
    }

    clear(){
        this.box.style.transition = "all 4s"

        this.box.style.opacity = 0

        setTimeout(() =>{
            this.delete()
            chooseYourWeapon(this.level)
        }, 4000)
    }

    delete(){
        if(this.box.parentNode != null){
            this.box.parentNode.removeChild(this.box)
        }
        setTimeout(() => {
            this.deleted = true
        }, 1000)
    }
}