'''
Dictionary of dictionaries containing stock name, price and ammount.
'''

stockprice_dict = {
    "A1": {"name": "Soda", "price": 1.50, "stock": 10},
    "A2": {"name": "Water", "price": 1.20, "stock": 6},
    "B1": {"name": "Crisps", "price": 1.00, "stock": 2},
    "B2": {"name": "Chocolate", "price": 1.30, "stock": 4},
    "C1": {"name": "Gum", "price": 0.80, "stock": 3}
}
order_list = []
order_number = 0

def coin_input(order_number=0):
    order_number+= 1
    accepted_coins = ["2", "0.50", "0.5", "0.2", "0.20", "1"]
    wallet = 0.0
    while True: #Loop takes moent inputs, checks against accepted list. Ends when done is typed
        coins = input(f"Balance: {wallet:.2f} \nInsert coins (£2, £1, 50p, 20p) type 'done' to proceed: ")
        if coins == 'done':
            return order_items(wallet,order_number)
        elif coins not in accepted_coins:
            print("-"*50,"\nSorry, this machine only accepts £2, £1, 50p, 20p coins.")
        else:
            wallet+= float(coins)
            print("-"*50)



'''
Function to allow for ordering product and printing the vending machine menu.
'''
def order_items(wallet,order_number): #Function to collect the orders from the machine
    while True:
        try:
            print("="*6, "Vending Machine Menu", "="*6)
            print(f"| A1 | {stockprice_dict['A1']['name']} - £{stockprice_dict['A1']['price']:.2f}  Stock: {stockprice_dict['A1']['stock']}")
            print(f"| A2 | {stockprice_dict['A2']['name']} - £{stockprice_dict['A2']['price']:.2f}  Stock: {stockprice_dict['A2']['stock']}")
            print(f"| B1 | {stockprice_dict['B1']['name']} - £{stockprice_dict['B1']['price']:.2f}  Stock: {stockprice_dict['B1']['stock']}")
            print(f"| B2 | {stockprice_dict['B2']['name']} - £{stockprice_dict['B2']['price']:.2f}  Stock: {stockprice_dict['B2']['stock']}")
            print(f"| C1 | {stockprice_dict['C1']['name']} - £{stockprice_dict['C1']['price']:.2f}  Stock: {stockprice_dict['C1']['stock']}")
            print(f"Balance: {wallet:.2f}")
            print()
            print("-"*50)
            choice = input("Enter product code (A1, B2, ect), enter 'done' once you are ready to proceed: ")
            if choice == "done":
                return discount_application(wallet,order_number)

            elif stockprice_dict[choice]["stock"] == 0: #Prevents stock from being bought when empty.
                print("Sorry, that product isn't avaliable.")

            elif wallet < stockprice_dict[choice]["price"]: # Checks to see if user has the funds
                print("Sorry, you don't have the funds for that item.")
            
            elif wallet >= stockprice_dict[choice]["price"]: # Confirms the user has the funds, adds choice to list for discount, removes stock and money from wallet.
                order_list.append(choice)
                wallet -= stockprice_dict[choice]["price"]
                stockprice_dict[choice]["stock"] -= 1
                print(f"{stockprice_dict[choice]['name']} added to order list. £{stockprice_dict[choice]['price']:.2f} deducted.")
                print(f"Remaining Balance: £{wallet:.2f}")
        except KeyError:
            print("Sorry, that product isn't avaliable.")

'''
Function that takes the wallet and order_number (For future use.) Calculates the discount % an applies discount.
'''

def discount_application(wallet,order_number): # Fucntion to apply a discount based on how much bought + total
    discount = 0
    total = 0
    discount_amount = "0%"

    for i in order_list:
        total += stockprice_dict[i]["price"] # Creates a total price
    if total >= 7:
        discount = (total * 15) / 100 # Applies discount 15%
        discount_amount = "15%"
        wallet += (total * 15) / 100 #Adds the discounted funds back to the wallet to be put out as change

    elif total >= 5:
        discount = (total * 10) / 100
        discount_amount = "10%"
        wallet += (total * 10) / 100

    elif len(order_list) >= 3:
        discount = (total * 5) / 100
        discount_amount = "5%"
        wallet += (total * 5) / 100

    total -= discount
    return change_output(wallet, order_number,total,discount_amount)


'''
Function that takes the total, order number and wallet. Calculates if the order number is odd and applies £1 cash back.
Calculates chanage by removing money from wallet in a loop until wallet cannot remove 0.2 without being < 0.
At the end it loops back to the start.
'''

def change_output(wallet,order_number,total, discount_amount): #Function calculates how much change is given in coins, all change that cannot be given is stated
    change = 0
    two_pound_coins = 0
    one_pound_coins = 0
    fifty_p_coins = 0
    twenty_p_coins = 0
    odd_order = False
    if order_number % 2 != 0 and total >= 2:
        odd_order = True
        one_pound_coins +=1
        change +=1

    while True:
        if wallet - 2 >= 0: # Checks if wallets remaining funds can be minused by 2
            change += 2 # adds to change variable
            wallet -= 2 # removes it 
            two_pound_coins += 1 # increments a counter for end of function.
        elif wallet - 1 >= 0:
            change += 1
            wallet -= 1
            one_pound_coins += 1
        elif wallet - 0.5 >= 0:
            change += 0.5
            wallet -= 0.5
            fifty_p_coins += 1
        elif wallet - 0.2 >= 0:
            change += 0.2
            wallet -= 0.2
            twenty_p_coins += 1
        elif wallet - 0.2 < 0: #If wallet cannot remove 0.2 without being < 0, then remaining change cannot be dispensed.
            print(f"Your change is £{change:.2f}") # Final output
            if odd_order == True:
                print("Congrats, your order was an odd order, enjoy £1.")

            print(f"{two_pound_coins} £2 coins. \n{one_pound_coins} £1 coins. \n{fifty_p_coins} 50p coins. \n{twenty_p_coins} 20p coins.")

            if wallet > 0:
                print(f"£{wallet:.2f} could not be dispensed.")
            return final_output(wallet,order_number,total,discount_amount,odd_order)
    

def final_output(wallet,order_number,total,discount_amount,odd_order):

    print("-"*50)
    for i in order_list:
        print(f"{i} -- £{stockprice_dict[i]['price']:.2f}")
    print(f'Order Number: {order_number}\n'
        f'Total price: £{total:.2f}'
        f'\nDiscounts applied: {discount_amount}'
        f'\nUndispensed change: £{wallet:.2f}'
        )


    wallet = 0
    return coin_input(order_number) # Loops back to start.
            
coin_input()