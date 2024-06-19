from PBQA import DB, LLM
from time import strftime, time

import logging

logging.basicConfig(level=logging.INFO)

db = DB(path="examples/db")
db.load_pattern("examples/weather.yaml")
db.load_pattern("examples/conversation.yaml")

llm = LLM(db=db, host="192.168.0.137")
llm.connect_model(
    model="llama",
    port=8080,
    stop=["<|eot_id|>", "<|start_header_id|>"],
)
llm.connect_model(
    model="phi",
    port=8081,
    stop=[
        "<|end|>",
        "<|im_end|>",
        "<|endoftext|>",
        "<|end|>",
        "<|assistant|>",
        "<|user|>",
    ],
)

print(
    llm.ask(
        "Could I see the stars tonight?",
        "weather",
        "llama",
        external={"now": strftime("%Y-%m-%d %H:%M")},
    )
)

print(
    llm.ask(
        "Could I see the stars tonight?",
        "weather",
        "llama",
        external={"now": strftime("%Y-%m-%d %H:%M")},
    )
)

print(
    llm.ask(
        "Could I see the stars tonight?",
        "weather",
        "llama",
        external={"now": strftime("%Y-%m-%d %H:%M")},
    )
)
