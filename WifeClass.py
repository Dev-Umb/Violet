import linecache
import random
import sched
import threading
import time

import chardet
import nonebot
import requests
from zhon.hanzi import punctuation
from awesome.plugins.NewWife.random_config_index import *

GOD = 1149558764
LoveTalkList = list()
YanDereList = list()


# 老公类，用于绑定用户账号和计算渣男值
class husband:
    def __init__(self, ID: str):
        self.ID = ID
        self.FuckingBoy = 0

    def getClass(self):
        return self

    # 判断这个用户是不是渣男
    def isFuckingBoy(self) -> bool:
        return True if self.FuckingBoy > 20 else False


def Random(tuple: ()):
    return random.randint(0, len(tuple) - 1)


def WifeHair(HairColor: str, HairShape) -> str:
    return HairColor + HairShape


@nonebot.scheduler.scheduled_job(
    'cron',
    second=6
)
def getLoveTalk():
    threading.Thread(target=_getLove()).start()


def _getLove():
    url = "https://chp.shadiao.app/api.php"
    data = str(requests.get(url, timeout=3).text).encode('gbk').decode('gbk')
    if data in LoveTalkList: return
    with open('love.txt', 'a') as f:
        f.write(data + '\n')
        f.close()
    LoveTalkList.append(data)


# 老婆生成类
def is_rightful(word: str):  # 判断是不是阳间文字
    for ch in word:
        if not ('\u4e00' <= ch <= '\u9fff' or 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'):
            return False
    return True


import string

stri = 'today is friday, so happy..!!!'


def deletePunctuation(stri: str) -> str:  # 去除标点符号
    stri = stri.replace(' ', '').replace('\n', '')
    punctuation_string = string.punctuation
    for i in punctuation_string:
        stri = stri.replace(i, '')
    for i in punctuation:
        stri = stri.replace(i, '')
    return stri


class WifeObj:
    def getMarry(self) -> str:
        if self.liking > 100 and not self.isMerry:
            self.isMerry = True
        elif self.isMerry:
            return '我们已经结婚了哦'
        return MarriageVow[Random(MarriageVow)] if self.liking > 100 else '你太着急了，让我们再培养培养感情吧'

    def getDict(self) -> dict:
        return {
            'name': self.name,
            'age': self.age,
            'husband': self.husband.ID,
            'ouBai': self.ouBai,
            'height': self.height,
            'weight': self.weight,
            'character': self.Character,
            'bud': self.bud,
            'isMerry': self.isMerry,
            'liking': self.liking,
            'work': self.work,
            'race': self.race,
            'WifeNickName': self.WifeNickName,
            'HusbandNickName': self.HusbandNickName,
            'hair': self.Hair,
            'eyesColor': self.eyesColor
        }

    def setNickName(self, NickName: str, isWife: bool):
        NickName = deletePunctuation(NickName)
        if NickName in BanTalkMember:
            self.liking -= 2
            return '滚'
        if NickName in self.banNickName:
            return '我都说了我不要这个名字'
        if len(NickName) <= 1: return '?'
        if random.randint(0, self.liking) < 30 or not is_rightful(NickName) or len(NickName) >= 6:
            self.banNickName.append(NickName)
            return '好难听的名字，我不要'
        if isWife:
            self.WifeNickName = NickName
            return f'好'
        else:
            self.HusbandNickName = NickName
            return f'好的{self.HusbandNickName}'

    def __init__(self, thisHusband: husband):
        self.husband = thisHusband  # 绑定husband对象
        self.WifeNickName = '老婆'  # 你叫女朋友为‘老婆’
        self.HusbandNickName = "老公"  # 女朋友叫你,默认为老公
        self.eyesColor = Color[Random(Color)]  # 瞳色
        self.banNickName = list()
        self.work = work[Random(work)]  # 老婆的职业

        self.Hair = Color[Random(Color)] + Hair[Random(Hair)]  # 发型样式

        self.race = race[Random(race)]  # 种族

        self.name = surname[Random(surname)] + name[Random(name)]  # 姓名

        self.ouBai = ouBaiSize[Random(ouBaiSize)]

        self.Character = Character[Random(Character)]

        self.age = random.randint(16, 24)

        self.height = str(random.randint(150, 170) if self.race != '矮人' else random.randint(120, 140))

        self.weight = str(random.randint(40, 60))

        self.bud = Bud[Random(Bud)]

        self.liking = random.randint(0, 30)

        self.isMerry = False

        self.isTalk = False

        self.scence = None

        self.isMaxTalkNum = False

    # 最后把生成的对象添加到字典中
    def addInWifeDict(self):
        WifeDict[self.name] = self

    def getHusbandId(self) -> str:
        return self.husband.ID

    def getLoveScence(self) -> object:
        if self.isMaxTalkNum:
            self.liking -= 2 if self.liking > -100 else WifeDict.pop(self)
            if self.liking <= -100: return '你真的很烦，再见!'
            return '你烦不烦，做你自己的事情去'
        data = getScence(self) if self.scence is None else self.scence
        self.scence = getScence(self)
        self.isMaxTalkNum = True
        threading.Thread(target=self.Delay).start()
        return data.replace('你', self.HusbandNickName)

    def BanUser(self):
        self.isMaxTalkNum = False

    def Delay(self):  # 限制访问频率
        s = sched.scheduler(time.time, time.sleep)
        s.enter(10, 1, self.BanUser)
        s.run()

    def couples(self) -> str:
        WifeDict.pop(self.name)
        return f'{self.name}:{Couples[self.Character]}'

    def WifeIndex(self) -> str:
        return f'{self.name}\n' \
               f'性格：{self.Character}\n' \
               f'种族：{self.race}\n' \
               f'职业：{self.work}\n' \
               f'特点：{self.bud}\n' \
               f'头发：{self.Hair}\n' \
               f'瞳色：{self.eyesColor}\n' \
               f'胸围：{self.ouBai}\n' \
               f'身高：{self.height}cm\n' \
               f'体重：{self.weight}kg\n' \
               f'当前好感度：{self.liking}\n'


WifeDict = dict()


def getScence(self: WifeObj) -> str:
    if self.Character == '病娇':
        return YanDereList[random.randint(0, len(YanDereList) - 1)].replace('\n', '')
    data = LoveTalkList[random.randint(0, len(LoveTalkList) - 1)]
    return data.replace('\n', '')
