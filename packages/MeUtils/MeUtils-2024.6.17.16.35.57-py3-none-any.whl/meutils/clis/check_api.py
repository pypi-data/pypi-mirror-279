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
from meutils.notice.feishu import send_message

from meutils.db.redis_db import redis_client
from meutils.llm.check_api import check_api_key_or_token


@cli.command()
def check_and_update_api_keys(check_url, feishu_url):
    """传入配置文件"""

    api_keys = get_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)[0].tolist()
    logger.debug(api_keys)

    if feishu_url in redis_client:
        api_keys += redis_client.lrange(feishu_url, 0, -1) | xmap(lambda x: x.decode())

    logger.debug(api_keys)

    # check api key
    api_keys = async_to_sync(check_api_key_or_token)(api_keys, check_url)

    logger.debug(api_keys)

    if feishu_url in redis_client:
        lastest_api_keys = redis_client.lrange(feishu_url, 0, -1) | xmap(lambda x: x.decode())

        # to_update_api_keys
        api_keys = (
                list(set(api_keys) - set(lastest_api_keys))  # 新增的
                + lastest_api_keys | xfilter_(lambda api_key: api_key in api_keys)  # 存量有效的&按当前顺序
        )

        redis_client.delete(feishu_url)

    redis_client.rpush(feishu_url, *api_keys)

    api_keys_str = api_keys | xjoin('\n')
    send_message(f"{feishu_url}\n\n{api_keys_str}", title="更新api-keys")


if __name__ == '__main__':
    cli()  # https://api.deepseek.com/user/balance https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf\?sheet\=X0ZN3H
