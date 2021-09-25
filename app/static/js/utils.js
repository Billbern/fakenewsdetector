const close = '<svg width="16" height="16" fill="#fff" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M2.252 2.252a.857.857 0 011.213 0L8 6.788l4.535-4.536a.858.858 0 011.214 1.213L9.212 8l4.537 4.535a.858.858 0 01-1.214 1.214L8 9.212l-4.535 4.537a.858.858 0 01-1.213-1.214L6.788 8 2.252 3.465a.857.857 0 010-1.213z"/></svg>'
const clear = '<svg width="16" height="16" fill="#f00" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M2.252 2.252a.857.857 0 011.213 0L8 6.788l4.535-4.536a.858.858 0 011.214 1.213L9.212 8l4.537 4.535a.858.858 0 01-1.214 1.214L8 9.212l-4.535 4.537a.858.858 0 01-1.213-1.214L6.788 8 2.252 3.465a.857.857 0 010-1.213z"/></svg>'

const loader = document.getElementById('loader-id');
const articleText = document.getElementById("article-text");
const resultBanner = document.getElementById("result-banner");
const totalWordsText = document.getElementById("totalWords");
const totalCharsText = document.getElementById("totalChar");

const userName = document.getElementById("uname");
const passWord = document.getElementById("pword");

const delButton = document.getElementById("delbutton");
const loginButton = document.getElementById("loginbutton");
const detectButton = document.getElementById("predict-button-id");
const btnLogin = document.getElementById("btn-login");

const loginForm = document.getElementById("loginform");
const flashMessage = document.getElementById("flashmessage");

const getPrediction = async (text) => {
    const response = await fetch('/predict', {
        method: 'POST',
        body: JSON.stringify({ 'text': text }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    //extract JSON from the http response
    const myJson = await response.json();
    return myJson.result;
}

async function logInUser(name, pwd) {
    const response = await fetch('/login', {
        method: 'POST',
        body: JSON.stringify({ 'username': name, 'password': pwd }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json();
    return myJson;
}


function showLoginBox() {
    let loginDisplay = document.getElementById("loginBox");

    if (loginDisplay.style.display === 'none') {
        loginButton.innerHTML = close;
        loginButton.style.marginLeft = "28px";
        loginDisplay.style.display = 'block';
    } else {
        loginButton.innerText = 'Login';
        loginButton.style.marginLeft = "0";
        loginDisplay.style.display = 'none';
    }

}

function predictionReponse() {
    // start spinner and remove old prediction
    if (articleText.value) {

        loader.style.display = 'inline';
        resultBanner.textContent = '';

        let prediction = getPrediction(articleText.value);

        prediction.then((res) => {

            loader.style.display = 'none';

            if (res === "real") {
                articleText.style.border = "3px solid green";
                resultBanner.style.color = "green";
                resultBanner.textContent = "This is a Real news!";
            } else {
                articleText.style.border = "3px solid red";
                resultBanner.style.color = "red";
                resultBanner.textContent = "This is a Fake news!";
            }
        }, (error) => {
            // console.error("Fake New Detection Failed: " + error);
            articleText.style.border = "3px solid red";
            resultBanner.style.color = "red";
            resultBanner.textContent = "Authentication Failed;";
        });
    } else {
        articleText.style.border = "3px solid red";
        resultBanner.style.color = "red";
        resultBanner.textContent = "no news to authenticate";
    }


}

function getTotalsWords() {
    const newWords = articleText.value.split(' ');
    totalWordsText.innerText = newWords.length;
}

function getTotalsChars() {
    totalCharsText.innerText = articleText.value.replace(' ', '').length;
}


function clearTextBox() {
    articleText.value = "";
    totalWordsText.innerText = "0";
    totalCharsText.innerText = "0";
    delButton.style.display = "none";
}


function getTextUtils() {
    delButton.style.display = "inline-block";
    getTotalsWords();
    getTotalsChars();
}


userName.addEventListener("change", ()=>{
    if(passWord.value){
        btnLogin.removeAttribute('disabled');
    }
}, false)

passWord.addEventListener("change", ()=>{
    if(userName.value){
        btnLogin.removeAttribute('disabled');
    }
}, false)



loginForm.addEventListener("submit", (e)=>{
    e.preventDefault();
    
    let reponse = logInUser(userName.value, passWord.value);
    
    reponse.then((res)=>{

        if(res['Error']){
            flashMessage.innerHTML = `${res['Error']} <span class="ms-1" id="flashclear">${clear}<span/> `;
        }else{
            const firstDay = new Date();
            const expires = new Date(firstDay.getTime() + 7 * 24 * 60 * 60 * 1000);
            document.cookie = `token=${res['Success'].token}; expires=${expires}; path=/; Secure`
            window.location.href = '/dashboard';
        }

    })
}, false)

articleText.addEventListener("change", getTextUtils, false);
delButton.addEventListener("click", clearTextBox, false);
loginButton.addEventListener("click", showLoginBox, false);
detectButton.addEventListener("click", predictionReponse, false);