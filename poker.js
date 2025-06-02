const suits = ['S', 'H', 'D', 'C'];
const values = ['A', 'K', 'Q', 'J', '1', '9', '8', '7', '6', '5', '4', '3', '2'];
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
            img.src = `/images/cards/${cardCode}.png`;
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
    imgElement.classList.add('selected');
    selectedCards.add(card);
  } else if (selectedBoard.length < 5) {
    selectedBoard.push(card);
    imgElement.classList.add('selected');
    selectedCards.add(card);
  }

  updateDisplay();
}

function updateDisplay() {
  handDisplay.textContent = selectedHand.join(', ');
  boardDisplay.textContent = selectedBoard.join(', ');
}

function resetSelection() {
  selectedHand.length = 0;
  selectedBoard.length = 0;
  selectedCards.clear();
  document.querySelectorAll('.card-img').forEach(img => img.classList.remove('selected'));
  updateDisplay();
}

renderCards();
