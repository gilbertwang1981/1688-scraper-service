from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json
import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('aliCookieMonitor.yaml', 'r') as file:
    config = yaml.load(file)


def my_task():
    for user in config['aliCookie']['users']:
        data = json.dumps({"offerId": str(config['aliCookie']['offerId']), "userName": str(user)})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=config['aliCookie']['url'], data=data, headers=headers)

        if response.status_code != 200:
            robot = config['aliCookie']['robot']
            alert = {
                'msgtype': 'text',
                'text': {
                    'content': str('1688账号') + str(user) + str('异常探测结果：') + str(response.status_code)
                }
            }
            requests.post(robot, json=alert)


scheduler = BlockingScheduler()

scheduler.add_job(my_task, 'interval', seconds=config['aliCookie']['interval'])

scheduler.start()

