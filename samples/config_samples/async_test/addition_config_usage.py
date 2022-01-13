#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 11-12-2020
           """


async def b() -> None:
    """
    :rtype: None
    """
    import config2

    print(config2.A_CONSTANT)


if __name__ == "__main__":

    async def c() -> None:
        """
        :rtype: None
        """
        await b()

    import asyncio

    asyncio.run(c())
