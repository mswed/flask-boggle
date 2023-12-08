const guessBtn = document.querySelector('#guess-btn')
const guessText = document.querySelector('#guess')
const msg = document.querySelector('#messages')
const score = document.querySelector('#score')
const allowedTime = 2
const timer = document.querySelector('#timer')
const timesPlayed = document.querySelector('#times-played')
const highScore = document.querySelector('#high-score')

guessBtn.addEventListener('click', async (evt) => {
    evt.preventDefault()
    console.log('Sending a guess!')
    await submitGuess()
})

async function submitGuess() {
    if (parseInt(timer.innerText) < allowedTime) {
        console.log(parseInt(timer.innerText) < allowedTime)
        const data = new FormData();
        data.append('guess', guessText.value)
        const res = await axios.post('/guess', data)
        console.log(res.data.result)
        if (res.data.result === 'ok') {
            score.innerText = parseInt(score.innerText) + guessText.value.length
        }
        msg.innerText = `Server says ${guessText.value} is ${res.data.result}`
    }

}


document.addEventListener('DOMContentLoaded', (evt) => {
    let runTime = 0
    let interval = setInterval(function () {
        let time = parseInt(timer.innerText)
        if (runTime === allowedTime - 1) {
            clearInterval(interval)
            endGame()
        }
        runTime += 1
        timer.innerText = runTime

    }, 1000)
})

const endGame = async function () {
    const data = {score: score.innerText}
    const res = await axios.post('/end', data)
    timesPlayed.innerText = parseInt(timesPlayed.innerText) + 1
    let cleanHighScore = highScore.innerText.replace('(', '')
    cleanHighScore = parseInt(cleanHighScore.replace(')', ''))

    highScore.innerText = `(${cleanHighScore + 1})`
    alert('Ooops! Your time is up! ')

}