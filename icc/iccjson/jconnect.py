import jsonschema
from jsonschema import validate
import json
import os


def get_json(json_path):
    json_data = ""
    with open(json_path, "r") as f:
        json_data = f.read()
    json_file = json.loads(json_data)
    return json_file


def get_schema(name_schema):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    recipe_schema_path = cur_dir + "/recipe_schema.json"
    user_ing_schema_path = cur_dir + "/user_ing_schema.json"
    ing_info_schema_path = cur_dir + "/ing_info_schema.json"
    ing_schema_path = cur_dir + "/ing_schema.json"

    switcher = {
        "ing": get_json(ing_schema_path),
        "recipe": get_json(recipe_schema_path),
        "user_ing": get_json(user_ing_schema_path),
        "ing_info": get_json(ing_info_schema_path),
    }

    return switcher.get(name_schema)


def get_test(test_name):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    recipe_test_path = cur_dir + "/recipe_test.json"
    user_ing_test_path = cur_dir + "/user_ing_test.json"
    ing_info_test_path = cur_dir + "/ing_info_test.json"
    ing_test_path = cur_dir + "/ing_test.json"

    switcher = {
        "ing": get_json(ing_test_path),
        "recipe": get_json(recipe_test_path),
        "user_ing": get_json(user_ing_test_path),
        "ing_info": get_json(ing_info_test_path),
    }

    return switcher.get(test_name)


def get_data(name_json):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    recipe_path = cur_dir + "/recipe.json"
    user_ing_path = cur_dir + "/user_ing.json"
    ing_info_path = cur_dir + "/ing_info.json"

    switcher = {
        "recipe": get_json(recipe_path),
        "user_ing": get_json(user_ing_path),
        "ing_info": get_json(ing_info_path),
    }

    return switcher.get(name_json)


def make_ing(name, quantity, unit, date):
    return {
        "name": name,
        "quantity": quantity,
        "quantity_unit": unit,
        "store_time": date,
    }


def add_ing_temp():

    ing3 = make_ing("watermelon sugar", 500, "g", "2020-10-07 13:34")
    ing4 = make_ing("watermelon sugar3", 500, "g", "2020-10-07 13:34")
    ing5 = make_ing("watermelon sugar2", 500, "g", "2020-10-07 13:34")
    ings = [ing3, ing4, ing5]

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    user_ing_path = cur_dir + "/user_ing.json"
    print(user_ing_path)

    with open(user_ing_path, "w") as outfile:
        # json.dump(ing3, outfile)
        # json.dump(ing3, outfile)
        outfile.write(json.dumps(ings))


add_ing_temp()
