# -*- coding:utf-8 -*-
class Mahjong(object):
    color = 0
    number = 0
    color_dict = {1: "character", 2: "dot", 3: "bamboo", 4: "dragon", 5: "wind"}
    number_dict = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
    dragon_dict = {1:"中",2:"发",3:"白"}
    wind_dict={1:"东",2:"南",3:"西",4:"北"}
    def __init__(self,color,number):
        self.color=color
        self.number=number
    def __str__(self):
        if self.color_dict[self.color] == "character":
            return self.number_dict[self.number] + "万"
        if "bamboo" == self.color_dict[self.color]:
            if (self.number == 1):
                return "幺鸡"
            return self.number_dict[self.number] + "条"
        if (self.color_dict[self.color] == "dot"):
            return self.number_dict[self.number]+"筒"
        if (self.color_dict[self.color]=="dragon"):
            return self.dragon_dict[self.number]
        if (self.color_dict[self.color]=="wind"):
            return self.wind_dict[self.number]
    def compareTo(self,that):
        if (self.color<that.color): return -1
        if (self.color>that.color): return 1
        if (self.number<that.number): return -1
        if (self.number>that.number): return 1
        return 0
class Meld(object):
    def __init__(self,tiles,ismine=True):
        self.ismine=ismine
        self.tiles=tiles
        self.sort(self.tiles)
        assert self.judge()!=0
        self.meld_dict={0:"Error",1:"碰",2:"吃",3:"杠",4:"将"}
    def sort(self,tiles):
        for i in list(range(len(tiles)-1)):
            for j in list(range(i+1,len(tiles))):
                if(tiles[i].compareTo(tiles[j])>0):
                    tiles[i],tiles[j]=tiles[j],tiles[i]
    def judge(self):
        if len(self.tiles)==3:
            if self.tiles[0].color==self.tiles[1].color==self.tiles[2].color:
                if self.tiles[0].number==self.tiles[1].number==self.tiles[2].number:
                    return 1
                if (self.tiles[0].number+1==self.tiles[1].number)&(self.tiles[1].number+1==self.tiles[2].number):
                    return 2
        if len(self.tiles)==4:
            if self.tiles[0].color==self.tiles[1].color==self.tiles[2].color==self.tiles[3].color:
                if self.tiles[0].number==self.tiles[1].number==self.tiles[2].number==self.tiles[3].number:
                    return 3
        if len(self.tiles)==2:
            if self.tiles[0].compareTo(self.tiles[1])==0:
                return 4
        return 0
    def __str__(self):
        return self.meld_dict[self.judge()]
    def detail(self):
        detail=self.meld_dict[self.judge()]+":"
        for tile in self.tiles:
            detail+=tile.__str__()+" "
        return detail
if(__name__=='__main__'):
    tiles=[];
    tiles.append(Mahjong(1,1))
    tiles.append(Mahjong(1,1))
    for i in tiles:
        print i
    meld=Meld(tiles)
    print meld
    print meld.detail()