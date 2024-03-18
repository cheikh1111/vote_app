document.addEventListener('DOMContentLoaded', () => {
    let passwordDivs = document.querySelectorAll('.password');
    for (let passwordDiv of passwordDivs) {
        let passwordInput = passwordDiv.querySelector('input');
        let viewSpan = passwordDiv.querySelector('span');

        viewSpan.addEventListener('click', () => {
            if (passwordInput.type === 'text') {
                passwordInput.type = 'password';
                viewSpan.innerText = 'monter';
            } else {
                passwordInput.type = 'text';
                viewSpan.innerText = 'cacher';
            }
        });

        passwordInput.addEventListener('focus', function() {
            this.parentElement.style.border = '2px solid black';
        });

        passwordInput.addEventListener('blur', function() {
            this.parentElement.style.border = '1px solid black';
        });
    }
});
