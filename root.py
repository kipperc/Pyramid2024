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
        self.rooms = {
            'Foyer': {
                'description': 'You are in the Foyer. It is dimly lit with torches on the walls.',
                'items': ['torch', 'dog'],
                'exits': {'north': 'Antechamber'}
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
                'exits': {'east': 'Grand Gallery', 'north': 'Throne Room'}
            },
            'Throne Room': {
                'description': 'You are in the Throne Room. A majestic throne sits at the far end.',
                'items': ['sword', 'shield'],
                'exits': {'south': 'Treasury'}
            },
        }
        self.exit_room = random.choice(list(self.rooms.keys()))
        self.rooms[self.exit_room]['is_exit'] = True  # Mark the exit room
        self.current_room = random.choice(list(self.rooms.keys()))
        self.inventory = []
        self.place_key()


        self.game_started= False
        self.key_found = False  # Initialize key_found attribute
        self.current_room = None  # Initialize current_room attribute
       # List of available rooms
        self.available_rooms = ['Foyer', 'Antechamber', 'Grand Gallery', 'Treasury', 'Throne Room']
        # Randomly select a starting room
        self.current_room = random.choice(self.available_rooms)

    def check_win_condition(self, current_room):
        return self.key_found and current_room == self.exit_room


    async def move(self, direction):
        if direction in self.rooms[self.current_room]['exits']:
            new_room = self.rooms[self.current_room]['exits'][direction]
            self.current_room = new_room
            # Check if the player has reached the exit room
            if new_room == self.exit_room:
                # Check if the player has the key in their inventory to win
                if 'key' in player_inventory[ctx.author.id] and player_current_room[ctx.author.id] == 'Exit':
                    return True, "Congratulations! You have escaped the pyramid."
                else:
                    return False, "You need the key to unlock the exit and escape the pyramid."
            return True, f"You move {direction}. {self.rooms[self.current_room]['description']}"
        else:
            return False, "You cannot move in that direction."
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


bot.game = PyramidGame()
bot.game_started = False  # Set to False initially

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Check if the message author is the bot itself
    if message.author == bot.user:
        return

    # Check if the message is a command invocation
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    # Check if the message is from a guild and if it's the first message after the bot joins
    if message.guild and not bot.game_started:
        await message.channel.send("Welcome to the game! Please use the !start command to begin.")
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
    - ![direction]: Move to a different room (e.g., !north).
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
    # Check if the player is already in a room
    if player_current_room.get(ctx.author.id) is not None:
        await ctx.send("You are already in the game.")
        return

    # Initialize player attributes if not already done
    if ctx.author.id not in player_current_room:
        player_current_room[ctx.author.id] = ctx.bot.game.current_room
        has_key[ctx.author.id] = False
        player_inventory[ctx.author.id] = []

    # Check if a game is already in progress
    if ctx.bot.game is None:
        ctx.bot.game = PyramidGame()  # Create a new instance of PyramidGame
        bot.game_started = True  # Set game_started flag to True
        player_current_room[ctx.author.id] = ctx.bot.game.current_room
        await ctx.send("You have started the game!")  # Notify the player
    else:
        await ctx.send("A game is already in progress.")

@bot.command()
async def take(ctx, item):
    # Check if the game is started
    if not bot.game_started:
        await ctx.send("You are not currently in the game.")
        return

    # Check if the item is the key
    if item.lower() == "key":
        # Add the key to the player's inventory
        player_inventory[ctx.author.id].append(item)
        await ctx.send(f"You have taken the {item}.")
    else:        await ctx.send(f"The {item} is not available to take.")

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

async def move_direction(ctx, direction):
    global player_current_room  # Access the global variable

    # Check if the player is in the game
    if ctx.author.id not in player_current_room:
        await ctx.send("You are not currently in the game.")
        return

    game = ctx.bot.game
    success, message = game.move(direction)

    # Check if the movement was successful
    if success:
        # Update the player's current room
        player_current_room[ctx.author.id] = ctx.bot.game.current_room
        await ctx.send(message)
    else:
        await ctx.send(message)

@bot.command()
async def look(ctx):
    global player_current_room

    # Check if the player is in the game
    if ctx.author.id not in player_current_room:
        await ctx.send("You are not currently in the game.")
        return

    current_room = player_current_room[ctx.author.id]
    if current_room is None:
        await ctx.send("You haven't started the game yet.")
        return

    game = ctx.bot.game
    current_room_info = game.rooms.get(current_room)

    if current_room_info:
        items = current_room_info.get('items', [])
        if items:
            item_list = ", ".join(items)
            await ctx.send(f"Items in the room: {item_list}")
            await ctx.send(f'You are in the {current_room}.')
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


# Run the bot
bot.run('')
