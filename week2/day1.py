from openai import OpenAI
import dotenv
import os
import time
dotenv.load_dotenv()

# gpt
gpt_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# claude
claude_client = OpenAI(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com/v1/"
)


# gpt_response = gpt_client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
# )

# print(gpt_response.choices[0].message.content)

# claude_response = claude_client.chat.completions.create(
#     model="claude-3-haiku-20240307",
#     messages=[
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
# )

# print(claude_response.choices[0].message.content)

# assign system message to both the client, then make them talk to each other
gpt_messages = [
    {"role": "system", "content": "you are a assistant, you disagree with anything in the conversation and you challenge everything, in a snarky way."},
    {"role": "user", "content": "Hello, how are you?"}
]

claude_messages = [
    {"role": "system", "content": "you are a assistant, you try to agree with everything in the conversation and you keep the conversation going."},
]

# gpt_response = gpt_client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=gpt_messages
# )


# print(f"GPT: {gpt_response.choices[0].message.content}")

# claude_response = claude_client.chat.completions.create(
#     model="claude-3-haiku-20240307",
#     messages=claude_messages
# )

# print(f"Claude: {claude_response.choices[0].message.content}")


for i in range(5):
    gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=gpt_messages
    )
    gpt_text = gpt_response.choices[0].message.content
    gpt_messages.append({"role": "assistant", "content": gpt_text})
    claude_messages.append({"role": "user", "content": gpt_text})

    print(f"GPT: {gpt_text}")

    claude_response = claude_client.chat.completions.create(
        model="claude-3-haiku-20240307",
        messages=claude_messages
    )
    claude_text = claude_response.choices[0].message.content
    claude_messages.append({"role": "assistant", "content": claude_text})
    gpt_messages.append({"role": "user", "content": claude_text})

    print(f"Claude: {claude_text}")

    time.sleep(1)
    print("--------------------------------")