from unittest import TestCase, TestLoader, TextTestRunner, TestSuite, loader, mock
from unittest.mock import call, MagicMock, mock_open, patch, Mock
from war import get_start_time, replace_cards, init_deck_and_deal_cards, play_war
import sys

class test_war(TestCase):

    def setUp(self) -> None:
        global get_start_time
        global replace_cards
        global init_deck_and_deal_cards
        global play_war

        self.get_start_time = get_start_time
        self.replace_cards = replace_cards
        self.init_deck_and_deal_cards = init_deck_and_deal_cards
        self.play_war = play_war

        get_start_time = MagicMock()
        replace_cards = MagicMock()
        init_deck_and_deal_cards = MagicMock()
        play_war = MagicMock()

    def tearDown(self) -> None:
        global get_start_time
        global replace_cards
        global init_deck_and_deal_cards
        global play_war

        get_start_time = self.get_start_time
        replace_cards = self.replace_cards
        init_deck_and_deal_cards = self.init_deck_and_deal_cards
        play_war = self.play_war

class test_time(test_war):
    
    def test_get_start_time(self):
        time = self.get_start_time()
        self.assertIsInstance(time, float)

class test_replace_deck(test_war):
    
    def test_replace_cards(self):
        l = []
        for i in range(30):
            l.append(i)
        
        cards = self.replace_cards(l)
        self.assertTrue(len(cards) == 30)
        self.assertNotEqual(l, cards)

class test_init_hands(test_war):

    def test_init_deck_and_deal_cards(self):
        player_one_deck, player_two_deck = self.init_deck_and_deal_cards()

        player_one_highest_card = -1
        player_two_highest_card = -1

        for card in player_one_deck:
            if card > player_one_highest_card:
                player_one_highest_card = card
        
        for card in player_two_deck:
            if card > player_two_highest_card:
                player_two_highest_card = card

        self.assertEqual(len(player_one_deck), 26)
        self.assertEqual(len(player_two_deck), 26)
        self.assertLess(player_one_highest_card, 13)
        self.assertLess(player_two_highest_card, 13)

class test_war_run(test_war):

    def test_play_war(self):
        list_one = [2, 7, 12]
        list_two = [5, 3, 6]

        list_three = [12, 3, 4, 5, 11, 6]
        list_four = [12, 8, 7, 9, 10, 2]

        list_five = [12, 3, 4, 5, 10, 11, 7]
        list_six = [12, 6, 7, 5, 9, 8, 5]

        win_bit_one, turns = self.play_war(list_one, list_two)
        win_bit_two, turns = self.play_war(list_three, list_four)
        win_bit_three, turns = self.play_war(list_five, list_six)

        self.assertEqual(win_bit_one, 1)
        self.assertEqual(win_bit_two, 2)
        self.assertEqual(win_bit_three, 1)



def main():
    test_classes = [test_time, test_replace_deck, test_init_hands, test_war_run]

    loader = TestLoader()
    suites = []

    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites.append(suite)
        big_suite = TestSuite(suites)
    result = TextTestRunner(verbosity=2).run(big_suite)
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    main()
