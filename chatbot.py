from openai import OpenAI
client = OpenAI()

userMessage = input("What subject would you like to learn? ")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant. Respond in just a few sentences at most."},
        {"role": "user", "content": userMessage}
    ]
)

print(completion.choices[0].message.content)