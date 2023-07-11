let table = document.querySelector('#board');
let currentWord = document.querySelector('#current-word');
let validMatches = document.querySelector('#valid-matches');
let countdownElement = document.querySelector("#countdown");
let boardContainer = document.querySelector('#board-container');
let score = document.querySelector('#score');
let gameArea = document.querySelector('#game-area');
let isMouseDown = false;
let word = null;

document.addEventListener('DOMContentLoaded', async function (e) {
    let game = await axios.get('/game').then(a => { return a.data });
    let board = game.board;
    let endTime = new Date(game.endTime);

    let countdownFunction = setInterval(function () {
        let now = new Date().getTime();
        let distance = endTime.getTime() - now;
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        countdownElement.innerHTML = "Time: " + minutes + "m " + seconds + "s ";

        if (distance < 0) {
            clearInterval(countdownFunction);
            countdownElement.innerHTML = "Countdown finished!";
            boardContainer.className = 'blur';
            let newTable = table.cloneNode(true);
            newTable.querySelectorAll('td').forEach(a => { a.className = ''; })

            table.parentNode.replaceChild(newTable, table);

            let gameOverMsg = document.createElement('h1');
            gameOverMsg.innerText = `Times up! Final score: ${score.innerText}`;
            document.body.prepend(gameOverMsg);
        }
    }, 1000);

    table.addEventListener('mousedown', function (e) {
        if (e.target.nodeName === "P") {
            isMouseDown = true;
            word = new Word(board, e.target.parentNode.id);
            currentWord.innerText = e.target.innerText;
            e.target.parentNode.className = 'selected';
        }
        else if (e.target.nodeName === "TD") {
            isMouseDown = true;
            word = new Word(board, e.target.id);
            currentWord.innerText = e.target.children[0].innerText;
            e.target.className = 'selected';
        };
    });

    document.addEventListener('mouseup', async function () {
        isMouseDown = false;
        if (word === null) { return };
        let data = await axios.post('/game', { word: word.submitWord() }).then(a => { return a.data });
        // console.log(data);
        let match = document.createElement('li');
        match.innerText = word.submitWord();
        if (data === 'ok') {
            score.innerText = Number(score.innerText) + 100;
            validMatches.append(match);
        }

        word = null;
        currentWord.innerText = '';
        Array.from(table.querySelectorAll('td')).forEach(a => { a.className = ''; });
    });

    table.addEventListener('mouseover', function (e) {
        if (!isMouseDown) { return };
        if (e.target.nodeName !== "P") { return };
        if (word.checkcell(e.target.parentNode.id) === 'pass') {
            currentWord.innerText += e.target.innerText;
            e.target.parentNode.className = 'selected';
        };
    });



});


