"""
Unit tests for cards.py

Run with:
    python -m unittest test_cards.py
"""

import unittest
from cards import create_deck, shuffle_deck, draw_cards


class TestCardFunctions(unittest.TestCase):

    def test_deck_has_52_cards(self):
        deck = create_deck()
        self.assertEqual(len(deck), 52)

    def test_deck_has_no_duplicate_cards(self):
        deck = create_deck()
        self.assertEqual(len(deck), len(set(deck)))

    def test_deck_contains_all_four_suits(self):
        deck = create_deck()
        suits = {card[1] for card in deck}
        self.assertEqual(suits, {'Spade', 'Heart', 'Diamond', 'Club'})

    def test_deck_contains_ranks_one_to_thirteen(self):
        deck = create_deck()
        ranks = {card[0] for card in deck}
        self.assertEqual(ranks, set(range(1, 14)))

    def test_shuffle_returns_same_cards_in_different_order(self):
        deck = create_deck()
        original_order = deck.copy()

        shuffled = shuffle_deck(deck)

        # Same 52 cards, just reordered
        self.assertEqual(len(shuffled), len(original_order))
        self.assertEqual(set(shuffled), set(original_order))

    def test_draw_cards_returns_requested_number(self):
        deck = create_deck()
        hand = draw_cards(deck, 5)
        self.assertEqual(len(hand), 5)

    def test_draw_cards_returns_top_of_deck(self):
        deck = create_deck()
        hand = draw_cards(deck, 5)
        self.assertEqual(hand, deck[:5])

    def test_draw_cards_default_is_five(self):
        deck = create_deck()
        hand = draw_cards(deck)
        self.assertEqual(len(hand), 5)

    def test_draw_cards_with_non_integer_raises_typeerror(self):
        deck = create_deck()
        with self.assertRaises(TypeError):
            draw_cards(deck, "five")


if __name__ == '__main__':
    unittest.main()
