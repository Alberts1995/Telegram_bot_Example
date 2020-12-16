from unlocal import MysqlManager
import requests
import random
from datetime import datetime
from config_r import TOKEN

db = MysqlManager()



def viner():
    while True:
        s = datetime.now().today().strftime("%Y-%m-%d %H:%M:%S")
        for i in db.get_time():
            if str(i[4]) <= s and i[6] == "1":
                url = f'https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={i[1]}&message_id={i[5]}'
                req = requests.get(url)
                if i[8] == 'определиться случайно' and db.select_info_viner() == 0:
                    db.inser_status(i[5])
                elif i[8] == 'определиться случайно':
                    random_viner = []
                    for y in db.select_info_viner():
                        random_viner.append(y[2])
                    Shab_nav = random.choice(random_viner)
                    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={i[1]}&text={i[3]}: {Shab_nav}'
                    req = requests.get(url)
                    db.inser_status(i[5])
                    db.delet_draw(i[5])

                else:
                    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={i[1]}&text={i[3]}: {i[8]}'
                    req = requests.get(url)
                    db.inser_status(i[5])
                    db.delet_draw(i[5])
viner()