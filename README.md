<!--![warg](.github/images/warg.svg)-->

<p align="center">
  <img src=".github/images/warg.svg" alt='Warg' />
</p>

<h1 align="center">Warg</h1>

<!--# Warg-->

| [![Build Status](https://travis-ci.com/aivclab/warg.svg?branch=master)](https://travis-ci.com/aivclab/warg) | [![Documentation](https://img.shields.io/static/v1?label=&message=docs&color=EE4C2C&style=for-the-badge)](https://pything.github.io/warg/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) | [![Coverage Status](https://coveralls.io/repos/github/aivclab/warg/badge.svg?branch=master)](https://coveralls.io/github/aivclab/warg?branch=master) | [![codebeat badge](https://codebeat.co/badges/e788d8e5-9934-44bf-85e2-b8043e5806bc)](https://codebeat.co/projects/github-com-pything-warg-master) | [![Codeship Status for pything/warg](https://app.codeship.com/projects/34b921f0-5e8f-0138-1e29-1ef237e9df62/status?branch=master)](https://app.codeship.com/projects/392349) | [![codecov](https://codecov.io/gh/pything/warg/branch/master/graph/badge.svg?token=g59R80u4j2)](https://codecov.io/gh/pything/warg) |
|-------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|

| Workflows                                                                                                                                                                                                   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Publish Python 🐍 distributions 📦 to PyPI and TestPyPI](https://github.com/pything/warg/workflows/Publish%20Python%20%F0%9F%90%8D%20distributions%20%F0%9F%93%A6%20to%20PyPI%20and%20TestPyPI/badge.svg) |
| ![On Push Any Documentation Check](https://github.com/pything/warg/workflows/On%20Push%20Any%20Documentation%20Check/badge.svg)                                                                             |
| ![CodeQL](https://github.com/pything/warg/workflows/CodeQL/badge.svg)                                                                                                                                       |

> Devour everything :wolf:
> Prey upon

![python](.github/images/python.svg)

___

```Old-Norse: Varg```

## Only for use with Python 3.6+

This package is a selection of generalised small utility classes for many use-cases in any python project, a brief
description of each follow. No external dependencies, #pure-python. Warg is strictly only using standard library functionality, hopefully forever..

- A class for easing return of multiple values, implicit handling of args and kwargs and more. Neat access options to
  the underlying \_\_dict\_\_ of the class instance, supporting almost any variation that comes to mind.

- A class for executing any 'heavy' function asynchronously storing any results in a bounded queue. Note: communication
  and organisation is costly, intended for heavy processing functions and general queuing.

- A set of utility functions for parsing/sanitising python config files, and presenting attributes using common python
  conventions and practices.

- Some Mixin classes for iterating Mapping Types.

- A single base class and metaclass, differentiating on whether subclasses singletons should be instated on own subclass
  basis or on the supertype.

- A wrapper class, shorthand "GDKC", for delayed construction of class instances, with a persistent set of proposed
  kwargs that remain subject to change until final construction.

- A "contract" decorator, "kw passing" is a concept that lets one make a contract with the caller that all kwargs with
  be passed onwards to a receiver, this lets the caller inspect available kwargs of the the receiver function allowing
  for autocompletion, typing and documentation fetching.

- and more..

# Disclaimer

I personally view the collection of tools as a general extensions of the python language for my workflow. I seek to
provide implementations and ideas that should remain valid and useful even through future versions of the python
language.\
These tools are useful to me, I however suspect many of the assumptions and decisions that I made will be frowned upon
by more pythonic developers, hence why I would never propose any of these tools be provided in any other way than as
installable "extensions".\
I seek to make the implementations quite easy to read and intuitive to experienced python developers, but I would
refrain usage of "warg" if collaborating with less experienced python developers that would not inspect the
implementation details of the package.

Lastly use "warg" with caution for long term projects, as some features might break as python naturally evolves in
future releases. Warg uses some advanced features of python and sometimes abuse notation/syntax, with some pretty hard
assumptions on parameter input and interaction.

With these rambling comments in mind please have fun with it ![epic_face](.github/images/epic_face.png)

___
> With great power comes great responsibility :wink:
___
