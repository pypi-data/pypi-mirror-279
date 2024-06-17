import string
from abc import ABC, abstractmethod
from codecs import lookup
from datetime import date, datetime, time
from enum import Enum
from numbers import Number
from typing import (
    Any,
    Iterable,
    Iterator,
    List,
    LiteralString,
    Optional,
    Self,
    Sequence,
    Union,
)


class Escaping:
    """
    Utility object to escape strings for SQL interpolation.
    """

    @classmethod
    def escape_literal(cls, input: Any) -> str:
        """
        Replaces "\\\\" with "\\\\\\\\" and "'" with "'", then surrounds the input with singlequotes.
        """
        if not isinstance(input, str):
            output = Escaping.escape_string(str(input))
        else:
            output = Escaping.escape_string(input)
        if not isinstance(input, Number):
            output = "'" + output + "'"
        if isinstance(input, datetime):
            output = "DATETIME " + output
        elif isinstance(input, date):
            output = "DATE " + output
        elif isinstance(input, time):
            output = "TIME " + output
        return output

    @classmethod
    def escape_identifier(cls, input: str) -> str:
        """
        Replaces "`" with "``", then surrounds the input with backticks.
        """
        output = input
        output = output.replace("`", "``")
        output = "`" + output + "`"
        return output

    @classmethod
    def escape_string(cls, input: str) -> str:
        """
        Replaces "'" with "''" and "\\\\" with "\\\\\\\\".
        """
        output = input
        output = output.replace("'", "''")
        output = output.replace("\\", "\\\\")
        return output


class PyFormat(str, Enum):
    """
    Enum representing the format wanted for a query argument.
    """

    AUTO = "s"
    """Automatically chosen (``%s`` placeholder)."""
    TEXT = "t"
    """Text parameter (``%t`` placeholder)."""
    BINARY = "b"
    """Binary parameter (``%b`` placeholder)."""


class Sql(object):
    """
    SQL String Composition utility module based on the interfaces of psycopg's
    sql.py

    General usage guidance is to
    1. Compose many objects together into a Composed object and
    2. Call <mariadb cursor>.execute(<Composed>.as_string(), <data>)

    Example:

        cols = {
            Sql.Identifier("first_name"): "Alice",
            Sql.Identifier("last_name"): "Smith",
        }
        query = Sql.SQL("INSERT INTO my_table ({headings}) VALUES ({vals})").format(
            headings=Sql.SQL(",").join(cols.keys())),
            vals=Sql.SQL(",").join(Sql.Placeholder() * len(cols.keys())),
        )
        cursor.execute(query, list(cols.values()))

    is the modular, coposed equivalent to:

        query = "INSERT INTO my_table ( `first_name` , `last_name` ) VALUES ( %s , %s )
        values = ["Alice", "Smith"]
        cursor.execute(query, values)

    """

    class Composable(ABC):
        """
        Abstract base class for objects that can be used to compose an SQL string.

        `!Composable` objects can be passed directly to
        `~psycopg.Cursor.execute()`, `~psycopg.Cursor.executemany()`,
        `~psycopg.Cursor.copy()` in place of the query string.

        `!Composable` objects can be joined using the ``+`` operator: the result
        will be a `Composed` instance containing the objects joined. The operator
        ``*`` is also supported with an integer argument: the result is a
        `!Composed` instance containing the left argument repeated as many times as
        requested.
        """

        def __init__(self, obj: Any):
            self._obj = obj

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self._obj!r})"

        @abstractmethod
        def as_bytes(self) -> bytes:
            """
            Return the value of the object as bytes.
            """
            raise NotImplementedError

        def as_string(self) -> str:
            """
            Return the value of the object as string.
            """
            b = self.as_bytes()
            return b.decode()

        def __iter__(self) -> Iterator[Self]:
            raise NotImplementedError

        def __add__(self, other: "Sql.Composable") -> "Sql.Composed":
            if isinstance(other, Sql.Composed):
                return Sql.Composed([self]) + other
            if isinstance(other, Sql.Composable):
                return Sql.Composed([self]) + Sql.Composed([other])
            else:
                return NotImplemented

        def __mul__(self, n: int) -> "Sql.Composed":
            return Sql.Composed([self] * n)

        def __eq__(self, other: Any) -> bool:
            return type(self) is type(other) and self._obj == other._obj

        def __ne__(self, other: Any) -> bool:
            return not self.__eq__(other)

        def __hash__(self) -> int:
            return self._obj.__hash__()

    class Composed(Composable):
        """
        A `Composable` object made of a sequence of `!Composable`.

        The object is usually created using `!Composable` operators and methods.
        However it is possible to create a `!Composed` directly specifying a
        sequence of objects as arguments: if they are not `!Composable` they will
        be wrapped in a `Literal`.

        `!Composed` objects are iterable (so they can be used in `_SQL.join` for
        instance).
        """

        _obj: List["Sql.Composable"]

        def __init__(self, seq: Sequence[Any]):
            seq = [
                obj if isinstance(obj, Sql.Composable) else Sql.Literal(obj)
                for obj in seq
            ]
            super().__init__(seq)

        def as_bytes(self) -> bytes:
            return b" ".join(obj.as_bytes() for obj in self._obj)

        def __iter__(self) -> Iterator["Sql.Composable"]:
            return iter(self._obj)

        def __add__(self, other: "Sql.Composable") -> "Sql.Composed":
            if isinstance(other, Sql.Composed):
                return Sql.Composed(self._obj + other._obj)
            if isinstance(other, Sql.Composable):
                return Sql.Composed(self._obj + [other])
            else:
                return NotImplemented

        def join(self, joiner: Union["Sql.SQL", LiteralString]) -> "Sql.Composed":
            """
            Return a new `!Composed` interposing the `!joiner` with the `!Composed` items.

            The `!joiner` must be an `SQL` or a str which will be interpreted as
            an `SQL`.
            """
            if isinstance(joiner, str):
                joiner = Sql.SQL(joiner)
            elif not isinstance(joiner, Sql.SQL):
                raise TypeError(
                    "Composed.join() argument must be str or Sql._SQL,"
                    f" got {joiner!r} instead"
                )

            return joiner.join(self._obj)

    class SQL(Composable):
        """
        A `Composable` representing a snippet of SQL statement.

        `!SQL` exposes `join()` and `format()` methods useful to create a template
        where to merge variable parts of a query (for instance field or table
        names).

        The `!obj` string doesn't undergo any form of escaping, so it is not
        suitable to represent variable identifiers or values: you should only use
        it to pass constant strings representing templates or snippets of SQL
        statements; use other objects such as `Identifier` or `Literal` to
        represent variable parts.
        """

        _obj: LiteralString
        _formatter = string.Formatter()

        def __init__(self, obj: LiteralString):
            super().__init__(obj)
            if not isinstance(obj, str):
                raise TypeError(f"SQL values must be strings, got {obj!r} instead")

        def as_string(self) -> str:
            return self._obj.strip()

        def as_bytes(self) -> bytes:
            return self._obj.strip().encode()

        def format(self, *args: Any, **kwargs: Any) -> "Sql.Composed":
            """
            Merge `Composable` objects into a template.

            :param args: parameters to replace to numbered (``{0}``, ``{1}``) or
                auto-numbered (``{}``) placeholders
            :param kwargs: parameters to replace to named (``{name}``) placeholders

            The method is similar to the Python `str.format()` method: the string
            template supports auto-numbered (``{}``), numbered (``{0}``,
            ``{1}``...), and named placeholders (``{name}``), with positional
            arguments replacing the numbered placeholders and keywords replacing
            the named ones. However placeholder modifiers (``{0!r}``, ``{0:<10}``)
            are not supported.

            If a `!Composable` objects is passed to the template it will be merged
            according to its `as_string()` method. If any other Python object is
            passed, it will be wrapped in a `Literal` object and so escaped
            according to SQL rules.
            """
            rv: List["Sql.Composable"] = []
            autonum: Optional[int] = 0
            pre: LiteralString
            for pre, name, spec, conv in self._formatter.parse(self._obj):  # type: ignore
                if spec:
                    raise ValueError("no format specification supported by SQL")
                if conv:
                    raise ValueError("no format conversion supported by SQL")
                if pre:
                    rv.append(Sql.SQL(pre))

                if name is None:
                    continue

                if name.isdigit():
                    if autonum:
                        raise ValueError(
                            "cannot switch from automatic field numbering to manual"
                        )
                    rv.append(args[int(name)])
                    autonum = None

                elif not name:
                    if autonum is None:
                        raise ValueError(
                            "cannot switch from manual field numbering to automatic"
                        )
                    rv.append(args[autonum])
                    autonum += 1

                else:
                    rv.append(kwargs[name])

            return Sql.Composed(rv)

        def join(self, seq: Iterable["Sql.Composable"]) -> "Sql.Composed":
            """
            Join a sequence of `Composable`.

            :param seq: the elements to join.
            :type seq: iterable of `!Composable`

            Use the `!SQL` object's string to separate the elements in `!seq`.
            Note that `Composed` objects are iterable too, so they can be used as
            argument for this method.
            """
            rv = []
            it = iter(seq)
            try:
                rv.append(next(it))
            except StopIteration:
                pass
            else:
                for i in it:
                    rv.append(self)
                    rv.append(i)

            return Sql.Composed(rv)

    class Identifier(Composable):
        """
        A `Composable` representing an SQL identifier or a dot-separated sequence.

        Identifiers usually represent names of database objects, such as tables or
        fields. PostgreSQL identifiers follow `different rules`__ than SQL string
        literals for escaping (e.g. they use double quotes instead of single).

        .. __: https://www.postgresql.org/docs/current/sql-syntax-lexical.html# \
            SQL-SYNTAX-IDENTIFIERS

        Multiple strings can be passed to the object to represent a qualified name,
        i.e. a dot-separated sequence of identifiers.
        """

        _obj: Sequence[str]

        def __init__(self, *strings: str):
            super().__init__(strings)

            if not strings:
                raise TypeError("Identifier cannot be empty")

            for s in strings:
                if not isinstance(s, str):
                    raise TypeError(
                        f"SQL identifier parts must be strings, got {s!r} instead"
                    )

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({', '.join(map(repr, self._obj))})"

        def as_bytes(self) -> bytes:
            escs = [Escaping.escape_identifier(s).encode() for s in self._obj]
            return b".".join(escs)

    class Literal(Composable):
        """
        A `Composable` representing an SQL value to include in a query.

        Usually you will want to include placeholders in the query and pass values
        as `~cursor.execute()` arguments. If however you really really need to
        include a literal value in the query you can use this object.
        """

        def as_bytes(self) -> bytes:
            escs = Escaping.escape_literal(self._obj).encode()
            return escs

    class Placeholder(Composable):
        """A `Composable` representing a placeholder for query parameters.

        If the name is specified, generate a named placeholder (e.g. ``%(name)s``,
        ``%(name)b``), otherwise generate a positional placeholder (e.g. ``%s``,
        ``%b``).

        The object is useful to generate SQL queries with a variable number of
        arguments.
        """

        def __init__(
            self,
            name: str = "",
            format: Union[str, PyFormat] = PyFormat.AUTO,
        ):
            super().__init__(name)

            if not isinstance(name, str):
                raise TypeError(f"expected string as name, got {name!r}")

            if ")" in name:
                raise ValueError(f"')' not allowed. Invalid name: {name!r}")

            if type(format) is str:
                format = PyFormat(format)
            if not isinstance(format, PyFormat):
                raise TypeError(
                    f"expected PyFormat as format, got {type(format).__name__!r}"
                )

            self._format: PyFormat = format

        def __repr__(self) -> str:
            parts = []
            if self._obj:
                parts.append(repr(self._obj))
            if self._format is not PyFormat.AUTO:
                parts.append(f"format={self._format.name}")

            return f"{self.__class__.__name__}({', '.join(parts)})"

        def as_string(self) -> str:
            code = self._format.value
            return f"%({self._obj}){code}" if self._obj else f"%{code}"

        def as_bytes(self) -> bytes:
            return self.as_string().encode()

    NULL = SQL("NULL")
    NONNULL = SQL("NOT NULL")
    PRIMARY = SQL("PRIMARY KEY")
    DEFAULT = SQL("DEFAULT")

    @classmethod
    def foreignKey(
        cls,
        keyname: Identifier,
        column: Identifier | Composed,
        foreign_table: Identifier,
        foreign_column: Identifier | Composed,
        actions: SQL = SQL(""),
    ) -> Composed:
        return Sql.SQL(
            "CONSTRAINT {kn} FOREIGN KEY ({col}) REFERENCES {ft} ({fc}) {act}"
        ).format(
            kn=keyname,
            col=column,
            ft=foreign_table,
            fc=foreign_column,
            act=actions,
        )

    @classmethod
    def createTable(cls, table: Identifier, defs: tuple[Composed, ...]) -> Composed:
        """
        Create a table from a tuple of column defintions and table constraints.
        """
        return Sql.SQL("CREATE TABLE IF NOT EXISTS {tbl} ({cols})").format(
            tbl=table, cols=Sql.SQL(", ").join(defs)
        )

    @classmethod
    def basicInsert(
        cls, table: Identifier, columns: dict[Identifier, Any]
    ) -> tuple[Composed, list[Any]]:
        """
        Generate an INSERT query and list of values to use in SmartCursor.safe_execute().

        columns should be a dict of column identifiers and the values to insert.

        Example usage:
            cols = {
                Sql.Identifier("first_name"): "Alice",
                Sql.Identifier("last_name"): "Smith",
            }
            (query, values) = Sql.basicInsert(Sql.Identifier("people"), cols)
            cursor.safe_execute(query, values)

            print(query.as_string())
            # INSERT INTO `people` ( `first_name` , `last_name` ) VALUES ( %s , %s )
            print(values)
            # ["Alice", "Smith"]
        """
        query = Sql.SQL("INSERT INTO {tbl} ({columns}) VALUES ({values})").format(
            tbl=table,
            columns=Sql.SQL(", ").join(columns.keys()),
            values=Sql.SQL(", ").join([Sql.Placeholder()] * len(columns.keys())),
        )
        values = list(columns.values())
        return (query, values)

    @classmethod
    def basicUpdate(
        cls, table: Identifier, columns: dict[Identifier, Any]
    ) -> tuple[Composed, list[Any]]:
        """
        Generate an UPDATE query and list of values to use in SmartCursor.safe_execute().

        columns should be a dict of column identifiers and the values to insert.
        The last item in the dict will be used as the WHERE condition.

        Example usage:
            cols = {
                Sql.Identifier("first_name"): "Alvin",
                Sql.Identifier("last_name"): "Smyth",
                Sql.Identifier("id"): 1,
            }
            (query, values) = Sql.basicInsert(Sql.Identifier("people"), cols)
            cursor.safe_execute(query, values)

            print(query.as_string())
            # UPDATE `people` SET `first_name` = %s , `last_name` = %s WHERE `id` = %s
            print(values)
            # ["Alvin", "Smyth", 1]
        """
        p = [key + Sql.SQL("=") + Sql.Placeholder() for key in columns.keys()]
        last = p.pop()
        query = Sql.SQL("UPDATE {tbl} SET {pairs} WHERE {where}").format(
            tbl=table,
            pairs=Sql.SQL(",").join(p),
            where=last,
        )
        values = list(columns.values())
        return (query, values)
