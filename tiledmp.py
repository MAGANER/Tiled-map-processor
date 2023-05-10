import json
import sys


#first argument is input json-map
#second argument is output json-map
#
#and the start of argv list is the name of the script, so we skip it
def check_args():
    if len(sys.argv) != 3:
        print("not enough arguments!")
        exit(-1)

#this script processes only maps, stored in json files
def read_file():
    with open(sys.argv[1]) as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(str(e))
            exit(-1)

#constant values, used to compute actual position of tile in game
def extract_constans(data):
    return {"width":data["width"],"height":data["height"],"tile_width":data["tile_width"],"tile_height":data["tile_height"]}

def get_layer(number,data):
    if number <= len(data["layers"]):
        return data["layers"][number]["data"]
    #return empty list if number is out of length
    return []
def get_layer_by_name(name,data):
    for n in range(len(data["layers"])):
        if name in data["layers"][n]["name"]:
            return data["layers"][n]
    return []

#Tiled doesn't store map as matrix regular matrix,
#but it saves map(it's actually a matrix) in 1d array
#so first subsequence of array is first matrix line,
#second subsquence is second matrix line e.t.c.
#Every element of matrix is code of tile.

#get list of tile's code and it's position(in pixels)
def get_tiles(tile_layer,constants):
    positions = []
    for y in range(0,constants["height"]):
        for x in range(0,constants["width"]):
            code = tile_layer[y][x]
            #skip empty space
            if code != '0':
                x_pos = x*constans["tile_width"]
                y_pos = y*constans["tile_height"]
                positions.append((int(code),x_pos,y_pos))
    return positions
