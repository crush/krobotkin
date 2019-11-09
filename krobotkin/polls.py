from dataclasses import dataclass
import typing as t_


@dataclass
class Vote:
    '''Indicates a vote submitted to a poll.
    Votes are scored by the rank order they are submitted in.
    '''

    voter: str
    score: int
    option_index: int


@dataclass
class Poll:
    '''A ranked voting poll.
    '''

    question: str
    options: t_.List[str]
    votes: t_.List[Vote]


@dataclass
class Tally:
    '''A tally of the votes submitted to a poll.
    The results are a dictionary mapping options to the total score of the
    votes accumulated.
    '''

    question: str
    results: t_.Dict[str, int]


def vote_score(poll: Poll, voter: str) -> int:
    '''Compute the score to assign to the next vote that would be submitted by
    a particular voter on a given poll.
    '''

    votes_submitted = len([v for v in poll.votes if v.voter == voter])

    return len(poll.options) - votes_submitted


def try_vote(p: Poll, voter: str, opt_index: int) -> t_.Optional[Vote]:
    '''Create a vote for a poll.
    Returns a new vote if and only if the voter has not already voted for the
    provided option, otherwise returns None.
    '''

    if any(v.voter == voter and v.option_index == opt_index for v in p.votes):
        return None

    score = vote_score(p, voter)

    return Vote(voter, score, opt_index)


def submit_vote(p: Poll, v: Vote) -> Poll:
    '''Update a poll by adding a new vote to it.
    '''

    return Poll(p.question, p.options, p.votes + [v])


def retract_vote(p: Poll, voter: str, opt_index: int) -> Poll:
    '''Remove a vote cast by a particular voter for a given option,
    returning an updated poll.
    '''

    ind = [
        i
        for i in range(len(p.votes))
        if p.votes[i].voter == voter and p.votes[i].option_index == opt_index
    ]

    if len(ind) == 0:
        return p

    i = ind[0]

    return Poll(p.question, p.options, p.votes[:i] + p.votes[i + 1:])


def tally_results(p: Poll) -> Tally:
    '''Tally up the scores from all the votes for a poll.
    '''

    results = {opt: 0 for opt in p.options}

    for vote in p.votes:
        q = p.options[vote.option_index]
        results[q] += vote.score

    return Tally(p.question, results)
