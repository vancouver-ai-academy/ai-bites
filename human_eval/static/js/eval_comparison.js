let currentButton = null;
const submitFeedbackButton = document.getElementById('feedbackButton');
const toggleButtons = Array.from(document.getElementsByClassName('toggler'));

const choiceState = {
    choice: null
}

function resetButtons() {
    toggleButtons.forEach(button => {
        button.classList.remove('active');
    });
    submitFeedbackButton.disabled = true;
}


const compareViewport = document.getElementById('compare-viewport');
function startFetchUx() {
    console.log('startFetchUx');
    handleCardHighlight(-1);
    console.log(compareViewport);
    compareViewport.style.display = 'hidden';
}

function endFetchUx() {
    console.log('endFetchUx');
    compareViewport.style.display = 'flex';
}

function handleLogin() {
    const emailInput = document.getElementById("email-input");

    if (emailInput.value.trim() === '') {
        alert('Please enter your email.');
        return;
    }

    
    const loginOverlay = document.getElementById('login_overlay');
    loginOverlay.style.display = 'none';

    const welcomeMessage = document.getElementById('welcome-message');
    welcomeMessage.innerHTML = `${emailInput.value}`;

    const compareColumns = document.getElementById('compare-columns');
    compareColumns.style.display = 'flex';

    fetchDataEvalArcade();
    
}

function fetchDataEvalArcade() {
    // const compareIdsElement = document.getElementById('compare-columns');
    // compareIdsElement.style.display = 'none'; // Change 'color' and 'red' to desired style property and value
             
    startFetchUx();
    const welcomeMessage = document.getElementById('welcome-message');
   fetch('/eval_get_insight_cards', {
        method: 'POST', // Use POST to send data
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"dataset":"csm", "user":welcomeMessage.innerText})
    })
        .then(response => response.json())
        .then(data => {
            count = data.count;
            user = data.username;

            if (data.n_insights === 0) {
                // TODO: better UX here.
                alert("You have evaluated all insights. Thank you for your feedback!");
            } else {
                // Populate title
                // const title = document.getElementById('title');
                // title.innerHTML = `${data.title}`;
                // Add style to compare-ids element
                // const compareIdsElement = document.getElementById('compare-columns');
                // compareIdsElement.style.display = 'none'; // Change 'color' and 'red' to desired style property and value
                
                // Populate Insights
                const insightBlob1 = document.getElementById('insight-blob1');
                insightBlob1.innerHTML = `${data.insight_card_a}`;

                const insightBlob2 = document.getElementById('insight-blob2');
                insightBlob2.innerHTML = `${data.insight_card_b}`;

                const question = document.getElementById('form-header');
                question.innerHTML = ` Which Output is Better?  
                                     <p style="font-style: italic;font-size: 1.2rem;color:gray" id="insight-desc">Task: "${data.task}"</p> 
                                                     <p style="font-style: italic;font-size: .8rem;color:gray;margin-top:-10px" id="insight-desc">"${data.criterion}</p>
                                     `;
                
                const timestamp = document.getElementById('timestamp');
                timestamp.innerHTML = `${data.timestamp}`

                // const countElement = document.getElementById('count');
                // countElement.innerHTML = count;
            }
        })
        .then(resetButtons)
        .then(endFetchUx)
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}


const handleCardHighlight = (id) => {
    const selectedClass = 'selected';
    const insightCardElementIds = ['insight-blob1', 'insight-blob2'];
    
    const insightCardElements = insightCardElementIds.map(id => document.getElementById(id)) 

    const selectetInsightCardIds = id === 99 ? insightCardElementIds : id >= 0 ? [insightCardElementIds[id]] : [];
    
    insightCardElements.forEach(element => {
        if (selectetInsightCardIds.includes(element.id)) {
            element.classList.add(selectedClass);
        }
        else {
            element.classList.remove(selectedClass);
        }
    })
}


const handleInsightSelect = (button, id) => {
    handleCardHighlight(id);

    Array.from(document.getElementsByClassName('toggler')).forEach(element => {
        if(element !== button) {
            element.classList.remove('active');
        }
    });
    console.log({id})
    choiceState.choice = id;
    button.classList.add('active');
    submitFeedbackButton.disabled = false;
}


submitFeedbackButton.addEventListener('click', function() {
    submitFeedbackButton.disabled = true;
    const form = document.getElementById('compare-form');

    const parser = new DOMParser();
    const full_content = document.getElementById('feedbackForm')?.innerHTML;
    const doc = parser.parseFromString(full_content, 'text/html');
    const divs = doc.getElementsByTagName('div');
    const timestamp = document.getElementById('timestamp').innerText;

    const welcomeMessage = document.getElementById('welcome-message');
    console.log({choiceState});
    const feedback = {
        user: welcomeMessage.innerText,
        choice: choiceState.choice,
        text: form.querySelector('textarea[name="reason"]').value,
        timestamp: timestamp,
        question: document.getElementById('form-header').innerText,

    }

    fetch('/submit-feedback-compare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedback)
    })
    .then(response => {
        if (!response.ok) {
            alert("Feedback Bug");
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {

        console.log('Feedback submitted successfully:', data);

        // Clear form and switch panes
        form.reset();

         // Fetch new insight HTML
        fetchDataEvalArcade();  // Call the fun
        
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
    });
});


// document.addEventListener('DOMContentLoaded', () => {
//     fetchDataEvalArcade();
// });