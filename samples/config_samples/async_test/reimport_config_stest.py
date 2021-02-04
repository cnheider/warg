#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 11-12-2020
           """

if __name__ == "__main__":

    async def a():
        import addition_config_usage

        await addition_config_usage.b()
        import config2

        print(config2.ANOTHER_CONSTANT)

    import asyncio

    asyncio.run(a())
