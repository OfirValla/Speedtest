from apscheduler.schedulers.blocking import BlockingScheduler
from discord_webhook import DiscordWebhook, DiscordEmbed
from speedtest import Speedtest
from datetime import datetime
import urllib
import os


# --------------------------------------------------- CONSTS --------------------------------------------------------- #


DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')


# --------------------------------------------------- METHODS -------------------------------------------------------- #


def send_discord_message(sections):
    if type(sections) is not list:
        sections = [sections]

    webhook = DiscordWebhook(url=DISCORD_WEBHOOK, username='Speedtest')
    for section in sections:
        embed = DiscordEmbed(title=section['Title'],
                             description=section['Content'],
                             color=section['Color'])
        webhook.add_embed(embed)

    webhook.execute()


# -------------------------------------------------------------------------------------------------------------------- #

def has_network_connection(host='https://www.google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


# -------------------------------------------------------------------------------------------------------------------- #


def do_speedtest():
    if not has_network_connection():
        return

    connection = Speedtest()

    connection.download()
    connection.upload()

    ping = connection.results.ping
    download = connection.results.download / 1024 / 1024
    upload = connection.results.upload / 1024 / 1024

    send_discord_message([
        {'Title': 'Latency', 'Content': f'The latency of the test was: {ping}ms', 'Color': '03b2f8'},
        {'Title': 'Download Speed', 'Content': f'The download speed is: {download:.2f}MB', 'Color': '03b2f8'},
        {'Title': 'Upload Speed', 'Content': f'The upload speed is: {upload:.2f}MB', 'Color': '03b2f8'}
    ])


# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(do_speedtest, 'interval', minutes=30, next_run_time=datetime.now())
    scheduler.start()

