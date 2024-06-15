.. _config-label:

Configurations
==============

Precedence
----------

|project_name| configurations follow a hierarchical design pattern.

1. Command line configurations - see :ref:`cli-custom-config-label`

2. Configuration files - ``pyproject.toml`` / ``msort.ini``

3. Default configurations

The recommended pattern is to use a ``pyproject.toml`` file.

Defaults
--------

|project_name| configurations can be split into **ordering** and **general**.

General defaults
................
:auto_static: Defaults to True

Check to see if methods could be static methods and convert to a static method if so.

:use_msort_group: Defaults to True

Controls whether the ``msort_group`` decorator should be considered when running msort. See :ref:`msort-group-label`

:use_property_groups: Defaults to False

Controls whether methods related to a property are grouped together or not.

.. code-block:: python

    class MyClass:
        def __init__(self):
            self._name = "myclass"
            self._age = 5

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, new_name: str):
            self._name = new_name

        @property
        def age(self):
            return self._age

        @name.getter
        def name(self):
            return self._name

        @age.deleter
        def age(self):
            del self._age

        @name.deleter
        def name(self):
            del self._name

        @age.setter
        def age(self, new_age: str):
            self._age = new_age

        @age.getter
        def age(self):
            return self._age

In this example class, we have two properties defined, ``name`` and ``age``.
|project_name| can sort these methods in two ways:
* According to the component sorting order

* According to property groups

Sorting by component sorting order would lead to:

.. code-block:: python

    class MyClass:
        def __init__(self):
            self._name = "myclass"
            self._age = 5

        @property
        def age(self):
            return self._age

        @property
        def name(self):
            return self._name

        @age.getter
        def age(self):
            return self._age

        @name.getter
        def name(self):
            return self._name

        @age.setter
        def age(self, new_age: str):
            self._age = new_age

        @name.setter
        def name(self, new_name: str):
            self._name = new_name

        @age.deleter
        def age(self):
            del self._age

        @name.deleter
        def name(self):
            del self._name

Properties get sorted above getters, above setters and above deleters.

By using the ``--use-property-groups`` option we can sort by property related methods:

.. code-block:: python

    class MyClass:
        def __init__(self):
            self._name = "myclass"
            self._age = 5

        @property
        def age(self):
            return self._age

        @age.getter
        def age(self):
            return self._age

        @age.setter
        def age(self, new_age: str):
            self._age = new_age

        @age.deleter
        def age(self):
            del self._age

        @property
        def name(self):
            return self._name

        @name.getter
        def name(self):
            return self._name

        @name.setter
        def name(self, new_name: str):
            self._name = new_name

        @name.deleter
        def name(self):
            del self._name

In this case, the four ``age`` methods are followed by the four ``name`` methods. The sub-ordering of properties,
setters, deleters respects the sorting level configuration.

Ordering defaults
.................

See :ref:`components-label` for details on each component.

:ellipsis: Defaults to 0
:class docstring: Defaults to 0
:typed class attribute: Defaults to 1
:untyped class attribute: Defaults to 2
:dunder methd: Defaults to 3
:msort group: Defaults to 4
:class method: Defaults to 5
:static method: Defaults to 6
:property: Defaults to 7
:getter: Defaults to 8
:setter: Defaults to 9
:deleter: Defaults to 10
:decorated method: Defaults to 11
:instance method: Defaults to 12
:private method: Defaults to 13
:inner class: Defaults to 14

Configuration Files
-------------------

Configurations can be specified using the legacy ``msort.ini`` file or the more modern ``pyproject.toml``
file.

By default, msort will search for a configuration file named either ``msort.ini`` or ``pyproject.toml`` in the
working directory.

An alternatively named ``.ini`` or ``.toml`` file can also be used and then specified to msort using the
``--config-path`` option on the command line.

pyproject.toml
..............
Below is an example ``pyproject.toml`` with msort tool groups

.. code-block:: toml

    [tool.msort.order]
    dunder_method = 3
    msort_group = 4
    class_method = 5
    static_method = 6
    getter = 7
    setter = 8
    property = 9
    decorated_method = 10
    instance_method = 11
    private_method = 12
    inner_class = 13

    [tool.msort]
    use_msort_group = true
    auto_static = false

In this example configuration, ``property`` methods have been set to level 9, below ``getter`` and ``setter``.
By default, ``property`` is normally level 7.


msort.ini
.........

Below is an example ``msort.ini`` file

.. code-block:: ini

    [msort.order]
    dunder_method = 3
    private_method = 4
    msort_group = 5
    class_method = 6
    static_method = 7
    property = 8
    getter = 9
    setter = 10
    deleter = 11
    decorated_method = 12
    instance_method = 13
    inner_class = 14

    [msort]
    use_msort_group = True
    auto_static = False

In this example configuration, ``private_method`` has been set to level 4 so that
private methods appear at the top of the class rather than the bottom.
