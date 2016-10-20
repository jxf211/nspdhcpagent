# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""DB related custom exceptions.

Custom exceptions intended to determine the causes of specific database
errors. This module provides more generic exceptions than the database-specific
driver libraries, and so users of oslo.db can catch these no matter which
database the application is using. Most of the exceptions are wrappers. Wrapper
exceptions take an original exception as positional argument and keep it for
purposes of deeper debug.

Example::

    try:
        statement(arg)
    except sqlalchemy.exc.OperationalError as e:
        raise DBDuplicateEntry(e)


This is useful to determine more specific error cases further at execution,
when you need to add some extra information to an error message. Wrapper
exceptions takes care about original error message displaying to not to loose
low level cause of an error. All the database api exceptions wrapped into
the specific exceptions provided belove.


Please use only database related custom exceptions with database manipulations
with `try/except` statement. This is required for consistent handling of
database errors.
"""

import six



class DBError(Exception):

    """Base exception for all custom database exceptions.

    :kwarg inner_exception: an original exception which was wrapped with
        DBError or its subclasses.
    """

    def __init__(self, inner_exception=None):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(six.text_type(inner_exception))


class DBDuplicateEntry(DBError):
    """Duplicate entry at unique column error.

    Raised when made an attempt to write to a unique column the same entry as
    existing one. :attr: `columns` available on an instance of the exception
    and could be used at error handling::

       try:
           instance_type_ref.save()
       except DBDuplicateEntry as e:
           if 'colname' in e.columns:
               # Handle error.

    :kwarg columns: a list of unique columns have been attempted to write a
        duplicate entry.
    :type columns: list
    :kwarg value: a value which has been attempted to write. The value will
        be None, if we can't extract it for a particular database backend. Only
        MySQL and PostgreSQL 9.x are supported right now.
    """
    def __init__(self, columns=None, inner_exception=None, value=None):
        self.columns = columns or []
        self.value = value
        super(DBDuplicateEntry, self).__init__(inner_exception)


class DBReferenceError(DBError):
    """Foreign key violation error.

    :param table: a table name in which the reference is directed.
    :type table: str
    :param constraint: a problematic constraint name.
    :type constraint: str
    :param key: a broken reference key name.
    :type key: str
    :param key_table: a table name which contains the key.
    :type key_table: str
    """

    def __init__(self, table, constraint, key, key_table,
                 inner_exception=None):
        self.table = table
        self.constraint = constraint
        self.key = key
        self.key_table = key_table
        super(DBReferenceError, self).__init__(inner_exception)


class DBDeadlock(DBError):

    """Database dead lock error.

    Deadlock is a situation that occurs when two or more different database
    sessions have some data locked, and each database session requests a lock
    on the data that another, different, session has already locked.
    """

    def __init__(self, inner_exception=None):
        super(DBDeadlock, self).__init__(inner_exception)


class DBInvalidUnicodeParameter(Exception):

    """Database unicode error.

    Raised when unicode parameter is passed to a database
    without encoding directive.
    """

    message = ("Invalid Parameter: "
                "Encoding directive wasn't provided.")


class DbMigrationError(DBError):

    """Wrapped migration specific exception.

    Raised when migrations couldn't be completed successfully.
    """

    def __init__(self, message=None):
        super(DbMigrationError, self).__init__(message)


class DBConnectionError(DBError):

    """Wrapped connection specific exception.

    Raised when database connection is failed.
    """

    pass


class InvalidSortKey(Exception):
    """A sort key destined for database query usage is invalid."""

    message = ("Sort key supplied was not valid.")


class ColumnError(Exception):
    """Error raised when no column or an invalid column is found."""


class BackendNotAvailable(Exception):
    """Error raised when a particular database backend is not available

    within a test suite.

    """


class RetryRequest(Exception):
    """Error raised when DB operation needs to be retried.

    That could be intentionally raised by the code without any real DB errors.
    """
    def __init__(self, inner_exc):
        self.inner_exc = inner_exc
