# Import libraries
import praw
import openai

# Set up Reddit credentials
reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent=os.environ["REDDIT_USER_AGENT"],
    username=os.environ["REDDIT_USERNAME"],
    password=os.environ["REDDIT_PASSWORD"],
)

# Set up OpenAI credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Choose a subreddit to monitor
subreddit = reddit.subreddit("test")

# Choose an OpenAI model to use
model = "chatgpt" # or "bing_chat"

# Define a function to generate a response from OpenAI
def generate_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}',
    }
    data = f'{{"model": "text-davinci-002", "prompt": "{prompt}", "temperature": 0.7, "max_tokens": 50, "stop": "\\n"}}'
    response = requests.post('https://api.openai.com/v1/engines/text-davinci-002/completions', headers=headers, data=data)
    response_text = response.json()['choices'][0]['text']
    return response_text

# Loop through new submissions in the subreddit
for submission in subreddit.stream.submissions():
    # Check if the submission title contains "u/gpt-bot"
    if "u/gpt-bot" in submission.title:
        # Extract the prompt from the title
        prompt = submission.title.split("u/gpt-bot")[1].strip()
        # Generate a response from OpenAI
        reply = generate_response(prompt)
        # Reply to the submission with the response
        submission.reply(reply)
