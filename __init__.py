import asyncio
import json
import re
import threading
import nonebot
from nonebot import on_command, NLPSession, on_startup, on_natural_language
from nonebot.command import Command, CommandSession
from .WifeClass import *
import difflib


def get_equal_rate(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


async def WriteToWifesIndex():
    with open('index.json', 'w+', encoding='utf-8') as f:
        src = '['
        for key in WifeDict:
            Wifejson = json.dumps(WifeDict[key].getDict(), ensure_ascii=False)
            src += Wifejson + ',\n'
        src += ']'
        src = src.replace(',\n]', ']')
        f.write(src)
        f.close()


def Read():
    try:
        with open('index.json', 'r+', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = str(line).replace('[', '').replace(',\n', '').replace(']', '')
                t = json.loads(line)
                user_id = husband(t['husband'])
                temp_wife = WifeObj(user_id)
                temp_wife.height = t['height']
                temp_wife.weight = t['weight']
                temp_wife.name = t['name']
                temp_wife.ouBai = t['ouBai']
                temp_wife.liking = t['liking']
                temp_wife.Character = t['character']
                temp_wife.age = t['age']
                temp_wife.isMerry = t['isMerry']
                temp_wife.work = t['work']
                temp_wife.race = t['race']
                temp_wife.bud = t['bud']
                try:
                    temp_wife.Hair = t['hair']
                    temp_wife.eyesColor = t['eyesColor']
                    temp_wife.WifeNickName = t['WifeNickName'] if not t['WifeNickName'] in BanTalkMember else '老婆'
                    temp_wife.HusbandNickName = t['HusbandNickName'] if not t[
                                                                                'HusbandNickName'] in BanTalkMember else '老公'
                except:
                    pass
                temp_wife.addInWifeDict()
                line = f.readline()
            f.close()
    except:
        with open('index.json', 'a+', encoding='utf-8') as f:
            f.close()



def ReadLove():
    try:
        f = open('love.txt', 'r')
        a = f.readline()
        while a:
            if not a in LoveTalkList:
                LoveTalkList.append(a)
            a = f.readline()
    except:
        f = open('love.txt', 'w+')
        f.close()
    try:
        f = open('yandere.txt', 'r',encoding='utf-8')
        a = f.readline().encode('utf-8').decode('utf-8')
        while a:
            if not a in YanDereList:
                YanDereList.append(a)
            a = f.readline()
    except:
         f = open('love.txt', 'w+')
         f.close()

@on_startup(func=Read)
@on_startup(func=ReadLove)
@on_command('getLove', only_to_me=True, aliases=('求分配女朋友'))
async def getGirlFirend(session: CommandSession):
    try:
        UserWife: WifeObj = await searchWife(session, True)
        await session.send(f'你已经有{UserWife.name}了', at_sender=True)
        return
    except:
        user = session.event['user_id']
        t = WifeObj(husband(user))
        await session.send(f'我是{t.name},我愿意与你在一起，今后请多关照')
        t.addInWifeDict()
        await WriteToWifesIndex()
        return


bot = nonebot.get_bot()


async def searchWife(session: CommandSession, isFirst: bool):
    id = session.event['user_id']
    for key in WifeDict:
        if WifeDict[key].husband.ID == id:
            return WifeDict[key]
    else:
        if not isFirst:
            await session.send(at_sender=True, message='你还没有女朋友呢，发送“求分配女朋友”来让上帝赐你一位吧，记得要好好珍惜')
        return -1


@on_command('couple', only_to_me=False, aliases='分手')
async def couple(session: CommandSession):
    try:
        UserWife: WifeObj = await searchWife(session, False)
        src = UserWife.couples()
        await session.send(at_sender=True, message=src)
        threading.Thread(target=save).start()
    except:
        pass


@on_command('help', only_to_me=False, aliases=('!help', '！help'))
async def help(session: CommandSession):
    await session.send(message='1.查询女朋友的信息\n'
                               '2.求分配女朋友\n'
                               '3.分手\n'
                               '4.呼叫女朋友的名or近似名\n'
                               '5.呼叫女朋友的昵称\n'
                               '6.老婆以后叫我+空格+昵称（请合法使用昵称）\n'
                               '7.老婆以后我叫你+空格+昵称（请合法使用昵称）\n')


@on_command('WifeCallToHusband', only_to_me=False, aliases='老婆以后叫我')
async def WifeCallToHusband(session: CommandSession):
    masg = session.current_arg_text.replace('老婆以后叫我', '')
    try:
        UserWife: WifeObj = await searchWife(session, False)
        await session.send(UserWife.setNickName(masg, isWife=False))
    except:
        return


@on_command('HusbandCallToWife', only_to_me=False, aliases='老婆以后我叫你')
async def HusbandCallToWife(session: CommandSession):
    masg = session.current_arg_text.replace('老婆以后我叫你', '')
    try:
        UserWife: WifeObj = await searchWife(session, False)
        await session.send(UserWife.setNickName(masg, isWife=True))
    except:
        return


@on_command('BanNickName', only_to_me=True, aliases='添加违禁词')
async def HusbandCallToWife(session: CommandSession):
    if session.event['user_id'] == GOD:
        masg = session.current_arg_text
        try:
            BanTalkMember.append(masg)
            await session.send(f'添加{masg}成功')
        except:
            return


@on_command('getWifeIndex', only_to_me=False, aliases='查询女朋友的信息')
async def getWifeIndex(session: CommandSession):
    try:
        userWife: WifeObj = await searchWife(session, False)
    except:
        return
    await bot.send_private_msg(user_id=userWife.husband.ID, message=userWife.WifeIndex())
    await session.send(at_sender=True, message='已经将我的信息私给你了，要~保~密~哦')
    await WriteToWifesIndex()


@on_natural_language(only_to_me=False)
async def CallWife(session: NLPSession):
    t1 = threading.Thread(target=sayLoving, args=(session,))
    t1.start()


def save():
    loop = asyncio.new_event_loop()
    a = WriteToWifesIndex()
    loop.run_until_complete(a)


def sayLoving(session: NLPSession):
    msg = session.msg_text
    if re.search('CQ:', msg) is not None or not 1 < len(msg) <= 10: return
    sendUser = session.event['user_id']
    try:
        if WifeDict[msg].husband.ID == sendUser:
            sendLove(WifeDict[msg], session)
        return
    except:
        pass
    Max: float = 0.4  # 先定相似度
    for key in WifeDict:
        t = get_equal_rate(key, msg)
        if (Max < t or msg == WifeDict[key].WifeNickName) and sendUser == WifeDict[key].getHusbandId():
            sendLove(WifeDict[key], session)
            threading.Thread(target=save).start()
            return


def sendLove(A: WifeObj, session: NLPSession):
    loop = asyncio.new_event_loop()
    a = session.send(at_sender=True, message=f'{A.name}:{A.getLoveScence()}')
    A.liking += 2 if A.liking < 200 else 0
    loop.run_until_complete(a)
