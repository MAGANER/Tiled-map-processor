import json
import sys


#first argument is input json-map
#second argument is output json-map
#
#and the start of argv list is the name of the script, so we skip it
def check_args():
    if not len(sys.argv) >= 3:
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
    return data

#constant values, used to compute actual position of tile in game
def extract_constans(data):
    return {"width":data["width"],"height":data["height"],"tile_width":data["tilewidth"],"tile_height":data["tileheight"]}

def get_layer(number,data):
    if number <= len(data["layers"]):
        return data["layers"][number]["data"]
    #return empty list if number is out of length
    return []
def get_layer_by_name(name,data):
    for n in range(len(data["layers"])):
        if name in data["layers"][n]["name"]:
            return data["layers"][n]["data"]
    return []


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#Tiled doesn't store map as matrix regular matrix,
#but it saves map(it's actually a matrix) in 1d array
#so first subsequence of array is first matrix line,
#second subsquence is second matrix line e.t.c.
#Every element of matrix is code of tile.

#get list of tile's code and it's position(in pixels)
def get_tiles(tile_layer,constants):
    #skip empty layers
    if not tile_layer:
        return []

    #convert layer into matrix
    tile_layer = list(chunks(tile_layer,constants["width"]))
    
    positions = []#result is stored here
    for y in range(0,constants["height"]):
        for x in range(0,constants["width"]):
            code = tile_layer[y][x]
            #skip empty space
            if code != '0':
                x_pos = x*constants["tile_width"]
                y_pos = y*constants["tile_height"]
                positions.append((int(code),x_pos,y_pos))
    return positions

#left value is name of list that will appear in output file
#right one is list of layers' names from input file
#NOTE:left value "tiles" is kind of keyword, so it will be used
#to process tile data
def parse_args():
    args = sys.argv[3:]
    parsed = {}
    for a in args:
        left, right = a.split("=")
        right = right.split(",")
        parsed[left] = right
    return parsed



def get_tiles_layers(data,names,constants):
    tiles = []
    for n in names:
        try: 
            tiles = tiles + get_tiles(get_layer_by_name(n,data),constants)
        except Exception as e:
            print(str(e))
    return tiles

#run script
if __name__ == "__main__":
    check_args()
    data = read_file()
    constants = extract_constans(data)
    args = parse_args()

    output = {}
    for key in args.keys():
        if key == "tiles":
            output["tiles"] = get_tiles_layers(data,args[key],constants)
    print(output["tiles"])
    
