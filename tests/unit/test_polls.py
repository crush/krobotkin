from krobotkin import polls

def test_vote_score():
    p1 = polls.Poll('testing', ['test1'], [])

    p2 = polls.Poll(
        'testing',
        ['test1', 'test2'],
        [polls.Vote('tester', 2, 1)])

    assert polls.vote_score(p1, 'tester') == 1
    assert polls.vote_score(p2, 'tester') == 1
