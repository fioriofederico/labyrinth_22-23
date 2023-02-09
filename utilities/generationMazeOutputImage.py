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
            self.__start.append(self.__percorsi[i]["start"])
            self.__goal = self.__percorsi[i]["goal"]
            self.__movimentPath.append(self.__percorsi[i]["movimentPath"])

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
            tuple_data = [(x[1], x[0]) for x in self.__movimentPath[i]]
            color = self.generateColorLine()
            draw.line(tuple_data, fill=color)
        draw.point(self.invert_coordinates(self.__goal), fill=colorGoal)
        converted_data = [(point[::-1], value) for point, value in breadcrumps]
        for i in range(len(converted_data)):
            draw.point(converted_data[i][0], self.generateGreyScale(converted_data[i][1]))
        im.save(pathImgOutput)

    def createMultiImageForPath(self, pathImgInput, pathImgOutput, breadcrumps):
        im = Image.open(pathImgInput)
        colorGoal = (255, 0, 0)
        print(len(self.__movimentPath))
        for i in range(len(self.__movimentPath)):
            tuple_data = [(x[1], x[0]) for x in self.__movimentPath[i]]
            color = self.generateColorLine()
            new_im = im.copy()
            draw = ImageDraw.Draw(new_im)
            draw.line(tuple_data, fill=color)
            draw.point(self.invert_coordinates(self.__goal), fill=colorGoal)
            converted_data = [(point[::-1], value) for point, value in breadcrumps]
            for i in range(len(converted_data)):
                draw.point(converted_data[i][0], self.generateGreyScale(converted_data[i][1]))
                new_im.save(f"{pathImgOutput}_{i}.tiff")

    def openJson(self):
        with open(self.__json) as json_file:
            data = json.load(json_file)
            self.__dataOfJson = data
            myKeys = []
            for i in range(len(data)):
                myKeys.append(list(data[i]))
            return myKeys