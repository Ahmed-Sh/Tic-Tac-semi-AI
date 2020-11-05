from random import sample


class TicTacToe:

    def __init__(self):
        self.player = "X"
        self.x_count = 0
        self.o_count = 0
        self.cells = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.win = False
        self.str = 0
        self.case = 0
        self.cords = [13, 23, 33, 12, 22, 32, 11, 21, 31]
        self.cords_d = {k: v for v, k in enumerate(self.cords)}
        self.player_select = {"user": self.players_input,
                              "easy": self.computer_input_easy,
                              "medium": self.computer_input_medium,
                              "hard": self.computer_input_hard
                              }

    def drawing_field(self):
        field = ("---------\n"
                 f"| {self.cells[0]} {self.cells[1]} {self.cells[2]} |\n"
                 f"| {self.cells[3]} {self.cells[4]} {self.cells[5]} |\n"
                 f"| {self.cells[6]} {self.cells[7]} {self.cells[8]} |\n"
                 "---------")
        return field

    def player_turn(self):
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"

    def computer_available_moves(self):
        cords = list()
        for i, val in enumerate(self.cells):
            if val != "X" and val != "O":
                cords.append(self.cords[i])
        return cords

    def computer_input_easy(self):
        print('Making move level "easy"')
        # print(f" player {self.player} moves")
        cords = self.computer_available_moves()
        x = sample(cords, 1)[0]     # sample returns a list of random choices from iterable
        self.cells[self.cords_d[x]] = self.player

    def computer_input_medium(self):
        print('Making move level "medium"')
        # print(f" player {self.player} moves")
        cords = self.computer_available_moves()
        test_win = self.check_possible_win(cords)
        test_lose = self.check_opponent_win(cords)
        x = sample(cords, 1)[0]
        if test_win:
            x = test_win
        elif test_lose:
            x = test_lose
        self.cells[self.cords_d[x]] = self.player

    def check_possible_win(self, move_list):
        for i in move_list:
            self.cells[self.cords_d[i]] = self.player
            if self.win_test():
                self.cells[self.cords_d[i]] = " "
                self.win = False
                return i
            else:
                self.cells[self.cords_d[i]] = " "

    def check_opponent_win(self, move_list):
        self.player_turn()
        for i in move_list:
            self.cells[self.cords_d[i]] = self.player
            if self.win_test():
                self.player_turn()
                self.cells[self.cords_d[i]] = " "
                self.win = False
                return i
            else:
                self.cells[self.cords_d[i]] = " "
        self.player_turn()

    def mini_max(self, max_player, player):
        cords = self.computer_available_moves()
        game_state = self.win_test()
        if game_state == self.player:
            return 10
        elif self.draw_check() == "Draw":
            return 0
        elif game_state is not None:
            return -10
        if max_player:
            max_eval = -1000     # low value to be replaced when compared with evaluation in max_eval(line 101)
            for i in cords:
                self.cells[self.cords_d[i]] = self.player
                evaluation = self.mini_max(False, player)
                self.cells[self.cords_d[i]] = " "
                max_eval = max(max_eval, evaluation)
            return max_eval
        else:
            min_eval = 1000
            for i in cords:
                self.cells[self.cords_d[i]] = "O" if self.player == "X" else "X"
                evaluation = self.mini_max(True, player)
                self.cells[self.cords_d[i]] = " "
                min_eval = min(min_eval, evaluation)
            return min_eval

    def computer_input_hard(self):
        print('Making move level "hard"')
        max_score = -1000       # initial state to start from
        best_move = -1          # initial state to start from
        cords = self.computer_available_moves()
        if len(cords) == 9:
            x = sample(cords, 1)[0]
            self.cells[self.cords_d[x]] = self.player
        else:
            for i in cords:
                self.cells[self.cords_d[i]] = self.player
                score = self.mini_max(False, self.player)
                self.cells[self.cords_d[i]] = " "
                if score > max_score:
                    max_score = score
                    best_move = i
            self.cells[self.cords_d[best_move]] = self.player

    def players_input(self):
        while True:
            x = "".join(input("Enter the coordinates: ")).split()
            for i in x:
                try:
                    if int(i) > 3:
                        print("Coordinates should be from 1 to 3!")
                        break
                    elif len(x) != 2:
                        print("Please enter two digit coordinates")
                        break
                except ValueError:
                    print("You should enter numbers!")
                    break
            else:
                user_cords = int("".join(x))
                if self.cells[self.cords_d[user_cords]] != "X" and self.cells[self.cords_d[user_cords]] != "O":
                    self.cells[self.cords_d[user_cords]] = self.player
                    break
                else:
                    print("This cell is occupied! Choose another one!")

    def win_test(self):
        self.str = ("".join(self.cells))
        self.case = [self.str[0:3], self.str[3:6], self.str[6:9], self.str[0:7:3],
                     self.str[1:8:3], self.str[2:9:3], self.str[0:9:4], self.str[2:7:2]]
        if "XXX" in self.case:
            return "X"
        elif "OOO" in self.case:
            return "O"

    def draw_check(self):
        self.x_count = self.cells.count("X")
        self.o_count = self.cells.count("O")
        if (self.x_count + self.o_count) == 9:
            return "Draw"

    def check_game(self):
        # print(f"start player {self.player} win checking")
        if self.win_test():
            if self.player == "X":
                print("X wins")
            elif self.player == "O":
                print("O wins")
            return True
        elif self.draw_check():
            print("Draw")
            return True
        else:
            return False

    def choose_turn(self, player_1, player_2):
        self.player_select[player_1]()
        print(self.drawing_field())
        if self.check_game():
            exit()
        self.player_turn()
        self.player_select[player_2]()
        print(self.drawing_field())
        if self.check_game():
            exit()
        self.player_turn()

    def play_game(self):
        while True:
            try:
                print("Welcome to Tic Tac Toe\n"
                      "please Choose Game mode:\n"
                      "for Human player choose 'user'\n"
                      "for pc choose from the following modes:\n"
                      "hard - medium - easy\n"
                      "type 'exit' if you wanna leave")
                user_input = [i for i in input("Input command: ").split()]
                print("choose 'X' or 'O' for first player")
                choice = input().lower()
                if choice == "o":
                    self.player_turn()
                if user_input[0] == "exit":
                    exit()
                else:
                    player_1, player_2 = user_input
                    break
            except ValueError:
                print("Bad parameters!")
        print(self.drawing_field())
        while True:
            self.choose_turn(player_1, player_2)


game = TicTacToe()
game.play_game()
