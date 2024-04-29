import discord
import random
from discord.ext import commands

player_current_room = {}
has_key = {}
player_inventory = {}
ctx=''
intents = discord.Intents.default()
intents.message_content = True

class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        ohshit_command = ctx.bot.get_command('ohshit')

        if ohshit_command:
            try:
                ohshit_output = await ctx.invoke(ohshit_command)
                if ohshit_output:
                    await ctx.send(ohshit_output)
                else:
                    await ctx.send("This command sucks, Try !ohshit instead.")
            except Exception as e:
                await ctx.send(f"An error occurred while fetching help: {e}")
        else:
            await ctx.send("This commands sucks, Try !ohshit instead.")

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())


class PyramidGame:
    def __init__(self):
        self.exit_room = None
        self.rooms = {
    'Foyer': {
        'description': 'You are in the Foyer. It is dimly lit with torches on the walls.',
        'items': ['torch', 'dog'],
        'exits': {'north': 'Antechamber', 'east': 'Hidden Passage'}
    },
    'Antechamber': {
        'description': 'You are in the Antechamber. There is a faint echo in the air.',
        'items': ['scroll', 'statue'],
        'exits': {'south': 'Foyer', 'west': 'Grand Gallery'}
    },
    'Grand Gallery': {
        'description': 'You are in the Grand Gallery. The walls are adorned with ancient artwork.',
        'items': ['painting', 'sarcophagus'],
        'exits': {'east': 'Antechamber', 'west': 'Treasury'}
    },
    'Treasury': {
        'description': 'You are in the Treasury. Gold and jewels glimmer in the dim light.',
        'items': ['coin', 'crown'],
        'exits': {'east': 'Grand Gallery', 'north': 'Throne Room', 'south': 'Candlelit Chamber', 'west': 'Mystic Observatory'}
    },
    'Throne Room': {
        'description': 'You are in the Throne Room. A majestic throne sits at the far end.',
        'items': ['sword', 'shield'],
        'exits': {'south': 'Treasury', 'west': 'Mystic Observatory', 'north': 'Chamber of Echoes'}
    },
    'Hidden Passage': {
        'description': 'You have found a hidden passage. The air is musty, and the walls are lined with cobwebs.',
        'items': ['spider', 'dagger'],
        'exits': {'east': 'Foyer', 'up': 'Dusty Attic'}
    },
    'Candlelit Chamber': {
        'description': 'You enter a Candlelit Chamber. The flickering flames cast eerie shadows on the walls.',
        'items': ['candle', 'tome'],
        'exits': {'north': 'Treasury','west':'Crystal Cavern'}
    },
    'Chamber of Echoes': {
        'description': 'Welcome to the Chamber of Echoes. Every sound you make reverberates off the walls.',
        'items': ['stone', 'bell'],
        'exits': {'south': 'Throne Room'}
    },
    'Mystic Observatory': {
        'description': 'You stand in the Mystic Observatory. The stars twinkle brightly through the domed ceiling.',
        'items': ['telescope', 'chart'],
        'exits': {'east': 'Treasury', 'south': 'Crystal Cavern'}
    },
    'Crystal Cavern': {
        'description': 'You enter a Crystal Cavern. The walls are lined with shimmering crystals of every color.',
        'items': ['crystal', 'gemstone'],
        'exits': {'north': 'Mystic Observatory', 'east':'Candlelit Chamber'}
    },
    'Enchanted Garden': {
        'description': 'You find yourself in an Enchanted Garden. Flowers bloom in vibrant colors all around you.',
        'items': ['flower', 'fruit'],
        'exits': {'north': 'Candlelit Chamber'}
    },
    'Dusty Attic': {
        'description': 'You climb up to the Dusty Attic. Old furniture and forgotten relics fill the space.',
        'items': ['cobweb', 'chest'],
        'exits': {'down': 'Hidden Passage', 'east': 'Forgotten Library'}
    },
    'Serpentine Corridor': {
        'description': 'You walk through the Serpentine Corridor. The walls twist and turn like a snake.',
        'items': ['snake', 'artifact'],
        'exits': {'west':'Echoing Hallway'}
    },
    'Forgotten Library': {
        'description': 'You enter the Forgotten Library. Dusty tomes line the shelves, waiting to be rediscovered.',
        'items': ['book', 'scroll'],
        'exits': {'east': 'Echoing Hallway', 'down':'Gloomy Cellar'}
    },
    'Gloomy Cellar': {
        'description': 'You descend into the Gloomy Cellar. The air is damp and musty, filled with the scent of decay.',
        'items': ['knife', 'barrel'],
        'exits': {'up': 'Forgotten Library'}
    },
    'Echoing Hallway': {
        'description': 'You find yourself in an Echoing Hallway. Every step echoes loudly, filling the space with sound.',
        'items': ['timepiece', 'lantern'],
        'exits': {'east': 'Serpentine Corridor','west': 'Forgotten Library'}
    },
}




        self.started = False
        opposite_direction = {
           'north': 'south',
           'south': 'north',
           'east': 'west',
           'west': 'east',
            'up': 'down',
            'down': 'up'
        }
        self.exit_room = random.choice(list(self.rooms.keys()))
        if self.exit_room:
            self.rooms[self.exit_room]['is_exit'] = True  # Mark the exit room
        self.current_room = random.choice(list(self.rooms.keys()))
        self.inventory = []
        self.place_key()
        self.players = {}  # Dictionary to store player information
        self.game_started= False
        self.key_found = False  # Initialize key_found attribute
        self.current_room = None  # Initialize current_room attribute
       # List of available rooms
        self.available_rooms = ['Foyer', 'Antechamber', 'Grand Gallery', 'Treasury', 'Throne Room']
        # Randomly select a starting room
        self.current_room = random.choice(self.available_rooms)
        pass

    async def move(self, direction, ctx):
        if direction not in self.rooms[self.current_room]['exits']:
            return False, "You can't go that way."

        new_room = self.rooms[self.current_room]['exits'][direction]

        # Check if the new room is the exit room
        if new_room == self.exit_room:
            if 'key' in player_inventory.get(ctx.author.id, []):
                return True, "Congratulations! You have entered the exit room with the key. You win!"
            else:
                return True, "You have entered the exit room without the key. You can still explore."

        # Update current room
        self.current_room = new_room

        # Check for items in the room
        room_items = self.rooms[self.current_room]['items']
        items_message = f"You see the following items in the room: {', '.join(room_items)}." if room_items else "There are no items in the room."
    
        return True, f"You have moved {direction}. You are now in {self.current_room}. {items_message}"


    def add_player(self, player_id):
        # Initialize player attributes
        self.players[player_id] = {
            'current_room': None,
            'has_key': False,
            'inventory': []
        }


    def check_win_condition(self, current_room):
        return self.key_found and current_room == self.exit_room

    def place_key(self):
        # Get a list of all rooms except the exit room
        candidate_rooms = [room for room in self.rooms.keys() if room != 'Exit']
        # Select a random room to place the key
        key_room = random.choice(candidate_rooms)
        # Place the key in the selected room
        self.rooms[key_room]['items'].append('key')

    def get_maze_listing(self):
        maze_listing = "Maze Listing:\n"
        for room_name, room_info in self.rooms.items():
            exits = ', '.join(room_info['exits'].keys())
            maze_listing += f"{room_name} - Exits: {exits}\n"
            if 'is_exit' in room_info and room_info['is_exit']:
                maze_listing += "  (Exit Room)\n"
        return maze_listing

    def print_maze(self):
        maze = ""
        for room, info in self.rooms.items():
            maze += f"{room}: Exits: {', '.join(info['exits'].keys())}\n"
        return maze

bot.game_started = False  # Set to False initially

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.game = None  # Initialize the game attribute

@bot.event
async def on_message(message):
    # Check if the message author is the bot itself
    if message.author == bot.user:
        return

    # Check if the message is a command invocation
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

# Command: Help
@bot.command()
async def ohshit(ctx):
    help_message = """
    **Pyramid 2024 - Help**

    How to Play: Journey through the maze until you find the key, then make it to the exit room to escape.
    Commands:
    - !start: Start a new game.
    - !kms: quits the game.
    - ![direction]: Move to a different room (!north, !south, !east, !west. !up, !down).
    - !look: Look around the current room.
    - !take [item]: Take an item from the room.
    - !maze: Print the layout of the maze.
    - !ohshit: Display this help message.
    - !escape: Checks to see if you can escape the pyramid.

    Have fun exploring the pyramid!
    """
    await ctx.send(help_message)


@bot.command()
async def start(ctx):
    global game_started  # Access the global variable

    # Check if a game is already in progress
    if ctx.bot.game is None:
        ctx.bot.game = PyramidGame()  # Create a new instance of PyramidGame
        # Initialize player attributes
        ctx.bot.game.add_player(ctx.author.id)
        await ctx.send("You have started the game!")  # Notify the player
    else:
        await ctx.send("A game is already in progress.")

@bot.command()
async def take(ctx, item):
    if ctx.bot.game is None:
        await ctx.send("You are not currently in the game.")
        return

    game = ctx.bot.game

    if item.lower() in game.rooms[game.current_room]['items']:
        if item.lower() in player_inventory.get(ctx.author.id, []):
            await ctx.send(f"You already have the {item}.")
            return
        else:
            player_inventory.setdefault(ctx.author.id, []).append(item.lower())
            game.rooms[game.current_room]['items'].remove(item.lower())  # Remove item from room
            await ctx.send(f"You have taken the {item}.")
    else:
        await ctx.send("That item is not available in this room.")

@bot.command()
async def kms(ctx):
    # Reset game state variables
    player_current_room.clear()
    has_key.clear()
    player_inventory.clear()
    ctx.bot.game = None

    # Set game_started flag to False
    bot.game_started = False

    await ctx.send("The game has been stopped. You can start a new game with !start.")

@bot.command()
async def north(ctx):
    await move_direction(ctx, 'north')

@bot.command()
async def south(ctx):
    await move_direction(ctx, 'south')

@bot.command()
async def east(ctx):
    await move_direction(ctx, 'east')

@bot.command()
async def west(ctx):
    await move_direction(ctx, 'west')

@bot.command()
async def up(ctx):
    await move_direction(ctx, 'up')

@bot.command()
async def down(ctx):
    await move_direction(ctx, 'down')

async def move_direction(ctx, direction):
    if ctx.bot.game is None:
        await ctx.send("You are not currently in the game.")
        return

    game = ctx.bot.game
    success, message = await game.move(direction, ctx)

    if success:
        await ctx.send(message)
    else:
        await ctx.send("You cannot move in that direction.")

@bot.command()
async def look(ctx):
    if ctx.bot.game is None:
        await ctx.send("You are not currently in the game.")
        return

    game = ctx.bot.game
    current_room_info = game.rooms.get(game.current_room)

    if current_room_info:
        items = current_room_info.get('items', [])
        if items:
            item_list = ", ".join(items)
            await ctx.send(f"Items in the room: {item_list}")
            await ctx.send(f'You are in the {game.current_room}.')
        else:
            await ctx.send("There are no items in the room.")
    else:
        await ctx.send("Invalid room. Please start a new game.")

# Command: Print the maze layout
@bot.command()
async def maze(ctx):
    game = ctx.bot.game
    maze_listing = game.get_maze_listing()
    await ctx.send(maze_listing)

@bot.command()
async def escape(ctx):
    if ctx.bot.game is not None:
        game = ctx.bot.game
        current_room = player_current_room.get(ctx.author.id)
        if current_room is None:
            await ctx.send("You are not currently in the game.")
            return

        if game.check_win_condition(current_room, has_key[ctx.author.id]):
            await ctx.send("Congratulations! You have escaped.")
            # Reset the game
            ctx.bot.game = None
            player_current_room[ctx.author.id] = None
            has_key[ctx.author.id] = False
            player_inventory[ctx.author.id] = []
        else:
            await ctx.send("You cannot escape yet.")
    else:
        await ctx.send("No game in progress.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't recognize that command. Type `!help` to see the list of available commands.")
    else:
        # For other errors, you can handle them as needed
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot
bot.run('INSERT BOT TOKEN HERE')
