#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_api_key
# @Time         : 2024/6/17 08:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


@alru_cache()
async def check(api_key_or_token, check_url):
    headers = {
        "Authorization": f"Bearer {api_key_or_token}",
        "Accept": "application/json"
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=30) as client:

            if api_key_or_token.startswith("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9"):
                payload = {
                    "token": api_key_or_token
                }
                response: httpx.Response = await client.post(check_url, json=payload)  # free-api: POST /token/check
            else:
                response: httpx.Response = await client.get(check_url)

            # todo: 可扩展

            # logger.debug(response.text)

            return (
                    response.is_success and
                    response.json().get("is_available")  # deepseek
                    or response.json().get("status")  # moonshot
                    or response.json().get("live")  # free-api: POST /token/check
            )

    except httpx.RequestError as exc:
        logger.error(exc)
        return False


async def check_api_key_or_token(
        api_keys: Union[str, List[str]],
        check_url="https://api.deepseek.com/user/balance",
):
    """
        {
        "is_available": false,
        "balance_infos": [
            {
                "currency": "CNY",
                "total_balance": "-0.00",
                "granted_balance": "0.00",
                "topped_up_balance": "-0.00"
            }
        ]
        }
    """
    if isinstance(api_keys, str):
        api_keys = [api_keys]

    tasks = map(partial(check, check_url=check_url), tqdm(api_keys))
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    # responses = await asyncio.gather(*tasks)

    return responses


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_spreadsheet_values

    #
    # api_keys = get_spreadsheet_values(feishu_url="https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=lVghgx", to_dataframe=True)[0].tolist()
    # print(arun(check_deepseek_api_key(api_keys)))

    api_keys = os.getenv("DEEPSEEK_API_KEY")

    # print(arun(check_deepseek_api_key(api_keys)))

    print(arun(check_api_key_or_token("api_keys")))
