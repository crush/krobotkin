from dataclasses import dataclass
import sqlite3 as sqlite
import typing as t_

import krobotkin.polls as polls


# Identifier tagging a data structure within the database.
Entity = int

# A functional interface that can store a Poll in the database.
StorePollI = t_.Callable[[Entity, polls.Poll], Entity]

# A functional interface that can retrieve a Poll from the database.
FetchPollI = t_.Callable[[Entity], t_.Optional[polls.Poll]]

# A functional interface that can delete a Poll from the database.
DeletePollI = t_.Callable[[Entity, polls.Poll], Entity]

# An entity with a special ID indicating 'not a valid entity yet.'
NULL = Entity(-1)


@dataclass
class Query:
    '''Identifiers for each query supported.
    '''

    CREATE_TABLE = 0
    CREATE_POLL = 1
    CREATE_OPTION = 2
    CREATE_VOTE = 3
    GET_POLL = 4
    GET_OPTIONS = 5
    GET_VOTES = 6
    DELETE_POLL = 7
    DELETE_OPTION = 8
    DELETE_VOTE = 9


def store_fn(cursor: sqlite.Cursor) -> StorePollI:
    '''Produces a closure over a SQLite3 database cursor that, when invoked,
    will insert the provided Poll into the database.
    '''
    
    def store(ent: Entity, poll: polls.Poll) -> Entity:
        if ent == NULL:
            return _create_new_poll(cursor, poll)

        return _update_poll(cursor, ent, poll)

    return store


def fetch_fn(cursor: sqlite.Cursor) -> FetchPollI:
    '''Produces a closure over a SQLite3 database cursor that, when invoked,
    will retrieve the Poll entity specified from the database.
    '''

    def fetch(ent: Entity) -> t_.Optional[polls.Poll]:
        return _retrieve_poll(cursor, ent)


    return fetch


def delete_fn(cursor: sqlite.Cursor) -> DeletePollI:
    '''Produces a closure over a SQLite3 database cursor that, when invoked,
    will delete a poll and everything associated with it from the database.
    '''

    def delete(ent: Entity, poll: polls.Poll) -> Entity:
        return _delete_poll(cursor, ent, poll)


    return delete


def _create_new_poll(cursor: sqlite.Cursor, poll: polls.Poll) -> Entity:
    cursor.execute(_q(Query.CREATE_POLL), (poll.question,))
    (poll_id,) = cursor.fetchone()

    for index, opt_txt in enumerate(poll.options):
        cursor.execute(_q(Query.CREATE_OPTION), (poll_id, index, opt_txt))

    return poll_id


def _update_poll(cursor: sqlite.Cursor, e: Entity, poll: polls.Poll) -> Entity:
    old_poll = _retrieve_poll(cursor, e)

    votes_to_delete = [v for v in old_poll.votes if v not in poll.votes]

    votes_to_create = [v for v in poll.votes if v not in old_poll.votes]

    for vote in votes_to_delete:
        cursor.execute(_q(Query.DELETE_VOTE), (e, vote.voter))

    for vote in votes_to_create:
        params = (e, vote.voter, vote.score, vote.option_index)
        cursor.execute(_q(Query.CREATE_VOTE), params)

    return e

def _retrieve_poll(cursor: sqlite.Cursor, ent: Entity) -> t_.Optional[polls.Poll]:
    cursor.execute(q_(Query.GET_QUESTIONS), (ent,))

    options = sorted([
        (index, option)
        for (_, index, option) in cursor.fetchall()
    ])

    cursor.execute(q_(Query.GET_VOTES), (ent,))

    votes = [
        (voter, score, option_index)
        for (_, voter, score, option_index) in cursor.fetchall()
    ]

    cursor.execute(q_(Query.GET_POLL), (ent,))

    (question,) = cursor.fetchone()

    return polls.Poll(
        question,
        [option[1] for option in option],
        votes)


def _delete_poll(cursor: sqlite.Cursor, e: Entity, poll: polls.Poll) -> Entity:
    for vote in poll.votes:
        cursor.execute(q_(Query.DELETE_VOTE), (e, vote.voter))

    for option in poll.options:
        cursor.execute(q_(Query.DELETE_OPTION), (e, option))

    cursor.execute(q_(Query.DELETE_POLL), (e,))

    return e


def _q(id_: Query) -> t_.Optional[str]:
    '''Given a query's identifier, retrieve the corresponding SQL as a string.
    '''
    
    QUERIES = {
        Query.CREATE_TABLES: '''
        create table if not exists polls (
            id integer primary key,
            created text not null,
            question text not null,
        );

        create table if not exists poll_options (
            id integer primary key,
            poll_id integer,
            index integer not null,
            option text not null,
            foreign key (poll_id) references polls (id)
        );

        create table if not exists votes (
            id integer primary key,
            poll_id integer,
            voter text not null,
            score integer not null,
            option_index integer not null
        );
        ''',
        
        Query.CREATE_POLL: '''
        insert into polls (created, question)
        values ('now', ?)
        returning id;
        ''',

        Query.CREATE_OPTION: '''
        insert into poll_options (poll_id, index, option)
        values (?, ?, ?)
        returning id;
        ''',

        Query.CREATE_VOTE: '''
        insert into votes (poll_id, voter, score, option_index)
        values (?, ?, ?, ?)
        returning id;
        ''',

        Query.GET_POLL: '''
        select question
        from polls
        where id = ?;
        ''',

        Query.GET_OPTIONS: '''
        select id, index, option
        from poll_options
        where poll_id = ?;
        ''',

        Query.GET_VOTES: '''
        select id, voter, score, option_index
        from votes
        where poll_id = ?;
        ''',

        Query.DELETE_POLL: '''
        delete from polls
        where id = ?;
        ''',

        Query.DELETE_OPTION: '''
        delete from poll_options
        where poll_id = ? and option = ?;
        ''',

        Query.DELETE_VOTE: '''
        delete from votes
        where poll_id = ? and voter = ?;
        '''
    }

    return QUERIES.get(id_)
