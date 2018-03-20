
# -*- coding: utf-8 -*-

"""
array 一维数组
n 多维数组里，每一维的长度
"""
def oneDimToMultiDim(data,m):
    newArray=[]
    temp=[]
    for i in range(len(data)):
        temp.append(data[i])
        if i%m==m-1:
            newArray.append(temp)
            temp=[]
    if len(temp)>0:
        newArray.append(temp)
    return newArray


if __name__ == '__main__':
    
    #test OneDimToMultiDim
    L=[0,1,2,3,4,5,6,7,8,9]
    L=oneDimToMultiDim(L,5)
    print('x')