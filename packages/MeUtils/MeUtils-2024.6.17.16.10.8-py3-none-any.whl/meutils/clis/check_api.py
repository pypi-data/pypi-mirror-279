#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_api_key
# @Time         : 2024/6/17 14:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.async_utils import async_to_sync

from meutils.config_utils.lark_utils import get_spreadsheet_values

from meutils.db.redis_db import redis_client
from meutils.llm.check_api import check_api_key_or_token


@cli.command()
def check_and_update_api_keys(check_url, feishu_url):
    """传入配置文件"""

    api_keys = get_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)[0].tolist()
    if feishu_url in redis_client:
        api_keys += redis_client.lrange(feishu_url, 0, -1) | xmap(lambda x: x.decode())

    # check api key
    api_keys = set(filter(lambda key: key is True, async_to_sync(check_api_key_or_token)(api_keys, check_url)))

    if feishu_url in redis_client:
        lastest_api_keys = redis_client.lrange(feishu_url, 0, -1) | xmap(lambda x: x.decode())

        # to_update_api_keys
        api_keys = (
                list(api_keys - set(lastest_api_keys))  # 新增的
                + lastest_api_keys | xfilter_(lambda api_key: api_key in api_keys)  # 存量有效的&按当前顺序
        )

        redis_client.delete(feishu_url)

    redis_client.rpush(feishu_url, *api_keys)


if __name__ == '__main__':
    cli()
