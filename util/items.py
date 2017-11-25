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

"""
main is the main body of the script
"""
def main():
    if len(sys.argv) < 3:
        print("please specify a database file and action")
        exit(1)
    DB.bind(provider='sqlite', filename=sys.argv[1], create_db=True)
    DB.generate_mapping(create_tables=True)
    if sys.argv[2] == "add":
        items = None
        if len(sys.argv) > 3:
            print("adding items from file \"{}\"".format(sys.argv[3]))
            with open(sys.argv[3]) as f:
                items = json.load(f)
            DB.commit()
        else:
            print("adding items from stdin")
            items = json.load(sys.stdin)
        with orm.db_session:
            for name, item in items["items"].items():
                if 'nourishment' not in item:
                    item["nourishment"] = None
                if 'power' not in item:
                    item["nourishment"] = None
                Item(minecraft_id=item['minecraft_id'], name=name, power=item['power'], rarity=item['rarity'],
                 starter_rarity=item['starter_rarity'], nourishment=item['nourishment'])
    else:
        print("unknown command '" + sys.argv[1] +"'")
        exit(1)

main()
