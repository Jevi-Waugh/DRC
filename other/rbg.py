colours = {"dark_blue_purple" : [75,0,130],
        "light_blue" : [240,248,255],
        "Light_purple" : [230,230,250],
        "Light_yellow" : [255,255,224],
        "Dark_yellow" : [51,51,0] }
        
for keys, items in colours.items():
    items = items[::-1]
    print(items)