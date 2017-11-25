"""
module items lets users easily modify the items database using json
"""
import sys
import json
import io

from pony import orm

DB = orm.Database()

"""
An item is a minecraft item that can spawn in hunger games chests
"""
class Item(DB.Entity):
    numeric_id = orm.PrimaryKey(int, auto=True)
    minecraft_id = orm.Required(str)
    name = orm.Required(str)
    power = orm.Optional(float)
    rarity = orm.Required(float)
    starter_rarity = orm.Required(float)
    nourishment = orm.Optional(float)

def item_to_obj(item):
    """item_to_obj takes an Item and removed name and numeric_id"""
    i = dict()
    i["minecraft_id"] = item.minecraft_id
    i["starter_rarity"] = item.starter_rarity
    i["rarity"] = item.starter_rarity
    if item.nourishment is not None:
        i["nourishment"] = item.nourishment
    if item.power is not None:
        i["power"] = item.power
    return i
def item_list_to_map(items):
    """item_list_to_map takes and item list and uses the item's name as a key"""
    return {i.name: item_to_obj(i) for i in items}


def main():
    """main is the main body of the script"""
    if len(sys.argv) < 3:
        print("please specify a database file and action")
        exit(1)
    DB.bind(provider='sqlite', filename=sys.argv[1], create_db=True)
    DB.generate_mapping(create_tables=True)
    if sys.argv[2] == "add":
        items = None
        if len(sys.argv) > 3:
            with open(sys.argv[3]) as json_file:
                items = json.load(json_file)
            DB.commit()
        else:
            items = json.load(sys.stdin)
        with orm.db_session:
            for name, item in items["items"].items():
                if 'nourishment' not in item:
                    item["nourishment"] = None
                if 'power' not in item:
                    item["nourishment"] = None
                Item(minecraft_id=item['minecraft_id'], name=name, power=item['power'], rarity=item['rarity'],
                 starter_rarity=item['starter_rarity'], nourishment=item['nourishment'])
    elif sys.argv[2] == "dump":
        dumpfile = None
        if len(sys.argv) > 3:
            print("dumping items to file \"{}\"".format(sys.argv[3]))
            dumpfile = open(sys.argv[3])
        else:
            dumpfile = sys.stdout
        with orm.db_session:
            items = orm.select(i for i in Item)
            json.dump({"items": item_list_to_map(items)}, dumpfile)
            dumpfile.write("\n")
    else:
        print("unknown command '" + sys.argv[1] +"'")
        exit(1)

main()
