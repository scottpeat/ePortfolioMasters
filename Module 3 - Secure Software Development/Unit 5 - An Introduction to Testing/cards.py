"""
Python program to shuffle a deck of cards.

Refactored from the original script (Source: Python Program to Shuffle
Deck of Cards) into three small functions so that the logic can be
unit tested with the unittest framework.
"""

import itertools
import random


def create_deck():
    """Create a standard 52-card deck as a list of (rank, suit) tuples."""
    return list(itertools.product(range(1, 14), ['Spade', 'Heart', 'Diamond', 'Club']))


def shuffle_deck(deck):
    """Shuffle a deck of cards in place and return it."""
    random.shuffle(deck)
    return deck


def draw_cards(deck, number=5):
    """Return the top 'number' cards from the deck."""
    return deck[:number]


if __name__ == '__main__':
    deck = create_deck()
    shuffle_deck(deck)
    hand = draw_cards(deck, 5)

    print("You got:")
    for card in hand:
        print(card[0], "of", card[1])
