from __future__ import annotations

import abc
import typing as t

## Define generic TypeVar to indicate a class instance type
T = t.TypeVar("T")


class RepositoryBase(t.Generic[T], metaclass=abc.ABCMeta):
    """A generic SQLAlchemy repository class base."""

    @abc.abstractmethod
    def add(self, entity: T):
        """Add new entity to database."""
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity: T):
        """Update existing entity."""
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: T):
        """Remove existing entity from database."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, entity_id) -> T:
        """Retrieve entity from database by its ID."""
        raise NotImplementedError()
