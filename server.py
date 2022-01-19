from sanic import Sanic
from sanic.response import html, json, text
from shapely import geometry
import pandas as pd
import time
app = Sanic(__name__)
res = []


def checkdata(edge, px, py):
    isCorrect = True
    if len(px) != edge or len(py) != edge:
        res.append('ERROR:Array dimensions do not match edges')
        isCorrect = False
    for x in px:
        if x < -180 or x > 180:
            isCorrect = False
            res.append('ERROR:Illegal longitude data :' +
                       str(x))  # -180 <= longitude <= 180
    for y in py:
        if y < -90 or y > 90:
            isCorrect = False
            res.append('ERROR:Illegal latitude data :' +
                       str(y))  # -90 <= latitude <= 90
    # Determines whether the requested polygon area exceeds the limit
    t = getTuple(px, py)
    polygon = geometry.Polygon(t)
    limitarea = 8100 * 3
    if polygon.area > limitarea:
        area = polygon.area
        areastr = str(area)
        limitstr = str(limitarea)
        res.append('ERROR:The requested polygon area is too large' +
                   ' Request area = ' + areastr + ' Limit area = ' + limitstr)
        isCorrect = False
    if isCorrect:
        return True
    else:
        return False


def getTuple(px, py):  # return [(px, py)] datatype for polygon
    t = []
    pxytemp = []
    i = 0
    while i < len(px) and i < len(py):
        pxytemp.append(px[i])
        pxytemp.append(py[i])
        i += 1
        t.append(tuple(pxytemp))
        pxytemp = []
    return t


def GetData(px, py):
    # Grid
    # Gets the boundary value of the polygon
    lon1 = min(px)  # left boundary
    lon2 = max(px)  # right boundary
    lat1 = max(py)  # up boundary
    lat2 = min(py)  # down boundary
    # print(left)
    # print(right)
    # print(up)
    # print(down)
    sqLength = 20  # per unit square has 20 * 20 cellgrid
    step = sqLength * 30 / 3600  # size of unit square
    cellgrid = 30 / 3600  # size of gpw cell grid
    toplatitude = 90
    leftlontitude = -180
    linecount = 0
    lonStartIndex = int((lon1 - leftlontitude) / cellgrid)
    lonEndIndex = int((lon2 - leftlontitude) / cellgrid)
    TempData = []
    s = time.time()
    with open('alldata.file', 'r') as fr:
        while True:
            line = fr.readline()
            linecount += 1
            curlatitude = toplatitude - linecount * cellgrid
            if not line:
                break
            # current latitude is between lat1 and lat2
            if(curlatitude <= lat1 and curlatitude >= lat2):
                # remove \n and space from end of current line
                line = line[0:len(line) - 2]
                DataofLine = line.split(' ')
                # convert str to float
                DataofLine = list(map(float, DataofLine))
                TempData.append(DataofLine[lonStartIndex: lonEndIndex])
            elif(curlatitude < lat2):
                break
    e = time.time()
    print(e - s)
    print(len(TempData))
    print(len(TempData[0]))
    # print(lonEndIndex - lonStartIndex)

    # according to per 20 * 20 square, get sumdata longitude and latitude
    StartLat = lat1
    StartLon = lon1
    i = 0
    j = 0
    curi = 0
    curj = 0
    # get polygon data from pointx and ponity list
    polygon = geometry.Polygon(getTuple(px, py))
    print(polygon)
    while True:
        i = curi
        j = curj
        tempsum = []
        sum = 0
        if i < curi + sqLength and i < len(TempData) and j < curj + sqLength and j < len(TempData[0]):
            # get locations of four angles of the cell
            # from up to down, left to right
            point1 = (StartLon + curj * cellgrid, StartLat - curi * cellgrid)
            point2 = (point1[0] + sqLength * cellgrid, point1[1])
            point3 = (point2[0], point1[1] - sqLength * cellgrid)
            point4 = (point1[0], point3[1])
            # form tuple
            grid = [point1, point2, point3, point4]
            # get Polygon data
            curgrid = geometry.Polygon(grid)
            # get intersection part of two polygons
            intersectPart = curgrid.intersection(polygon)
            tempsum.append(StartLon + curj * cellgrid)
            tempsum.append(StartLat - curi * cellgrid)
        while intersectPart.area > 0.0 and i < curi + sqLength and i < len(TempData):
            j = curj
            while j < curj + sqLength and j < len(TempData[0]):
                sum += TempData[i][j]
                j += 1
            i += 1
        if intersectPart.area > 0.0:  # Only intersected and contained cells are counted
            # The intersecting parts get the average population of the corresponding ratio
            tempsum.append((intersectPart.area / curgrid.area) * sum)
            # if((intersectPart.area / curgrid.area) < 1):
            #     print(((intersectPart.area / curgrid.area)))
            res.append(tempsum)
        if curj + sqLength < len(TempData[0]):
            curj += sqLength
            continue
        # End of line, beginning at the beginning again
        elif curj + sqLength >= len(TempData[0]) and curi + sqLength < len(TempData):
            curi += sqLength
            curj = 0
        else:
            break


def process(edge, pointx, pointy):
    pointx = list(map(int, pointx))  # convert type 'str' to 'int'
    pointy = list(map(int, pointy))
    legal = checkdata(edge, pointx, pointy)  # illgal data check
    if legal:
        GetData(pointx, pointy)


@app.route("/population")
async def request(request):
    edge = int(request.args['edge'][0])
    pointx = (request.args['pointx'][0]).split(' ')
    pointy = (request.args['pointy'][0]).split(' ')
    # print(edge)
    # print(pointx)
    # print(pointy)
    process(edge, pointx, pointy)
    return json({"res": res})
if __name__ == "__main__":
    app.run(host="localhost", port=8080)
