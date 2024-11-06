
var playerLevel = 1

const levelUI = document.createElement('span');
levelUI.className = "level-ui";
levelUI.innerHTML = `LvL. ${playerLevel}`;
document.getElementsByClassName("level-holder")[0].appendChild(levelUI);



class Healthbar{
    constructor(parent)
    {
        this.parent = parent;
        this.body = document.createElement("span");
        this.body.className = "healthbar";

        this.onHitAnimation = "on-hit-shake .2s 5";
        this.loseHPAnimation = ".6s shrink-out 1 forwards";
        this.gainHPAnimation = "1s grow-in 1";

        this.maxHP = 12;
        this.hp = this.maxHP;
        this.maxSegments = this.maxHP;
        this.tempHP = 0;
        this.segmentWidth = 14;

        this.text = document.createElement('span');
        this.text.className = "healthbar-text";
        this.text.innerText = `HP: ${this.hp}/${this.maxHP}`;

        this.resize(this.maxSegments);

        for (let i = 0; i < this.maxSegments; i++)
        {
            const current = document.createElement("div");
            current.className = "healthbar-segment";
            current.style.width = this.segmentWidth;
            this.body.appendChild(current);
        }
        document.getElementsByClassName("healthbar-holder")[0].appendChild(this.text);
        document.getElementsByClassName("healthbar-holder")[0].appendChild(this.body);
    }

    animate(func, args1, args2)
    {

    }

    resize(segments)
    {
        if (segments * this.segmentWidth > 330)
        {
            this.body.style.width = (segments/2) * this.segmentWidth + (segments * 4);
        }
        else 
        {
            this.body.style.width = segments * this.segmentWidth + (segments * 4);
        }
    }

    loseHP(num)
    {
        if (num == 0)
        {
            return true;
        }

        document.getElementsByClassName("healthbar-holder")[0].style.opacity = 0;
        document.getElementsByClassName("healthbar-holder")[0].style.animation = this.onHitAnimation;

        setTimeout (() => 
        {
            document.getElementsByClassName("healthbar-holder")[0].style.opacity = 1;
        }, 150);
        setTimeout(() => 
        {
            document.getElementsByClassName("healthbar-holder")[0].style.animation = "";
        }, 350)

        if (num < 1 && num > 0)  // if num is a percentage (i.e. 0.9, 0.65, etc.) 
        {
            console.log("percentage");
            var perc = num;
            //num = Math.floor(perc*(this.hp+this.tempHP)); --> %total Health (including tempHP)
            num = Math.floor(perc*this.hp) // %current Health
        }
        console.log(num);
        const num_children = $(".healthbar").children().length-1;
        console.log(num_children);
        setTimeout(() => 
        {
            for (let i = num_children; i > num_children-num; i--)
            {   
                const current = $(".healthbar").children()[i];
                current.style.animation = this.loseHPAnimation;  // ${0.25+offset}
                if (this.tempHP > 0)
                {
                    this.tempHP -= 1;
                }
                else
                {
                    this.hp -= 1;
                }
                setTimeout (() => 
                {
                    this.body.removeChild(current);
                }, 600);
            }
        }, 500);

        setTimeout(this.update.bind(this),  num * num + 500);
    }

    gainHP(num)
    {
        if (num + this.hp > this.maxHP){
            num = this.maxHP - this.hp;
        }
        const buffer = 200;
        for (let i = this.hp+1; i < this.hp+num+1; i++)
        {
            const current = document.createElement("div");
            current.className = "healthbar-segment";
            current.style.width = this.segmentWidth;
            current.style.opacity = 0;
            this.body.appendChild(current);
            setTimeout(() => 
            {
                current.style.animation = "1s grow-in 1";
                setTimeout(() => 
                {
                    current.style.opacity = 1;
                }, 200);
            }, buffer*(i - this.hp - 1));
        }
        this.hp += num;
        setTimeout(this.update.bind(this), buffer * num + 100);
    }

    gainTempHP(num)
    {
        if (!this.tempHP == 0) // if you already have tempHP
        {  
            if (this.tempHP < num)  // if new amount is more than current
            {  
                for (let x = this.tempHP; x > 0; x--)
                {
                    this.body.removeChild(this.body.lastChild);
                }
                this.tempHP = num;
            }
            else  // if new amount less than (or equal to!) current
            {
                return null;
            }
        }
        const buffer = 200;

        for (let i = 0; i < num; i++)
        {
            const current = document.createElement('div');
            current.className = "healthbar-segment";
            current.style.backgroundColor = "cyan";
            current.style.width = this.segmentWidth;
            current.style.opacity = 0;
            this.body.appendChild(current);
            setTimeout(() => 
            {
                current.style.animation = this.gainHPAnimation;
                setTimeout(() => 
                {
                    current.style.opacity = 1;

                }, 200);
            }, buffer*i);
            this.resize(this.maxHP+i);
        }
        this.tempHP = num;

        setTimeout(this.update.bind(this), num * num + 100);
    }

    update()
    {
        this.text.innerText = `HP: ${this.hp+this.tempHP}/${this.maxHP}`;
        if (this.hp < this.maxHP / 2)
        {
            this.body.classList.add("low-hp");
        }
        else 
        {
            this.body.classList.remove("low-hp")
        }
    }
}

test = new Healthbar("test");

var add = document.createElement("div");
add.className = "hp-add";

add.addEventListener("mouseup", () => 
{
    var overheal = 0;
    if (test.hp + 3 > test.maxHP)
        overheal = (test.hp+3) - test.maxHP;

    test.gainHP(3);

    if (overheal > 0)
    {
        test.gainTempHP(test.tempHP+overheal);
    }

});

var sub = document.createElement("div");
sub.className = "hp-sub";

sub.addEventListener("mouseup", () => 
{
    test.loseHP(3);
});

//document.getElementsByClassName('hud')[0].appendChild(add);
//document.getElementsByClassName('hud')[0].appendChild(sub);

