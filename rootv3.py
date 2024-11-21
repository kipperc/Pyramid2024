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
        'exits': {'east': 'Echoing Hallway','west':'Dusty Attic', 'down':'Gloomy Cellar'}
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
        self.players = {}  # To store player details
        self.active_player = None  # New attribute to track the active player
        self.current_room = None  # Track the active player's current room
        self.exit_room = None
        self.started = False
        self.poison_room = None
        self.remaining_moves = 100000
        self.place_key()
        self.place_excalibur()
        self.traps_triggered = set()
        self.place_trap()
        self.place_poison()
        self.players = {}  # Initialize player dictionary
        self.exit_room = self.choose_exit_room()
        self.game_started = False
        self.key_found = False
        self.player_inventory = {}
        pass
    
    def add_player(self, player_id):
        valid_rooms = list(self.rooms.keys())
        if not valid_rooms:
            raise ValueError("No valid rooms available to start the game.")
    
        start_room = random.choice(valid_rooms)
        self.players[player_id] = {
            'current_room': start_room,
            'inventory': []
        }
    
        # Set the first added player as the active player
        if self.active_player is None:
            self.active_player = player_id
            self.current_room = self.players[player_id]['current_room']
    
        print(f"Player {player_id} starts in {start_room}.")  # Debug info
        
    def set_active_player(self, player_id):
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
    
        self.active_player = player_id
        self.current_room = self.players[player_id]['current_room']  # Update current room based on the active player

    def move_player(self, player_id, direction):
        # Get current room for the player
        current_room = self.players[player_id]['current_room']
    
        # Check if the direction is valid in the current room
        if direction in self.rooms[current_room]['exits']:
            new_room = self.rooms[current_room]['exits'][direction]
            self.players[player_id]['current_room'] = new_room
        
            # Update current_room if this is the active player
            if player_id == self.active_player:
                self.current_room = new_room
            
            print(f"Player {player_id} moved to {new_room}.")
        else:
            print(f"Invalid direction! No exit {direction} in {current_room}.")


    def get_player_room(self, player_id):
        # Get the current room of a player
        if player_id in self.players:
            return self.players[player_id]['current_room']
        else:
            raise ValueError(f"Player {player_id} does not exist.")


    def choose_exit_room(self):
        # Get a list of all rooms except the Teleportation Chamber
        candidate_rooms = [room for room in self.rooms.keys() if room != 'Teleportation Chamber']
        # Select a random room as the exit room
        exit_room = random.choice(candidate_rooms)
        return exit_room
    
    
    async def move(self, direction, ctx):
        player_id = ctx.author.id
        game = game_manager.get_game(player_id)

        if not game:
            return False, "You are not currently in a game."

        # Get the player's current room from the dictionary
        current_room = game.get_player_room(player_id)

        # Check if the player's current room exists
        if not current_room:
            return False, "You are not currently in a valid room."

        if direction not in game.rooms[current_room]['exits']:
            return False, "You can't go that way."

        new_room = game.rooms[current_room]['exits'][direction]
        game.players[player_id]['current_room'] = new_room  # Update the player's room

        # Check for poison when entering the new room
        if new_room == game.poison_room and 'poison' in game.rooms[new_room]['items']:
            game.rooms[new_room]['items'].remove('poison')  # Remove the poison after triggering
            game.remaining_moves = min(game.remaining_moves, 20)  # Limit remaining moves
            return True, "You've been poisoned! You have 20 moves to escape before you die."

        # Handle traps
        if 'trap' in game.rooms[new_room]['items']:
            if new_room not in game.traps_triggered:
                game.traps_triggered.add(new_room)  # Add the room to traps_triggered
                teleport_destination = random.choice(list(game.rooms.keys()))
                game.players[player_id]['current_room'] = teleport_destination
                return True, f"You triggered a trap! You have been teleported to {teleport_destination}."

        # Handle Excalibur
        if 'excalibur' in game.rooms[new_room]['items']:
            game.rooms[new_room]['items'].remove('excalibur')
            game.players[player_id]['current_room'] = game.exit_room
            return True, "You found Excalibur! You've been teleported to the exit room."

        # Handle Teleportation Chamber
        if new_room == 'Teleportation Chamber':
            new_room = random.choice([room for room in game.rooms if room != 'Teleportation Chamber'])
            game.players[player_id]['current_room'] = new_room
            return True, f"You have been teleported to {new_room}."

        # Regular movement
        room_items = game.rooms[new_room]['items']
        items_message = f"You see the following items: {', '.join(room_items)}" if room_items else "There are no items in the room."

        exits = game.rooms[new_room].get('exits', {})
        if isinstance(exits, dict):
            exits_message = f"Exits: {', '.join(exits.keys())}"
        else:
            exits_message = "Exits are not properly defined in this room."

        # Return the movement result
        return True, f"You moved {direction}. \nYou are now in the {new_room}. \n{items_message} \n{exits_message}"


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
        candidate_rooms = [room for room in self.rooms.keys() if room != self.exit_room and room != 'Teleportation Chamber' and room != self.current_room]

        self.poison_room = random.choice(candidate_rooms)
        print(f"Poison placed in {self.poison_room}")  # Debug
    
        if 'items' in self.rooms[self.poison_room]:
            self.rooms[self.poison_room]['items'].append('poison')
            print(f"Poison successfully placed in {self.poison_room}")  # Debug
        else:
            print(f"Room {self.poison_room} does not have an items list.")  # Debug


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
    current_room = game.get_player_room(player_id)  # Get the player's current room
    
    # Normalize the item name to lowercase
    item = item.lower()

    # Logic to take an item in the player's specific game instance
    if item in [room_item.lower() for room_item in game.rooms[current_room]['items']]:
        if item in game.player_inventory.get(player_id, []):
            await ctx.send(f"You already have the {item}.")
        else:
            if item == 'key':
                game.key_found = True
                game.player_inventory.setdefault(player_id, []).append(item)
                game.rooms[current_room]['items'].remove(item)
                await ctx.send("You found the key!")
            else:
                game.player_inventory.setdefault(player_id, []).append(item)
                game.rooms[current_room]['items'].remove(item)
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

    # Call the move function
    move_result = await game.move(direction, ctx)

    # Check if move_result is None or if it's a tuple
    if move_result:
        success, message = move_result  # Unpack the tuple if available
    else:
        success, message = False, "An unknown error occurred."

    if success:
        await ctx.send(message)
    else:
        await ctx.send(message)


@bot.command()
async def start(ctx):
    player_id = ctx.author.id
    if player_id not in game_manager.player_games:
        # Create a new game for the player and add them to the game
        game = PyramidGame()
        game.add_player(player_id)  # Add player to the game
        game_manager.player_games[player_id] = game
        await ctx.send("You have started a new game!")
    else:
        await ctx.send("You are already in a game!")


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

    # Retrieve the player's current room from the players dictionary
    if player_id in game.players:
        current_room = game.players[player_id]['current_room']  # Get the player's current room
    else:
        await ctx.send("Player not found in the game.")
        return

    # Fetch the room information
    current_room_info = game.rooms.get(current_room)

    if current_room_info:
        # List items in the room
        room_items = current_room_info.get('items', [])
        items_message = f"You see the following items in the room: {', '.join(room_items)}." if room_items else "There are no items in the room."
        
        # List exits from the room
        exits_message = f"Exits: {', '.join(current_room_info['exits'].keys())}"
        
        # Send the room description
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
    
    # Get the player's actual current room
    current_room = game.get_player_room(player_id)

    if game.key_found:
        # Check if the player is in the exit room
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

    # Check if the player has an ongoing game
    if player_id not in game_manager.player_games:
        await ctx.send("You are not currently in a game.")
        return

    game = game_manager.player_games[player_id]

    # Cheat to give the player the key and move them to the exit room
    game.key_found = True  # Give the player the key
    game.players[player_id]['current_room'] = game.exit_room  # Move player to exit room

    await ctx.send(f"You have been moved to {game.exit_room} and have the key!")

    # Automatically check for win condition and escape
    if game.check_win_condition(game.exit_room):
        await ctx.send("Congratulations! You used a cheat to win the game.")
        del game_manager.player_games[player_id]  # Reset the game for the player


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
