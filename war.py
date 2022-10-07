import datetime
import random
import time
import sys

from numpy import integer

def replace_cards(win_pile:list) -> list:
    # I'll give 6 seconds avg for shuffling the deck
    # time.sleep(6)
    win_pile_copy = win_pile.copy()
    random.shuffle(win_pile_copy)
    return win_pile_copy

def get_start_time() -> float:
    return time.time()


def init_deck_and_deal_cards() -> tuple:
    deck = []

    #fill the deck
    for i in range(13):
        for j in range(4):
            deck.append(i)

    random.shuffle(deck)

    player_one = []
    player_two = []

    # give cards to players
    counter = 0
    for card in deck:
        if counter%2 == 0:
            player_one.append(card)
        else:
            player_two.append(card)
        counter+=1

    return player_one, player_two

def play_war(player_one: list, player_two: list) -> tuple:
    player_one_win_pile = []
    player_two_win_pile = []
    player_one_auto_loss = False
    player_two_auto_loss = False
    turns = 0

    while player_one != [] and player_two != []:
        turns += 1
        player_one_card = player_one.pop(0)
        player_two_card = player_two.pop(0)
        # mimic time placing card down on table
        #time.sleep(3)

        if player_one_card > player_two_card:
            player_one_win_pile.append(player_one_card)
            player_one_win_pile.append(player_two_card)
        elif player_one_card < player_two_card:
            player_two_win_pile.append(player_one_card)
            player_two_win_pile.append(player_two_card)
        else:
            # War!
            # It probably takes about 6 seconds to play all of the cards
            # and for the winner to collect them
            #time.sleep(6)
            player_one_prize = []
            player_two_prize = []
            player_one_play = -1
            player_two_play = -1            

            while player_one_play == player_two_play: 
                if player_one_play != -1:
                    player_one_prize.append(player_one_play)
                    player_two_prize.append(player_two_play)

                for i in range(2):
                    if player_one:
                        player_one_prize.append(player_one.pop(0))
                    elif not player_one:
                        # Player one doesn't have enough cards for War, auto loss
                        if len(player_one_win_pile) <= (2-i):
                            player_one_auto_loss = True
                            break
                        # Otherwise we just use our win pile
                        player_one = replace_cards(player_one_win_pile)
                        player_one_win_pile.clear()
                        player_one_prize.append(player_one.pop(0))
                if player_one:
                    player_one_play = player_one.pop(0)
                else:
                    if player_one_win_pile:
                        player_one = replace_cards(player_one_win_pile)
                        player_one_win_pile.clear()
                        player_one_play = player_one.pop(0)
                    else:
                        player_one_auto_loss = True
                        break

                for i in range(2):
                    if player_two:
                        player_two_prize.append(player_two.pop(0))
                    elif not player_two:
                        # Player two doesn't have enough cards for War, auto loss
                        if len(player_two_win_pile) <= (2-i):
                            player_two_auto_loss = True
                            break
                        # Otherwise we just use our win pile
                        player_two = replace_cards(player_two_win_pile)
                        player_two_win_pile.clear()
                        player_two_prize.append(player_two.pop(0))
                if player_two:
                    player_two_play = player_two.pop(0)
                else:
                    if player_two_win_pile:
                        player_two = replace_cards(player_two_win_pile)
                        player_two_win_pile.clear()
                        player_two_play = player_two.pop(0)
                    else:
                        player_two_auto_loss = True
                        break
            
            if player_one_auto_loss or player_two_auto_loss:
                break
            
            player_one_prize.append(player_one_card)
            player_two_prize.append(player_two_card)
            player_one_prize.append(player_one_play)
            player_two_prize.append(player_two_play)
            
            if player_one_play > player_two_play:
                player_one_win_pile.extend(player_one_prize)
                player_one_win_pile.extend(player_two_prize)
            else:
                player_two_win_pile.extend(player_one_prize)
                player_two_win_pile.extend(player_two_prize)
            player_one_prize.clear()
            player_two_prize.clear()            
        
        if player_one == []:
            player_one = replace_cards(player_one_win_pile)
            player_one_win_pile.clear()
        if player_two == []:
            player_two = replace_cards(player_two_win_pile)
            player_two_win_pile.clear()


    if player_one_auto_loss or player_one == []:
        win_bit = 2
    elif player_two_auto_loss or player_two == []:
        win_bit = 1
    else:
        win_bit = -1
    
    return win_bit, turns

def main():
    start_time = get_start_time()
    turn_total = 0
    games = 100000
    min_turns = 10000000000
    max_turns = -1
    for i in range(games):
        print(i)
        player_one, player_two = init_deck_and_deal_cards()
        win_bit, turns = play_war(player_one, player_two)
        turn_total += turns

        if turns > max_turns:
            max_turns = turns
        elif turns < min_turns:
            min_turns = turns
    
    turn_avg = turn_total / 100000

    end_time = time.time() - start_time
    #datetime.fromtimestamp(end_time).strftime('%Y-%m-%d')
    if win_bit == -1:
        sys.exit()

    #print(f"Player {win_bit} wins. Game took {end_time} to complete and {turns} turns.")
    print(f"Played {games} games, the turn avg was {turn_avg}, the max turns was {max_turns} and the min turns was {min_turns}")

if __name__ == "__main__":
    main()