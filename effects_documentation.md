There are 3 kinds of effects: 
    1. Instant
    2. Constant
    3. Repeated

## Instant
    
These effects happen instanteously. They apply only once and do something static like heal/damage, or give temporary hp.

## Constant

These effects linger and stay on, but are still only applied once. These include things like modifying a stat or replacing an object's method temporarily (like what combat tricks do)

## Repeated

These effects linger like Constants, but are re-applied anew each turn. They usually do things like damange over time. Each time and object's update function is called, all of the repeated effects attached to that object 'repeat' their effect.