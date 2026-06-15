# Unit 5: An Introduction to Testing – Unit Testing Activity

## Overview

This activity forms part of Unit 5 of my ePortfolio. It looks at automated testing using Python's `unittest` framework, and applies it to a small piece of existing code (a deck-of-cards shuffler), demonstrating how unit tests can be written for code that wasn't originally designed with testing in mind.

## Automated Testing: Key Concepts

Unit tests support the automated examination of code. Automation allows a complex process of checking code capability to be carried out quickly, repeatedly, and with far less risk of human error than manual testing.

There are three main types of automated testing:

- **Unit tests** – test small, specific units of functionality in isolation (e.g. a single function).
- **Functional/integration tests** – explore functional paths through the code, checking that components work correctly together.
- **Regression tests** – ensure that the behaviour and output of a program has not changed unexpectedly after additions or changes have been made.

### `unittest` Building Blocks

- **Test fixture** – the setup work needed before one or more tests can run, such as creating a database connection or starting a server.
- **Test case** – an individual unit of testing, checking the result for a particular set of inputs.
- **Test suite** – a collection of test cases (and/or other test suites) that are run together.
- **Test runner** – manages the execution of tests and presents the results to the user.

Tests are written as methods whose names start with `test`, and use assertion methods such as `assertEqual()`, `assertTrue()`, `assertFalse()`, and `assertRaises()` to check expected outcomes.

## The Original Code

The starting point for this activity was the following script, which builds a 52-card deck, shuffles it, and prints five cards:

```python
# Python program to shuffle a deck of card
# importing modules
import itertools, random
# make a deck of cards
deck = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))
# shuffle the cards
random.shuffle(deck)
# draw five cards
print("You got:")
for i in range(5):
   print(deck[i][0], "of", deck[i][1])
```

*Source: Python Program to Shuffle Deck of Cards.*

## Refactoring for Testability

This script runs immediately when executed and produces output via `print()`, which makes it difficult to test directly — there's nothing to call from a test, and no return value to check. Before unit tests could be written, the script was refactored into three small functions, **without changing its underlying logic**:

```python
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
```

This refactoring is itself a small example of reducing complexity: each function now has a single, clear responsibility (`create_deck`, `shuffle_deck`, `draw_cards`), each can be reasoned about independently, and each returns a value that a test can check.

## Unit Tests

The following tests were written using `unittest`, following the same pattern as the `TestStringMethods` example provided in the activity brief:

```python
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
```

Running `python -m unittest test_cards.py -v` executes all nine test cases successfully:

```
test_deck_contains_all_four_suits ... ok
test_deck_contains_ranks_one_to_thirteen ... ok
test_deck_has_52_cards ... ok
test_deck_has_no_duplicate_cards ... ok
test_draw_cards_default_is_five ... ok
test_draw_cards_returns_requested_number ... ok
test_draw_cards_returns_top_of_deck ... ok
test_draw_cards_with_non_integer_raises_typeerror ... ok
test_shuffle_returns_same_cards_in_different_order ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.005s

OK
```

## Reflection

Writing these tests highlighted a few things for me:

- **Testing randomness requires care.** `shuffle_deck` relies on `random.shuffle`, so a test cannot check for one specific output order. Instead, the test checks an *invariant* — that the deck still contains exactly the same 52 cards after shuffling, just in a different arrangement. This is a useful general lesson: when a function's exact output can't be predicted, test the properties that must always hold true regardless of the random outcome.
- **Refactoring and testing go hand in hand.** The original script couldn't be unit tested at all in its original form. Splitting it into small, single-purpose functions was a small step that directly reduced complexity (each function is now easy to read and reason about on its own) and, at the same time, made the code testable. This links back to the earlier complexity activity — improving testability and reducing complexity often happen together.
- **Mapping to test types.** Most of the tests above are **unit tests**, each checking one function in isolation (`create_deck`, `shuffle_deck`, `draw_cards`). If this code were extended — for example, into a full card game — **integration tests** would check that these functions work correctly together (e.g. that a full game loop creates a deck, shuffles it, and deals hands without overlap), and **regression tests** would ensure that future changes (such as adding jokers to the deck) don't break the existing 52-card behaviour for standard games.
- **Edge cases matter.** The `assertRaises` test for `draw_cards(deck, "five")` mirrors the `s.split(2)` example from the activity brief — checking that invalid input produces a sensible, expected error (`TypeError`) rather than an unclear failure further down the line.

## Files in This Activity

- `cards.py` – refactored deck-shuffling code (functions only, no behaviour change from the original)
- `test_cards.py` – unit tests for `cards.py`
