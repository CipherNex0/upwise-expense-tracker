const form = document.getElementById('form');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmPassword');
const mismatchingWarning = document.getElementById('passwordMismatch');

if(form) {
    form.addEventListener("input", (e) =>{
        if(password.value != confirmPassword.value){
            e.preventDefault();
            mismatchingWarning.style.display = 'block';
        }else{
            mismatchingWarning.style.display = 'none';
        }
    });
}