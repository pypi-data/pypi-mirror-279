#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2024/6/7 17:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
import shortuuid
from meutils.pipe import *

from openai.types.chat import ChatCompletion as _ChatCompletion, ChatCompletionChunk as _ChatCompletionChunk
from openai.types.chat.chat_completion import Choice as _Choice, ChatCompletionMessage as _ChatCompletionMessage, \
    CompletionUsage as _CompletionUsage
from openai.types.chat.chat_completion_chunk import Choice as _ChunkChoice, ChoiceDelta


class CompletionUsage(_CompletionUsage):
    prompt_tokens: int = 1
    completion_tokens: int = 1
    total_tokens: int = 1


class ChatCompletionMessage(_ChatCompletionMessage):
    role: Literal["assistant"] = "assistant"
    """The role of the author of this message."""


class Choice(_Choice):
    index: int = 0
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"] = None


class ChatCompletion(_ChatCompletion):
    id: str = Field(default_factory=shortuuid.random)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion"
    usage: CompletionUsage = CompletionUsage()


class ChunkChoice(_ChunkChoice):
    index: int = 0


class ChatCompletionChunk(_ChatCompletionChunk):
    id: str = Field(default_factory=shortuuid.random)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion.chunk"


chat_completion = ChatCompletion(
    choices=[Choice(message=ChatCompletionMessage(content=""))]
)
chat_completion_chunk = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(content=""))]
)
chat_completion_chunk_stop = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(content=""), finish_reason="stop")]
)


# chat_completion.choices[0].message.content = "*"
# chat_completion_chunk.choices[0].delta.content = "*"


class ChatCompletionRequest(BaseModel):
    """
    prompt_filter_result.content_filter_results
    choice.content_filter_results

    todo: ['messages', 'model', 'frequency_penalty', 'function_call', 'functions', 'logit_bias', 'logprobs', 'max_tokens', 'n', 'presence_penalty', 'response_format', 'seed', 'stop', 'stream', 'temperature', 'tool_choice', 'tools', 'top_logprobs', 'top_p', 'user']
    """
    model: str = ''  # "gpt-3.5-turbo-file-id"

    # [{'role': 'user', 'content': 'hi'}]
    # [{'role': 'user', 'content':  [{"type": "text", "text": ""}]]
    # [{'role': 'user', 'content':  [{"type": "image_url", "image_url": ""}]] # 也兼容文件
    # [{'role': 'user', 'content':  [{"type": "file", "file_url": ""}]]
    messages: List[Dict[str, Any]] = [{'role': 'user', 'content': 'hi'}]

    temperature: Optional[float] = 1
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    stream: Optional[bool] = False
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    user: Optional[str] = None

    # 1106
    response_format: Optional[Any] = None
    function_call: Optional[Any] = None

    # 拓展字段
    last_content: Optional[Any] = None

    payload: Optional[Dict[str, Any]] = Field(default_factory=dict)  # 任意接口转chat api
    return_raw_response: Optional[bool] = None

    additional_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict)

    refs: List[str] = []
    file_ids: List[str] = []

    search: Optional[bool] = None
    use_search: Optional[bool] = None  # 自动推断联网

    # glm
    assistant_id: str = ""
    conversation_id: str = ""  # kimi、glm4

    # todo：设计apikey入参
    # rag

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if isinstance((last_content := self.messages[-1].get('content')), list):  # 多模态
        #     self.last_content = last_content
        self.last_content: str = self.messages[-1].get('content')  # 大部分时间等价于user_content

        if file_ids := self.file_ids or self.refs:
            self.file_ids = file_ids
            self.refs = file_ids

        if search := self.use_search or self.search:
            self.search = search
            self.use_search = search

        # glm
        self.assistant_id = self.assistant_id or "65940acff94777010aa6b796"

        # deeplx
        if self.model.startswith('deeplx'):
            self.payload = {
                "text": self.last_content,
                "source_lang": "auto",
                "target_lang": 'EN' if self.model.endswith('en') else 'ZH',
                **self.payload
            }

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "hi"
                        }
                    ],
                    "stream": False
                },

                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "请按照下面标题，写一篇400字的文章\n王志文说，一个不熟的人找你借饯，说明他已经把熟人借遍了。除非你不想要了，否则不要借"
                        }
                    ],
                    "stream": False
                },

                # url
                {
                    "model": "url-gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "总结一下https://mp.weixin.qq.com/s/Otl45GViytuAYPZw3m7q9w"
                        }
                    ],
                    "stream": False
                },

                # rag
                {
                    "messages": [
                        {
                            "content": "分别总结这两篇文章",
                            "role": "user"
                        }
                    ],
                    "model": "gpt-3.5-turbo",
                    "stream": False,
                    "file_ids": ["cn2a0s83r07am0knkeag", "cn2a3ralnl9crebipv4g"]
                }

            ]
        }
    }


if __name__ == '__main__':
    # print(ChatCompletion(choices=[Choice(message=ChatCompletionMessage(content="ChatCompletion"))]))
    # print(ChatCompletionChunk(choices=[ChunkChoice(delta=ChoiceDelta(content="ChatCompletionChunk"))]))
    #
    print(chat_completion)
    print(chat_completion_chunk)
    print(chat_completion_chunk_stop)
