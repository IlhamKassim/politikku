document.addEventListener('DOMContentLoaded', () => {
    const options = document.querySelectorAll('.quiz-option');
    options.forEach(option => {
        option.addEventListener('click', function() {
            const isCorrect = this.dataset.correct === 'true';
            const feedbackBox = this.closest('.quiz-widget').querySelector('.quiz-feedback');
            
            // Remove previous states
            options.forEach(opt => opt.style.backgroundColor = 'white');
            
            if (isCorrect) {
                this.style.backgroundColor = '#c6f6d5';
                feedbackBox.className = 'quiz-feedback correct';
                feedbackBox.innerHTML = `<strong>Correct!</strong> ${this.dataset.explanation}`;
            } else {
                this.style.backgroundColor = '#fed7d7';
                feedbackBox.className = 'quiz-feedback incorrect';
                feedbackBox.innerHTML = `<strong>Not quite.</strong> ${this.dataset.explanation}`;
            }
        });
    });
});
