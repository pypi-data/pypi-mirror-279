# record.py

import datetime as dt
import numpy as np
from typing import (
    ClassVar, Generator, Mapping, Self,
    Awaitable, Callable, overload, Iterable
)
from dataclasses import dataclass, field

import pandas as pd
from sqlalchemy.orm.session import sessionmaker, Session
import sqlalchemy as db

from dataplace import ModelIO, SpaceStore, Callback

from market_break.labels import (
    BID, ASK, BID_VOLUME, ASK_VOLUME, OPEN, HIGH, LOW, CLOSE,
    TIMESTAMP, DATETIME, RECEIVED_DATETIME, EXCHANGE, SYMBOL,
    BUY, SELL, SIDE
)

__all__ = [
    "RecordTable",
    "RecordRow",
    "RecordStore",
    "record_store_callback",
    "record_callback",
    "record_database_callback",
    "create_record_database_table",
    "tables_names",
    "table_columns",
    "extract_record_table",
    "extract_dataframe",
    "insert_database_records",
    "table_name",
    "Columns"
]

type JsonValue = str | float | int
type Value = dt.datetime | JsonValue

@dataclass(slots=True, frozen=True)
class RecordRow(ModelIO, Mapping):
    """Represents a row in the record of the price data of a symbol."""

    exchange: str
    symbol: str
    timestamp: float
    datetime: dt.datetime
    received_datetime: dt.datetime
    open: float
    high: float
    low: float
    close: float
    bid: float
    ask: float
    bid_volume: float
    ask_volume: float
    side: str

    BID: ClassVar[str] = BID
    ASK: ClassVar[str] = ASK
    BID_VOLUME: ClassVar[str] = BID_VOLUME
    ASK_VOLUME: ClassVar[str] = ASK_VOLUME

    OPEN: ClassVar[str] = OPEN
    HIGH: ClassVar[str] = HIGH
    LOW: ClassVar[str] = LOW
    CLOSE: ClassVar[str] = CLOSE

    TIMESTAMP: ClassVar[str] = TIMESTAMP
    DATETIME: ClassVar[str] = DATETIME
    RECEIVED_DATETIME: ClassVar[str] = RECEIVED_DATETIME

    SIDE: ClassVar[str] = SIDE
    BUY: ClassVar[str] = BUY
    SELL: ClassVar[str] = SELL

    EXCHANGE: ClassVar[str] = EXCHANGE
    SYMBOL: ClassVar[str] = SYMBOL

    KEYS: ClassVar[tuple[str]] = (
        EXCHANGE, SYMBOL, TIMESTAMP, DATETIME, RECEIVED_DATETIME,
        OPEN, HIGH, LOW, CLOSE, BID, ASK, BID_VOLUME, ASK_VOLUME, SIDE
    )

    def __len__(self):

        return len(RecordRow.KEYS)

    def __iter__(self) -> Generator[str, None, None]:

        yield from RecordRow.KEYS

    def __getitem__(self, item: str) -> Value:

        return getattr(self, item)

    @property
    def signature(self) -> tuple[str, str]:

        return self.exchange, self.symbol

    def dump(self) -> dict[str, JsonValue]:

        data: dict[str, ...] = {**self}

        data[self.DATETIME] = data[self.DATETIME].isoformat()
        data[self.RECEIVED_DATETIME] = data[self.RECEIVED_DATETIME].isoformat()

        return data

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        return cls(
            exchange=data[cls.EXCHANGE],
            symbol=data[cls.SYMBOL],
            timestamp=(
                data[cls.TIMESTAMP] if cls.TIMESTAMP in data else
                dt.datetime.now().timestamp()
            ),
            datetime=(
                dt.datetime.fromisoformat(data[cls.DATETIME])
                if cls.DATETIME in data else dt.datetime.now()
            ),
            received_datetime=(
                dt.datetime.fromisoformat(data[cls.RECEIVED_DATETIME])
                if cls.RECEIVED_DATETIME in data else dt.datetime.now()
            ),
            open=data.get(cls.OPEN, np.nan),
            high=data.get(cls.HIGH, np.nan),
            low=data.get(cls.LOW, np.nan),
            close=data.get(cls.CLOSE, np.nan),
            bid=data.get(cls.BID, np.nan),
            ask=data.get(cls.ASK, np.nan),
            bid_volume=data.get(cls.BID_VOLUME, np.nan),
            ask_volume=data.get(cls.ASK_VOLUME, np.nan),
            side=data.get(cls.SIDE, np.nan)
        )

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> Self:

        return cls(**data)

    @classmethod
    def from_tuple(cls, data: tuple[JsonValue, ...]) -> Self:

        return cls.from_dict(dict(zip(cls.KEYS, data)))

@dataclass(slots=True)
class RecordTable(ModelIO):
    """Represents a table of price data record rows of a symbol."""

    symbol: str
    exchange: str
    memory: int = None
    data: pd.DataFrame = field(default=None, repr=False, hash=False)

    COLUMNS: ClassVar[tuple[str]] = RecordRow.KEYS

    EXCHANGE: ClassVar[str] = EXCHANGE
    SYMBOL: ClassVar[str] = SYMBOL

    MEMORY: ClassVar[str] = "memory"
    DATA: ClassVar[str] = "data"

    def __post_init__(self) -> None:

        if self.data is None:
            self.data = pd.DataFrame(
                {column: [] for column in self.COLUMNS},
                index=[]
            )

        else:
            self.validate_matching_columns()

    @overload
    def __getitem__(self, item: slice) -> Self:

        pass

    @overload
    def __getitem__(self, item: int) -> RecordRow:

        pass

    def __getitem__(self, item: slice | int) -> Self | RecordRow:

        if isinstance(item, slice):
            return RecordTable(
                symbol=self.symbol,
                exchange=self.exchange,
                memory=self.memory,
                data=self.data.iloc[item]
            )

        elif isinstance(item, int):
            return self.index_row(item)

    def __len__(self) -> int:

        return self.length

    def __hash__(self) -> int:

        return self.hash

    def __eq__(self, other: ...) -> bool:

        if type(other) is not type(self):
            return False

        other: RecordTable

        # noinspection PyUnresolvedReferences
        return (
            (self.signature == other.signature) and
            (len(self.data.columns) == len(other.data.columns)) and
            (set(self.data.columns) == set(other.data.columns)) and
            len(self.data) == len(other.data) and
            (self.data.values == other.data.values).all()
        )

    def __add__(self, other: ...) -> Self:

        if not isinstance(other, RecordTable):
            raise TypeError(
                f"both objects must be {RecordTable} "
                f"instances for addition, received: {type(other)}"
            )

        if self.signature != other.signature:
            raise ValueError(
                f"Cannot add two record objects of different signatures "
                f"({self.signature} and {other.signature})"
            )

        new = self.deepcopy()

        new.data = pd.concat([new.data, other.data])

        return new

    @property
    def length(self) -> int:

        return len(self.data)

    @property
    def is_empty(self) -> bool:

        return len(self.data) == 0

    @property
    def is_matching_columns(self) -> bool:

        return set(self.data.columns) != set(self.COLUMNS)

    @property
    def signature(self) -> tuple[str, str]:

        return self.exchange, self.symbol

    @property
    def hash(self) -> int:

        return hash(self.signature)

    def validate_not_empty(self) -> None:

        if self.is_empty:
            raise ValueError(f"No data in {repr(self)}")

    def validate_matching_columns(self) -> None:

        if self.is_matching_columns:
            raise ValueError(
                f"data columns and record column don't match "
                f"({self.data.columns} and {self.COLUMNS})"
            )

    @staticmethod
    def _process_data(data: dict[str, ...]) -> dict[str, ...]:

        if isinstance(data[DATETIME], pd.Timestamp):
            data[DATETIME] = data[DATETIME].to_pydatetime()

        if isinstance(data[RECEIVED_DATETIME], pd.Timestamp):
            data[RECEIVED_DATETIME] = data[RECEIVED_DATETIME].to_pydatetime()

        return data

    @staticmethod
    def _process_value(value: ...) -> ...:

        if isinstance(value, pd.Timestamp):
            value = value.to_pydatetime()

        return value

    def index_value(self, key: str, index: int) -> Value:

        self.validate_not_empty()

        return self._process_value(self.data[key].iloc[index])

    def last_value(self, key: str) -> Value:

        return self.index_value(key=key, index=-1)

    def first_value(self, key: str) -> Value:

        return self.index_value(key=key, index=0)

    def index_row(self, index: int) -> dict[str, Value]:

        self.validate_not_empty()

        return self._process_data(self.data.iloc[index].to_dict())

    def last_row(self) -> dict[str, Value]:

        return self.index_row(-1)

    def first_row(self) -> dict[str, Value]:

        return self.index_row(0)

    def first(self) -> RecordRow:

        self.validate_not_empty()

        return RecordRow(
            **self.first_row(),
            exchange=self.exchange, symbol=self.symbol
        )

    def last(self) -> RecordRow:

        self.validate_not_empty()

        return RecordRow(**self.last_row())

    def generate_rows(self) -> Generator[tuple[int, RecordRow], None, None]:

        for i, row in self.data.iterrows():
            yield i, RecordRow(**self._process_data(row.to_dict()))

    def rows(self) -> list[RecordRow]:

        return [data for i, data in self.generate_rows()]

    def append(self, data: RecordRow | dict[str, Value]) -> None:

        self.data.loc[len(self.data)] = {
            column: data[column] for column in self.COLUMNS
        }

        if self.memory:
            self.data.drop(
                self.data.index[:len(self.data) - self.memory],
                inplace=True
            )

    def pop(self, index: int) -> RecordRow:

        data = self.index_row(index=index)

        self.data.drop(index, inplace=True)

        return RecordRow(**data)

    def clear(self) -> None:

        self.data.drop(self.data.index, inplace=True)

    @classmethod
    def load(cls, data: dict[str, str | int | dict[str, JsonValue]]) -> Self:

        return cls(
            exchange=data[cls.EXCHANGE],
            symbol=data[cls.SYMBOL],
            memory=data.get(cls.MEMORY, None),
            data=pd.DataFrame.from_dict(data[cls.DATA], orient='columns')
        )

    def dump(self) -> dict[str, str | int | list[dict[str, JsonValue]]]:

        return {
            self.EXCHANGE: self.exchange,
            self.SYMBOL: self.symbol,
            self.MEMORY: self.memory,
            self.DATA: self.data.to_dict(orient='records')
        }

class RecordStore(SpaceStore[tuple[str, str], RecordTable]):
    """Represents a store for record tables."""

    def __init__(self) -> None:

        super().__init__(lambda data: data.signature, RecordTable)

    def map(self) -> dict[str, dict[str, list[RecordTable]]]:

        data = {}

        for (exchange, symbol), values in self.store.copy().items():
            if None in (exchange, symbol):
                continue

            data.setdefault(exchange, {})[symbol] = values

        return data

    def structure(self) -> dict[str, list[str]]:

        data = {}

        for (exchange, symbol), values in self.store.copy().items():
            if None in (exchange, symbol):
                continue

            data.setdefault(exchange, []).append(symbol)

        return data

    def exchanges(self) -> Generator[str, ..., ...]:

        for (exchange, symbol) in self.store:
            if None in (exchange, symbol):
                continue

            yield exchange

    def symbols(self) -> Generator[str, ..., ...]:

        for (exchange, symbol) in self.store:
            if None in (exchange, symbol):
                continue

            yield symbol

def record_callback(
        callback: Callable[[RecordRow], ... | Awaitable],
        preparation: Callable[[], Awaitable | ...] = None,
        enabled: bool = True,
        prepared: bool = False
) -> Callback:
    """
    Creates a callback to be called for price data record row objects.

    :param callback: The callback function to be called.
    :param preparation: The preparation function to be called.
    :param enabled: The value to enable the callback,
    :param prepared: The value to mark the callback as already prepared.

    :return: The callback object.
    """

    return Callback(
        callback=callback,
        types={RecordRow},
        preparation=preparation,
        enabled=enabled,
        prepared=prepared
    )

def record_store_callback(
        store: RecordStore,
        create: bool = True,
        add: bool = True,
        kwargs: dict[str, ...] = None
) -> Callback:
    """
    Creates a callback to store price data record row objects.

    :param store: The store object to store the record row in a table inside the store.
    :param create: The value to create new record tables for unknown symbols.
    :param add: The value to add the record row to the tables in the store.
    :param kwargs: Any keyword arguments for creating the record table objects.

    :return: The callback object.
    """

    async def wrapper(data: ModelIO) -> None:

        if not isinstance(data, tuple(callback.types)):
            return

        data: RecordRow

        for record in (
            store.get_all(data.signature) if data.signature in store else
            (
                store.add_all(
                    [
                        RecordTable(
                            exchange=data.exchange,
                            symbol=data.symbol,
                            **(kwargs or {})
                        )
                    ]
                ) if create else []
            )
        ):
            if add:
                record.append(data)

    callback = record_callback(wrapper)

    return callback

class Columns:

    @staticmethod
    def string_column(name: str, limit: int = 64) -> db.Column[str]:

        return db.Column(name, db.String(limit))

    @staticmethod
    def int_column(name: str, nullable: bool = True) -> db.Column[int]:

        return db.Column(name, db.Integer(), nullable=nullable)

    @staticmethod
    def float_column(name: str, nullable: bool = True) -> db.Column[float]:

        return db.Column(name, db.Float(), nullable=nullable)

    @staticmethod
    def datetime_column(name: str, nullable: bool = True) -> db.Column[dt.datetime]:

        return db.Column(name, db.DateTime(), nullable=nullable)

    COLUMNS_TYPES = {
        RecordRow.EXCHANGE: str,
        RecordRow.SYMBOL: str,
        RecordRow.TIMESTAMP: float,
        RecordRow.DATETIME: dt.datetime,
        RecordRow.RECEIVED_DATETIME: dt.datetime,
        RecordRow.OPEN: float,
        RecordRow.HIGH: float,
        RecordRow.LOW: float,
        RecordRow.CLOSE: float,
        RecordRow.BID: float,
        RecordRow.ASK: float,
        RecordRow.BID_VOLUME: float,
        RecordRow.ASK_VOLUME: float,
        RecordRow.SIDE: str
    }

    TYPES_GENERATORS = {
        str: string_column,
        int: int_column,
        float: float_column,
        dt.datetime: datetime_column
    }

    @staticmethod
    def generate(
            columns: Iterable[str],
            nullables: Iterable[str] | dict[str, bool] = None,
            non_nullables: Iterable[str] | dict[str, bool] = None,
            limited: Iterable[str] | dict[str, int] = None,
            limit: int = None,
            nullable: bool = None
    ) -> list[db.Column]:

        if nullables is None:
            nullables = ()

        if non_nullables is None:
            non_nullables = ()

        if limited is None:
            limited = ()

        if nullables is not None and not isinstance(nullables, dict):
            nullables = set(nullables)

        if non_nullables is not None and not isinstance(non_nullables, dict):
            non_nullables = set(non_nullables)

        generated = []

        for name in columns:
            kwargs = dict()

            column_type = Columns.COLUMNS_TYPES[name]

            if column_type in (int, float, dt.datetime):
                if name in nullables:
                    kwargs['nullable'] = (
                        nullables[name] if isinstance(nullables, dict) else True
                    )

                elif name in non_nullables:
                    kwargs['nullable'] = (
                        non_nullables[name] if isinstance(non_nullables, dict) else False
                    )

                elif nullable is not None:
                    kwargs['nullable'] = nullable

            if column_type is str:
                if name in limited:
                    kwargs['limit'] = limited[name] if isinstance(limited, dict) else limit

                elif limit is not None:
                    kwargs['limit'] = limit

            generated.append(
                Columns.TYPES_GENERATORS[column_type](name, **kwargs)
            )

        return generated

def create_record_database_table(
        name: str, metadata: db.MetaData = None, columns: Iterable[str] = None
) -> db.Table:
    """
    Creates a table for records in a database.

    :param name: The name of the table to create.
    :param metadata: The metadata object of the database.
    :param columns: The column names for the table.

    :return: The created table object.
    """

    if columns is None:
        columns = RecordRow.KEYS

    return db.Table(
        name,
        metadata or db.MetaData(),
        *Columns.generate(columns, non_nullables=[TIMESTAMP], limit=64)
    )

def record_database_callback(
        engine: db.Engine,
        metadata: db.MetaData = None,
        table: db.Table = None
) -> Callback:
    """
    Creates a callback to store price data record row objects.

    :param engine: The database engine.
    :param metadata: The metadata of the database.
    :param table: The table object to store records in.

    :return: The callback object.
    """

    session_maker = sessionmaker(bind=engine)

    metadata = metadata or db.MetaData()

    async def wrapper(data: ModelIO) -> None:

        if not isinstance(data, tuple(callback.types)):
            return

        data: RecordRow

        insert_database_records(
            records=[dict(**data)],
            engine=engine,
            session_maker=session_maker,
            metadata=metadata,
            table=table or "_".join(data.signature)
        )

    callback = record_callback(wrapper)

    return callback

def insert_database_records(
        records: Iterable[dict[str, str | float | int | dt.datetime]],
        engine: db.Engine,
        metadata: db.MetaData = None,
        session: Session = None,
        session_maker: sessionmaker = None,
        table: str | db.Table = None,
) -> None:

    first = None

    for first in records:
        break

    if first is None:
        return

    metadata = metadata or db.MetaData()

    if table is None:
        if (EXCHANGE not in first) or (SYMBOL not in first):
            raise ValueError(
                "both 'exchange' and 'symbol' must be defined for "
                "records when table is not given."
            )

        table: str | db.Table = table_name(exchange=first[EXCHANGE], symbol=first[SYMBOL])

    if isinstance(table, str):
        if table not in metadata.tables:
            db.Table(
                table,
                metadata or db.MetaData(),
                *Columns.generate(first, non_nullables=[TIMESTAMP], limit=64)
            )

            metadata.create_all(engine)

        table: db.Table = metadata.tables[table]

    created = False

    if session is None:
        session_maker = session_maker or sessionmaker(bind=engine)

        session = session_maker()

        created = True

    for data in records:
        session.execute(db.insert(table).values(**data))

    session.commit()

    if created:
        session.close()

def table_name(exchange: str, symbol: str) -> str:

    return f"{exchange}_{symbol}"

def tables_names(engine: db.Engine) -> list[str]:

    return db.inspect(engine).get_table_names()

def table_columns(engine: db.Engine, table: str) -> list[dict[str, ...]]:

    return db.inspect(engine).get_columns(table)

def extract_dataframe(engine: db.Engine, table: str, datetime: list[str] = None) -> pd.DataFrame:

    df = pd.read_sql(f'SELECT * FROM "{table}"', engine)

    auto = False

    if datetime is None:
        datetime = [DATETIME, RECEIVED_DATETIME]

        auto = True

    for table in (datetime or ()):
        if (table not in df) and auto:
            continue

        df[table] = pd.to_datetime(df[table], format='ISO8601')

    return df

def extract_record_table(engine: db.Engine, table: str) -> RecordTable:

    exchange, symbol = table.split("_")

    return RecordTable(
        symbol=symbol,
        exchange=exchange,
        data=extract_dataframe(engine, table=table)
    )
