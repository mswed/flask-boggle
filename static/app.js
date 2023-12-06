guessBtn = document.querySelector('#guess-btn')
guessText = document.querySelector('#guess')
msg = document.querySelector('#messages')

guessBtn.addEventListener('click', async (evt) => {
    evt.preventDefault()
    console.log('Sending a guess!')
    await submitGuess()
})

async function submitGuess() {
    const data = new FormData();
    data.append('guess', guessText.value)
    console.log(data)
    const res = await axios.post('/guess', data)
    console.log(res)
    msg.innerText = `Server says ${guessText.value} is ${res.data.result}`

}