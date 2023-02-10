import json
from PIL import Image, ImageDraw
import random

class GenerationMazeOutputImage:

    def __init__(self, jsonFile):
        self.__json = jsonFile
        self.__dataOfJson = None
        self.__percorsi = []
        self.__start = []
        self.__goal = None
        self.__movimentPath = []
        pass

    def getParamOnTheBestPath(self, keys):
        for i in range(len(keys)):
            self.__percorsi.append(self.__dataOfJson[i][keys[i][0]]["Opzione1"])
        for i in range(len(self.__percorsi)):
            if not self.__percorsi[i] == "NO WAY!":
                self.__start.append(self.__percorsi[i]["start"])
                self.__goal = self.__percorsi[i]["goal"]
                self.__movimentPath.append(self.__percorsi[i]["movimentPath"])
            else:
                self.__movimentPath.append("NO WAY!")

    def generateColorLine(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def generateGreyScale(self, value):
        value = value * value
        return (value, value, value)
    def invert_coordinates(self, point):
        x, y = point
        return (y, x)

    def createImageForAllPointStart(self, pathImgInput, pathImgOutput, breadcrumps):
        im = Image.open(pathImgInput)
        draw = ImageDraw.Draw(im)
        colorGoal = (255, 0, 0)
        for i in range(len(self.__movimentPath)):
            if not self.__movimentPath[i] == "NO WAY!":
                tuple_data = [(x[1], x[0]) for x in self.__movimentPath[i]]
                color = self.generateColorLine()
                draw.line(tuple_data, fill=color)
        draw.point(self.invert_coordinates(self.__goal), fill=colorGoal)
        converted_data = [(point[::-1], value) for point, value in breadcrumps]
        for i in range(len(converted_data)):
            draw.point(converted_data[i][0], self.generateGreyScale(converted_data[i][1]))
        im.save(pathImgOutput)

    def createImageForASpecifcStartPoint(self, pathImgInput, pathImgOutput, startPoint, breadcrumps):
        im = Image.open(pathImgInput)
        draw = ImageDraw.Draw(im)
        colorGoal = (255, 0, 0)
        if not self.__movimentPath[startPoint] == "NO WAY!":
            tuple_data = [(x[1], x[0]) for x in self.__movimentPath[startPoint]]
            color = self.generateColorLine()
            draw.line(tuple_data, fill=color)
            draw.point(self.invert_coordinates(self.__goal), fill=colorGoal)
            converted_data = [(point[::-1], value) for point, value in breadcrumps]
            for i in range(len(converted_data)):
                draw.point(converted_data[i][0], self.generateGreyScale(converted_data[i][1]))
        im.save(pathImgOutput)

    def openJson(self):
        with open(self.__json) as json_file:
            data = json.load(json_file)
            self.__dataOfJson = data
            myKeys = []
            for i in range(len(data)):
                myKeys.append(list(data[i]))
            return myKeys