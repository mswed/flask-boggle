class Game {
    // Define fields
    guessBtn = document.querySelector('#guess-btn')
    hintBtn = document.querySelector('#hint-btn')
    guessText = document.querySelector('#guess')
    msg = document.querySelector('#messages')
    score = document.querySelector('#score')
    timer = document.querySelector('#timer')
    timesPlayed = document.querySelector('#times-played')
    highScore = document.querySelector('#high-score')
    interval

    constructor(countDown) {
        this.countDown = countDown
        this.originalLength = countDown
        this.timer.innerText = this.countDown
        this.guessBtn.addEventListener('click', async (evt) => {
            evt.preventDefault()
            await this.submitGuess()
        })

        this.hintBtn.addEventListener('click', async (evt) => {
            evt.preventDefault()
            const hint = await this.getHint()
            for (let location of hint[1]) {
                for (let loc of location) {
                    const target =`#y${loc[0] + 1} #x${loc[1] + 1}`
                    const box = document.querySelector(target)
                    box.classList.add('test')
                    // box.style.backgroundColor = 'pink'
                    setTimeout(() => {
                        for (let box of document.querySelectorAll('.box')) {
                            box.classList.remove('test')
                        }
                    }, 3000)
                }
            }

        })
        this.startTimer()

    }

    async getHint(){
        const res = await axios.get('/hint')
        return res.data
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
            if (this.countDown <= 10) {
                this.timer.style.color = 'red'
            } else if (this.countDown <= this.originalLength / 2) {
                this.timer.style.color = 'orange'
            }
        }

    }
    async submitGuess() {
        if (parseInt(this.timer.innerText) > 0) {
            const data = new FormData();
            data.append('guess', this.guessText.value)
            const res = await axios.post('/guess', data)
            if (res.data.result === 'ok') {
                this.score.innerText = parseInt(this.score.innerText) + this.guessText.value.length
                this.msg.innerText = `${this.guessText.value} ${this.makeReadable(res.data.result)}`
                this.msg.style.color = '#37FF8B'
            } else {
                this.msg.innerText = `${this.guessText.value} ${this.makeReadable(res.data.result)}`
                this.msg.style.color = '#DD0426'
            }
        this.guessText.value = ''
        }
    }

    makeReadable(message) {
        const msgMap = {
            'ok': 'is a GREAT word!',
            'not-word': 'is not a valid word',
            'not-on-board': 'is not on the board',
            'already-guessed': 'was already guessed! Try again'
        }
        return msgMap[message]
    }

    async endGame() {
        const data = {score: this.score.innerText}
        const res = await axios.post('/end', data)
        this.timesPlayed.innerText = res.data.timesPlayed
        const newHighScore = res.data.highScore ? `NEW HIGH SCORE: ${res.data.highScore}!` : ''
        if (newHighScore) {
            this.highScore.innerText = `(${res.data.highScore})`
        }

        alert(`Time's up!\n\n SCORE: ${res.data.score}\n ${newHighScore}`)
    }


}

const g = new Game(120)