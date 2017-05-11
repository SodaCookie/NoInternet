class GameState:

    # Booleans
    running = True # check if game running
    terminal_on = True # If on we have default terminal; if off we get free mode
    phone_on = False # If on ignore commands, we append random messages to the current_message
    conversation_on = False # If on additional commands will be unlocked
    cheated = False # if true then game will exit and scold
    debug = False

    # Values
    days = 1
    network_status = "NO CONNECTION"
    flags = set()

    user_input = ""
    current_message = []
    previous_message = []

    conversation_log = []
    conversation_tree = None
    conversation_node = None # Contains the name of the node in the conversation
