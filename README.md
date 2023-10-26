# Tiled-map-processor
script to extract data from tiled_map_result.json in comfortable for further processing format.<br>
(script for processing data from https://www.mapeditor.org/ files)


## Usage example
### The minimal
Tiledmp has one reserved keyword ```tiles```, since it will be the name for json key, containing data about tiles<br>
in resulting file.<br>

```tiledmp input.json output.json tiles=layer1,layer2```<br>
Here there is only one option - ```tiles``` and it will contain data about tiles, extracted from ```layer1``` and ```layer2```.<br>
You should know there is no limit for number of layers. You can pass as many as you wish, but you should pass at least one.<br>
And ```tiles``` as key will have value, represented in form of list, containing tuples.<br>
For example:```(0,64,32)```, where 0 is tile code, and next values are x and y coordinates.<br>

### Extracting object layers
```tiledmp input.json output.json tiles=world bodies=land(x,y,width,height)```

In this example ```tiles``` will store data related to tiles that are stored in ```world``` layer.<br>
Also output.json will contain list connected to ```bodies``` key with list that stores data extracted from land layer.<br>
