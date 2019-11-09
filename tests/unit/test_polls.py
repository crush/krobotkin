from krobotkin import polls

def test_vote_score():
    p1 = polls.Poll('testing', ['test1'], [])

    p2 = polls.Poll(
        'testing',
        ['test1', 'test2'],
        [polls.Vote('tester', 2, 1)])

    assert polls.vote_score(p1, 'tester') == 1
    assert polls.vote_score(p2, 'tester') == 1


def test_try_vote():
    p1 = polls.Poll('testing', ['test1', 'test2'], [])

    p2 = polls.Poll(
        'testing',
        ['test1', 'test2'],
        [polls.Vote('tester', 2, 1)])

    v1 = polls.try_vote(p1, 'tester', 0)
    v2 = polls.try_vote(p2, 'tester', 1)
    v3 = polls.try_vote(p2, 'tester', 0)

    assert v1 is not None and v1.score == 2
    assert v2 is None
    assert v3 is not None and v3.score == 1


def test_subit_vote():
    p1 = polls.Poll('testing', ['test1', 'test2'], [])

    v1 = polls.Vote('tester', 2, 0)

    p2 = polls.submit_vote(p1, v1)

    assert len(p1.votes) == 0
    assert len(p2.votes) == 1


def test_retract_vote():
    p1 = polls.Poll(
        'testing',
        ['test1', 'test2'],
        [polls.Vote('tester', 2, 1)])

    p2 = polls.retract_vote(p1, 'tester', 1)

    assert len(p1.votes) == 1
    assert len(p2.votes) == 0


def test_tally_results():
    p1 = polls.Poll('testing', ['test1', 'test2'], [])

    p2 = polls.Poll(
        'testing',
        ['test1', 'test2'],
        [polls.Vote('tester', 2, 1)])

    r1 = polls.tally_results(p1)
    r2 = polls.tally_results(p2)

    assert r1.results['test1'] == 0
    assert r1.results['test2'] == 0
    
    assert r2.results['test1'] == 0
    assert r2.results['test2'] == 2
