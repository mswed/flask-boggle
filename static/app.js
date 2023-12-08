const guessBtn = document.querySelector('#guess-btn')
const guessText = document.querySelector('#guess')
const msg = document.querySelector('#messages')
const score = document.querySelector('#score')
const timer = document.querySelector('#timer')

guessBtn.addEventListener('click', async (evt) => {
    evt.preventDefault()
    console.log('Sending a guess!')
    await submitGuess()
})

async function submitGuess() {
    if (parseInt(timer.innerText) < 60) {
        console.log(parseInt(timer.innerText) < 60)
        const data = new FormData();
        data.append('guess', guessText.value)
        const res = await axios.post('/guess', data)
        console.log(res.data.result)
        if (res.data.result === 'ok') {
            score.innerText = parseInt(score.innerText) + guessText.value.length
        }
        msg.innerText = `Server says ${guessText.value} is ${res.data.result}`
    } else {
        alert('Ooops! Your time is up! ')
    }


}


document.addEventListener('DOMContentLoaded', (evt) => {
    let runTime = 0
    let interval = setInterval(function () {
        let time = parseInt(timer.innerText)
        if (runTime === 59) {
            clearInterval(interval)
        }
        runTime += 1
        timer.innerText = runTime

    }, 1000)
})
