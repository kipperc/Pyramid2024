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

class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        ctx = self.context
        ohshit_command = ctx.bot.get_command('ohshit')

        if ohshit_command:
            await ctx.send("This command sucks, Try !ohshit instead.")
        else:
            await ctx.send("This command sucks, Try !ohshit instead.")

            
# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())

# Store individual game instances for each player
player_games = {}  # Key: player_id, Value: PyramidGame instance


class PyramidGame:
    def __init__(self):
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
        
        self.exit_room = None
        self.rooms = { ... }  # Rooms dictionary as before
        self.started = False
        self.poison_room = None
        self.remaining_moves = 100000
        self.place_key()
        self.place_excalibur()
        self.traps_triggered = set()
        self.place_trap()
        self.players = {}  # Initialize player dictionary
        self.exit_room = self.choose_exit_room()
        self.game_started = False
        self.key_found = False
        self.player_inventory = {}
        pass
    
    def add_player(self, player_id):
        # When a player is added, they start in a random room
        start_room = random.choice(list(self.rooms.keys()))
        self.players[player_id] = {
            'current_room': start_room,
            'inventory': []
        }
        self.current_room = start_room  # Assign the starting room as the player's current room
        
    def validate_rooms(self):
        for room_name, room_data in self.rooms.items():
            if not isinstance(room_data.get('exits', {}), dict):
                raise ValueError(f"Exits for room {room_name} should be a dictionary!")


    def choose_exit_room(self):
        # Get a list of all rooms except the Teleportation Chamber
        candidate_rooms = [room for room in self.rooms.keys() if room != 'Teleportation Chamber']
        # Select a random room as the exit room
        exit_room = random.choice(candidate_rooms)
        return exit_room
    
    def get_player_room(self, player_id):
        # Get the current room of a player
        if player_id in self.players:
            return self.players[player_id]['current_room']
        return None

    
    async def move(self, direction, ctx):
        player_id = ctx.author.id
        game = game_manager.get_game(player_id)
        
        if not game:
            await ctx.send("You are not currently in a game.")
            return

        # Get the player's current room from the dictionary
        current_room = game.get_player_room(player_id)

        # Check if the player's current room exists
        if not current_room:
            await ctx.send("You are not currently in a valid room.")
            return

        if direction not in game.rooms[current_room]['exits']:
            await ctx.send("You can't go that way.")
            return

        new_room = game.rooms[current_room]['exits'][direction]
        game.players[player_id]['current_room'] = new_room  # Update the player's room

    
        # Handle poisoning
        if game.current_room == game.poison_room and 'poison' in game.rooms[game.current_room]['items']:
            game.rooms[game.current_room]['items'].remove('poison')
            game.remaining_moves = min(game.remaining_moves, 20)
            return True, "You've been poisoned! You have 20 moves to !escape before you die."

        if 'trap' in game.rooms[new_room]['items']:
            if new_room not in game.traps_triggered:
                game.traps_triggered.add(new_room)  # Add the room to traps_triggered
                teleport_destination = random.choice(list(game.rooms.keys()))
                game.current_room = teleport_destination
                return True, "You triggered a trap! You have been teleported to a random room."
            else:
                # If the trap has already been triggered in this room, don't trigger it again
                pass

        if 'excalibur' in game.rooms[new_room]['items']:
            game.rooms[new_room]['items'].remove('excalibur')
            game.current_room = game.exit_room
            return True, "You found Excalibur! You've been teleported to the exit room."

        if new_room == 'Teleportation Chamber':
            new_room = random.choice([room for room in game.rooms if room != 'Teleportation Chamber'])
            game.current_room = new_room
            return True, "You have been teleported to {game.current_room}."

        # Regular movement
        room_items = game.rooms[new_room]['items']
        items_message = f"You see the following items: {', '.join(room_items)}" if room_items else "There are no items in the room."
        exits = game.rooms[game.current_room].get('exits', {})
        if isinstance(exits, dict):
            exits_message = f"Exits: {', '.join(exits.keys())}"
        else:
            exits_message = "Exits are not properly defined in this room."

        await ctx.send(f"You moved {direction}. Now you are in {new_room}. {items_message} {exits_message}")


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
        # Get a list of all rooms except the exit room, teleportation chamber, and starting room
        candidate_rooms = [room for room in self.rooms.keys() if room != self.exit_room and room != 'Teleportation Chamber' and room != self.current_room]
        # Select a random room to place the Poison
        self.poison_room = random.choice(candidate_rooms)
        # Place the Poison in the selected room
        self.rooms[self.poison_room]['items'].append('poison')

    def place_key(self):
        print(type(self.rooms))  # Add this to see what type self.rooms is
        # Filter rooms that are not 'Exit' or 'Teleportation Chamber'
        candidate_rooms = [room for room in self.rooms.keys() if room not in ['Exit', 'Teleportation Chamber']]
        # Continue with the logic to place the key...
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


class GameManager:
    def __init__(self):
        self.player_games = {}  # Dictionary to manage games by player_id

    def start_game(self, player_id):
        if player_id not in self.player_games:
            self.player_games[player_id] = PyramidGame()
            return True
        return False

    def end_game(self, player_id):
        if player_id in self.player_games:
            del self.player_games[player_id]
            return True
        return False

    def get_game(self, player_id):
        return self.player_games.get(player_id, None)


# Create a global instance of GameManager
game_manager = GameManager()
game = PyramidGame()
game.validate_rooms()

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(f'Number of active games: {len(game_manager.player_games)}')


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
async def take(ctx, item):
    player_id = ctx.author.id

    # Check if the player has an ongoing game
    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in a game.")
        return

    game = game_manager.player_games[player_id]

    # Logic to take an item in the player's specific game instance
    if item.lower() in game.rooms[game.current_room]['items']:
        if item.lower() in game.player_inventory.get(player_id, []):
            await ctx.send(f"You already have the {item}.")
        else:
            if item.lower() == 'key':
                game.key_found = True
                game.player_inventory.setdefault(player_id, []).append(item.lower())
                game.rooms[game.current_room]['items'].remove(item.lower())
                await ctx.send("You found the key!")
            else:
                game.player_inventory.setdefault(player_id, []).append(item.lower())
                game.rooms[game.current_room]['items'].remove(item.lower())
                await ctx.send(f"You have taken the {item}.")
    else:
        await ctx.send("That item is not available in this room.")

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
    player_id = ctx.author.id
    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in a game.")
        return

    game = game_manager.get_game(player_id)
    success, message = await game.move(direction, ctx)
    
    if success:
        await ctx.send(message)
    else:
        await ctx.send(message)

@bot.command()
async def start(ctx):
    player_id = ctx.author.id
    if game_manager.start_game(player_id):
        await ctx.send(f"{ctx.author.display_name}, you have started your own game!")
    else:
        await ctx.send(f"{ctx.author.display_name}, you already have an ongoing game!")

@bot.command()
async def kms(ctx):
    player_id = ctx.author.id
    if game_manager.end_game(player_id):
        await ctx.send(f"{ctx.author.display_name}, your game has been stopped.")
    else:
        await ctx.send("You are not currently in the game.")


@bot.command()
async def look(ctx):
    player_id = ctx.author.id
    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.get_game(player_id)
    current_room = game.current_room
    current_room_info = game.rooms.get(current_room)

    if current_room_info:
        room_items = current_room_info.get('items', [])
        items_message = f"You see the following items in the room: {', '.join(room_items)}." if room_items else "There are no items in the room."
        exits_message = f"Exits: {', '.join(current_room_info['exits'].keys())}"

        await ctx.send(f"You are in the {current_room}. \n{items_message} \n{exits_message}")
    else:
        await ctx.send("Invalid room. Please start a new game.")




# Command: Print the maze layout
@bot.command()
async def maze(ctx):
    player_id = ctx.author.id
    
    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return
    
    game = game_manager.player_games[player_id]
    maze_map = game.generate_maze_map()
    await ctx.send("```" + maze_map + "```")

@bot.command()
async def escape(ctx):
    player_id = ctx.author.id
    
    # Check if the player has an ongoing game
    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in a game.")
        return

    game = game_manager.player_games[player_id]
    current_room = game.current_room  # Access current_room directly from the player's game instance

    if game.key_found:
        if game.check_win_condition(current_room):
            await ctx.send("Congratulations! You have escaped.")
            # Reset the game for this player
            del game_manager.player_games[player_id]  # Remove the player's game entry
            
        else:
            await ctx.send("You cannot escape yet. You need to be in the exit room.")
    else:
        await ctx.send("You do not have the key to escape.")

@bot.command()
async def exit_room(ctx):
    player_id = ctx.author.id

    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.player_games[player_id]  # Get the player's specific game instance
    exit_room = game.exit_room

    await ctx.send(f"The exit room is: {exit_room}")
    
@bot.command()
async def give_key(ctx):
    player_id = ctx.author.id

    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.player_games[player_id]  # Get the player's specific game instance

    # Give the key to the player and mark it as found in the game state
    if 'key' not in game.player_inventory.setdefault(player_id, []):
        game.player_inventory[player_id].append('key')
    game.key_found = True

    await ctx.send("You have received the key!")

    
@bot.command()
async def cheat_win(ctx):
    player_id = ctx.author.id

    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.player_games[player_id]  # Get the player's specific game instance
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
    player_id = ctx.author.id

    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.player_games[player_id]  # Get the player's specific game instance

    # Teleport the player to the exit room
    game.current_room = game.exit_room
    await ctx.send("You've been teleported to the exit room. Cheater!")


@bot.command()
async def key_location(ctx):
    player_id = ctx.author.id

    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.player_games[player_id]  # Get the player's specific game instance

    if game.key_found:
        await ctx.send("You already found the key!")
    else:
        await ctx.send(f"The key is located in the {game.exit_room}.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't recognize that command. Type `!help` to see the list of available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("It looks like you're missing a required argument. Please try again.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")


@bot.command()
async def moves_left(ctx):
    player_id = ctx.author.id

    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in the game.")
        return

    game = game_manager.player_games[player_id]  # Get the player's specific game instance

    await ctx.send(f"You have {game.remaining_moves} moves left.")

bot.run(TOKEN, reconnect=True)
