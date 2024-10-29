
var playerLevel = 1

const levelUI = document.createElement('span');
levelUI.className = "level-ui";
levelUI.innerHTML = `Level ${playerLevel}`;
document.getElementsByClassName("level-holder")[0].appendChild(levelUI);



class Healthbar{
    constructor(parent){
        this.parent = parent;
        this.body = document.createElement("span");
        this.body.className = "healthbar";

        this.maxHP = 12;
        this.hp = this.maxHP;
        this.maxSegments = this.maxHP;
        this.tempHP = 0;
        this.segmentWidth = 11;

        /*this.body.style.width = this.maxSegments * this.segmentWidth + (5 * this.maxSegments) - 1;*/

        this.body.style.gridTemplateColumns = `repeat(${this.maxSegments}, 1fr)`;
        for (let i = 0; i < this.maxSegments; i++){
            const current = document.createElement("div");
            current.className = "healthbar-segment";
            current.style.width = this.segmentWidth;
            this.body.appendChild(current);
        }

        document.getElementsByClassName("healthbar-holder")[0].appendChild(this.body)
    }

    resize(new_size){
        this.body.style.gridTemplateColumns = `repeat(${new_size}, 1fr)`;
    }

    loseHP(num){
        if (num == 0){
            return true;
        }

        setTimeout(() => {
            const current = $(".healthbar").children().last();
            current.css("animation",".2s tilt-shaking 10");
                setTimeout(function(){
                    current.css("opacity", 0);
                    $(".healthbar").children().last().remove();
                }, 350);

            if (num >= 0){
                this.loseHP(num-1);
                if (this.tempHP > 0){
                    this.tempHP -= 1;
                } else {
                    this.hp -= 1;
                    this.resize(this.maxHP);
                }
            }
        }, 600);

        setTimeout(this.update.bind(this),  num * num + 100);
    }

    gainHP(num){
        console.log("gaining...");
        if (num + this.hp > this.maxHP){
            num = this.maxHP - this.hp;
        }
        this.resize(this.hp+num)
        const buffer = 200;
        for (let i = this.hp+1; i < this.hp+num+1; i++){
            const current = document.createElement("div");
            current.className = "healthbar-segment";
            current.style.width = this.segmentWidth;
            current.style.opacity = 0;
            this.body.appendChild(current);
            setTimeout(function() {
                current.style.animation = "1s grow-in 1";
                setTimeout(function(){
                    current.style.opacity = 1;
                }, 200);
            }, buffer*(i - this.hp - 1));
        }
        this.hp += num;
        setTimeout(this.update.bind(this), buffer * num + 100);
    }

    gainTempHP(num){
        /* if you already have tempHP*/
        if (!this.tempHP == 0){
            /* if new amount is less than current, return, else continue*/
            if (this.tempHP < num){
                console.log("adding more hp");
                for (let x = this.tempHP; x > 0; x--){
                    this.body.removeChild(this.body.lastChild);
                }
                this.tempHP = num;
            } else {
                return null;
            }
        }
        const buffer = 200;
        this.resize(this.maxSegments+num);
        for (let i = 0; i < num; i++){
            const current = document.createElement('div');
            current.className = "healthbar-segment";
            current.style.backgroundColor = "cyan";
            current.style.width = this.segmentWidth;
            current.style.opacity = 0;
            this.body.appendChild(current);
            setTimeout(function() {
                current.style.animation = ".8s grow-in 1";
                setTimeout(function(){
                    current.style.opacity = 1;
                }, 200);
            }, buffer*i);
        }
        this.tempHP = num;
    }

    update(){



        if (this.hp < this.maxHP / 2){
            this.body.classList.add("low-hp");
        }

        else {
            this.body.classList.remove("low-hp")
        }
    }
}

test = new Healthbar("test");

setTimeout(function() {
    test.gainTempHP(5)
    setTimeout(function(){
        test.loseHP(10);
        setTimeout(() => {
            test.gainHP(40);
        }, 10000);
    }, 2000);
}, 2000);

