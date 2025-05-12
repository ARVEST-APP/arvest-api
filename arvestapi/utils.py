import json
import os
import datetime

def debug_print_response_body(rb, obj):
    if obj.debug:
        print(f"---\nDebug: {obj}")
        pretty_print_dict(rb, 1)
        print("---\n")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        write_json(rb, os.path.join(os.getcwd(), "debug", f"{current_time}_{obj}.json"))

def pretty_print_dict(d, level):
    tab = ""
    for i in range(level):
        tab = tab + " "
    for item in d:
        if isinstance(d[item], dict):
            pretty_print_dict(d[item], level + 1)
        else:
            print(f"{tab}{item} : {str(d[item])}")

def write_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def manifest_parser(manifest_data, type_chain = [], **kwargs):
    """
    A utility function for iteratively processing Manifest dict data.
    
    kwargs:
    - id_func: give a function that will treat an item if the item has and id field
    the function must have the following format: function(item, type_chain, args)
    - target_func: give a function that will treat an item if the item has a target field
    the function must have the following format: function(item, type_chain, args)
    """

    if "type" in manifest_data:
        type_chain.append(manifest_data["type"])
    else:
        type_chain.append("&&NO_TYPE")

    if kwargs.get("id_func", None) != None:
        if "id" in manifest_data:
            kwargs.get("id_func")(manifest_data, type_chain, kwargs.get("id_func_args", None))

    if kwargs.get("target_func", None) != None:
        if "target" in manifest_data:
            kwargs.get("target_func")(manifest_data, type_chain, kwargs.get("target_func_args", None))

    # Recursively treat other items:
    if "items" in manifest_data:
        for item in manifest_data["items"]:
            manifest_parser(item, type_chain, **kwargs)
    
    if "annotations" in manifest_data:
        if manifest_data["annotations"] != None:
            for item in manifest_data["annotations"]:
                manifest_parser(item, type_chain, **kwargs)
    
    if "body" in manifest_data:
        if manifest_data["body"] != None:
            manifest_parser(manifest_data["body"], type_chain, **kwargs)

    type_chain = type_chain.pop()