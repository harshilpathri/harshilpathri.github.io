const suits = ['S', 'H', 'D', 'C'];
const values = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'];
const selectedHand = [];
const selectedBoard = [];
const selectedCards = new Set();

const grid = document.getElementById('card-grid');
const handDisplay = document.getElementById('hand-display');
const boardDisplay = document.getElementById('board-display');

function renderCards() {
    for (const suit of suits) {
        for (const value of values) {
            const cardCode = `${value}${suit}`;
            console.log(cardCode)
            const img = document.createElement('img');
            img.src = `static/images/cards/${cardCode}.png`;
            img.alt = cardCode;
            img.className = 'card-img';
            img.dataset.card = cardCode;

            img.onclick = () => selectCard(cardCode, img);
            grid.appendChild(img);
        }
    }
}

function selectCard(card, imgElement) {
  if (selectedCards.has(card)) return;

  if (selectedHand.length < 2) {
    selectedHand.push(card);
    imgElement.classList.add('selected-hand');
    selectedCards.add(card);
  } else if (selectedBoard.length < 5) {
    selectedBoard.push(card);
    imgElement.classList.add('selected');
    resultBox.textContent = "";
    selectedCards.add(card);
  }

  updateDisplay();
}

function updateDisplay() {
    handDisplay.innerHTML = '';
    boardDisplay.innerHTML = '';

    selectedHand.forEach(card => {
    const img = document.createElement('img');
    img.src = `static/images/cards/${card}.png`;
    img.alt = card;
    handDisplay.appendChild(img);
    });

    selectedBoard.forEach(card => {
    const img = document.createElement('img');
    img.src = `static/images/cards/${card}.png`;
    img.alt = card;
    boardDisplay.appendChild(img);
    });

}

function resetSelection() {
  selectedHand.length = 0;
  selectedBoard.length = 0;
  selectedCards.clear();
  resultBox.textContent = "";
  document.querySelectorAll('.card-img').forEach(img => img.classList.remove('selected'));
  document.querySelectorAll('.card-img').forEach(img => img.classList.remove('selected-hand'));
  updateDisplay();
}

function calculateOdds() {
  if (selectedHand.length === 2) {
    const spinner = document.getElementById('spinner');
    document.getElementById('results-section').style.display = 'block';
    resultBox.textContent = "";
    spinner.style.display = 'block';

    fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        hand: selectedHand,
        board: selectedBoard
      }),
    })
    .then(res => res.json())
    .then(data => {
      spinner.style.display = 'none';

      if (data.error) {
        resultBox.textContent = "Error: " + data.error;
        return;
      }
      resultBox.textContent = `Win: ${(data.win * 100).toFixed(1)}%, Tie: ${(data.tie * 100).toFixed(1)}%, Lose: ${(data.lose * 100).toFixed(1)}%`;
    })
    .catch(err => {
      spinner.style.display = 'none';
      resultBox.textContent = "Request failed: " + err.message;
    });
  }
}




renderCards();
