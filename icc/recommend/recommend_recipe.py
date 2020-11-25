# from iccdb.db_manage import find_ing_info, find_user_ing, find_recipe, find_recipe_ing
from iccdb.db_manage import Icc_db
from recommend.compare_recipe import *


def get_total_quantity(need_ings):
    """get sum of quantity of ingredients that user needs to make the recipe

    Args:
       need_ings ingredients that user needs

    Returns:
        sum of quantity

    """
    return sum([ing["quantity"] for ing in need_ings])


# def recommend_recipe(recipes_need_quantity):
#     """find smallest quantity among quantities

#     Args:
#         recipes_need_quantity list of quantity total, each quantity total
#        show how much quantity user needs to make the recipe

#     Returns:
#         name of the recipe

#     """

#     ing = min(recipes_need_quantity, key=lambda recipe: recipe[0])
#     return ing[1]


def score_recipe(recipe, user_ings):
    need_ings = get_need_ings(recipe, user_ings)
    if need_ings == None:
        return 0

    # print("{}, need_ings: {}".format(recipe["name"], need_ings))

    # num of need ings / higher worse
    num_need_ings = len(need_ings)
    # print("num_need_ings: ", num_need_ings)

    # total need ings quantity  / higher worse
    # total_need_quan = sum(iterable=need_ings, lambda need_ing: need_ing["quantity"])
    total_need_quan = sum(need_ing["quantity"] for need_ing in need_ings)
    # print("total_need_quan: ", total_need_quan)

    # total left expir time / higher worse, because we don't need to use ing that has long time left
    # temp = time.fromisoformat(need_ings[0]["store_time"])
    # print(temp)
    total_time_left = 0

    time_format = "%Y-%m-%d %H:%M"
    db = Icc_db("icc")
    KST = timezone('Asia/Seoul')
    for need_ing in need_ings:
        ing_name = need_ing["name"]
        # print("ing_name: {}".format(ing_name))

        ing_info = db.find_ing_info(ing_name)

        # when user doesn't have the ingredient
        if "store_time" not in need_ing.keys():
            # print(need_ing)
            continue

        # print("need_ing: {}".format(need_ing))
        # print("info_info: {}".format(ing_info))
        expiration_duration_min = ing_info["expiration_duration"]
        expiration_duration_day = expiration_duration_min / (60 * 24)

        dt_store_time = dt.datetime.strptime(need_ing["store_time"],
                                             time_format)
        dt_store_time_localized = KST.localize(dt_store_time)
        cur_time = dt.datetime.now(tz=KST)

        timepassed_timedelta = (cur_time - dt_store_time_localized)
        timepassed_sec = int(timepassed_timedelta.total_seconds())
        timepassed_min = int(timepassed_sec / 60)
        timepassed_day = int(timepassed_sec / (60 * 60 * 24))

        timeleft_min = abs(expiration_duration_min - timepassed_min)
        timeleft_day = abs(expiration_duration_day - timepassed_day)

        # water, seasonings.. don't count
        if timeleft_day > 30:
            continue

        # total_time_left += timeleft_min
        total_time_left += timeleft_day

    # print("total time left: {}".format(total_time_left))

    # consider number of total need ings and time left for now
    return num_need_ings * -1 + total_time_left * -1


def recommed_recipe():

    icc_db = Icc_db("icc")
    user_ings = icc_db.find_user_ings(returnID=False)

    cur_score = -100000000
    best_recipe = ""
    for recipe in icc_db.find_recipes():
        score = score_recipe(recipe, user_ings)
        if score > cur_score:
            cur_score = score
            best_recipe = recipe["name"]
        print("recipe: {}, score: {}".format(recipe["name"], score))

    return best_recipe


def remove_recipe_ing_from_user_ing(recipe_name):
    """
    make a recipe and remove used ings from user_ings
    """

    icc_db = Icc_db("icc")
    recipe = icc_db.find_recipe(recipe_name, returnID=False)
    user_ings = icc_db.find_user_ings(returnID=False)
    need_ings = get_need_ings(recipe, user_ings)

    if need_ings == None or need_ings == []:
        print("user ingredients are enough to make {}, start making {}".format(recipe_name, recipe_name))

        for recipe_ing in recipe["ings"]:
            recipe_ing["quantity"] = -1 * recipe_ing["quantity"]
            icc_db.update_user_ing(recipe_ing)
    else:
        print("user ingredients not enough to make {}, need_ings: {}".format(recipe_name, need_ings))
