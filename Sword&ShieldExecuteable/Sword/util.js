let eventQueue = []

function awesomeTimeout(fn, delay) {
    eventQueue.push({fn: fn, delay: delay, t: window.gameTime, done: false})
}

function doEvents() {
    for (let e of eventQueue) {
        if (window.gameTime - e.t > e.delay) {
            e.fn()
            e.done = true
        }
    }
    eventQueue = eventQueue.filter(e => !e.done)
}