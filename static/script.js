// Store shuffled questions in Local Storage
function storeShuffledQuestions(questions) {
    localStorage.setItem('shuffledQuestions', JSON.stringify(questions));
}

// Retrieve shuffled questions from Local Storage
function getShuffledQuestions() {
    const storedQuestions = localStorage.getItem('shuffledQuestions');
    return storedQuestions ? JSON.parse(storedQuestions) : [];
}

document.addEventListener('DOMContentLoaded', function() {
    const showAnswerButtons = document.querySelectorAll('.show-answer-btn');
    showAnswerButtons.forEach(button => {
        button.addEventListener('click', function() {
            const answerElement = this.nextElementSibling;
            if (answerElement.style.display === 'none') {
                answerElement.style.display = 'block';
                this.textContent = 'Hide Answer';
            } else {
                answerElement.style.display = 'none';
                this.textContent = 'Show Answer';
            }
            // Add the following code to include question_index in the form data
            const questionIndexInput = document.createElement('input');
            questionIndexInput.type = 'hidden';
            questionIndexInput.name = 'question_index';
            questionIndexInput.value = this.dataset.questionIndex;
            this.parentElement.appendChild(questionIndexInput);
        });
    });
});
