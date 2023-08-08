'''
Code based on https://gist.github.com/benoit-cty/a5855dea9a4b7af03f1f53c07ee48d3c
Script to archive Slack messages from a channel list.
You have to create a Slack Bot and invite to private channels.
View https://github.com/docmarionum1/slack-archive-bot for how to configure your account.
Then provide the bot token to this script with the list of channels.
'''

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json, os

# don't put the bot token where it winds up in github
TOKEN = os.environ['TOKEN']

channels = {
    'general': 'CG7UZ382H',
    'bioinformatics': 'CG7HJ2620',
    'random': 'CG92GAGR4'
}

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=TOKEN)
# Store conversation history
conversation_history = []


def backup_channel(channel_name, channel_id):
    '''
    :channel_id: ID of the channel you want to send the message to
    '''
    try:
        print('Getting messages from', channel_name)
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated
        result = client.conversations_history(channel=channel_id)
        all_message = []
        all_message += result["messages"]
        while result['has_more']:
            print("\tGetting more...")
            result = client.conversations_history(channel=channel_id, cursor=result['response_metadata']['next_cursor'])
            all_message += result["messages"]
        # Save to disk
        filename = f'{channel_name}.json'
        print(f'  We have downloaded {len(all_message)} messages from {channel_name}.')
        print('  Saving to', filename)
        with open(filename, 'w') as outfile:
            json.dump(all_message, outfile)
    except SlackApiError as e:
        print("Error using conversation: {}".format(e))


if __name__ == "__main__":
    # Iterate channels
    for chan_name, chan_id in channels.items():
        backup_channel(chan_name, chan_id)
