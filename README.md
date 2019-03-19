# Warg
```Old-Norse: Varg``` 

![warg](.github/images/warg.svg) ![warg](.github/images/python.svg)

[![Build Status](https://travis-ci.com/aivclab/warg.svg?branch=master)](https://travis-ci.com/aivclab/warg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Coverage Status](https://coveralls.io/repos/github/aivclab/warg/badge.svg?branch=master)](https://coveralls.io/github/aivclab/warg?branch=master)
___
> Devour everything.
___

This package is a selection of generalised  small utilities classes for many use-cases, a brief description of each follows.

- A class for easing return of multiple values, implicit handling of args and kwargs and more. 

- A class for executing any 'heavy' function asynchronously any storing results in a bounded queue. 
Note: communication and organisation is costly, intended for heavy processing functions and general queuing.
