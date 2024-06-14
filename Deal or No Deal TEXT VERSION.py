import random
import numpy as np

NUMBERS = [i for i in range(1,8)]
PRICES = [10, 100, 500, 10000, 100000, 500000, 1000000]
OFFER_RATIO = [0.1, 0.2, 0.4, 0.7, 1.1]

def main():
    
    # Shuffle the cash amounts and assign them to the suitcases
    suitcase_prices = shuffle_case(NUMBERS,PRICES)

    # Game introduction
    game_intro()
    
    # Dictionary of hidden suitcases with prices
    hidden_suitcase = suitcase_prices

    # Dictionary of revealed suitcase with prices
    open_suitcase = {}
    player_suitcase = {}


    # Player chooses a suitcase to put on the podium
    player_num, player_cash = first_pick(NUMBERS, suitcase_prices)
    update_suitcase(player_num, hidden_suitcase, player_suitcase)

    # Track how many offers have been played
    count = 0

    # Continue offer new deals until player takes the deal or runs out of suitcases
    while count <= 4:

        # Host reveals a random suitcase from the hidden suitcases
        reveal = reveal_suitcase(hidden_suitcase)

        # Update the remaining suitcases and display
        update_suitcase(reveal, hidden_suitcase, open_suitcase)
        display_prices(player_cash, hidden_suitcase)

        # Banker offers to buy the player's suitcase
        offer = banker_offer(PRICES, hidden_suitcase, open_suitcase, player_cash)
        count, price = deal_or_no_deal(count, offer, player_cash)

    # Reveal the price won and player suitcase amount
    congrats(price, player_cash)



################################### BASE GAME FUNCTIONS #########################################

def clear_terminal():
    for i in range(20):
      print('\n')

def game_intro():
    print("Welcome to a game of Deal or No Deal!")
    print("")

# User pick first suitcase
def first_pick(NUMBERS, dict):
    while True:
        try:
            num = int(input("Pick a suitcase (enter a number betwween 1 and 7): "))    
        except ValueError:
            print("Not a valid number. Try again.")
            print("")
            continue
        else:
            if num >= 1 and num <= len(NUMBERS):
                break
            else:
                print("Not a valid number. Try again.")
                print("")
                continue
    clear_terminal()
    print("Your chosen suitcase is:", str(num))
    amount = dict[num]
    return num, amount

# Shuffle the cash amounts and assign them to the suitcases
# Outputs a dictionary of {'suitcase number': $ cash amount} pairs
def shuffle_case(NUMBERS,PRICES):
    suitcase_prices = {}
    prices_shuffled = random.sample(PRICES,  len(PRICES))
    for i in range(len(NUMBERS)):
        suitcase_prices[NUMBERS[i]] = prices_shuffled[i]
    return suitcase_prices

# Add a dollor sign to each number in num_list
def add_dollar_sign(num_list):
    price_list  = []
    for i in range(len(num_list)):
        price = "$"+str(num_list[i])
        price_list.append(price)
    return price_list

# Remove key-value pair with key "num" from dict1 and add to dict2
def move(num, dict1, dict2):
    if num in dict1:
        dict2[num] = dict1[num]
        del dict1[num]
    return dict1, dict2

# Update dictionaries of hidden and revealed suitcase based on selected suitcase number
# Display the remaining (hidden) suitcase numbers
def update_suitcase(num, dict1, dict2):
    dict1, dict2 = move(num, dict1, dict2)
    if len(dict1) > 1:
        print("The remaining suitcases are: ")
        print(*dict1.keys(), sep = ", ")
    else:
        print("The remaining suitcase is: ")
        print(*dict1.keys(), sep = ", ")
    print("")

# Display remaining prices
def display_prices(player_cash, hidden_suitcase):
    prices = list(hidden_suitcase.values()) + [player_cash]
    prices.sort()
    print("The remaining prices are: ")
    print(*add_dollar_sign(prices), sep = ", ")
    press_continue()

# Reveal the cash inside a hidden suitcase
def reveal_suitcase(dict1):
    num = random.choice(list(dict1.keys()))
    print("The host will now reveal the cash inside suitcase", str(num))
    print("The cash inside suitcase "+str(num)+" is $"+str(dict1[num]))
    press_continue()
    return num

# Banker offers to buy the player's suitcase
def banker_offer(PRICES, hidden_suitcase, open_suitcase, player_cash):
    cash_hidden = np.sum(PRICES) - np.sum(list(open_suitcase.values())) + player_cash
    offer =  OFFER_RATIO[-len(hidden_suitcase)] * cash_hidden / (len(hidden_suitcase) + 1) + np.sqrt(player_cash)
    offer = int(offer)
    if offer >= 1000000:
        offer = 925000
    elif offer >= np.max(list(hidden_suitcase.values())):
        offer = np.max(list(hidden_suitcase.values())) * 0.75
    print("The banker offers to buy your suitcase for $"+str(offer))
    return offer

# Press any key to continue
def press_continue():
    print("")
    input("Press any key to continue...")
    print("")

# Deal or no deal
def deal_or_no_deal(count, offer, player_cash):
    while True:
        print("")
        ans = input("Deal or no deal? ").lower() #convert input string to lowercase
        if ans == "deal":
            print("")
            print("You have a deal!")
            count = 99
            break
        elif ans == "no deal":
            print("")
            print("You rejected the banker's offer")
            press_continue()
            break
        else:
            print('Not a valid response. Type in "deal" or "no deal".')
            continue
    if count == 99:
        price = offer
    else:
        price = player_cash
    print("")
    count += 1
    return count, price
    
# Reveal the price won and player suitcase amount
def congrats(price, player_cash):
    print("Congratulations! You won: $"+str(price)+"!")
    print("")
    print("The amount in your suitcase was: $"+str(player_cash)+".")
    print("")



if __name__ == '__main__':
    main()
