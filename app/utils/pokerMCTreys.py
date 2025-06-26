from treys import Card, Evaluator, Deck
from concurrent.futures import ProcessPoolExecutor

# Convert 'AS', 'KH', etc. to treys Card
def str_to_treys(card_str):
    rank = card_str[:-1]
    suit = card_str[-1].lower()
    if rank == '10':
        rank = 'T'
    return Card.new(rank + suit)

def _treys_worker(args):
    hand, board, n = args
    evaluator = Evaluator()
    hand = [str_to_treys(c) for c in hand]
    board = [str_to_treys(c) for c in board]
    win = tie = lose = 0

    for _ in range(n):
        deck = Deck()
        # Remove player's hand and board from deck
        for c in hand + board:
            deck.cards.remove(c)
        # Draw opponent hand
        opp_hand = deck.draw(2)
        # Draw remaining board cards
        full_board = board + deck.draw(5 - len(board))
        # Evaluate
        p1_score = evaluator.evaluate(full_board, hand)
        opp_score = evaluator.evaluate(full_board, opp_hand)
        if p1_score < opp_score:
            win += 1
        elif p1_score == opp_score:
            tie += 1
        else:
            lose += 1

    return win, tie, lose

def treys_calculate_odds(hand, board=None, simCount = 3 * 10**3, n_jobs=4):
    if board is None:
        board = []
    per_job = simCount // n_jobs
    args = [(hand, board, per_job) for _ in range(n_jobs)]
    win = tie = lose = 0

    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        for w, t, l in executor.map(_treys_worker, args):
            win += w
            tie += t
            lose += l

    total = win + tie + lose
    return {
        "win": round(win / total, 4),
        "lose": round(lose / total, 4),
        "tie": round(tie / total, 4)
    }