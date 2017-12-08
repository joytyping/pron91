#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'Liangmingli'
from girlatlas.GirlAtlas import GirlAtlas
from girlatlas.GirlAtlasDataBase import DatabaseManager
import time
from time import gmtime, strftime
import traceback
import sys, os

SLEEP_per_Album = 10
def main():
    ob = GirlAtlas()
    db = DatabaseManager()
    maxPageNumber = ob.fetchMaxPageNumber()
    db.updatePageSize(size=maxPageNumber)
    currentPageIndex = db.getDBPageIndex()

    readNum = maxPageNumber - currentPageIndex


    while readNum > 0:
        print('获取当前页:' + str(readNum))
        results = ob.fetchTargetPage(readNum)


        for result in results:
            id = result['albumId']
            url = result['albumURL']

            isAlbumExist = db.isAlbumExist(id)

            if isAlbumExist:
                # db.updateAlbum(result,0)
                print('')
            else:
                db.insertAlbum(result)

            picUrls=ob.fetchAlbum(url)

            for picUrl in picUrls:
                if db.isPictureExist(picUrl):
                    # db.updatePicture(picUrl,0)
                    print('')
                else:
                    db.insertPicture(id,picUrl)

        currentPageIndex = currentPageIndex + 1
        db.updatePageIndex(currentPageIndex)

        nowMaxPageNumber = ob.fetchMaxPageNumber()
        if (nowMaxPageNumber != maxPageNumber):
            pageDiff = nowMaxPageNumber - maxPageNumber
            currentPageIndex = currentPageIndex - pageDiff
            maxPageNumber = nowMaxPageNumber

        readNum = maxPageNumber - currentPageIndex

        time.sleep(SLEEP_per_Album)
        print('')


    print('End')



    return

def generateLogPath():

    pathName = os.path.dirname(sys.argv[0])

    strTime = strftime("%Y-%m-%d %H-%M-%S", gmtime())

    directory = pathName + "/crash/"
    logFilePath =  directory + strTime+"log.txt"

    if not os.path.exists(directory):
        os.makedirs(directory)
    return logFilePath

if __name__ == '__main__':
    logFilePath = generateLogPath()
    #This line opens a log file
    log = open(logFilePath, "w")
    try:

        main()
        # if AmIRunning():
        #     print("I am Running")
        # else:
        #     print("I am not Running")
        #     main()

    except Exception:
        traceback.print_exc(file=log)