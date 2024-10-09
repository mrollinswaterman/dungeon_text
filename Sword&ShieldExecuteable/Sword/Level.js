class Level{
    constructor(level, weapon){
        this.level = level
        this.slimes = []

        this.weapon = weapon

        if(this.level === 1){
            window.xScroll = 0

            main = () =>{
                window.gameTime += Date.now() - time
                time = Date.now()

                //player stuff
                if(!player1.dead && !player1.cutscene){
                    player1.update()
                    player1.weapon.update()
                }

                //environment stuff
                sun.update()
                moon.update()
                cloudList.forEach(cloud => cloud.update())
                uTreeList.forEach(tree => {
                    tree.update()
                })
                lTreeList.forEach(tree => {
                    tree.update()
                })

                //enemy stuff
                Object.values(this.slimes).forEach(slime => {
                    if(!slime.dead && !player1.cutscene && !player1.dead){
                        slime.update()
                    }
                })

                //boss stuff
                if(player1.x >= encounterDist && player1.cutscene == false){
                    encounterDist = 100000000000000000000000000
                    player1.enemyCount = 1
                    player1.cutscene = true
                }
                if(!boss.dead){
                    boss.update()

                    if(boss.healthbar.hp < boss.hpVal/2 && !boss.secondPhase){
                        boss.secondPhase = true
                        boss.jumpDamage = 45
                        boss.dashDamage = 25
                        boss.dashRecovery = 1500
                        boss.img.src = "images/Bosses/Reginald-secondPhase.png"
                    }
                }

                if(boss.dead){
                    if(boss.item && !boss.item.pickedUp){
                        boss.item.update()
                    }
                }

                if(!gerald.dead){
                    gerald.update()
                }

                //is the player dead?
                doEvents()
                if(!player1.dead){
                    requestAnimationFrame(main)
                }else{
                    console.log('player-death')
                }
            }

        } else if(this.level === 2){
            window.xScroll = 0

            main = () => {
                window.gameTime += Date.now() - time
                time = Date.now()

                //player stuff
                
                if(!player1.dead){
                    player1.update()
                    player1.weapon.update()
                }

                //evironment stuff
                sun.update()
                moon.update()
                cloudList.forEach(cloud => cloud.update())
                uTreeList.forEach(tree => {
                    tree.update()
                })
                lTreeList.forEach(tree => {
                    tree.update()
                })

                //enemy stuff
                Object.values(this.slimes).forEach(slime => {
                    if(!slime.dead && !player1.cutscene && !player1.dead){
                        slime.update()
                        if(slime.snowballAttack){

                            if(slime.snowball){
                                slime.snowball.update()
                            }
                        }
                    }
                })

                //boss stuff
                if(player1.x >= encounterDist && player1.cutscene == false){
                    encounterDist = 100000000000000000000000000
                    player1.enemyCount = 1
                    player1.cutscene = true
                }
                if(!boss.dead){
                    boss.update()
                    boss.weapon.update()

                    if(boss.snowball && !boss.snowball.done){
                        boss.snowball.update()
                    }
                }
                if(boss.dead){
                    if(boss.item && !boss.item.pickedUp){
                        boss.item.update()
                    }
                }

                //is the player dead?
                doEvents()
                if(!player1.dead){
                    requestAnimationFrame(main)
                }else{
                    console.log('player-death')
                }

            }
        }
    }
    
    initializeEverything(){
        this.initializeEnviroment()
        this.initializePlayer()
        this.initializeEnemies()
        this.initializeBoss()

        setTimeout(() =>{
            requestAnimationFrame(main)
        }, 2000)
    }

    initializeEnviroment(){
                    
        if(this.level === 1){
            enviroment = generateForest(window.innerWidth)
        } else if(this.level === 2){
            enviroment = generateWinterWonderland(window.innerWidth)
        }
            
        cloudList = enviroment.cloudList
        sun = enviroment.sun
        moon = enviroment.moon
        uTreeList = enviroment.upperTreeList
        lTreeList = enviroment.lowerTreeList
    }

    initializePlayer(){
        if(player1 != null){
            if(player1.dead){
                player1 = new Player(1, this.weapon, this.slimes)
                player1.newGame = true
            }
        } else {
            player1 = new Player(1, this.weapon, this.slimes)
        }


        player1.weapon.adjust()

        player1.levelCounter = this.level

    }


    initializeEnemies(){

        if(this.level === 1){
                        
            this.slimes[0] = new Slime(0, player1, "small")
            
            this.slimes[1] = new Slime(1, player1, "small")
            this.slimes[2] = new Slime(1.1, player1, "small")

            this.slimes[3] = new Slime(1.5, player1, "medium")
            
            this.slimes[4] = new Slime(1.9, player1, "medium")
            this.slimes[5] = new Slime(1.95, player1, "small")

            this.slimes[6] = new Slime(2.3, player1, "medium")
            this.slimes[7] = new Slime(2.35, player1, "medium")

        } else if(this.level === 2){
            //stuff

            this.slimes[0] = new IceSlime(0, player1, "small")
            this.slimes[1] = new IceSlime(.1, player1, "small")
            this.slimes[2] = new IceSlime(0.2, player1, "small")
            this.slimes[3] = new IceSlime(.3, player1, "small")

            this.slimes[4] = new IceSlime(1, player1, "small")
            this.slimes[5] = new IceSlime(1.1, player1, "small")
            //this.slimes[6] = new IceSlime(1.15, player1, "medium")
            
            // this.slimes[7] = new IceSlime(1.5, player1, "medium")
            // this.slimes[8] = new IceSlime(1.55, player1, "medium")

            // this.slimes[9] = new IceSlime(1.8, player1, "medium")
            // this.slimes[10] = new IceSlime(1., player1, "medium")
            this.slimes[11] = new IceSlime(1.5, player1, "small")
            this.slimes[12] = new IceSlime(1.55, player1, "small")
        }
    }

    initializeBoss(){
        if(this.level === 1){

            encounterDist = 6585

            sign.style.left = encounterDist + 2000
            
            boss = new Reginald(encounterDist + window.innerWidth, player1)
            
            bossList = []
            bossList.push(boss)
            
            gerald = new Gerald(boss.x+boss.width+200)
        } else if(this.level === 2){

            encounterDist = 4800//6585

            sign.style.left = encounterDist + 2000
            
            boss = new Amelia(encounterDist + window.innerWidth, player1)

            bossList = []
            bossList.push(boss)

        }
    }

}