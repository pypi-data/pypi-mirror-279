import enum
from collections import defaultdict
from sqlalchemy.ext.declarative import DeclarativeMeta
from types import ModuleType


def get_schema_objects(schema: ModuleType) -> list:
    """Extracts all objects from a sqlalchemy schema.

    Args:
        schema (module): A module containing sqlalchemy objects.

    Returns:
        list: A list of sqlalchemy objects.
    """
    return [getattr(schema, name) for name in dir(schema)]


def get_tables(objects: list) -> list[DeclarativeMeta]:
    """Extracts all sqlalchemy tables from a list of schema objects.

    Args:
        objects (list): A list of sqlalchemy schema objects.

    Returns:
        list: A list of sqlalchemy tables.
    """
    return [
        obj
        for obj in objects
        if isinstance(obj, DeclarativeMeta) and hasattr(obj, "__tablename__")
    ]


def get_enums(objects: list) -> list:
    """Extracts all enums from a list of sqlalchemy schema objects.

    Args:
        objects (list): A list of sqlalchemy schema objects.

    Returns:
        list: A list of sqlalchemy enums.
    """
    return [obj for obj in objects if issubclass(obj, enum.Enum)]


def determine_dependencies(objects: list) -> dict[str, list[str]]:
    """Determines the dependencies between tables.

    Args:
        objects (list): A list of sqlalchemy schema objects.

    Returns:
        dict[str, list[str]]: A dictionary where the key is a table name and the value is a list of tables that the key table depends on.
    """
    dependencies = defaultdict(list)

    # Initialize the dictionary with all tables to ensure empty arrays for tables with no dependencies
    for obj in objects:
        if hasattr(obj, "__tablename__"):
            table_name = obj.__tablename__
            dependencies[table_name]  # This ensures an entry is created for each table

    # Populate the dependencies
    for obj in objects:
        if hasattr(obj, "__tablename__"):
            table = obj.__table__
            for fk in table.foreign_keys:
                parent_table = fk.column.table
                # Skip self-references
                if parent_table.name != table.name:
                    dependencies[table.name].append(parent_table.name)

    return dependencies
