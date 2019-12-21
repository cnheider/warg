# Warg
```Old-Norse: Varg```

![warg](.github/images/warg.svg)
![python](.github/images/python.svg)

[![Build Status](https://travis-ci.com/aivclab/warg.svg?branch=master)](https://travis-ci.com/aivclab/warg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Coverage Status](https://coveralls.io/repos/github/aivclab/warg/badge.svg?branch=master)](https://coveralls.io/github/aivclab/warg?branch=master)
___
> Devour everything :wolf:
___

This package is a selection of generalised  small utilities classes for many use-cases, a brief description of each follows.

- A class for easing return of multiple values, implicit handling of args and kwargs and more.

- A class for executing any 'heavy' function asynchronously storing any results in a bounded queue.
Note: communication and organisation is costly, intended for heavy processing functions and general queuing.

- A set of utility functions for parsing/sanitising python config files, and presenting attributes using common python conventions and practices.

- Some Mixin classes for iterating Mapping Types.

- A single base class and metaclass, differentiating on whether subclasses singletons should be instated on
 own subclass basis or on the supertype.

- A "contract" decorator, "kw passing" is a concept that lets one make a contract with the caller that all
          kwargs with be passed onwards to a receiver, this lets the caller inspect available kwargs of the
          the receiver function allowing for autocompletion, typing and documentation fetching.

- and more..

# Disclaimer
Use warg with caution, some features might break as python naturally evolves.
Warg uses some advanced features of python and sometimes abuse notation/syntax, with some pretty hard
 assumptions on input and interaction. 
With this in mind please have fun with it ![epic_face](.github/images/epic_face.png)

___
> With great power comes great responsibility :wink:
___
