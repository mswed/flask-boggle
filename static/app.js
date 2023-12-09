class Game {
    // Define fields
    guessBtn = document.querySelector('#guess-btn')
    guessText = document.querySelector('#guess')
    msg = document.querySelector('#messages')
    score = document.querySelector('#score')
    timer = document.querySelector('#timer')
    timesPlayed = document.querySelector('#times-played')
    highScore = document.querySelector('#high-score')
    interval

    constructor(countDown) {
        this.countDown = countDown
        this.timer.innerText = this.countDown
        this.guessBtn.addEventListener('click', async (evt) => {
            evt.preventDefault()
            console.log('Sending a guess!')
            await this.submitGuess()
        })

        this.startTimer()

    }

    startTimer() {
        this.interval = setInterval(this.tick.bind(this), 1000)
    }

    tick() {
        if (this.countDown === 0) {
            clearInterval(this.interval)
            this.endGame()
        } else {
            this.countDown -= 1
            this.timer.innerText = this.countDown
        }

    }
    async submitGuess() {
        if (parseInt(this.timer.innerText) < this.countDown) {
            console.log(parseInt(this.timer.innerText) < this.countDown)
            const data = new FormData();
            data.append('guess', this.guessText.value)
            const res = await axios.post('/guess', data)
            if (res.data.result === 'ok') {
                this.score.innerText = parseInt(this.score.innerText) + this.guessText.value.length
            }
           this. msg.innerText = `{${this.guessText.value} ${this.makeReadable(res.data.result)}`
        }
    }

    makeReadable(message) {
        const msgMap = {
            'ok': 'Nice!',
            'not-word': 'is not a valid word',
            'not-on-board': 'is not on the board'
        }
        return msgMap[message]
    }

    async endGame() {
        const data = {score: this.score.innerText}
        const res = await axios.post('/end', data)
        this.timesPlayed.innerText = parseInt(this.timesPlayed.innerText) + 1
        let cleanHighScore = this.highScore.innerText.replace('(', '')
        cleanHighScore = parseInt(cleanHighScore.replace(')', ''))

        this.highScore.innerText = `(${cleanHighScore + 1})`
        alert('Ooops! Your time is up! ')
    }


}

const g = new Game(10)