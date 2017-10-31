#!/usr/bin/python3
# -*- coding: utf-8 -*-

import orm
import asyncio
from models import User, Blog, Comment


async def save_test(loop):
    await orm.create_pool(loop=loop, user='root', password='1106', database='awesome')

    u = User(name='Test', email='test3@example.com', passwd='1234567890', image='about:blank')

    await User.save(u)

loop = asyncio.get_event_loop()
loop.run_until_complete(save_test(loop))
loop.close()



