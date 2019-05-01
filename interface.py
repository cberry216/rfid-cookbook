import sqlite3

INDEX_RFID = 0
INDEX_NAME = 1
INDEX_INGREDIENTS = 2
INDEX_INSTRUCTIONS = 3


class Interface:

    def __init__(self, connection=None, cursor=None):
        if connection is None:
            self.connection = sqlite3.connect('db.sqlite')
        else:
            self.connection = connection
        self.cursor = self.connection.cursor()

    def recipe_exists(self, rfid):
        sql = "SELECT COUNT(*) FROM recipe WHERE id=?;"
        self.cursor.execute(sql, (rfid,))
        result = self.cursor.fetchone()
        if result[0] == 1:
            return True
        if result[0] > 1:
            print('Recipe conflicts')
        return False

    def get_recipe(self, rfid):
        sql = "SELECT * FROM recipe WHERE id=?;"
        self.cursor.execute(sql, (rfid,))
        result = self.cursor.fetchone()

        recipe = {}
        recipe['name'] = result[INDEX_NAME]

        recipe['ingredients'] = []
        for ingredient in result[INDEX_INGREDIENTS].split('|'):
	    if ingredient != "":
            	recipe['ingredients'].append(ingredient)

        recipe['instructions'] = []
        for instruction in result[INDEX_INSTRUCTIONS].split('|'):
	    if instruction != "":
            	recipe['instructions'].append(instruction)

        return recipe

    def add_recipe(self, rfid, name, ingredients, instructions):
        ingredients_concat = ""
        instructions_concat = ""
        for ingredient in ingredients:
            ingredients_concat += ingredient + "|"
        for instruction in instructions:
            instructions_concat += instruction + "|"

        sql = "INSERT INTO recipe (id, name, ingredients, instructions) VALUES (?,?,?,?);"
        self.cursor.execute(sql, (rfid, name, ingredients_concat, instructions_concat))
        self.connection.commit()

        return self.get_recipe(rfid)

    def create_recipe(self, rfid):
        name = raw_input("What is the recipe name? ")

        ingredients = []
        ingredient = raw_input("First ingredient ('next' to continue to instructions): ")
        while ingredient != 'next':
            ingredient_count = raw_input("Measure/Quantity of " + ingredient + ": ")
            ingredient_string = str(ingredient_count) + " of " + ingredient
            ingredients.append(ingredient_string + "|")
            ingredient = raw_input("Next ingredient ('next' to continue to instructions): ")

        instructions = []
        numbered_instruction = 1
        instruction = raw_input("First Instruction ('next' to complete recipe): ")
        while instruction != 'next':
            instructions.append(instruction + "|")
            instruction = raw_input("Next Instruction ('next' to complete recipe): ")

        return self.add_recipe(rfid, name, ingredients, instructions)


    def print_recipe(self, recipe):
        name = recipe['name']
        ingredients = recipe['ingredients']
        instructions = recipe['instructions']

        LINE_LENGTH = 60
        NAME_SPACE_LENGTH = int(((len(name) - LINE_LENGTH) / 2) - 1)
        INGREDIENTS_SPACE_LENGTH = int(((len("ingredients") - LINE_LENGTH) / 2) - 2)
        INSTRUCTIONS_SPACE_LENGTH = int(((len("instructions") - LINE_LENGTH) / 2) - 2)

	print("*" * LINE_LENGTH)
        print(name)
        print("*" * LINE_LENGTH)
	print("*")

	print("*- Ingredients")
	print("*")
        
        for ingredient in ingredients:
            print("* " + ingredient)
	
	print("*")
	print("*- Instructions")
	print("*")

        for i in range(len(instructions)):
            print("* " + str(i + 1) + ") " + instructions[i])
	
        print("*" * LINE_LENGTH)



    def process_rfid(self, rfid):
        rfid = str(rfid[0]) + str(rfid[1]) + str(rfid[2]) + str(rfid[3]) + str(rfid[4])

        recipe = None

        if self.recipe_exists(rfid):
            recipe = self.get_recipe(rfid)
        else:
            recipe = self.create_recipe(rfid)

        self.print_recipe(recipe)
