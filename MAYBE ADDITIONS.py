# Possibles ADDITIONS FOR LATER:
 
 #ADD PLAYER INSTANCES:
 
class PyramidGame:
    def __init__(self):
        # Initialize game attributes

    def add_player(self, player_id):
        # Create a new game instance for the player
        self.players[player_id] = PyramidGame()

    def get_player_game(self, player_id):
        # Return the game instance for the player
        return self.players.get(player_id)

# Initialize the game in the `start` command
@bot.command()
async def start(ctx):
    game = PyramidGame()
    game.add_player(ctx.author.id)
    await ctx.send("You have started the game!")

# Retrieve the player's game instance in other commands
@bot.command()
async def move(ctx, direction):
    game = ctx.bot.game.get_player_game(ctx.author.id)
    # Move the player in the game instance

@bot.command()
async def look(ctx):
    game = ctx.bot.game.get_player_game(ctx.author.id)
    # Look around in the player's game instance

@bot.command()
async def take(ctx, item):
    game = ctx.bot.game.get_player_game(ctx.author.id)
    # Take an item in the player's game instance

# Other commands similarly modified to operate on the player's game instance


#ADD NPCS

class NPC:
    def __init__(self, name, description, dialogue):
        self.name = name
        self.description = description
        self.dialogue = dialogue

    def get_dialogue(self):
        return self.dialogue

class Room:
    def __init__(self, name, description, items, npc=None):
        self.name = name
        self.description = description
        self.items = items
        self.npc = npc

    def get_description(self):
        if self.npc:
            return f"{self.description}\nYou see {self.npc.name} here."
        else:
            return self.description

class MazeGame:
    def __init__(self):
        # Initialize rooms and NPCs
        self.rooms = {
            'Foyer': Room('Foyer', 'You are in the Foyer.', ['torch']),
            'ExitRoom': Room('Exit Room', 'You are in the Exit Room.', []),
        }

        self.rooms['Foyer'].npc = NPC('Guide', 'A friendly guide', 'The exit room is to the north.')

    # Other methods for interacting with the game

# Command for talking to NPCs
@bot.command()
async def talk(ctx, npc_name):
    if ctx.bot.game is None:
        await ctx.send("You are not currently in the game.")
        return

    game = ctx.bot.game
    current_room = game.current_room

    if current_room.npc and current_room.npc.name.lower() == npc_name.lower():
        dialogue = current_room.npc.get_dialogue()
        await ctx.send(f"{current_room.npc.name}: {dialogue}")
    else:
        await ctx.send(f"There is no NPC named {npc_name} in this room.")

#ADD RIDDLE ROOM
class Room:
    def __init__(self, name, description, riddle=None, solution=None, items=None, exits=None):
        self.name = name
        self.description = description
        self.riddle = riddle  # Riddle prompt
        self.solution = solution  # Correct solution to the riddle
        self.items = items if items else []  # Items in the room
        self.exits = exits if exits else {}  # Exits from the room

    def present_riddle(self):
        return self.riddle

    def check_solution(self, answer):
        return answer.lower() == self.solution.lower()

# Example usage:
riddle_room = Room(
    name="Riddle Room",
    description="You enter a dimly lit room with a mysterious aura.",
    riddle="I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?",
    solution="echo",
    exits={'north': 'Exit Room'}
)

# Handle player interaction
async def handle_riddle(ctx, room):
    await ctx.send(room.description)
    await ctx.send(room.present_riddle())
    
    def check(answer):
        return answer.author == ctx.author and answer.channel == ctx.channel
    
    try:
        answer = await bot.wait_for('message', check=check, timeout=60)  # Wait for player's answer
        if room.check_solution(answer.content):
            await ctx.send("Correct! You solved the riddle and can proceed to the next room.")
            # Allow player to proceed to the next room
            # Update player's current room
        else:
            await ctx.send("Incorrect answer. Try again.")
            # Provide another chance for the player to solve the riddle
    except asyncio.TimeoutError:
        await ctx.send("Time's up! You didn't solve the riddle in time.")

# Example command to interact with the riddle room
@bot.command()
async def enter_riddle_room(ctx):
    await handle_riddle(ctx, riddle_room)
    
#EXTRA TRAPS
    
class PyramidGame:
    def __init__(self):
        # Other initialization code...
        self.trap_count = 0  # Add a trap count attribute to keep track of the number of traps placed

    def place_trap(self):
        # Get a list of all rooms except the exit room and teleportation chamber
        candidate_rooms = [room for room in self.rooms.keys() if room != self.exit_room and room != 'Teleportation Chamber']

        # Select three random rooms to place traps
        trap_rooms = random.sample(candidate_rooms, 3)

        for trap_room in trap_rooms:
            # Place the trap in the selected room
            self.rooms[trap_room]['items'].append('trap')
            self.trap_count += 1  # Increment the trap count

