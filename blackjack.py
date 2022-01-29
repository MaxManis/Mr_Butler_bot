import requests


url = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'

response = requests.get(url)
data = response.json()
deck_id = data['deck_id']


def deal():
    hand = []
    count = 1
    for i in range(2):
        take_url = f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}'
        take_res = requests.get(take_url)
        card = take_res.json()
        link = card['cards'][0]['image']
        value = card['cards'][0]['value']
        suit = card['cards'][0]['suit']

        res = {
            'link': link,
            'value': value,
            'suit': suit,
        }
        hand.append(res)
        count += 1
    return hand


def total(hand):
    total = 0
    for card in hand:
        if card['value'] == "JACK" or card['value'] == "QUEEN" or card['value'] == "KING":
            total += 10
        elif card['value'] == "ACE":
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += int(card['value'])
    return total


def hit(hand):
    count = 1
    take_url = f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}'
    take_res = requests.get(take_url)
    card = take_res.json()
    link = card['cards'][0]['image']
    value = card['cards'][0]['value']
    suit = card['cards'][0]['suit']

    res = {
        'link': link,
        'value': value,
        'suit': suit,
    }
    hand.append(res)
    return hand


def print_results(dealer_hand, player_hand):
    d_hand = ''
    p_hand = ''
    for i in dealer_hand:
        val = i['value']
        d_hand += val + ', '
    for i in player_hand:
        val = i['value']
        p_hand += val + ', '

    res = "The dealer has a " + d_hand + "for a total of " + str(total(dealer_hand)) + \
          "\nYou have a " + p_hand + "for a total of " + str(total(player_hand))
    return res


def blackjack(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        res = "Congratulations! You got a Blackjack!\n"
        return res
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        res = "Sorry, you lose. The dealer got a blackjack.\n"
        return res


def score(dealer_hand, player_hand):
    if total(player_hand) == 21:
        res = print_results(dealer_hand, player_hand) + "\nCongratulations! You got a Blackjack!\n"
        return res
    elif total(dealer_hand) == 21:
        res = print_results(dealer_hand, player_hand) + "\nSorry, you lose. The dealer got a blackjack.\n"
        return res
    elif total(player_hand) > 21:
        res = print_results(dealer_hand, player_hand) + "\nSorry. You busted. You lose.\n"
        return res
    elif total(dealer_hand) > 21:
        res = print_results(dealer_hand, player_hand) + "\nDealer busts. You win!\n"
        return res
    elif total(player_hand) < total(dealer_hand):
        res = print_results(dealer_hand, player_hand) + "\nSorry. Your score isn't higher than the dealer. You lose.\n"
        return res
    elif total(player_hand) > total(dealer_hand):
        res = print_results(dealer_hand, player_hand) + "\nCongratulations. Your score is higher than the dealer. You win\n"
        return res

