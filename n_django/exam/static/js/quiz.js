const url = window.location.href


const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')

//arrow function
const activateTimer = (time) => {

    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>Timer: 0${time}:00</b>` //to display 01:00
    }

    else {
        timerBox.innerHTML = `<b>Timer: ${time}:00</b>` // to display 10:00
    }

    let minutes = time - 1
    //when we initially start (example: 5mins, countdown looks like: 5:00 and then 4:59)

    let seconds = 60

    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        // console.log('Seconds')
        seconds -- 
        if (seconds < 0 ){ //if seconds reaches less than 0 it sets seconds value to 59. 
            seconds = 59
            minutes --
        }

        if (minutes.toString().length < 2) {
            displayMinutes = '0'+ minutes
        } 

        else{
            displayMinutes = minutes
        }

        if (seconds.toString().length < 2) {
            displaySeconds = '0'+ seconds
        } 

        else {
            displaySeconds = seconds
        }

        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = '<b>00:00</b'
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')
                sendData()
            },)
        }

        timerBox.innerHTML = `Timer: <b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000) //time changes every single second
}
 
// ajax gets data without re - reloading the page
$.ajax({
    type: 'GET',
    url: `${url}/data/`, //getting data from this url (data is being received from view through JSONresponse)
    success: function(response){
        // console.log(response)
        const data = response.data
        // console.log(data)

        // each element has key and value as question and answer respectively
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){  //for of statement loops through the values of an iterable object
                // console.log(question)
                // console.log(answers)
                // mb = margin bottom, mt - margin top
                
                quizBox.innerHTML += `
                    
                    <div class='mb-2'> 
                        <b>${question}</b>
                `
                answers.forEach(answer =>{
                    quizBox.innerHTML +=`
                        <div>
                            <input type='radio' class='ans' id='${question}-${answer}' name='${question}' value='${answer}'>
                            <label for='${question}'>${answer}</label>
                        </div>
                    `
                })
            }
            quizBox.innerHTML +=`<hr>`
        })
        activateTimer(response.time)
        
    },
    error: function(error){
        console.log(error)
    }
})


const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value

    elements.forEach(el => {
        if (el.checked){
            data[el.name] = el.value
        } 
        else{
            if (!data[el.name]){
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}/save/`,
        data: data,
        // here response is the object passed as the first argument of all Ajax requests callbacks
        success: function(response){
            // console.log(response)
            const results = response.results
            // console.log(results)
            quizForm.classList.add('not-visible')

            //passed is the key used in views.py that returns passed or not under JsonResponse
            scoreBox.innerHTML = `${response.passed ? 'Passed' : 'Failed'}. Your result is ${response.score.toFixed(2)}.`

            results.forEach(res=>{
                const resDiv= document.createElement('div')
                for (const [question, resp] of Object.entries(res)){
                    // console.log(question)
                    // console.log(resp)
                    // console.log('******')

                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'test-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered'){
                        resDiv.innerHTML += '| Not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        // console.log(answer, correct)

                        if (answer == correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `| Answered: ${answer}`
                        }
                        else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | Correct Answer: ${correct}`
                            resDiv.innerHTML += ` | Answered: ${answer}`
                        }
                    }
                }
                // const body = document.getElementsByTagName('BODY')[0]

                resultBox.append(resDiv)
            })

        },
        error: function(error){
            console.log(error)
        }


    })
}


quizForm.addEventListener('submit', e =>{
    e.preventDefault()

    sendData()
})

