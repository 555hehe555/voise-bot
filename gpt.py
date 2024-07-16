from groq import Groq

client = Groq(
    api_key="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",
)

def generate(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

