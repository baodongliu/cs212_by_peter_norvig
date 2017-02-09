#!/usr/bin/env python3
'''\
This is the notes from CS 212 instructed by Peter Norvig in udacity
It is hard, but it is fun hard.
'''
import random


# ====================================================================
# Write a function to summarize the ∑x²
# ====================================================================
def ss_bad(nums):
    '''\
    This is the rookie way to define a function and get the total
    This is sequential style
    '''
    total = 0
    for i in range(len(nums)):
        total += nums[i] * nums[i]

    return total


print(ss_bad([1, 2, 3, 4, 5]))


def ss_good(nums):
    '''\
    This is a better way to define a function and get the total
    This is based on functional style
    '''
    return sum(x**2 for x in nums)


print(ss_good([1, 2, 3, 4, 5]))


# =============================================================================
# Write a poker program
# ?? --------> Problem --------> Specs --------> Code
#   Understand         Spefify          Design
#
# First, Make an inventory of concepts that we're going to have to deal with
# 1. Understand
#       Notion of hands
#       A hand consists of 5 cards
#       A Card has a rank and suit
# 2.Specify
#       Pokers(hands) --------> hand
#       hand rank:
#           n-kind
#           straight
#           flush
# Representing Hands
# ['JS', 'JD', '2S', '2C', '7H'], use list, good
# [(11, 's'), (11, 'D'), (2, 'S'), (2, 'C'), (7, 'H')], use list of tuple, good
# set(['JS', 'JD', '2S', '2C', '7H']), use set, problems with more than one set
#                                      of playing cards
# 'JS JD 2S 2C 7H', use string, need split command to parse the string
# =============================================================================


# =============================================================================
# Quniz: Understanding max
# =============================================================================
print(max([3, 4, 5, 0]), max([3, 4, -5, 0], key=abs))


def poker(hands):
    'Return the best hand: poker([hand, ...]) => [hand, ...]'
    # return max(hands, key=hand_rank)
    # Just return max, only one hand can be returned.
    # It won't handle the suituation, where there is a tie.
    # Introduce a new function, called allmax to return a list of max values
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    'Return a list of all items equal to the max of the iterable'
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result


def hand_rank(hand):
    # =========================================================================
    # There are 9 different types of hands that we know about, from straight
    # flush at the top to high card at the bottom, and we number them from, say
    # 0 to 8, with 8 being the highest for the straight flush.
    # =========================================================================
    # ranks = card_ranks(hand)
    # if straight(ranks) and flush(hand):
    #     return 8
    # elif kind(4, ranks):
    #     return 7
    # elif ...
    # Will this work?
    # A. Yes
    # B. No, errors.
    # C. No, some wrong
    # D. No, all wrong
    # The above solution will work for most cases, but it doesn't work for all
    # the cases.
    # For example
    #   10, 10, ...  ==> rank: 1
    #   9, 9, ...    ==> rank: 1
    # But we know that we want the pair of 10s to outrank the pair of 9s, so
    # we've got to come up with some way to make that comparison, so that
    # we're able to distinguish between 2 rankings that are the same in terms
    # of what they're called.
    # It looks like that means that we're going to have to use something more
    # complicated than just this ranking from 0 to 8.
    # I'm going to propose a couple possibilities.
    # One possibility would be to continue to return integers but to use bigger
    # ones. So let's take an example of what we want to compare.
    # Let's say we have 2 hands that are 4 of a kind.
    # One has four 9s and a 5, and the other one has four 3s and a 2.
    # 99995 <=== should be higer
    # 33332 <=== should be lower
    # Under the old formulation, they would both be ranked as a 7
    # because 7 is the rank for 4 of a kind.
    # So if we want to change that to use a different type of result,
    # we could use integers and we could say,
    # let's say, 70905 and 70302,
    # so the 9 and the 5 to represent that this is 4 of a kind of 9s with a 5
    # left over and the 3 and the 2 to say it's 4 of a kind of 3s with a 2
    # left over. We could use real numbers. We could say 7.0905 or 7.0302.
    # Another possibility is we could use tuples.
    # We could use 7, 9, 5 versus 7, 3, 2.
    # A tuple is just like a list, except it can't be modified and it has a
    # slightly different set of operations associated with it.
    # But basically, it just means a grouping of 3 values in this case.
    # What I want you to tell me is out of these 3 possibilities,
    # which one of them would work at all
    # and which one of them seems best in terms of being most convenient
    # and easy to work with within our program?
    # int       70905       70302           # work
    # real      7.0905      7.0302          # work
    # tuples    (7, 9, 5)   (7, 3, 2)       # work and best
    # (7, 9, 5) > (7, 3, 2)

    # Stright flush, Jack high (J, 10, 9, 8, 7)     => (8, 11)
    # Four aces and a queen kicker (A, A, A, A, Q)  => (7, 14, 12)
    # Full house, eight over kings (8, 8, 8, K, K)  => (6, 8, 13)
    # Flush, 10-8 (10, 8, 7, 5, 3)                  => (5, [10, 8, 7, 5, 3])
    # Straight, Jack high (J, 10, 9, 8, 7)          => (4, 11)
    # Three Sevens (7, 7, 7, 5, 2)                  => (3, 7, [7, 7, 7, 5, 2])
    # Two pairs, (J, J, 3, 3, K)             => (2, 11, 3, [13, 11, 11, 3, 3])
    # Pair of twos, Jack High (2, 2, J, 6, 3)=> (1, 2, [11, 6, 3, 2, 2])
    # Got nothing (7, 5, 4, 3, 2)            => (0, 7, 5, 4, 3, 2)

    # ranks = card_ranks(hand)

    # if straight(ranks) and flush(hand):
    #     return (8, max(ranks))  # 2 3 4 5 6 => (8, 6) 6 7 8 9 10  => (8, 10)
    # elif kind(4, ranks):
    #     return (7, kind(4, ranks), kind(1, ranks))
    # elif kind(3, ranks) and kind(2, ranks):
    #     return (6, kind(3, ranks), kind(2, ranks))
    # elif flush(hand):
    #     return (5, ranks)
    # elif straight(ranks):
    #     return (4, max(ranks))
    # elif kind(3, ranks):
    #     return (3, kind(3, ranks), ranks)
    # elif two_pair(ranks):
    #     return (2, two_pair(ranks), ranks)
    # elif kind(2, ranks):
    #     return (1, kind(2, ranks), ranks)
    # else:
    #     return (0, ranks)

    # The above representation is OK. But we repreat ourself, like:
    # elif kind(3, ranks) and kind(2, ranks):
    #     return (6, kind(3, ranks), kind(2, ranks))
    # kind(3, ranks) and kind(2, ranks) are repreated.
    # It voilate the rule of DRY: Don't Repeat Yourself.
    # We need to refactor the program here.
    # Refactoring doesn't change the program functionality but increase the elegance

    # counts is the count of each rank; rank lists corresponding ranks.
    # E.g. '7 T 7 9 7' => counts = [3, 1, 1]; ranks = [7, 10, 9]
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])

    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)

    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1

    # return (9 if (5,) == counts else
    #         8 if straight and flush else
    #         7 if (4, 1) == counts else
    #         6 if (3, 2) == counts else
    #         5 if flush else
    #         4 if straight else
    #         3 if (3, 1, 1) == counts else
    #         2 if (2, 2, 1) == counts else
    #         1 if (2, 1, 1, 1) == counts else
    #         0), ranks

    # The above return statement is not so pretty. Refactor it.
    # Define a lookup table
    # 3 * straight + 5 * flush, use bool to int conversion
    count_rankings = {(5,): 9, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3,
                      (2, 2, 1): 2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}

    return max(count_rankings[counts], 3 * straight + 5 * flush), ranks


def group(items):
    "Return a lit of [(count, x)...], highest count firsts, then highest x first."
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)


def unzip(pairs):
    return zip(*pairs)


def card_ranks(hand):
    'Return a list of ranks, sorted by with higher first'
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse=True)
    # return ranks
    # By just returning ranks, it will fail in hand: AS 2S 3C 4C 5D
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks


def straight(ranks):
    'Return True if the ordered ranks form a 5-card straight'
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5


def flush(hand):
    ' return true if all the cards have the same suit.'
    suits = [s for r, s in hand]
    return len(set(suits)) == 1


def kind(n, ranks):
    '''\
    Return the first rank that this hand has exactly n of
    Return None if there no n-of-kind in the hand.
    '''
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


def two_pair(ranks):
    '''\
    If there are two pair, return the two ranks as a tuple: (highest, lowest);
    Otherwise return None.
    '''
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))

    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None


# =============================================================================
# It is important that each part of the specificatin of the spcification gets
# turned into a piece of code that implements it and a test that tests it.
# If you don't have tests like these, then you don't know when you're done,
# and you won't know if you've done it right and you won't have confidence that
# any future changes might not be breaking something. So remember, to be a good
# programmer, you must be a good tester. Write your test cases and test them
# often.
# One important principle of testing is to do extreme values.
# =============================================================================
def test():
    'Test cases for the functions in poker program.'
    sf = '6C 7C 8C 9C TC'.split()       # Straight flush
    fk = '9D 9H 9S 9C 7D'.split()       # four-kind
    fh = 'TD TC TH 7C 7D'.split()       # full house
    tp = '5S 5D 9H 9C 6S'.split()       # two pairs
    s1 = 'AS 2S 3S 4S 5C'.split()       # A-5 Straight
    s2 = '2C 3C 4C 5S 6S'.split()       # 2-6 Straight
    ah = 'AS 2S 3S 4S 6C'.split()       # A high
    sh = '2S 3S 4S 6C 7D'.split()       # 7 high

    assert poker([s1, ah, sh]) == [s1]
    assert poker([s1, s2, ah, sh]) == [s2]

    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)

    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) is None
    assert kind(2, fkranks) is None
    assert kind(1, fkranks) == 7
    assert two_pair(fkranks) is None
    assert two_pair(tpranks) == (9, 5)

    # Python 2 can use statement == True or == False
    # But in python 3, statement is True or is False
    # assert straight([9, 8, 7, 6, 5]) == True
    # assert straight([9, 8, 8, 6, 5]) == False

    # assert flush(sf) == True
    # assert flush(fk) == False

    assert straight([9, 8, 7, 6, 5]) is True
    assert straight([9, 8, 8, 6, 5]) is False

    assert flush(sf) is True
    assert flush(fk) is False

    # assert card_ranks returns correct ranks
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert poker([sf, fk, fh]) == [sf]
    # Add 2 new assert statements here.
    # The first should check that when fk plays fh, fk is the winner.
    # The second should confirm that fh playing against fh return fh and fh as tie.
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]

    # Add 2 new assert statements here.
    # The first should assert that when poker is called with a single hand, it
    # returns that hand.
    # The second should check of the case of 100 hands.
    assert poker([sf]) == [sf]
    assert poker([sf] + 99 * [fh]) == [sf]

    # Add 3 new assert statements here.
    # To make sure the hand_rank return correct hands
    assert hand_rank(sf) == (8, (10, 9, 8, 7, 6))
    assert hand_rank(fk) == (7, (9, 7))
    assert hand_rank(fh) == (6, (10, 7))

    return 'tests pass'


print(test())


def deal(num_of_hands, n=5, deck=[r + s for r in '23456789TJQKA' for s in 'SHDC']):
    'Shuffle the deck and deal out num_of_hands n-card hands.'
    random.shuffle(deck)
    return [deck[n * i:n * (i + 1)] for i in range(num_of_hands)]


print(deal(2, 7))


# =============================================================================
# Wikipedia: Poker hand probability:
#    5 of a Kind:  0.0010%
# Straight Flush:  0.0015%
#    4 of a Kind:  0.024 %
#     Full House:  0.140 %
#          Flush:  0.196 %
#       Straight:  0.401 %
#    3 of a kind:  2.11  %
#         2 Pair:  4.75  %
#           Pair: 42.25  %
#      High Card: 50.11  %
#
# Random Deal %
#   52?                 1/card
#   50,000              1000/card
#   700,000             10/least_common_rank
#   52!                 one each
# =============================================================================
def hand_percentages(n=700 * 1000):
    'Sample n random hands and print a table of percentages for each type of hand.'
    hand_names = ['High Card', 'Pair', '2 Pair', '3 of a Kind', '3 of a Kind',
                  'Flush', 'Full House', '4 of a Kind', 'Straight Flush', '5 of a Kind']
    counts = [0] * 10
    for i in range(n // 10):
        for hand in deal(10, n=5, deck=[r + s for r in '23456789TJQKA' for s in 'SHDC'] * 2):
            ranking = hand_rank(hand)[0]
            print(ranking)
            counts[ranking] += 1

    for i in reversed(range(10)):
        print('{:>14s}: {:6.3f} %'.format(hand_names[i], 100. * counts[i] / n))


# hand_percentages()


# =============================================================================
# Lesson1: Summary
# Understand
# Define pieces
# Reuse
# Test
# Explore:
#       correctness
#       efficiency
#       elegance
#       features
# =============================================================================


# =============================================================================
# Bad Shuffle
# =============================================================================
def suffle1(deck):
    "A bad shuffle's algorithm."
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        swap(deck, i, j)


def swap(deck, i, j):
    "Swap elements i and j of a collection."
    print('Swap', i, j)
    deck[i], deck[j] = deck[j], deck[i]
