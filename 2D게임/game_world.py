
# layer 0: Background Objects
# layer 1: Foreground Objects
# layer 2: bullet Objects
# layer 3: monster Objects
objects = [[], [], [], []]


def add_object(o, layer):
    objects[layer].append(o)


def add_objects(l, layer):
    for o in l:
        add_object(o, layer)


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            return


def Return_layer2_obj():
    return objects[2]

def Return_layer3_obj():
    return objects[3]

def clear():
    for o in all_objects():
        del o
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

