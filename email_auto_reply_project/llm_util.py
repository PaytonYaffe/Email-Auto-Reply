from openai import OpenAI
from .settings import OPENAI_API_KEY  # adjust import path if needed

def generate_prompt(email_content: str) -> str:
    return f"""
    You are given an email. Extract the sender and receiver names.

    The receiver is who the email is addressed TO (usually at the beginning).
    The sender is who WROTE the email (typically at the end, after words like "Regards", "Best", "Thanks", or just their name).

    Email: "{email_content}"

    Respond with exactly the following format:

    Sender Name: [Sender's Name]
    Receiver Name: [Receiver's Name]
    Inquiry Questions: [
        [First inquiry question]
        [Second inquiry question]
        ...
    ]

    Ensure:
    - The "inquiry_questions" list contains only the extracted questions.
    - If there are no questions, return an empty list: "inquiry_questions": []

    """


def extract_sender_and_receiver_names(email_content: str):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = generate_prompt(email_content)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "developer",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    try:
        result = completion.choices[0].message.content.strip().split("\n")
        print(f"### ### ### ### OpenAI response: {result}")

        # Find sender and receiver by scanning for their labels
        sender_name = None
        receiver_name = None
        for line in result:
            if "Sender Name:" in line:
                sender_name = line.split(":")[1].strip()
            elif "Receiver Name:" in line:
                receiver_name = line.split(":")[1].strip()

    except Exception as e:
        print(f"Error extracting names from OpenAI response: {e}")
        sender_name = None
        receiver_name = None

    try:
        # Filter out bracket lines, empty lines, and header lines
        inquiry_questions = [
            line.strip() for line in result
            if line.strip()
            and line.strip() != "["
            and line.strip() != "]"
            and not line.strip().startswith("Sender")
            and not line.strip().startswith("Receiver")
            and not line.strip().startswith("Inquiry Questions")
        ]
        print(f" ### ### ### Extracted questions: {inquiry_questions=}")
    except Exception as e:
        print(f"Error extracting questions from OpenAI response: {e}")
        inquiry_questions = []

    return sender_name, receiver_name, inquiry_questions