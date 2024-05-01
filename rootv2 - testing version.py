import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("\033[31mLooks like you haven't properly set up a Discord token environment variable in the `.env` file. (Secrets on replit)\033[0m")
    print("\033[33mNote: If you don't have a Discord token environment variable, you will have to input it every time. \033[0m")
    TOKEN = input("Please enter your Discord token: ")

ctx=''
intents = discord.Intents.default()
intents.message_content = True
player_inventory = ()

class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self, ctx):
        ohshit_command = ctx.bot.get_command('ohshit')

        if ohshit_command:
            await ctx.send("This command sucks, Try !ohshit instead.")
        else:
            await ctx.send("This command sucks, Try !ohshit instead.")
            
# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())

class PyramidGame:
    def __init__(self):
        self.exit_room = None
        self.rooms = {
    'Foyer': {
        'description': 'You are in the Foyer. It is dimly lit with torches on the walls.',
        'items': ['torch', 'dog'],
        'exits': {'north': 'Antechamber', 'east': 'Hidden Passage', 'up': 'Teleportation Chamber'}
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
        'exits': {'west': 'Foyer', 'up': 'Dusty Attic'}
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
        'exits': {'east': 'Echoing Hallway','west':'Dusty Atttic', 'down':'Gloomy Cellar'}
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
    'Teleportation Chamber': {  # New room: Teleportation Chamber
                'description': 'You are in the Teleportation Chamber. Everything seems to shimmer around you.',
                'items': ['portal'],
                'exits': {'down': 'Foyer'} 
            }
        }

        self.started = False
        self.poison_room = None
        self.inventory = []
        self.place_key()
        self.place_excalibur()  # Place Excalibur in a random room
        self.traps_triggered = set()  # Initialize traps_triggered as an empty set
        self.place_trap()
        self.players = {}  # Dictionary to store player information
        self.exit_room = self.choose_exit_room()
        self.game_started= False
        self.key_found = False  # Initialize key_found attribute
        self.current_room = None  # Initialize current_room attribute
       # List of available rooms
        self.available_rooms = ['Foyer', 'Antechamber', 'Grand Gallery', 'Treasury', 'Throne Room']
        # Randomly select a starting room
        self.current_room = random.choice(self.available_rooms)
        self.poison_moves_remaining = 0
        pass

    def choose_exit_room(self):
        # Get a list of all rooms except the Teleportation Chamber
        candidate_rooms = [room for room in self.rooms.keys() if room != 'Teleportation Chamber']
        # Select a random room as the exit room
        exit_room = random.choice(candidate_rooms)
        return exit_room
    
    async def move(self, direction, ctx):
            if direction not in self.rooms[self.current_room]['exits']:
                return False, "You can't go that way."

            new_room = self.rooms[self.current_room]['exits'][direction]

            # Check if the new room is the exit room
                
            if self.poison_moves_remaining > 0:
                # If affected by poison, move in the opposite direction
                opposite_direction = {
                    'north': 'south',
                    'south': 'north',
                    'east': 'west',
                    'west': 'east',
                    'up': 'down',
                    'down': 'up'
                }
                if direction in opposite_direction:
                    direction = opposite_direction[direction]
                self.poison_moves_remaining -= 1

            if 'trap' in self.rooms[new_room]['items']:
                if new_room not in self.traps_triggered:
                    self.traps_triggered.add(new_room)  # Add the room to traps_triggered
                    teleport_destination = random.choice(self.rooms.keys())
                    self.current_room = teleport_destination
                    return True, "You triggered a trap! You have been teleported to a random room."
                else:
                    # If the trap has already been triggered in this room, don't trigger it again
                    pass

            # Check if the player found Excalibur
            if 'excalibur' in self.rooms[new_room]['items']:
                # Remove Excalibur from the room
                self.rooms[new_room]['items'].remove('excalibur')
                # Teleport the player to the key room
                self.current_room = self.exit_room
                return True, "You found Excalibur! You've been teleported to the exit room."

            if new_room == 'Teleportation Chamber':
                # Teleport the player to a random room
                new_room = random.choice([room for room in self.rooms if room != 'Teleportation Chamber'])

                # Update current room
                self.current_room = new_room

                # Inform the player about the teleportation
                return True, f"You have been teleported to {self.current_room}."

            # If none of the special conditions are met, proceed with the regular movement
            self.current_room = new_room
            # Check for items in the room
            room_items = self.rooms[self.current_room]['items']
            items_message = f"You see the following items in the room: {', '.join(room_items)}." if room_items else "There are no items in the room."
    
            # Get exits information
            exits_message = f"Exits: {', '.join(self.rooms[self.current_room]['exits'].keys())}"

            return True, f"You have moved {direction}. \nYou are now in {self.current_room}. \n{items_message} \n{exits_message}"

    def add_player(self, player_id):
        # Initialize player attributes
        self.players[player_id] = {
            'current_room': None,
            'inventory': []
        }


    def check_win_condition(self, current_room):
        return self.key_found and current_room == self.exit_room
    
    def place_trap(self):
        # Get a list of all rooms except the exit room and teleportation chamber
        candidate_rooms = [room for room in self.rooms.keys() if room != self.exit_room and room != 'Teleportation Chamber']
        # Select a random room to place the trap
        trap_room = random.choice(candidate_rooms)
        # Place the trap in the selected room
        self.rooms[trap_room]['items'].append('trap')
        
    def place_poison(self):
        # Get a list of all rooms except the exit room and teleportation chamber
        candidate_rooms = [room for room in self.rooms.keys() if room != self.exit_room and room != 'Teleportation Chamber']
        # Select a random room to place the Poison
        self.poison_room = random.choice(candidate_rooms)
        # Place the Poison in the selected room
        self.rooms[self.poison_room]['items'].append('Poison')
        
    def place_key(self):
        # Get a list of all rooms except the exit room
        candidate_rooms = [room for room in self.rooms.keys() if room not in ['Exit', 'Teleportation Chamber']]
        # Select a random room to place the key
        key_room = random.choice(candidate_rooms)
        # Place the key in the selected room
        self.rooms[key_room]['items'].append('key')

    def place_excalibur(self):
        # Get a list of all rooms except the exit room and key room
        candidate_rooms = [room for room in self.rooms.keys() if room != 'Teleportation Chamber']
        # Select a random room to place Excalibur
        excalibur_room = random.choice(candidate_rooms)
        # Place Excalibur in the selected room
        self.rooms[excalibur_room]['items'].append('excalibur')
    
    def generate_maze_map(self):
        maze_map = ""
        for room_name, room_info in self.rooms.items():
            exits = ', '.join(room_info['exits'].keys())
            maze_map += f"{room_name} - Exits: {exits}\n"

            # Add lines for each exit
            for direction, exit_room in room_info['exits'].items():
                maze_map += f"   |---{direction}---> {exit_room}\n"

            maze_map += "\n"
        return maze_map

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
    > !start: Start a new game.
    > !kms: quits the game.
    > ![direction]: Move to a different room (!north, !south, !east, !west. !up, !down).
    > !look: Look around the current room.
    > !take [item]: Take an item from the room.
    > !maze: Print the layout of the maze.
    > !ohshit: Display this help message.
    > !escape: Checks to see if you can escape the pyramid.

    Have fun exploring the pyramid!
    """
    await ctx.send(help_message)


@bot.command()
async def start(ctx):
    if ctx.bot.game is None:
        ctx.bot.game = PyramidGame()  # Create a new instance of PyramidGame
        # Initialize player attributes
        ctx.bot.game.add_player(ctx.author.id)
        await ctx.send("You have started the game!")  # Notify the player
    else:
        # Reset the game for a new player
        ctx.bot.game.add_player(ctx.author.id)
        await ctx.send("You have joined the existing game!")

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
            if item.lower() == 'key':
                game.key_found = True  # Mark the key as found
                player_inventory.setdefault(ctx.author.id, []).append(item.lower())
                game.rooms[game.current_room]['items'].remove(item.lower())  # Remove item from room
                await ctx.send("You found the key!")
            elif item.lower() == 'excalibur':
                # Teleport the player to the exit room
                game.current_room = game.exit_room
                await ctx.send("You found Excalibur! You've been teleported to the exit room.")
            else:
                player_inventory.setdefault(ctx.author.id, []).append(item.lower())
                game.rooms[game.current_room]['items'].remove(item.lower())  # Remove item from room
                await ctx.send(f"You have taken the {item}.")
    else:
        await ctx.send("That item is not available in this room.")
 


@bot.command()
async def kms(ctx):
    # Reset game state variables
    game.key_found = False
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
        # Check for items in the room
        room_items = current_room_info.get('items', [])
        items_message = f"You see the following items in the room: {', '.join(room_items)}." if room_items else "There are no items in the room."
    
        # Get exits information
        exits_message = f"Exits: {', '.join(current_room_info['exits'].keys())}"

        await ctx.send(f"You are in the {game.current_room}. \n{items_message} \n{exits_message}")
    else:
        await ctx.send("Invalid room. Please start a new game.")



# Command: Print the maze layout
@bot.command()
async def maze(ctx):
    game = ctx.bot.game
    maze_map = game.generate_maze_map()
    await ctx.send("```" + maze_map + "```")

@bot.command()
async def escape(ctx):
    if ctx.bot.game is not None:
        game = ctx.bot.game
        current_room = game.current_room  # Access current_room directly from the game instance

        if game.key_found:
            if game.check_win_condition(current_room):
                await ctx.send("Congratulations! You have escaped.")
                # Reset the game
                ctx.bot.game = None
                game.key_found = False
                current_room = None
                
            else:
                await ctx.send("You cannot escape yet.")
        else:
            await ctx.send("You do not have the key to escape.")
    else:
        await ctx.send("No game in progress.")





@bot.command()
async def exit_room(ctx):
    if ctx.bot.game is None:
        await ctx.send("No game in progress.")
        return

    game = ctx.bot.game
    exit_room = game.exit_room

    await ctx.send(f"The exit room is: {exit_room}")
    
@bot.command()
async def give_key(ctx):
    if ctx.bot.game is None:
        await ctx.send("No game in progress.")
        return

    player_id = ctx.author.id
    game = ctx.bot.game

    # Give the key to the player
    player_inventory.setdefault(player_id, []).append('key')
    game.key_found = True

    await ctx.send("You have received the key!")
    
@bot.command()
async def cheat_win(ctx):
    if ctx.bot.game is None:
        await ctx.send("No game in progress.")
        return

    game = ctx.bot.game
    current_room = game.current_room

    # Check if the current room is the exit room and the key has been found
    if game.check_win_condition(current_room):
        await ctx.send("Cheater! You've already won the game.")
    else:
        # Mark the key as found and set the current room to the exit room
        game.key_found = True
        game.current_room = game.exit_room
        await ctx.send("Congratulations! You've cheated your way to victory.")

@bot.command()
async def cheat_teleport_exit(ctx):
    if ctx.bot.game is None:
        await ctx.send("No game in progress.")
        return

    game = ctx.bot.game
    game.current_room = game.exit_room
    await ctx.send("You've been teleported to the exit room. Cheater!")

@bot.command()
async def key_location(ctx):
    if ctx.bot.game is None:
        await ctx.send("You are not currently in the game.")
        return

    game = ctx.bot.game

    if game.key_found:
        await ctx.send("You already found the key!")
    else:
        await ctx.send(f"The key is located in the {game.exit_room}.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't recognize that command. Type `!help` to see the list of available commands.")
    else:
        # For other errors, you can handle them as needed
        await ctx.send(f"An error occurred: {str(error)}")


bot.run(TOKEN, reconnect=True)