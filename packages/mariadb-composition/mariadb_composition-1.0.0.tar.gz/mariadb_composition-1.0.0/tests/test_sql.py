import re
from datetime import date, datetime, time

import pytest

from mariadb_composition import PyFormat, Sql


def test_Composable():
    composable1 = Sql.SQL("SELECT * FROM")
    composable2 = Sql.Identifier("table")
    composed1 = composable1 + composable2
    assert isinstance(composed1, Sql.Composed)
    a1 = "SELECT * FROM `table`"
    assert composed1.as_string() == a1

    q2 = composed1 + Sql.SQL("WHERE")
    a2 = "SELECT * FROM `table` WHERE"
    assert q2.as_string() == a2

    ids = (Sql.Identifier("column1"), Sql.Identifier("column2"))
    pls = Sql.Placeholder() * 2
    pairs = list(map(lambda id, pl: (id + Sql.SQL("=") + pl), ids, pls))
    q3 = Sql.SQL("WHERE") + Sql.SQL(",").join(pairs)
    a3 = "WHERE `column1` = %s , `column2` = %s"
    assert q3.as_string() == a3

    assert not ids[0] == ids[1]
    assert not ids[0] == pls._obj[0]
    assert ids[0] != ids[1]
    assert ids[0] != pls._obj[0]
    assert pls._obj[0] == pls._obj[1]


def test_Composed():
    q1 = Sql.Composed([Sql.SQL("INSERT INTO"), Sql.Identifier("table")])
    a1 = """INSERT INTO `table`"""
    assert q1.as_string() == a1


def test_Composed_repr():
    """
    basicUpdate() creates a pretty complex Composed object. Use that to test
    the __repr__ of most of the underlying types.
    """
    cols = {
        Sql.Identifier("first_name"): "Alvin",
        Sql.Identifier("last_name"): "Smyth",
        Sql.Identifier("id"): 1,
    }
    (query, values) = Sql.basicUpdate(Sql.Identifier("people"), cols)
    a = "Composed([SQL('UPDATE '), Identifier('people'), SQL(' SET '), Composed([Composed([Identifier('first_name'), SQL('='), Placeholder()]), SQL(','), Composed([Identifier('last_name'), SQL('='), Placeholder()])]), SQL(' WHERE '), Composed([Identifier('id'), SQL('='), Placeholder()])])"
    assert repr(query) == a


def test_Composed_join():
    fields = Sql.Identifier("foo") + Sql.Identifier("bar")  # a Composed
    q1 = fields.join(",")
    a1 = """`foo` , `bar`"""
    assert q1.as_string() == a1

    joiner = Sql.SQL(",")
    q2 = fields.join(joiner)
    a2 = a1
    assert q2.as_string() == a2

    # Pass a bad joiner on purpose.
    with pytest.raises(
        TypeError,
        match=re.escape(
            "Composed.join() argument must be str or Sql._SQL, got 3 instead"
        ),
    ):
        fields.join(3)  # type: ignore


def test_SQL():
    q1 = Sql.SQL("SELECT {0} FROM {1}").format(
        Sql.SQL(",").join([Sql.Identifier("foo"), Sql.Identifier("bar")]),
        Sql.Identifier("table"),
    )
    a1 = """SELECT `foo` , `bar` FROM `table`"""
    assert q1.as_string() == a1

    # Pass a bad non-str on purpose.
    with pytest.raises(
        TypeError,
        match=re.escape("SQL values must be strings, got 3 instead"),
    ):
        Sql.SQL(3)  # type: ignore


def test_SQL_as_string():
    q1 = Sql.SQL(", ")
    a1 = ","
    assert q1.as_string() == a1


def test_SQL_format():
    q1 = Sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
        Sql.Identifier("people"), Sql.Identifier("id"), Sql.Placeholder()
    )
    a1 = """SELECT * FROM `people` WHERE `id` = %s"""
    assert q1.as_string() == a1

    q2 = Sql.SQL("SELECT * FROM {tbl} WHERE name = {name}").format(
        tbl=Sql.Identifier("people"), name="O'Rourke"
    )
    a2 = """SELECT * FROM `people` WHERE name = 'O''Rourke'"""
    assert q2.as_string() == a2

    # Can not mix numbered with autonumbered
    with pytest.raises(
        ValueError,
        match=re.escape("cannot switch from automatic field numbering to manual"),
    ):
        Sql.SQL("SELECT * FROM {} WHERE {1}} = {2}").format(
            Sql.Identifier("people"), Sql.Identifier("id"), Sql.Placeholder()
        )

    # Can not mix autonumbered with numbered
    with pytest.raises(
        ValueError,
        match=re.escape("cannot switch from manual field numbering to automatic"),
    ):
        Sql.SQL("SELECT * FROM {0} WHERE {1} = {}").format(
            Sql.Identifier("people"), Sql.Identifier("id"), Sql.Placeholder()
        )

    # Can mix named with numbered
    q3 = Sql.SQL("SELECT * FROM {0} WHERE {1} = {val}").format(
        Sql.Identifier("people"), Sql.Identifier("id"), val=Sql.Placeholder()
    )
    assert q3.as_string() == a1

    # Can mix named with auto numbered
    q4 = Sql.SQL("SELECT * FROM {} WHERE {id} = {}").format(
        Sql.Identifier("people"), Sql.Placeholder(), id=Sql.Identifier("id")
    )
    assert q4.as_string() == a1

    # Can not use format conversions
    with pytest.raises(
        ValueError,
        match=re.escape("no format conversion supported by SQL"),
    ):
        Sql.SQL("SELECT * FROM {0!r} WHERE {1} = {2}").format(
            Sql.Identifier("people"), Sql.Identifier("id"), Sql.Placeholder()
        )

    # Can not use format specifications
    with pytest.raises(
        ValueError,
        match=re.escape("no format specification supported by SQL"),
    ):
        Sql.SQL("SELECT * FROM {0:<20} WHERE {1} = {2}").format(
            Sql.Identifier("people"), Sql.Identifier("id"), Sql.Placeholder()
        )


def test_SQL_join():
    q1 = Sql.SQL(",").join(Sql.Identifier(n) for n in ["foo", "bar", "baz"])
    a1 = "`foo` , `bar` , `baz`"
    assert q1.as_string() == a1


def test_Identifier():
    # Pass a bad non-str on purpose.
    with pytest.raises(
        TypeError,
        match=re.escape("SQL identifier parts must be strings, got 3 instead"),
    ):
        Sql.Identifier(3)  # type: ignore

    # Pass a bad nothing on purpose.
    with pytest.raises(
        TypeError,
        match=re.escape("Identifier cannot be empty"),
    ):
        Sql.Identifier()  # type: ignore

    ids = [
        Sql.Identifier("foo"),
        Sql.Identifier("ba'r"),
        Sql.Identifier('ba"z'),
        Sql.Identifier("bu`z"),
    ]
    q1 = Sql.SQL(",").join(ids)
    a1 = """`foo` , `ba'r` , `ba"z` , `bu``z`"""
    assert q1.as_string() == a1

    q2 = Sql.SQL("SELECT {} FROM {}").format(
        Sql.Identifier("table", "field"), Sql.Identifier("schema", "table")
    )
    a2 = """SELECT `table`.`field` FROM `schema`.`table`"""
    assert q2.as_string() == a2


def test_Literal():
    lits = [
        Sql.Literal("fo'o"),
        Sql.Literal(42),
        Sql.Literal(42.10),
        Sql.Literal(date(2000, 1, 1)),
        Sql.Literal(time(13, 14, 15, 16)),
        Sql.Literal(datetime(2000, 1, 1, 13, 14, 15, 16)),
    ]
    assert (
        (Sql.SQL(", ").join(lits).as_string())
        == "'fo''o' , 42 , 42.1 , DATE '2000-01-01' , TIME '13:14:15.000016' , DATETIME '2000-01-01 13:14:15.000016'"
    )


def test_Placeholder():
    # Pass a bad non-str name on purpose.
    with pytest.raises(
        TypeError,
        match=re.escape("expected string as name, got 3"),
    ):
        Sql.Placeholder(3)  # type: ignore

    # Pass a disallowed ')' on purpose.
    with pytest.raises(
        ValueError,
        match=re.escape("')' not allowed. Invalid name: '(badname)'"),
    ):
        Sql.Placeholder("(badname)")

    # Pass a string that isn't a string of PyFormat.
    with pytest.raises(
        ValueError,
        match=re.escape("'str' is not a valid PyFormat"),
    ):
        Sql.Placeholder("goodname", "str")

    # Pass a bad non-str format on purpose.
    with pytest.raises(
        TypeError,
        match=re.escape("expected PyFormat as format, got 'int'"),
    ):
        Sql.Placeholder("goodname", 3)  # type: ignore

    pl1 = Sql.Placeholder("goodname", "t")
    pl2 = Sql.Placeholder("goodname", PyFormat.TEXT)
    assert pl1 == pl2

    names = ["foo", "bar", "baz"]

    q1 = Sql.SQL("INSERT INTO my_table ({}) VALUES ({})").format(
        Sql.SQL(",").join(map(Sql.Identifier, names)),
        Sql.SQL(",").join(Sql.Placeholder() * len(names)),
    )
    a1 = """INSERT INTO my_table ( `foo` , `bar` , `baz` ) VALUES ( %s , %s , %s )"""
    assert (q1.as_string()) == a1

    q2 = Sql.SQL("INSERT INTO my_table ({}) VALUES ({})").format(
        Sql.SQL(", ").join(map(Sql.Identifier, names)),
        Sql.SQL(", ").join(map(Sql.Placeholder, names)),
    )
    a2 = """INSERT INTO my_table ( `foo` , `bar` , `baz` ) VALUES ( %(foo)s , %(bar)s , %(baz)s )"""
    assert (q2.as_string()) == a2


def test_Placeholder_repr():
    pl1 = Sql.Placeholder("goodname")
    a1 = "Placeholder('goodname')"
    assert repr(pl1) == a1

    pl2 = Sql.Placeholder("goodname", PyFormat.TEXT)
    a2 = "Placeholder('goodname', format=TEXT)"
    assert repr(pl2) == a2


def test_foreignKey():
    q1 = Sql.foreignKey(
        Sql.Identifier("id"),
        Sql.Identifier("col"),
        Sql.Identifier("ftable"),
        Sql.Identifier("fcol"),
        Sql.SQL("on delete set null"),
    )
    a1 = "CONSTRAINT `id` FOREIGN KEY ( `col` ) REFERENCES `ftable` ( `fcol` ) on delete set null"
    assert q1.as_string() == a1


def test_createTable():
    defs = (
        Sql.Identifier("id") + Sql.SQL("INT") + Sql.PRIMARY,
        Sql.Identifier("text") + Sql.SQL("TEXT") + Sql.NULL,
    )
    q1 = Sql.createTable(Sql.Identifier("table"), defs)
    a1 = (
        "CREATE TABLE IF NOT EXISTS `table` ( `id` INT PRIMARY KEY , `text` TEXT NULL )"
    )
    assert q1.as_string() == a1


def test_basicInsert():
    cols = {
        Sql.Identifier("first_name"): "Alice",
        Sql.Identifier("last_name"): "Smith",
    }
    (query, values) = Sql.basicInsert(Sql.Identifier("people"), cols)
    a = "INSERT INTO `people` ( `first_name` , `last_name` ) VALUES ( %s , %s )"
    assert (query.as_string()) == a
    assert values == ["Alice", "Smith"]


def test_basicUpdate():
    cols = {
        Sql.Identifier("first_name"): "Alvin",
        Sql.Identifier("last_name"): "Smyth",
        Sql.Identifier("id"): 1,
    }
    (query, values) = Sql.basicUpdate(Sql.Identifier("people"), cols)
    a = "UPDATE `people` SET `first_name` = %s , `last_name` = %s WHERE `id` = %s"
    assert (query.as_string()) == a
    assert values == ["Alvin", "Smyth", 1]
