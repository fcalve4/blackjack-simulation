import unittest
from main import BlackjackSimulation




class TestBlackjackSimulation(unittest.TestCase):

    def setUp(self):
        # This method is run before each test
        self.game = BlackjackSimulation()

    def test_calculate_hand_total_soft_hand(self):
        # Test calculation of a soft hand
        hand = ['A', 6]  # Ace and 6
        total, type0 = self.game.calculate_hand_total(hand)
        self.assertEqual(total, 17)
        self.assertEqual(type0, 'soft')
        
        hand = ['A', 6, 'A']  # Ace, 6, and another Ace
        total, type0 = self.game.calculate_hand_total(hand)
        self.assertEqual(total, 18)  # One Ace as 11, the other as 1
        self.assertEqual(type0, 'soft')

    def test_calculate_hand_total_hard_hand(self):
        # Test calculation of a hard hand
        hand = [10, 6, 5]  # 10, 6, and 5
        total, type0 = self.game.calculate_hand_total(hand)
        self.assertEqual(total, 21)
        self.assertEqual(type0, 'hard')

    def test_check_for_blackjack(self):
        # Test detection of blackjack
        player_hand = ['A', 10]
        dealer_hand = ['A', 9]
        player_natural, dealer_natural = self.game.check_for_blackjack(player_hand, dealer_hand)
        self.assertTrue(player_natural)
        self.assertFalse(dealer_natural)

    def test_is_hand_splittable(self):
        # Test if a hand is splittable
        hand = [8, 8]  # Two cards of the same rank
        self.assertTrue(self.game.is_hand_splittable(hand))

        hand = [8, 9]  # Different rank cards
        self.assertFalse(self.game.is_hand_splittable(hand))

    def test_is_hand_doublable(self):
        # Test if a hand is doublable
        hand = [5, 6]
        self.assertTrue(self.game.is_hand_doublable(hand))

        hand = [5, 6, 2]
        self.assertFalse(self.game.is_hand_doublable(hand))

    def test_dealer_logic(self):
        # Test dealer's behavior based on soft 17 rule
        shoe = self.game.deck * self.game.num_decks
        dealer_hand = [7, 'A']  # Initial soft 18
        dealer_total = self.game.dealer_logic(shoe, dealer_hand)
        self.assertGreaterEqual(dealer_total, 17)
        self.assertLessEqual(dealer_total, 21)  # Should not bust









    def test_play_hand_with_logic(self):

        shoe = [10, 10, 10, 10, 10, 10]

        player_hand = [8, 8]
        dealer_hand = [4, 3]

        number = self.game.play_hand_with_logic(shoe, player_hand, dealer_hand)
        self.assertEqual(number, 20)

    def test_play_hand_with_logic1(self):

        shoe = [10, 10, 10, 10, 10, 10]

        player_hand = ['A', 'A']
        dealer_hand = [4, 3]

        number = self.game.play_hand_with_logic(shoe, player_hand, dealer_hand)
        self.assertEqual(number, 30)

    def test_play_hand_with_logic2(self):

        shoe = [10, 10, 10, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]

        player_hand = [5, 5]
        dealer_hand = ['A', 6]

        number = self.game.play_hand_with_logic(shoe, player_hand, dealer_hand)
        self.assertEqual(number, 10)

if __name__ == '__main__':
    unittest.main()