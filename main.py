from apscheduler.schedulers.blocking import BlockingScheduler
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, time
from speedtest import Speedtest
import zoneinfo
import urllib
import os


# --------------------------------------------------- CONSTS --------------------------------------------------------- #


DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
TIMEZONE =  zoneinfo.ZoneInfo(os.getenv('TIMEZONE'))


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


def is_night_time():
    currtime = datetime.now(tz=timezone)
    now_time = currtime.time()
    return time(00, 00) <= now_time <= time(7, 00)


# -------------------------------------------------------------------------------------------------------------------- #


def do_speedtest():
    now = datetime.now(tz=timezone)

    if not has_network_connection() or is_night_time():
        print(f'{now} NightTime - Not running speed test')
        return

    print(f'{now} Running speed test')
    connection = Speedtest()

    connection.download()
    connection.upload()

    ping = connection.results.ping
    download = connection.results.download / 1024 / 1024
    upload = connection.results.upload / 1024 / 1024

    send_discord_message([
        {'Title': 'Latency', 'Content': f'The latency of the test was: {ping}ms', 'Color': 'fff38e'},
        {'Title': 'Download Speed', 'Content': f'The download speed is: {download:.2f}MB', 'Color': '6afff3'},
        {'Title': 'Upload Speed', 'Content': f'The upload speed is: {upload:.2f}MB', 'Color': 'bf71ff'}
    ])


# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(do_speedtest, 'interval', minutes=30, next_run_time=datetime.now())
    scheduler.start()

