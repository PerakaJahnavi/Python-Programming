from itertools import product
user_num = int(input("Enter your logo 0 for '❌', 1 for '⭕': "))
logos = ['❌', '⭕']
player1_logo = logos[user_num]
logos.remove(player1_logo)
player2_logo = logos[0]
look = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
to_continue = True
turns = 4.5


def display():
    for i in range(3):
        print('   '.join(look[i]))


def player_1():
    print("\nPlayer1: Please enter your position(row, column): ")
    player1_choice = list(map(int, input().split()))
    look[player1_choice[0] - 1][player1_choice[1] - 1] = player1_logo
    display()


def player_2():
    print("\nPlayer2: Please enter your position(row, column): ")
    player2_choice = list(map(int, input().split()))
    look[player2_choice[0] - 1][player2_choice[1] - 1] = player2_logo
    display()


def combo_check(combos):
    for combo in combos:
        if (look[combo[0][0] - 1][combo[0][1] - 1] == '❌'
                and look[combo[1][0] - 1][combo[1][1] - 1] == '❌'
                and look[combo[2][0] - 1][combo[2][1] - 1] == '❌'):
            print("'❌' Won!")
            return True
        elif (look[combo[0][0] - 1][combo[0][1] - 1] == '⭕'
              and look[combo[1][0] - 1][combo[1][1] - 1] == '⭕'
              and look[combo[2][0] - 1][combo[2][1] - 1] == '⭕'):
            print("'⭕' Won!")
            return True
        else:
            pass


def logics():
    col_combos = [list(product([1, 2, 3], [1])), list(product([1, 2, 3], [2])), list(product([1, 2, 3], [3]))]
    row_combos = [list(product([1], [1, 2, 3])), list(product([2], [1, 2, 3])), list(product([3], [1, 2, 3]))]
    diagonal_combos = [[(1, 1), (2, 2), (3, 3)], [(3, 1), (2, 2), (1, 3)]]
    if combo_check(row_combos) or combo_check(col_combos) or combo_check(diagonal_combos):
        return True
    else:
        return False


display()
while to_continue:
    player_1()
    turns -= 0.5
    if logics():
        to_continue = False
        continue
    player_2()
    turns -= 0.5
    if logics():
        to_continue = False
        continue
    if turns == 0.5:
        player_1()
        print("GAME OVER!")
        to_continue = False






