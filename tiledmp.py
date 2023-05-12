import json
import sys
import re

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
        if "data" in data["layers"][number]:
            return data["layers"][number]["data"]
        else:
            return data["layers"][number]["objects"]       
    #return empty list if number is out of length
    return []
def get_layer_by_name(name,data):
    for n in range(len(data["layers"])):
        if name in data["layers"][n]["name"]:
            if "data" in data["layers"][n]:
                return data["layers"][n]["data"]
            else:
                return data["layers"][n]["objects"]

    print("Warning: name '{}' wasn't found in the layer!".format(name))
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

#NOTE:left value "tiles" is kind of keyword, so it will be used to process tile data
def parse_args():
    args = sys.argv[3:]
    parsed = {}
    for a in args:
        left, right = a.split("=")
        parsed[left] = right
    return parsed

#cycle through all layers, containing tiles
# uniting them into one big tile data list
def get_tiles_layers(data,names,constants):
    tiles = []
    for n in names:
        try: 
            tiles = tiles + get_tiles(get_layer_by_name(n,data),constants)
        except Exception as e:
            print(str(e))
    return tiles

#get all dicts from specific layer, which name's value matches with one from list
def filter_layer_with_names(data,layer_name,names):
    layer = get_layer_by_name(layer_name,data)
    if not names or len(names) == 1 and names[0] == "":
        print("Warning:no names provided to filter {}!".format(layer_name))
        return layer
    else:
        return list(filter(lambda n:n["name"] in names,layer))

#get only required data from filtered layer
def extract_data(filtered_layer):
    new_data = []
    for d in filtered_layer:
        new_d = {}
        new_d["properties"] = d["properties"]
        new_d["width"] = d["width"]
        new_d["height"] = d["height"]
        new_d["x"] = d["x"]
        new_d["y"] = d["y"]
        new_d["name"] = d["name"]
        new_data.append(new_d)
    return new_data

#run script
if __name__ == "__main__":
    check_args()
    data = read_file()
    constants = extract_constans(data)
    args = parse_args()
    output = {}
    
    for key in args.keys():
        #process special reserved keyword and obtain tile
        if key == "tiles":
            output["tiles"] = get_tiles_layers(data,args[key],constants)
        else:
            val = args[key]
            pattern = re.compile(r"\(.*\)")
            m = pattern.search(val)
            
            #get objects with specific names
            if m:
                names = m.group(0)[1:-1]
                names = names.split(",")

                begin = m.span()[0]#get the begin of ( and then we can get the layer's name
                output[key] = extract_data(filter_layer_with_names(data,val[:begin-1],names))
            else:
                #get all
                output[key] = extract_data(filter_layer_with_names(data,val[:begin-1],[]))


    #write output into file
    output_file_name = sys.argv[2]
    with open(output_file_name,"w") as f:
        json.dump(output,f)
