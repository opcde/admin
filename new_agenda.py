"""
This script is used to create a new agenda for the last Tuesday of next month.
"""
import os
import sys
import json
import datetime
import requests

# Load the configuration from config.json
with open('config.json', encoding='utf-8') as f:
    config = json.load(f, encoding='utf-8')

if 'telegram_bot_token' not in config or 'telegram_chat_id' not in config:
    print('Missing entries in config.json!')
    sys.exit(1)

for meetings in ['general', 'board']:
    for doctypes in ['agendas', 'minutes']:
        # Check to make sure the directories exist
        if not os.path.exists(f'./{meetings}/{doctypes}'):
            print(f'Expected directory {meetings}/{doctypes} does not exist!')
            sys.exit(1)

    today = datetime.date.today()
    next_month = today.replace(day=1) + datetime.timedelta(days=32)
    last_tuesday = next_month.replace(day=1) - datetime.timedelta(days=1)
    while last_tuesday.weekday() != 1:
        last_tuesday -= datetime.timedelta(days=1)
    print(f'Last Tuesday of the month is {last_tuesday}')

    # Get the most recent agenda by ctime
    agendas = os.listdir(f'./{meetings}/agendas')
    agendas.sort(key=lambda x, m=meetings: os.path.getctime(f'./{m}/agendas/{x}'))
    most_recent = agendas[-1]

    print(f'Most recent agenda is {most_recent}')
    if not os.path.exists(f'./{meetings}/agendas/{last_tuesday}'):
        # Copy the most recent agenda to a new agenda for the last Tuesday
        #os.system(f'cp ./{meetings}/agendas/{most_recent} ./{meetings}/agendas/agenda_{last_tuesday}.md')
        print(f'Copied {most_recent} to agenda_{last_tuesday}.md')
        # Commit the new agenda
        os.system(f'git add ./{meetings}/agendas/agenda_{last_tuesday}.md')
        os.system(f'git commit -m "Add agenda for {last_tuesday}"')
        os.system('git push origin master')
        # Tell everyone on telegram
        print(f'Notifying telegram chat {config.telegram_chat_id}')
        result = requests.post(f'https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage', data={
            'chat_id': config.telegram_chat_id,
            'text': f'New {meetings} agenda for {last_tuesday} is available at {config.github_repo_base_url}/tree/master/{meetings}/agendas/agenda_{last_tuesday}.md'
        })
        if result.status_code != 200:
            print(f'Failed to notify telegram chat {config.telegram_chat_id}')
        else:
            print('Notified telegram chat successfully:')
            print(result.text)
    else:
        print(f'Agenda for {last_tuesday} already exists, exiting')
        sys.exit(0)
