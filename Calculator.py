# -*- coding:utf-8 -*-
from Mahjong import *
from Group import *
import copy


class Calculator(object):
    def __init__(self, handtiles, ting_tile, iszimo, melds=[]):
        assert len(handtiles) + len(melds) * 3 == 14
        self.funList = [dandiao, wuzi, queyimen, erwubajiang, pengfeng, laoshaofu, yibangao, siguiyi, minggang, angang,
                        bianzhang, kanzhang, lianliu, xixiangfeng, pinghu, self.buqiuren, self.menqing, self.zimo]
        self.handtiles = handtiles
        self.ting_tile = ting_tile
        self.iszimo = iszimo
        self.melds = melds
        self.fan = 0
        self.group = Group(handtiles, melds)
        self.group.judge()

    def presentCondition(self):
        print "*******************牌面情况*********************"
        print "手牌:",
        for tile in self.group.handtiles:
            print tile,
        print
        if len(self.group.melds) <> 0:
            print "吃碰杠:",
            for meld in self.group.melds:
                print meld.detail(),
            print
        print "成牌:",
        print self.ting_tile
        print "自摸",
        if (self.iszimo):
            print "是"
        else:
            print "否"

    def calculate(self):
        allFan = []
        allFanStr = []
        for result in self.group.allResult:
            fan = 0
            fanStr = []
            for fun in self.funList:
                fan += fun(self.ting_tile, result)
                if fun(self.ting_tile, result) > 0:
                    fanStr.append(presentFan(fun, self.ting_tile, result))
            allFan.append(fan)
            allFanStr.append(fanStr)
        index = allFan.index(max(allFan))
        print "*******************番数*********************"
        presentResult(self.ting_tile, self.group.allResult[index])
        for s in allFanStr[index]:
            print s
        print "总计:", str(allFan[index]) + "番"

    def buqiuren(self, ting_tile, result):
        assert len(result) == 5
        if self.iszimo == True:
            for meld in result:
                if meld.ismine == False: return 0
            return 4
        else:
            return 0

    buqiuren.__name__ = "不求人"
    buqiuren.__doc__ = 4

    def menqing(self, ting_tile, result):
        assert len(result) == 5
        if self.iszimo == False:
            for meld in result:
                if meld.ismine == False: return 0
            return 2
        else:
            return 0

    menqing.__name__ = "门清"
    menqing.__doc__ = 2

    def zimo(self, ting_tile, result):
        assert len(result) == 5
        if (self.buqiuren(ting_tile, result) == 0 and self.iszimo):
            return 1
        return 0

    zimo.__name__ = "自摸"
    zimo.__doc__ = 1


def presentResult(ting_tile, result):
    assert len(result) == 5
    print "成牌:", ting_tile
    for meld in result:
        print meld.detail(),
    print


def dandiao(ting_tile, result):
    assert len(result) == 5
    if (result[0].tiles[0].color == ting_tile.color and result[0].tiles[0].number == ting_tile.number):
        return 1
    else:
        return 0


dandiao.func_name = "单调"
dandiao.func_doc = 1


def wuzi(ting_tile, result):
    assert len(result) == 5
    total = resultToTotal(result)
    if (total[4][0] == 0 and total[5][0] == 0):
        return 1
    else:
        return 0


wuzi.func_name = "无字"
wuzi.func_doc = 1


def queyimen(ting_tile, result):
    assert len(result) == 5
    total = resultToTotal(result)
    temp = 0
    for i in range(1, 4):
        if total[i][0] == 0:
            temp += 1
    if temp == 1:
        return 1
    else:
        return 0


queyimen.func_name = "缺一门"
queyimen.func_doc = 1


def erwubajiang(ting_tile, result):
    assert len(result) == 5
    if (result[0].tiles[0].number in [2, 5, 8]):
        return 1
    else:
        return 0


erwubajiang.func_name = "二,五,八将"
erwubajiang.func_doc = 1


def pengfeng(ting_tile, result):
    assert len(result) == 5
    value = 0
    for meld in result:
        if (meld.__str__() == "碰" and meld.tiles[0].color == 5):
            value += 1
    return value


pengfeng.func_name = "碰风"
pengfeng.func_doc = 1


def laoshaofu(ting_tile, result):
    assert len(result) == 5
    value = 0
    total = resultToTotal(result)
    for color in range(1, 4):
        if (total[color][1] > 0 and total[color][2] > 0 and total[color][3] > 0 and total[color][7] > 0 and
                    total[color][8] > 0 and total[color][9] > 0):
            value += 1
        if (total[color][1] > 1 and total[color][2] > 1 and total[color][3] > 1 and total[color][7] > 1 and
                    total[color][8] > 1 and total[color][9] > 1): value += 1
    return value


laoshaofu.func_name = "老少副"
laoshaofu.func_doc = 1


def yibangao(ting_tile, result):
    assert len(result) == 5
    value = 0
    for i in range(0, 4):
        for j in range(i + 1, 5):
            if result[i].__str__() == "吃" and result[j].__str__() == "吃":
                if result[i].detail() == result[j].detail():
                    value += 1
    return value


yibangao.func_name = "一般高"
yibangao.func_doc = 1


def siguiyi(ting_tile, result):
    assert len(result) == 5
    value = 0
    total = resultToTotal(result)
    for meld in result:
        if meld.__str__() == "杠":
            color = meld.tiles[0].color
            number = meld.tiles[0].number
            total[color][number] -= 4
    for color in range(1, 6):
        for number in range(1, len(total[color])):
            if total[color][number] == 4:
                value += 1
    return value


siguiyi.func_name = "四归一"
siguiyi.func_doc = 1


def minggang(ting_tile, result):
    value = 0
    assert len(result) == 5
    for meld in result:
        if meld.__str__() == "杠" and meld.ismine == False:
            value += 1
    return value


minggang.func_name = "明杠"
minggang.func_doc = 1


def angang(ting_tile, result):
    value = 0
    assert len(result) == 5
    for meld in result:
        if meld.__str__() == "杠" and meld.ismine == True:
            value += 2
    return value


angang.func_name = "暗杠"
angang.func_doc = 2


def bianzhang(ting_tile, result):
    assert len(result) == 5
    if ting_tile.color in [1, 2, 3] and ting_tile.number in [3, 7]:
        for meld in result:
            if meld.ismine and meld.__str__() == "吃" and meld.tiles[0].color == ting_tile.color:

                if meld.tiles[-1].number == 3 and ting_tile.number == 3: return 1
                if meld.tiles[0].number == 7 and ting_tile.number == 7: return 1
    return 0


bianzhang.func_name = "边张"
bianzhang.func_doc = 1


def kanzhang(ting_tile, result):
    assert len(result) == 5
    for meld in result:
        if meld.ismine and meld.__str__() == "吃" and meld.tiles[0].color == ting_tile.color:
            if (meld.tiles[1].number == ting_tile.number): return 1
    return 0


kanzhang.func_name = "坎张"
kanzhang.func_doc = 1


def lianliu(ting_tile, result):
    assert len(result) == 5
    isover = True
    count = 0
    value = 0
    total = resultToTotal(result)
    for color in range(1, 4):
        count = 0
        for number in range(1, len(total[color])):
            if total[color][number] > 0:
                isover = False
                count += 1
            else:
                isover = True
                count = 0
            if count == 6:
                value += 1
                count = 0
                isover = True
    return value


lianliu.func_name = "连六"
lianliu.func_doc = 1


def xixiangfeng(ting_tile, result):
    assert len(result) == 5
    value = 0
    for i in range(0, 4):
        for j in range(i + 1, 5):
            if result[i].__str__() == "吃" and result[j].__str__() == "吃":
                if result[i].tiles[0].color <> result[j].tiles[0].color:
                    if result[i].tiles[0].number == result[j].tiles[0].number:
                        value += 1
    return value


xixiangfeng.func_name = "喜相逢"
xixiangfeng.func_doc = 1


def pinghu(ting_tile, result):
    assert len(result) == 5
    for meld in result[1:5]:
        if meld.__str__() <> "吃":
            return 0
    if (result[0].tiles[0].color in [1, 2, 3]):
        return 2
    else:
        return 0


pinghu.func_name = "平胡"
pinghu.func_doc = 2


def presentFan(fun, ting_tile, result):
    return fun.__name__ + "*" + str(fun(ting_tile, result) / fun.__doc__) + "  " + str(fun(ting_tile, result)) + "番"


def resultToTotal(result, allmineohter=1):
    total = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             4: [0, 0, 0, 0], 5: [0, 0, 0, 0, 0]}
    if allmineohter == 1:
        for meld in result:
            for tile in meld.tiles:
                total[tile.color][tile.number] += 1
        for i in range(1, 6):
            total[i][0] = sum(total[i][1:])
        return total
    elif allmineohter == 2:
        for meld in result:
            if meld.ismine:
                for tile in meld.tiles:
                    total[tile.color][tile.number] += 1
        for i in range(1, 6):
            total[i][0] = sum(total[i][1:])
        return total
    elif allmineohter == 3:
        for meld in result:
            if not (meld.ismine):
                for tile in meld.tiles:
                    total[tile.color][tile.number] += 1
        for i in range(1, 6):
            total[i][0] = sum(total[i][1:])
        return total


if __name__ == "__main__":
    tiles = []
    tiles.append(Mahjong(1, 1))
    tiles.append(Mahjong(1, 2))
    tiles.append(Mahjong(1, 3))
    tiles.append(Mahjong(1, 1))
    tiles.append(Mahjong(1, 2))
    tiles.append(Mahjong(1, 3))
    tiles.append(Mahjong(1, 7))
    tiles.append(Mahjong(1, 8))
    tiles.append(Mahjong(1, 9))
    # tiles.append(Mahjong(2, 7))
    # tiles.append(Mahjong(2, 8))
    # tiles.append(Mahjong(2, 9))
    tiles.append(Mahjong(3, 4))
    tiles.append(Mahjong(3, 4))
    m=[]
    m.append(Meld([Mahjong(2,7),Mahjong(2,8),Mahjong(2,9)]))
    c = Calculator(tiles, Mahjong(1, 1),True,m)
    c.presentCondition()
    c.calculate()
    # result = []
    # result.append(Meld([Mahjong(3, 1), Mahjong(3, 1)]))
    # result.append(Meld([Mahjong(2, 1), Mahjong(2, 2), Mahjong(2, 3)]))
    # result.append(Meld([Mahjong(2, 4), Mahjong(2, 5), Mahjong(2, 6)]))
    # result.append(Meld([Mahjong(5, 3), Mahjong(5, 3), Mahjong(5, 3)]))
    # result.append(Meld([Mahjong(1, 4), Mahjong(1, 4), Mahjong(1, 4), Mahjong(1, 4)], ismine=True))
    # ting_tile = Mahjong(2, 2)
    # presentFan(angang,ting_tile,result)
    # print dandiao(ting_tile, result)
    # print wuzi(ting_tile,result)
    # print queyimen(ting_tile,result)
    # print erwubajiang(ting_tile,result)
    # print pengfeng(ting_tile,result)
    # print laoshaofu(ting_tile,result)
    # print yibangao(ting_tile,result)
    # print minggang(ting_tile,result)
    # print lianliu(ting_tile, result)
    # print resultToTotal(result, allmineohter=1)
