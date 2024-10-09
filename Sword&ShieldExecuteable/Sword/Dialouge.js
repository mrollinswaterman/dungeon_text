const punctuation = [".", "?", "!"]


const Reginald_Speech = [
    {
        speaker:"Reginald", 
        text:`Hoho! What have we here?  You seem to have lost your way little one.  Never fear, I shall send you back home.`
    },
    {
        speaker:"Reginald", 
        text:"Gerald! Fetch me my sword, that I may valiently vanquish this coniving criminal! ", 
        delete: true
    },
    {
        speaker: "Gerald", 
        text:". . .", 
        delete: true
    },
    {
        speaker:"Reginald", 
        text:"What's that? ", 
        delete: true
    },
    {
        speaker:"Gerald", 
        text:". . .", 
        delete: true
    },
    {
        speaker:"Reginald", 
        text:"You can't find it?  Why the Devil not? ", 
        delete: true
    },
    {
        speaker:"Gerald", 
        text:". . .", 
        delete: true
    },
    {
        speaker: "Reginald", 
        text: "Hmph! No matter.  I'll best this bothersome bandit with my own two hands.  So says SIR REGINALD S SLIME! ",
    }
]

const Reginald_Alt_Speech = [
    [
        {
            speaker:"Reginald",
            text:""
        }
    ]
]

// const Reginald_Alt_Speech = [
//     [
//         {
//             speaker: "Reginald", 
//             text: `Hoho! You have returned to test your mettle against the most masterful man-at-arms in all the land! Machinate all you wish little one, for you will NEVER best Sir Reginald!`
//         }
//     ],
//     [
//         {
//             speaker:"Reginald", 
//             text: "Back for more already? Your boastful bravado is unbecoming in the face of one as brilliantly bodacious as I. Your bumbling belligerance will soon be put to an end."
//         }
//     ],

//     [
//         {
//             speaker: "Reginald", 
//             text:"You know old boy, you've been trying so hard to get past me, I thought that this time, I'd just let you on by.", 
//             delete: true
//         }, 
//         {
//             speaker: "Reginald",
//             text:"HA! I'm only joking of course. Well come on then, give me your best shot!",
//         }
//     ],
//     [
//         {
//             speaker: "Reginald",
//             text: "Why hello again! It's been quite a while, I was beginning to worry about you. It would be a shame to have someone other than me send you back to the Pits. Don't take so long next time, eh old chap?",
//         }
//     ],
 
// ]

// [
//     {
//         speaker:"Reginald", 
//         text: "Well this is a little awkard, but Gerald hasn't been able to find my sword yet. I don't suppose you've seen it?",  
//         delete: true
//     },
//     {
//         speaker: "Player", 
//         text: ". . .",
//         delete: true
//     },
//     {
//         speaker: "Reginald", 
//         text: "Hmm... No I suppose not. Well anyway... to battle!"
//     }
// ],


const Amelia_Speech = [
    {
        speaker: "Amelia", 
        text: "Oh. Hello there. You don't belong in this place. How did you get here?", 
        delete: true
    },
    {
        speaker: "Player", 
        text: ". . .", 
        delete: true
    },
    {
        speaker:"Ameila", 
        text: "Ah, strong silent type I see. No matter. To reach this place, you must have gotten past Reginald at least. That is commendable.",
    },
    {
        speaker: "Amelia", 
        text: " Unfortunately, your journey ends here. Perhaps I will see you again... But I doubt it very much.", 
        delete: true
    }

]

const Amelia_Alt_Speech = [
    [
        {
            speaker: "Amelia", 
            text: "I'll make this quick if you don't mind. I'm very busy as of late.", 
            delete: true
        }
    ],
    [
        {
            speaker: "Amelia",
            text: "Back from the Pits I see. Imagine it, you crawled all the way here from that cursed place only to be sent right back. It's shame really. For your sake, I won't dawdle.",
            delete: true
        }
    ]

]

// const Amelia_Alt_Speech = [
//     [
//         {
//             speaker:"Amelia",
//             text: "...",
//             delete:false
//         }
//     ]
// ]

const LevelTwo = `
And so our hero has slain Sir Reginald, the mightest of the High King's accountants.  
The First Vassal.  
The King is surely weakened by this loss, but it is far from a lethal blow.  
To begin the end of the High King's reign, our hero must next journey north to the Sacred Land of Asmorel.  
There, in the bitter cold of an eternal winter, he will face the next of his great challengers...  
The Archbishop.
`

const Plot = {
    2: LevelTwo

}

const WeaponInfo = {
    "TrustySword": {name: "Trusty Sword", info: "A standard broadsword. While there are many like it, this one is yours. With a balanced weight, good attack speed and modest damage, your Trusty Sword is an ideal weapon with which to start your journey.", type: "sword"},
    "ReginaldJr": {name:"Reginald Jr.", info: "The favored weapon of the High King's mightiest accountant. It was clearly built for a larger user, you can still wield it with a certain amount of difficulty. Your reward for mastering such an unwieldly weapon is a very long range and very high damage.", type: "greatsword"}
}
