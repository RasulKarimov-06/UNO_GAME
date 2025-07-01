import pygame
import sys
from button1 import Button
import re
import random
import time
from pygame import mixer
import sqlite3

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Uno Odyssey")

BG = pygame.image.load("Assets/Background.png") #file

def get_font(size):
    return pygame.font.Font("Assets/font (1).ttf", size) #file

def play(colour):
    running= True
    while running:


        pygame.init()

        # Define colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)

        # Create the main menu screen
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("UNO Menu")

        # Create a font
        font = pygame.font.Font(None, 36)


        card_pos = {17:-225, 15:-150, 13:-75, 11:0, 9:75, 7:150, 5:225, 3:300, 1:375, -1:3000} #data structure
        #/////////////////////////////////////////////////////////////////
        #Graphical Functions

        def draw_text(text, color, x, y):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            screen.blit(text_surface, text_rect)

        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 32)
        fonts = pygame.font.Font('freesansbold.ttf', 24)
        popupfont = pygame.font.Font('freesansbold.ttf', 20)
        clock = pygame.time.Clock()

        def increment_win(username):
            try:
                connect = sqlite3.connect("testing2.db") #file
                cursor = connect.cursor()

                # Fetch the current number of wins
                query = "SELECT Wins FROM User WHERE Username = ?"
                cursor.execute(query, (username,))
                current_wins = cursor.fetchone()[0]

                # Increment the number of wins
                new_wins = current_wins + 1

                # Update the database with the new number of wins
                update_query = "UPDATE User SET Wins = ? WHERE Username = ?"
                cursor.execute(update_query, (new_wins, username))

                connect.commit()
                print(f"Win count for {username} has been incremented.")

            except sqlite3.Error as error:
                print("Error incrementing wins:", error)
            finally:
                if connect:
                    connect.close()
                    print("SQLite connection is closed")

        def is_username_unique(username):
            try:
                connect = sqlite3.connect("testing2.db") #file
                cursor = connect.cursor()

                query = "SELECT * FROM User WHERE Username = ?"
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                return result is None  # If result is None, username is unique
            except sqlite3.Error as error:
                print("Error checking username uniqueness:", error)
                return False
            finally:
                if connect:
                    connect.close()

        def register(username, password):
            try:
                connect = sqlite3.connect("testing2.db") #file
                cursor = connect.cursor()

                newUser = """INSERT INTO User
                (Username, Password, Wins)
                VALUES (?, ?, ?)"""

                cursor.execute(newUser, (username, password, 0))

                connect.commit()
                print("New user has been added to the database")

            except sqlite3.Error as error:
                print("Failure in adding user", error)
            finally:
                if connect:
                    connect.close()
                    print("SQLite connection is closed")

        def check_login(username, password):
            try:
                connect = sqlite3.connect("testing2.db") #file
                cursor = connect.cursor()

                query = "SELECT * FROM User WHERE Username = ? AND Password = ?"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()

                return result is not None  # If result is not None, login is successful
            except sqlite3.Error as error:
                print("Error checking login credentials:", error)
                return False
            finally:
                if connect:
                    connect.close()

        def recovery (username,password):
            connect = sqlite3.connect("testing2.db") #file
            cursor = connect.cursor()

            query = "SELECT * FROM User WHERE Username = ?"
            cursor.execute(query, (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                # Update the password for the specified username
                cursor.execute('UPDATE User SET password = ? WHERE username = ?', (password, username))
                connect.commit()
                return True
            else:
                return False

        def draw_text(text, color, x, y):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            screen.blit(text_surface, text_rect)

        def play_menu():
            account = None
            running = True
            while running:
                screen.fill((0, 0, 0))
                MENU_TEXT = get_font(40).render("LOGIN TO PLAY", True, "White")
                MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

                cursor_pos = pygame.mouse.get_pos()
                # Create a "Register and Login" button
                register_button = pygame.Rect(300, 200, 200, 50)
                login_button = pygame.Rect(300, 275, 200, 50)
                recovery_button = pygame.Rect(300, 350, 200, 50)
                pygame.draw.rect(screen, (0, 255, 0), register_button)
                draw_text("Register", (0, 0, 0), 400, 225)
                pygame.draw.rect(screen, (0, 255, 0), login_button)
                draw_text("Login", (0, 0, 0), 400, 300)
                pygame.draw.rect(screen, (0,255,0), recovery_button)
                draw_text("Recovery", (0, 0, 0), 400, 375)

                QUIT_BUTTON = Button(image=None, pos=(400, 500), 
                            text_input="BACK", font=get_font(25), base_color="#d7fcd4", hovering_color=colour)
                QUIT_BUTTON.changeColor(cursor_pos)
                QUIT_BUTTON.update(SCREEN)

                SCREEN.blit(MENU_TEXT, MENU_RECT)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if register_button.collidepoint(event.pos):
                            register_main()
                        if login_button.collidepoint(event.pos):
                            print("Login Activated")
                            login_main()
                        if recovery_button.collidepoint(event.pos):
                            print("Recovery Activated")
                            recovery_main()
                        if QUIT_BUTTON.checkForInput(cursor_pos):
                            running=False

                pygame.display.update()
            return running

        def register_main():

            username_box_height = 32
            password_box_height = 32
            box_spacing = 45  # Spacing between the two boxes

            # Initial positions
            input_box_y = (600 - (username_box_height + password_box_height + box_spacing)) // 2
            username_box = pygame.Rect(285, input_box_y, 200, username_box_height)
            password_box = pygame.Rect(285, input_box_y + username_box_height + box_spacing, 200, password_box_height)

            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            username_color = color_inactive
            password_color = color_inactive
            username_active = False
            password_active = False
            username_text = ''
            password_text = ''
            max_length = 20  # Maximum character limit
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if username_box.collidepoint(event.pos):
                            username_active = not username_active
                            password_active = False
                            username_color = color_active if username_active else color_inactive
                            password_color = color_inactive
                        elif password_box.collidepoint(event.pos):
                            password_active = not password_active
                            username_active = False
                            password_color = color_active if password_active else color_inactive
                            username_color = color_inactive
                        else:
                            username_active = False
                            password_active = False
                            username_color = color_inactive
                            password_color = color_inactive
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if username_text and password_text:
                                if is_username_unique(username_text):
                                    username = username_text
                                    password = password_text
                                    username_text = ''
                                    password_text = ''
                                    register(username, password)
                                    running = False
                                else:
                                    popup = popupfont.render("Username already exists. Please choose a different username.", True, (255, 255, 255))
                                    screen.blit(popup, (80, 460))
                                    pygame.display.update()
                                    time.sleep(1.5)
                        elif event.key == pygame.K_BACKSPACE:
                            if username_active:
                                username_text = username_text[:-1]
                            elif password_active:
                                password_text = password_text[:-1]
                        else:
                            if len(username_text) < max_length and username_active:
                                username_text += event.unicode
                            elif len(password_text) < max_length and password_active:
                                password_text += event.unicode

                screen.fill((30, 30, 30))

                user_head = fonts.render("Username", True, (255, 255, 255))
                pass_head = fonts.render("Password", True, (255, 255, 255))
                screen.blit(user_head, (400 - user_head.get_width() // 2, 220))
                screen.blit(pass_head, (400 - pass_head.get_width() // 2, 295))

                # Render the current text for the username.
                username_txt_surface = font.render(username_text, True, username_color)
                width = max(200, username_txt_surface.get_width() + 10)
                username_box.w = width
                username_box.x = 400 - username_box.width // 2  # Center the box
                screen.blit(username_txt_surface, (username_box.x + 5, username_box.y + 5))
                pygame.draw.rect(screen, username_color, username_box, 2)

                # Render the current text for the password.
                password_txt_surface = font.render("*" * len(password_text), True, password_color)
                width = max(200, password_txt_surface.get_width() + 10)
                password_box.w = width
                password_box.x = 400 - password_box.width // 2  # Center the box
                screen.blit(password_txt_surface, (password_box.x + 5, password_box.y + 5))
                pygame.draw.rect(screen, password_color, password_box, 2)

                pygame.display.flip()
                clock.tick(30)
    
        def login_main():
            account = None
            win=None
            username_box_height = 32
            password_box_height = 32
            box_spacing = 45  # Spacing between the two boxes

            # Initial positions
            input_box_y = (600 - (username_box_height + password_box_height + box_spacing)) // 2
            username_box = pygame.Rect(285, input_box_y, 200, username_box_height)
            password_box = pygame.Rect(285, input_box_y + username_box_height + box_spacing, 200, password_box_height)

            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            username_color = color_inactive
            password_color = color_inactive
            username_active = False
            password_active = False
            username_text = ''
            password_text = ''
            max_length = 20  # Maximum character limit
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if username_box.collidepoint(event.pos):
                            username_active = not username_active
                            password_active = False
                            username_color = color_active if username_active else color_inactive
                            password_color = color_inactive
                        elif password_box.collidepoint(event.pos):
                            password_active = not password_active
                            username_active = False
                            password_color = color_active if password_active else color_inactive
                            username_color = color_inactive
                        else:
                            username_active = False
                            password_active = False
                            username_color = color_inactive
                            password_color = color_inactive
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if username_text and password_text:
                                if check_login(username_text, password_text):
                                    print("Successfully logged in as",username_text)
                                    account = username_text
                                    running = False
                                else:
                                    account = None
                        elif event.key == pygame.K_BACKSPACE:
                            if username_active:
                                username_text = username_text[:-1]
                            elif password_active:
                                password_text = password_text[:-1]
                        else:
                            if len(username_text) < max_length and username_active:
                                username_text += event.unicode
                            elif len(password_text) < max_length and password_active:
                                password_text += event.unicode

                screen.fill((30, 30, 30))

                user_head = fonts.render("Username", True, (255, 255, 255))
                pass_head = fonts.render("Password", True, (255, 255, 255))
                screen.blit(user_head, (400 - user_head.get_width() // 2, 220))
                screen.blit(pass_head, (400 - pass_head.get_width() // 2, 295))

                # Render the current text for the username.
                username_txt_surface = font.render(username_text, True, username_color)
                width = max(200, username_txt_surface.get_width() + 10)
                username_box.w = width
                username_box.x = 400 - username_box.width // 2  # Center the box
                screen.blit(username_txt_surface, (username_box.x + 5, username_box.y + 5))
                pygame.draw.rect(screen, username_color, username_box, 2)

                # Render the current text for the password.
                password_txt_surface = font.render("*" * len(password_text), True, password_color)
                width = max(200, password_txt_surface.get_width() + 10)
                password_box.w = width
                password_box.x = 400 - password_box.width // 2  # Center the box
                screen.blit(password_txt_surface, (password_box.x + 5, password_box.y + 5))
                pygame.draw.rect(screen, password_color, password_box, 2)

                pygame.display.flip()
                clock.tick(30)

            if account != None:
                game(account)
            elif account == None:
                running = False

        def recovery_main():
            account = None
            username_box_height = 32
            password_box_height = 32
            box_spacing = 45  # Spacing between the two boxes

            # Initial positions
            input_box_y = (600 - (username_box_height + password_box_height + box_spacing)) // 2
            username_box = pygame.Rect(285, input_box_y, 200, username_box_height)
            password_box = pygame.Rect(285, input_box_y + username_box_height + box_spacing, 200, password_box_height)

            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            username_color = color_inactive
            password_color = color_inactive
            username_active = False
            password_active = False
            username_text = ''
            password_text = ''
            max_length = 20  # Maximum character limit
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if username_box.collidepoint(event.pos):
                            username_active = not username_active
                            password_active = False
                            username_color = color_active if username_active else color_inactive
                            password_color = color_inactive
                        elif password_box.collidepoint(event.pos):
                            password_active = not password_active
                            username_active = False
                            password_color = color_active if password_active else color_inactive
                            username_color = color_inactive
                        else:
                            username_active = False
                            password_active = False
                            username_color = color_inactive
                            password_color = color_inactive
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if username_text and password_text:
                                if recovery(username_text, password_text):
                                    print("Successfully changed password")
                                    account = username_text
                                    running = False
                                else:
                                    print("Username does not exist")
                                    account = None
                        elif event.key == pygame.K_BACKSPACE:
                            if username_active:
                                username_text = username_text[:-1]
                            elif password_active:
                                password_text = password_text[:-1]
                        else:
                            if len(username_text) < max_length and username_active:
                                username_text += event.unicode
                            elif len(password_text) < max_length and password_active:
                                password_text += event.unicode

                screen.fill((30, 30, 30))

                user_head = fonts.render("Username", True, (255, 255, 255))
                pass_head = fonts.render("Password", True, (255, 255, 255))
                screen.blit(user_head, (400 - user_head.get_width() // 2, 220))
                screen.blit(pass_head, (400 - pass_head.get_width() // 2, 295))

                # Render the current text for the username.
                username_txt_surface = font.render(username_text, True, username_color)
                width = max(200, username_txt_surface.get_width() + 10)
                username_box.w = width
                username_box.x = 400 - username_box.width // 2  # Center the box
                screen.blit(username_txt_surface, (username_box.x + 5, username_box.y + 5))
                pygame.draw.rect(screen, username_color, username_box, 2)

                # Render the current text for the password.
                password_txt_surface = font.render("*" * len(password_text), True, password_color)
                width = max(200, password_txt_surface.get_width() + 10)
                password_box.w = width
                password_box.x = 400 - password_box.width // 2  # Center the box
                screen.blit(password_txt_surface, (password_box.x + 5, password_box.y + 5))
                pygame.draw.rect(screen, password_color, password_box, 2)

                pygame.display.flip()
                clock.tick(30)


        def fetch_win(account):
            try:
                connect = sqlite3.connect("testing2.db") #file
                cursor = connect.cursor()

                query = "SELECT Wins FROM User WHERE Username = ?"
                cursor.execute(query, (account,))
                result = cursor.fetchone()

                if result is not None:  # If result is not None, login is successful
                    wins=result[0]
                    return wins
                else:
                    print("User not found")
            except sqlite3.Error as error:
                print("Error in finding wins:", error)
                return False
            finally:
                if connect:
                    connect.close()

        def game(account):
            running = True
            while running:
                cursor_pos = pygame.mouse.get_pos()
                screen.fill(BLACK)
                wins=fetch_win(account)
                username_text = "Username: " + account
                win_text = "Win count: " + str(wins)
                accounts = fonts.render(username_text, True, (255, 255, 255))
                win_counts = fonts.render(win_text, True, (255,255,255))
                accounts_rect = accounts.get_rect(center=(400, 450))
                win_rects = win_counts.get_rect(center=(400,500))
                screen.blit(accounts, accounts_rect)
                screen.blit(win_counts, win_rects)
                draw_text("UNO Menu", WHITE, 400, 100)

                # Create a "New Game" button
                new_game_button = pygame.Rect(300, 200, 200, 50)
                pygame.draw.rect(screen, GREEN, new_game_button)
                draw_text("Multiplayer", BLACK, 400, 225)
                ai_button = pygame.Rect(300, 300, 200, 50)
                pygame.draw.rect(screen, GREEN, ai_button)
                draw_text("Beat AI", BLACK, 400, 325)
                QUIT_BUTTON = Button(image=None, pos=(400, 550), 
                            text_input="BACK", font=get_font(16), base_color="#d7fcd4", hovering_color=colour)
                QUIT_BUTTON.changeColor(cursor_pos)
                QUIT_BUTTON.update(SCREEN)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if new_game_button.collidepoint(event.pos):
                            player_selection(account)
                        if ai_button.collidepoint(event.pos):
                            ai_game(account)
                        if QUIT_BUTTON.checkForInput(cursor_pos):
                            running = False

                pygame.display.update()


        def ai_game(account):
            print("Welcome to the AI game")
            ai = True
            start_game(2, ai, account)
            

        def player_selection(account):
            global playeramount
            running = True
            while running:
                screen.fill(BLACK)
                cursor_pos = pygame.mouse.get_pos()
                draw_text("Select Number of Players", WHITE, 400, 100)

                # Create buttons for 2, 3, and 4 players
                button_2_players = pygame.Rect(300, 200, 200, 50)
                button_3_players = pygame.Rect(300, 300, 200, 50)
                button_4_players = pygame.Rect(300, 400, 200, 50)
                QUIT_BUTTON = Button(image=None, pos=(400, 550), 
                            text_input="BACK", font=get_font(25), base_color="#d7fcd4", hovering_color=colour)
                QUIT_BUTTON.changeColor(cursor_pos)
                QUIT_BUTTON.update(SCREEN)

                pygame.draw.rect(screen, GREEN, button_2_players)
                pygame.draw.rect(screen, GREEN, button_3_players)
                pygame.draw.rect(screen, GREEN, button_4_players)

                draw_text("2 Players", BLACK, 400, 225)
                draw_text("3 Players", BLACK, 400, 325)
                draw_text("4 Players", BLACK, 400, 425)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_2_players.collidepoint(event.pos):
                            playeramount=2
                            ai = False
                            start_game(playeramount, ai, account)
                        elif button_3_players.collidepoint(event.pos):
                            playeramount=3
                            ai = False
                            start_game(playeramount, ai, account)
                        elif button_4_players.collidepoint(event.pos):
                            playeramount=4
                            ai = False
                            start_game(playeramount, ai, account)
                        elif QUIT_BUTTON.checkForInput(cursor_pos):
                            running = False
                pygame.display.update()

        def start_game(playeramount, ai, account):
            # You can now pass `num_players` to your UNO game logic
            # Initialize your UNO game with the selected number of players

            screen = pygame.display.set_mode((800,600))
            screen.fill('orange')

            colours_coords={"Red": 0, "Green": 78 , "Yellow": 154, "Blue": 233} #list of colours // data structure
            values_coords={'0':0,'1':56,'2':112,'3':164,'4':216,'5':270,'6':322,'7':376,'8':428,'9':482,"Draw Two":640,"Skip":588,"Reverse":534} #list of values // data structure
            specials_coords={"Wild":694,"Wild Draw Four":746} #list of wilds // data structure

            retrieve_colours={0: "Red", 78: "Green" , 154: "Yellow", 233: "Blue"} #list of colours //data structure
            retrieve_values={0:'0', 56:'1', 112:'2', 164:'3', 216:'4', 270:'5', 322:'6', 376:'7', 428:'8', 482:'9', 640:"Draw Two", 588:"Skip", 534:"Reverse"} #list of values // data structure
            retrieve_specials={694:"Wild", 746:"Wild Draw Four"} #list of wilds // data structure

            spritesheet = pygame.image.load("spritesheet.png") #file

            #Player Font
            font = pygame.font.Font('freesansbold.ttf', 32)

            #Hint Font
            fonts = pygame.font.Font('freesansbold.ttf', 24)

            #Game Functions
            def WholeDeck():
                deck=[] #initialise deck
                colours=["Red", "Green", "Yellow", "Blue"] #list of colours // data structure
                values=[0,1,2,3,4,5,6,7,8,9,"Draw Two","Skip","Reverse"] #list of values // data structure
                specials=["Wild","Wild Draw Four"] #list of wilds // data structure
                for colour in colours: #cycling through all colours
                    for value in values: #cycling through all values 
                        cardVal = "{} {}".format(colour,value) #formating the cards as Red 4, Blue 2, etc
                        deck.append(cardVal) #appending these new values we created through format into the deck list
                        if value !=0: #if value doesn't equal zero we can append them twice so there is two of ever Blue 2
                            deck.append(cardVal) #ensures uniqueness of Red 0, Blue 0, etc. Only 1 Zero for each colour
                for i in range(4): #creating only 4 wild and 4 wild draw 4 in the deck
                    deck.append(specials[0])
                    deck.append(specials[1])
                return deck

            #Now we need to shuffle the list so the cards are randomised within the deck
            def shuffle(deck):
                for cardPos in range(len(deck)):#cycle through the entire deck we created
                    randPos=random.randint(0,107) #108 cards in UNO deck, use 107 to access every single one of them
                    deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos] #swapping each element with a random element, to create shuffling
                    if deck[0]=="Wild" or "Wild Draw Four": #making sure that the deck doesn't start of with wilds as when the game starts the colour called is randomised and players will not know
                        deck[0], deck[randPos] = deck[randPos], deck[0] #swapping them with random position very rare to have another wild
                return deck

            GameDeck=WholeDeck() #constructing the deck
            GameDeck=shuffle(GameDeck)
            GameDeck=shuffle(GameDeck)
            discards=[] #so we can see the top card of the discard pile to show which moves are valid or not

            #We now need to make a function that will draw a specific amount of cards out for the user
            #amount will be the number of cards in the user's hand
            def Draw(amount):
                CardsDrawn=[] #initialising list to hold user cards
                for i in range(amount): #done so we can cycle amount of times as amount will be an integer
                    CardsDrawn.append(GameDeck.pop(0)) #so once we draw from the deck we remove it from the top
                return CardsDrawn

            #we need to create a function that allows the players to see their own hand
            def ShowHand(players, playerturn):
                card_rects =[]
                hand = players[playerturn]
                card_pos = {17:-225, 15:-150, 13:-75, 11:0, 9:75, 7:150, 5:225, 3:300, 1:375, -1:3000} #data structure
                if len(hand)%2==0:
                    j = card_pos[len(hand)-1]
                else:
                    j = card_pos[len(hand)]
                for i in hand:
                    if i == 'Wild':
                        value_coord = specials_coords[i]
                        colour_coord = 0
                    elif i == 'Wild Draw Four':
                        value_coord = specials_coords[i]
                        colour_coord = 0
                    else:
                        splits=i.split(' ', 1)
                        colour_coord = colours_coords[splits[0]]
                        value_coord = values_coords[splits[1]]
           
                    card_rect = pygame.Rect(value_coord,colour_coord, 50, 78) #last two variables are card size, first two are coords
                    card_rects.append(card_rect)
                    individual_card = spritesheet.subsurface(card_rect)
                    screen.blit(individual_card, (j,400))
                    j+=75
                return card_rects

            #This functions purpoe is to indicate what cards can be played based on the previous card dealt
            def canPlay(colour,value,playerhand): #making a function to judge legal moves
                for card in playerhand: #cycles through player hand
                    if "Wild" in card: #if wild is found in player hand
                        return True #legal move
                    elif colour in card or value in card: #if colour or value matches the hand
                        return True #legal move
                return False #if it fails to meet either condiditons there is no legal move here

            def Legal(colour,value,card): #making a function to judge legal moves
                if "Wild" in card: #if wild is found in player hand
                    return True #legal move
                elif colour in card or value in card: #if colour or value matches the hand
                    return True #legal move
                elif "Wild" in discards[-1]:
                    if colour in card:
                        return True
                return False #if it fails to meet either condiditons there is no legal move here

            def Wild(colours):
                looped = True
                while looped == True:
                    screen.fill(BLACK)

                    red_button = pygame.Rect(300, 150, 200, 50)
                    green_button = pygame.Rect(300, 250, 200, 50)
                    yellow_button = pygame.Rect(300, 350, 200, 50)
                    blue_button = pygame.Rect(300, 450, 200, 50)

                    pygame.draw.rect(screen, GREEN, red_button)
                    pygame.draw.rect(screen, GREEN, green_button)
                    pygame.draw.rect(screen, GREEN, yellow_button)
                    pygame.draw.rect(screen, GREEN, blue_button)

                    draw_text("RED", BLACK, 400, 175)
                    draw_text("GREEN", BLACK, 400, 275)
                    draw_text("YELLOW", BLACK, 400, 375)
                    draw_text("BLUE", BLACK, 400, 475)

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if red_button.collidepoint(event.pos):
                                currentColour = colours[0]
                                looped = False
                            elif green_button.collidepoint(event.pos):
                                currentColour = colours[1]
                                looped = False
                            elif yellow_button.collidepoint(event.pos):
                                currentColour = colours[2]
                                looped = False
                            elif blue_button.collidepoint(event.pos):
                                currentColour = colours[3]
                                looped = False
                    pygame.display.update()
                return currentColour

            def DrawTwo(players, playerturn, playerdirection):
                playerDraw=playerturn+playerdirection #allows for the next player onward to collect the cards
                if playerDraw>=playeramount: #same conditional as the cycling 
                    playerDraw=0
                elif playerturn<0:
                    playerDraw=playeramount-1
                players[playerDraw].extend(Draw(2)) #the player that the +2 follows is forced to draw 2 cards

            def DrawFour(players, playerturn, playerdirection):
                playerDraw=playerturn+playerdirection
                if playerDraw>=playeramount:
                    playerDraw=0
                elif playerturn<0:
                    playerDraw=playeramount-1
                players[playerDraw].extend(Draw(4)) #subsequent player draws 4

            def Skip(playerturn, playeramount):
                    if playerturn==playeramount: #if the player turn reaches the player amount we need to cycle back
                        playerturn=0 #so we bring it back to 0
                    elif playerturn<0: #if the direction is opposite and goes below 0, we bring it back to playeramount-1 
                        playerturn=playeramount-1
                    return playerturn

            def show_player():
                player_font = font.render("Player: " +str(playerturn+1), True, (255, 255, 255))
                screen.blit(player_font, (325,500))

            def show_discard():
                discard_card = discards[-1]
                if discard_card == 'Wild':
                    value_coord = specials_coords[discard_card]
                    colour_coord = 0
                elif discard_card == 'Wild Draw Four':
                    value_coord = specials_coords[discard_card]
                    colour_coord = 0
                else:
                    splits=discard_card.split(' ', 1)
                    colour_coord = colours_coords[splits[0]]
                    value_coord = values_coords[splits[1]]

                discard_card_rect = pygame.Rect(value_coord,colour_coord, 50, 78) #last two variables are card size, first two are coords
                individual_card = spritesheet.subsurface(discard_card_rect) #file structure
                screen.blit(individual_card, (375,50))

            def register_clicks(mousex, mousey, initial_x, end):
                if 478>=mousey>=400:
                    if end>=mousex>=initial_x:
                        card_count=-1
                        for x in range(initial_x,end+1,75):
                            cards=x
                            cards+=50
                            card_count+=1
                            if cards>=mousex>=x:
                                rect_string = card_rects[card_count]
                                values = list(rect_string)
                                return values

            def reaction():
                CLICK = font.render("CLICK NOW!", True, (255,255,255))
                clicked = False
                start = time.time()
                while clicked == False:
                    screen.fill('orange')
                    screen.blit(CLICK, (300,275))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            end=time.time()
                            clicked = True
                interval = end - start
                return interval

            mixer.music.load("Let's Play.mp3") #file structure
            mixer.music.play(-1)
            #now we will start our match with the players
            players=[] #initialising players hands
            colours=["Red", "Green", "Yellow", "Blue"] #colours list that will be prevalent during Wild choices // data structure
            for i in range(playeramount): #gives each player five cards
                players.append(Draw(5))
            playerturn=0 #initalise a variable to indicate whos turn it is
            playerdirection=1 #create a variable to indicate who's turn is going to be next, i used 1 as if a reverse card is played we can multiply it by -1 to flip the direction
            playing=True #initialises variable that carries out the game
            discard_pos = 0
            Starting = False
            while Starting == False:
                if 'Wild' in GameDeck[discard_pos]:
                    discard_pos+=1
                else:
                    Starting = True
            discards.append(GameDeck.pop(discard_pos)) #discards list will take the first card in the deck

            splitCards=discards[-1].split(' ',1) #last card (which is on top) will be split into its string and integer
            currentColour=splitCards[0] #self explanatory
            if currentColour!='Wild': #if colour is not equal to wild then values from the split will be accounted for
                currentVal=splitCards[1]
            else:
                currentVal='Any' #if not then any value can be chosen

            if ai == True:
                running = True
                playerturn = 0  # 0 for human player, 1 for AI player
                card = None

                while running:
                    Legals = False
                    skipped  = False
                    passed = False
                    if "Wild" in discards[-1]:
                        currentColour = currentColour
                        currentVal = 'Any'
                    else:
                        splitCards = discards[-1].split(' ',1)
                        currentColour = splitCards[0]
                        currentVal=splitCards[1]
                    values=[]
                    card_rects = ShowHand(players, playerturn)
                    playerhand = players[playerturn]
                    if len(playerhand)%2==0:
                        initial_x = card_pos[len(playerhand)-1]
                        even_x = card_pos[len(playerhand)+1]
                        end = 800 - even_x
                    else:
                        initial_x = card_pos[len(playerhand)]
                        end = 800 - initial_x
                        pygame.display.update()
                    screen.fill('orange')
                    ShowHand(players, playerturn)
                    show_player()
                    show_discard()
                    pygame.display.update()

                    if playerturn == 0:  # Human player's turn
                        if canPlay(currentColour, currentVal, playerhand):
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                    pygame.mixer.music.pause()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if event.button == 1:
                                        mousex, mousey = pygame.mouse.get_pos()
                                        values=register_clicks(mousex, mousey, initial_x, end)
                                        if values !=None:
                                            if values[0] == 694:
                                                card = retrieve_specials[values[0]]
                                                currentColour = Wild(colours)
                                                Legals = True
                                                for x in range(len(players[playerturn])):
                                                    if card == players[playerturn][x]:
                                                        break
                                                discards.append(players[playerturn].pop(x))
                                            elif values[0] == 746:
                                                card = retrieve_specials[values[0]]
                                                currentColour = Wild(colours)
                                                DrawFour(players, playerturn, playerdirection)
                                                Legals = True
                                                for x in range(len(players[playerturn])):
                                                    if card == players[playerturn][x]:
                                                        break
                                                discards.append(players[playerturn].pop(x))
                                            else:
                                                color = retrieve_colours[values[1]]
                                                value = retrieve_values[values[0]]
                                                card = color + " " + value
                                                if Legal(currentColour, currentVal, card) == False:
                                                    hint = fonts.render("Illegal Move can only play same colour, value or Wild", True, (255,255,255))
                                                    screen.blit(hint, (80,275))
                                                    pygame.display.update()
                                                    time.sleep(2.5)
                                                else:
                                                    if value == "Reverse": #function for reverse cards
                                                        playerdirection=playerdirection*-1 #inverse player direction
                                                    elif value == "Skip": #function for skip
                                                        skipped = True
                                                    elif value == "Draw Two": #function for draw 2
                                                        DrawTwo(players,playerturn,playerdirection)
                                                    Legals = True
                                                    for x in range(len(players[playerturn])):
                                                        if card == players[playerturn][x]:
                                                            break
                                                    discards.append(players[playerturn].pop(x))
                                            screen.fill('orange')
                                            ShowHand(players, playerturn)
                                            show_discard()
                                            pygame.display.update()
                                            if len(players[playerturn]) == 0:
                                                player_font = font.render("Player: " +str(playerturn+1)+" is the Winner!", True, (255, 255, 255))
                                                screen.blit(player_font, (200, 300))
                                                pygame.display.update()
                                                pygame.mixer.music.pause()
                                                time.sleep(5)
                                                increment_win(account)
                                                running = False
                                            elif len(players[playerturn]) == 1:
                                                SLOW = font.render("TOO SLOW!", True, (255,255,255))
                                                UNO = font.render("UNO!", True, (255,255,255))
                                                if "Wild" in discards[-1]:
                                                    react = 1.5
                                                else:
                                                    react = 0.75
                                                if reaction() > react:
                                                    screen.fill('orange')
                                                    screen.blit(SLOW, (315,275))
                                                    pygame.display.update()
                                                    players[playerturn].extend(Draw(2))
                                                    time.sleep(2)
                                                else:
                                                    screen.fill('orange')
                                                    screen.blit(UNO,(350,275))
                                                    pygame.display.update()
                                                    time.sleep(2)
                                            elif len(players[playerturn]) > 11:
                                                player_font = font.render("Player: " +str(playerturn+1)+" loses, they still have 11+ cards!", True, (255, 255, 255))
                                                screen.blit(player_font, (75, 300))
                                                pygame.display.update()
                                                pygame.mixer.music.pause()
                                                time.sleep(5)
                                                running = False
                        else:
                            players[playerturn].extend(Draw(1))
                            time.sleep(1.5)
                            Legals = True
                        if Legals == True:
                            if skipped == True:
                                playerturn=playerturn+playerdirection
                                playerturn=Skip(playerturn, playeramount)
                            playerturn=playerturn+playerdirection #moves on to the next player, if skip was played this stacks on and misses next player
                            if playerturn>=playeramount: #cycling function again to ensure that player direction doesn't go out of bounds even when there is no specific function played
                                playerturn=0
                            elif playerturn<0:
                                playerturn=playeramount-1
                            while passed == False:
                                screen.fill('orange')
                                if skipped == False:
                                    pass_font = fonts.render("Pass to AI, click when you're ready!", True, (255,255,255))
                                    screen.blit(pass_font,(180,275))
                                else:
                                    pass_font = fonts.render("Pass to Player: "+str(playerturn+1)+" click when you're ready!", True, (255,255,255))
                                    screen.blit(pass_font,(160,275))
                                pygame.display.update()
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        passed = True

                    else: #AI turn
                        play = False
                        # Simulate AI's move (replace this with your AI logic)
                        if canPlay(currentColour, currentVal, playerhand):
                            play = True
                            available_cards = []
                            for i in range(len(playerhand)):
                                if "Wild" in playerhand:
                                    available_cards.append(playerhand[i])
                                elif Legal(currentColour, currentVal, playerhand[i]) == True:
                                    available_cards.append(playerhand[i])
                            for i in range(len(available_cards)):
                                if "Wild" in available_cards[i]:
                                    available_cards[0], available_cards[i] = available_cards[i], available_cards[0]
                            cardChosen = available_cards[0]
                            data = cardChosen.split(' ', 1)
                            if "Wild" == cardChosen:
                                reds=0
                                greens=0
                                blues=0
                                yellows=0
                                wilds=0
                                for card in available_cards:
                                    classify = card.split(' ', 1)
                                    if classify[0] == "Red":
                                        reds+=1
                                    elif classify[0] == "Blue":
                                        blues+=1
                                    elif classify[0] == "Yellow":
                                        yellows+=1
                                    elif classify[0] == "Green":
                                        greens+=1
                                    else:
                                        wilds=wilds
                                colour_count=[reds,blues,yellows,greens]
                                colours_count={reds:"Red", blues:"Blue", greens:"Green", yellows:"Yellow"}
                                colour_count.sort(reverse=True)
                                currentColour = colours_count[colour_count[0]]
                                screen.fill('orange')
                                show_discard()
                                colour_show = fonts.render("AI has picked "+currentColour, True, (255,255,255))
                                screen.blit(colour_show, (275, 300))
                                pygame.display.update()
                                time.sleep(1)
                                Legals = True
                                currentVal = 'Any'
                                for x in range(len(players[playerturn])):
                                    if cardChosen == players[playerturn][x]:
                                        break
                                discards.append(players[playerturn].pop(x))
                            elif "Wild Draw Four" == cardChosen:
                                reds=0
                                greens=0
                                blues=0
                                yellows=0
                                wilds=0
                                for card in available_cards:
                                    classify = card.split(' ', 1)
                                    if classify[0] == "Red":
                                        reds+=1
                                    elif classify[0] == "Blue":
                                        blues+=1
                                    elif classify[0] == "Yellow":
                                        yellows+=1
                                    elif classify[0] == "Green":
                                        greens+=1
                                    else:
                                        wilds=wilds
                                colour_count=[reds,blues,yellows,greens]
                                colours_count={reds:"Red", blues:"Blue", greens:"Green", yellows:"Yellow"}
                                colour_count.sort(reverse=True)
                                currentColour = colours_count[colour_count[0]]
                                screen.fill('orange')
                                show_discard()
                                colour_show = fonts.render("AI has picked "+currentColour, True, (255,255,255))
                                screen.blit(colour_show, (275, 300))
                                pygame.display.update()
                                time.sleep(1)
                                DrawFour(players, playerturn, playerdirection)
                                Legals = True
                                for x in range(len(players[playerturn])):
                                    if cardChosen == players[playerturn][x]:
                                        break
                                discards.append(players[playerturn].pop(x))
                            else:
                                currentColour = data[0]
                                currentVal = data[1]
                                if currentVal == "Reverse": #function for reverse cards
                                    playerdirection=playerdirection*-1 #inverse player direction
                                elif currentVal == "Skip": #function for skip
                                    skipped = True
                                elif currentVal == "Draw Two": #function for draw 2
                                    DrawTwo(players,playerturn,playerdirection)
                                Legals = True
                                for x in range(len(players[playerturn])):
                                    if cardChosen == players[playerturn][x]:
                                        break
                                discards.append(players[playerturn].pop(x))

                            if len(players[playerturn]) == 0:
                                player_font = font.render("AI is the Winner!", True, (255, 255, 255))
                                screen.blit(player_font, (270, 300))
                                pygame.display.update()
                                pygame.mixer.music.pause()
                                time.sleep(5)
                                running = False
                            elif len(players[playerturn]) > 11:
                                player_font = font.render("AI loses, they have 11+ cards!", True, (255, 255, 255))
                                screen.blit(player_font, (215, 300))
                                pygame.display.update()
                                pygame.mixer.music.pause()
                                time.sleep(5)
                                increment_win(account)
                                running = False
                        else:
                            players[playerturn].extend(Draw(1))
                            Legals = True
                        if Legals == True:
                            if skipped == True:
                                playerturn=playerturn+playerdirection
                                playerturn=Skip(playerturn, playeramount)
                            playerturn=playerturn+playerdirection #moves on to the next player, if skip was played this stacks on and misses next player
                            if playerturn>=playeramount: #cycling function again to ensure that player direction doesn't go out of bounds even when there is no specific function played
                                playerturn=0
                            elif playerturn<0:
                                playerturn=playeramount-1
                        # Update the display
                        screen.fill('orange')
                        show_discard()
                        # Display message for AI turn
                        if play == True:
                            ai_message_text = "AI has played "+cardChosen
                        else:
                            ai_message_text = "No legal card in hand"

                        ai_message = fonts.render(ai_message_text, True, (255, 255, 255))
                        ai_message_rect = ai_message.get_rect(center=(400, 300))  # Adjust the position as needed
                        screen.blit(ai_message, ai_message_rect)
                        pygame.display.update()
                        time.sleep(1.5)  # Wait for 1.5 seconds during AI turn

            else:
                running = True
                card = None
                while running:
                    Legals = False
                    skipped  = False
                    passed = False
                    if "Wild" in discards[-1]:
                        currentColour = currentColour
                        currentVal = 'Any'
                    else:
                        splitCards = discards[-1].split(' ',1)
                        currentColour = splitCards[0]
                        currentVal=splitCards[1]
                    values=[]
                    card_rects = ShowHand(players, playerturn)
                    playerhand = players[playerturn]
                    if len(playerhand)%2==0:
                        initial_x = card_pos[len(playerhand)-1]
                        even_x = card_pos[len(playerhand)+1]
                        end = 800 - even_x
                    else:
                        initial_x = card_pos[len(playerhand)]
                        end = 800 - initial_x
                        pygame.display.update()
                    screen.fill('orange')
                    ShowHand(players, playerturn)
                    show_player()
                    show_discard()
                    pygame.display.update()
                    if canPlay(currentColour, currentVal, players[playerturn]):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                pygame.mixer.music.pause()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    mousex, mousey = pygame.mouse.get_pos()
                                    values=register_clicks(mousex, mousey, initial_x, end)
                                    if values !=None:
                                        if values[0] == 694:
                                            card = retrieve_specials[values[0]]
                                            currentColour = Wild(colours)
                                            Legals = True
                                            for x in range(len(players[playerturn])):
                                                if card == players[playerturn][x]:
                                                    break
                                            discards.append(players[playerturn].pop(x))
                                        elif values[0] == 746:
                                            card = retrieve_specials[values[0]]
                                            currentColour = Wild(colours)
                                            DrawFour(players, playerturn, playerdirection)
                                            Legals = True
                                            for x in range(len(players[playerturn])):
                                                if card == players[playerturn][x]:
                                                    break
                                            discards.append(players[playerturn].pop(x))
                                        else:
                                            color = retrieve_colours[values[1]]
                                            value = retrieve_values[values[0]]
                                            card = color + " " + value
                                            if Legal(currentColour, currentVal, card) == False:
                                                hint = fonts.render("Illegal Move can only play same colour, value or Wild", True, (255,255,255))
                                                screen.blit(hint, (80,275))
                                                pygame.display.update()
                                                time.sleep(2.5)
                                            else:
                                                if value == "Reverse": #function for reverse cards
                                                    playerdirection=playerdirection*-1 #inverse player direction
                                                elif value == "Skip": #function for skip
                                                    skipped = True
                                                elif value == "Draw Two": #function for draw 2
                                                    DrawTwo(players,playerturn,playerdirection)
                                                Legals = True
                                                for x in range(len(players[playerturn])):
                                                    if card == players[playerturn][x]:
                                                        break
                                                discards.append(players[playerturn].pop(x))
                                        screen.fill('orange')
                                        ShowHand(players, playerturn)
                                        show_discard()
                                        pygame.display.update()
                                        if len(players[playerturn]) == 0:
                                            player_font = font.render("Player: " +str(playerturn+1)+" is the Winner!", True, (255, 255, 255))
                                            screen.blit(player_font, (200, 300))
                                            pygame.display.update()
                                            pygame.mixer.music.pause()
                                            time.sleep(5)
                                            running = False
                                        elif len(players[playerturn]) == 1:
                                            SLOW = font.render("TOO SLOW!", True, (255,255,255))
                                            UNO = font.render("UNO!", True, (255,255,255))
                                            if "Wild" in discards[-1]:
                                                react = 1.5
                                            else:
                                                react = 0.75
                                            if reaction() > react:
                                                screen.fill('orange')
                                                screen.blit(SLOW, (315,275))
                                                pygame.display.update()
                                                players[playerturn].extend(Draw(2))
                                                time.sleep(2)
                                            else:
                                                screen.fill('orange')
                                                screen.blit(UNO,(350,275))
                                                pygame.display.update()
                                                time.sleep(2)
                                        elif len(players[playerturn]) > 11:
                                            player_font = font.render("Player: " +str(playerturn+1)+" loses, they still have 11+ cards!", True, (255, 255, 255))
                                            screen.blit(player_font, (75, 300))
                                            pygame.display.update()
                                            pygame.mixer.music.pause()
                                            time.sleep(5)
                                            running = False
                    else:
                        players[playerturn].extend(Draw(1))
                        time.sleep(1)
                        Legals = True
                    if Legals == True:
                        if skipped == True:
                            playerturn=playerturn+playerdirection
                            playerturn=Skip(playerturn, playeramount)
                        playerturn=playerturn+playerdirection #moves on to the next player, if skip was played this stacks on and misses next player
                        if playerturn>=playeramount: #cycling function again to ensure that player direction doesn't go out of bounds even when there is no specific function played
                            playerturn=0
                        elif playerturn<0:
                            playerturn=playeramount-1
                        while passed == False:
                            screen.fill('orange')
                            pass_font = fonts.render("Pass to Player "+str(playerturn+1)+" click when you're ready!", True, (255,255,255))
                            screen.blit(pass_font,(160,275))
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    passed = True

        running = play_menu()
        pygame.display.update()

def create_leaderboard():
    connection = sqlite3.connect('testing2.db')
    cursor = connection.cursor()

    cursor.execute("SELECT Username, Wins FROM User ORDER BY Wins DESC LIMIT 5")
    leaderboard_data = cursor.fetchall()

    leaderboard_font = get_font(22)
    y_position = 150  # Adjust the vertical position as needed

    for position, (username, wins) in enumerate(leaderboard_data, start=1):
        line = f"{position}. {username}: {wins} wins"
        text = leaderboard_font.render(line, True, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=(SCREEN.get_width() // 2, y_position))
        SCREEN.blit(text, text_rect)
        y_position += 60  # Adjust the vertical spacing as needed

    connection.close()
    
def options(colour):
    running = True
    if colour == "White":

        QUIT_BUTTON = Button(image=None, pos=(400, 550), 
                            text_input="QUIT", font=get_font(40), base_color="Black", hovering_color="Green")

    else:
        QUIT_BUTTON = Button(image=None, pos=(400, 550), 
                            text_input="QUIT", font=get_font(40), base_color="Black", hovering_color=colour)
    while running:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(48).render("LEADERBOARD", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)
        create_leaderboard()

        connection = sqlite3.connect('testing2.db')
        cursor = connection.cursor()
        cursor.execute("SELECT Username FROM User ORDER BY Wins DESC LIMIT 1")
        top_user = cursor.fetchone()
        connection.close()

        if top_user:
            congratulations_message = get_font(20).render(f"Congratulations, {top_user[0]}!", True, "Gold")
            congratulations_rect = congratulations_message.get_rect(center=(400, 460))
            SCREEN.blit(congratulations_message, congratulations_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running=False

        pygame.display.update()

font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            SCREEN.blit(text_surface, text_rect)

def settings(colour):
    looped = True
    BLACK = (0,0,0)
    while looped == True:
        cursor_pos = pygame.mouse.get_pos()
        MENU_TEXT = get_font(25).render("CHANGE YOUR FONT COLOUR", True, colour)
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 60))
        SCREEN.fill(BLACK)
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        red_button = pygame.Rect(300, 150, 200, 50)
        green_button = pygame.Rect(300, 250, 200, 50)
        yellow_button = pygame.Rect(300, 350, 200, 50)
        blue_button = pygame.Rect(300, 450, 200, 50)

        pygame.draw.rect(SCREEN, "Red", red_button)
        pygame.draw.rect(SCREEN, "Green", green_button)
        pygame.draw.rect(SCREEN, "Yellow", yellow_button)
        pygame.draw.rect(SCREEN, "Blue", blue_button)

        QUIT_BUTTON = Button(image=None, pos=(400, 550), 
                        text_input="BACK", font=get_font(25), base_color="#d7fcd4", hovering_color=colour)
        QUIT_BUTTON.changeColor(cursor_pos)
        QUIT_BUTTON.update(SCREEN)

        draw_text("RED", BLACK, 400, 175)
        draw_text("GREEN", BLACK, 400, 275)
        draw_text("YELLOW", BLACK, 400, 375)
        draw_text("BLUE", BLACK, 400, 475)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looped = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if red_button.collidepoint(event.pos):
                    colour = "Red"
                    looped = False
                elif green_button.collidepoint(event.pos):
                    colour = "Green"
                    looped = False
                elif yellow_button.collidepoint(event.pos):
                    colour = "Yellow"
                    looped = False
                elif blue_button.collidepoint(event.pos):
                    colour="Blue"
                    looped = False
                elif QUIT_BUTTON.checkForInput(cursor_pos):
                    looped = False
        pygame.display.update()
    return colour

def main_menu():
    colour = "White"
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("UNO ODYSSEY", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Assets/Play Rect.png"), pos=(400, 200), 
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color=colour)
        OPTIONS_BUTTON = Button(image=pygame.image.load("Assets/Options Rect.png"), pos=(400, 300), 
                            text_input="OPTIONS", font=get_font(40), base_color="#d7fcd4", hovering_color=colour)
        SETTINGS_BUTTON = Button(image=pygame.image.load("Assets/Options Rect.png"), pos=(400, 400), 
                            text_input="SETTINGS", font=get_font(40), base_color="#d7fcd4", hovering_color=colour)
        QUIT_BUTTON = Button(image=pygame.image.load("Assets/Quit Rect.png"), pos=(400, 500), 
                            text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color=colour)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]:
            button.scaleDown(0.6)
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(colour)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(colour)
                if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    colour=settings(colour)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
