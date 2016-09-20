# -*- coding:utf-8 -*-
from Mahjong import Meld
from Mahjong import Mahjong
class Group(object):
    #各种组合方法#############################################################################
    def totalToResult_jiang(self,color,number):        #对子
        assert self.total[color][number]>=2
        temp=[]
        temp.append(Mahjong(color,number))
        temp.append(Mahjong(color,number))
        meld=Meld(temp)
        self.result.append(meld)
        self.total[color][number]-=2
        self.handtiles=self.totalToTiles(self.total)
    def resultToTotal_jiang(self,index):
        meld=self.result[index]
        assert meld.__str__()=='将'
        color=meld.tiles[0].color
        number=meld.tiles[0].number
        self.total[color][number]+=2;
        self.result.pop(index)
        self.handtiles=self.totalToTiles(self.total)
    def totalToResult_ke(self,color,number):           #刻
        assert self.total[color][number] >= 3
        temp = []
        temp.append(Mahjong(color, number))
        temp.append(Mahjong(color, number))
        temp.append(Mahjong(color,number))
        meld = Meld(temp)
        self.result.append(meld)
        self.total[color][number]-=3
        self.handtiles = self.totalToTiles(self.total)
    def resultToTotal_ke(self,index):
        meld = self.result[index]
        assert meld.__str__() == '碰'
        color = meld.tiles[0].color
        number = meld.tiles[0].number
        self.total[color][number] += 3;
        self.result.pop(index)
        self.handtiles = self.totalToTiles(self.total)
    def totalToResult_shun(self,color,number):      #顺子
        assert number<=7
        assert self.total[color][number]>=1
        assert self.total[color][number+1]>=1
        assert self.total[color][number+2]>=1
        temp=[]
        temp.append(Mahjong(color,number))
        temp.append(Mahjong(color, number+1))
        temp.append(Mahjong(color, number+2))
        meld=Meld(temp)
        self.result.append(meld)
        self.total[color][number]-=1
        self.total[color][number+1] -= 1
        self.total[color][number+2] -= 1
        self.handtiles = self.totalToTiles(self.total)
    def resultToTotal_shun(self,index):
        meld =self.result[index]
        assert meld.__str__()=='吃'
        color=meld.tiles[0].color
        number=meld.tiles[0].number
        self.total[color][number]+=1
        self.total[color][number+1] += 1
        self.total[color][number+2] += 1
        self.result.pop(index)
        self.handtiles = self.totalToTiles(self.total)
    def resultToTotal(self,index):
        meld=self.result[index]
        if meld.__str__()=="吃":
            self.resultToTotal_shun(index)
        if meld.__str__()=="碰":
            self.resultToTotal_ke(index)
        if meld.__str__()=="将":
            self.resultToTotal_jiang(index)
    #各种组合方法##################################################################################




    #牌组与表之间的转换#############################################################################
    def tilesToTotal(self,tiles):          #牌组转换至统计表
        total={1:[0,0,0,0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0,0,0,0],3:[0,0,0,0,0,0,0,0,0,0],4:[0,0,0,0],5:[0,0,0,0,0]}
        for tile in tiles:
            total[tile.color][tile.number]+=1
        for i in range(1,6):
            total[i][0]=sum(total[i][1:])
        return total
    def totalToTiles(self,total):          #统计表转换成牌组
        tiles=[]
        for i in range(1,6):
            t=0
            for j in total[i][1:]:
                t+=1
                for k in range(j):
                    tiles.append(Mahjong(i,t))
        return tiles
    #牌组与表之间的转换#############################################################################





    def __init__(self,handtiles,melds=[]):
        self.allResult=[]                           #所有的胡牌结果
        self.result=[]                              #临时存储胡牌结果   元素为Meld
        self.allTiles=[]
        self.melds=melds                            #原有的吃碰或杠
        self.handtiles=handtiles                    #手牌
        self.sort(handtiles)                        #排序
        for tile in self.handtiles:
            self.allTiles.append(tile)
        for meld in self.melds:
            for tile in meld.tiles:
                self.allTiles.append(tile)
        self.total=self.tilesToTotal(handtiles)     #统计
        self.allTotal=self.tilesToTotal(self.allTiles)
        assert len(self.melds)*3+len(handtiles)==14 #判断先决条件
    def sort(self, tiles):
        for i in range(len(tiles) - 1):
            for j in range(i + 1, len(tiles)):
                if (tiles[i].compareTo(tiles[j]) > 0):
                    tiles[i], tiles[j] = tiles[j], tiles[i]



    def back(self):                                 #退回至只有将牌的情况
        while(len(self.result)>1):
            if(self.result[-1].__str__!='将'):
                self.resultToTotal(-1)





    def judge(self):                                #将将牌提取出来
        for color in range(1,6):
            for number in range(1,len(self.total[color])):
                if (self.total[color][number]>=2):
                    self.totalToResult_jiang(color,number)
                    self.analyse();
                    self.resultToTotal_jiang(0)
                    assert len(self.result)==0


    def analyse(self):                              #分析剩下的3n张牌是否满足胡牌条件
        if len(self.handtiles)==0:
            copy={"Own":[],"Attach":[]}
            for meld in self.result:
                copy["Own"].append(meld)
            for meld in self.melds:
                copy["Attach"].append(meld)
            self.allResult.append(copy)
            self.back()
            return
        color=self.handtiles[0].color
        number=self.handtiles[0].number
        if (self.total[color][number]in[1,2]):
            if ((color in [4,5]) or number+2>9 or self.total[color][number+1]==0 or self.total[color][number+2]==0):
                self.back()
                return
            else:
                self.totalToResult_shun(color,number)
                self.analyse()
        elif(self.total[color][number]==3):
            self.totalToResult_ke(color,number)
            self.analyse()
        elif(self.total[color][number]==4):
            if ((color in [4,5]) or number+2>9 or self.total[color][number+1]==0 or self.total[color][number+2]==0):
                self.back()
                return
            else:

                self.totalToResult_shun(color,number)
                self.totalToResult_ke(color,number)
                self.analyse()
        self.back()


def tilesToTotal(tiles):  # 牌组转换至统计表
    total = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             4: [0, 0, 0, 0], 5: [0, 0, 0, 0, 0]}
    for tile in tiles:
        total[tile.color][tile.number] += 1
    for i in range(1, 6):
        total[i][0] = sum(total[i][1:])
    return total



def ting(tiles,melds=[]):
    ting_tiles=[]
    assert len(tiles)+len(melds)*3==13

    allTiles=[]
    for tile in tiles:
        allTiles.append(tile)
    for meld in melds:
        for tile in meld.tiles:
            allTiles.append(tile)
    allTotal=tilesToTotal(allTiles)
    tile_num={1:9,2:9,3:9,4:3,5:4}
    for color in range(1,6):
        for number in range(1,tile_num[color]+1):
            if allTotal[color][number]<=4:
                tiles.append(Mahjong(color,number))
                group=Group(tiles,melds)
                group.judge()
                if len(group.allResult)>0:
                    ting_tiles.append(Mahjong(color,number))
                for i in range(len(tiles)):
                    if (tiles[i].color==color and tiles[i].number==number):
                        tiles.pop(i)
                        break
    return ting_tiles
if(__name__=='__main__'):
    tiles=[]
    tiles.append(Mahjong(1,1))
    tiles.append(Mahjong(1, 1))
    tiles.append(Mahjong(1, 1))
    tiles.append(Mahjong(1, 2))
    tiles.append(Mahjong(1, 3))
    tiles.append(Mahjong(1, 4))
    tiles.append(Mahjong(1, 5))
    tiles.append(Mahjong(1, 6))
    tiles.append(Mahjong(1, 7))
    tiles.append(Mahjong(1,8))
    tiles.append(Mahjong(1,9))
    tiles.append(Mahjong(1, 9))
    tiles.append(Mahjong(1,9))
    # meld=[]
    # meld.append(Mahjong(4,1))
    # meld.append(Mahjong(4, 1))
    # meld.append(Mahjong(4, 1))
    # meld.append(Mahjong(4, 1))
    # meld=Meld(meld)
    hehe=ting(tiles)
    for tile in hehe:
        print tile,
    # group=Group(tiles,[meld])
    # group.judge()
    # for tile in group.handtiles:
    #     print tile,
    # if len(group.melds)>0:
    #     for meld in group.melds:
    #         print meld.detail(),
    # print
    # for result in group.allResult:
    #     for kind in result:
    #         for meld in result[kind]:
    #             print kind,meld.detail()
    # for tile in group.allTiles:
    #     print tile,
    # print
    # for color in range(1,6):
    #     for number in group.allTotal[color]:
    #         print number,
    #     print