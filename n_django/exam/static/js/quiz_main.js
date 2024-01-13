
// The spread syntax is denoted by three dots, …. - It takes in an iterable (e.g an array) and expands it into individual elements and makes copy only.
const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href
// console.log(url)

// arrow function
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', ()=>{

    // console.log(modalBtn)
    const pk = modalBtn.getAttribute('data-pk')
    const subject = modalBtn.getAttribute('data-subject')
    const name = modalBtn.getAttribute('data-quiz')
    const numberOfQuestions = modalBtn.getAttribute('data-questions')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
        <div class='h5 mb-3'>Are you sure you want to beign '<b>${name}</b>'? </div>
        <div class='text-muted'>
            <ul style="list-style-type: none;">
                <li>Subject: <b>${subject}</b></li>
                <li>Number of questions: <b>${numberOfQuestions}</b></li>
                <li>Score to pass: <b>${scoreToPass}%</b></li>
                <li>Time: <b>${time} min</b></li>
            </ul>
        </div>
    `
    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk
    })
}))