import sqlite3 
import os
import view
import model
from model import pass_hash, generate_account_id, new_id, id_exist, lookup_price
from model import Account, Trades, Position

while True:
    choice = view.main_menu()
    #LOGIN CHOICE
    if choice == '1' or choice.capitalize() == 'Log in':
        view.verify_login()
        username = input('\nUsername: ')
        password = input('Password: ')
        account  = Account(username=username,password=password)
        if not account:
            view.incorrect_login()
        while account:
            view.login_menu()
            choice = input('\nWhat would you like to do?: ')
            if choice == '1':
                account.get_balance(username,password)
                print (account.get_balance(username,password))
                input()
            elif choice == '2':
                try:
                    amount = input('How much would you like to deposit? ')
                    account.account_bal += float(amount)
                    account.save()
                    view.deposit_success(amount)
                except ValueError:
                    print('Please enter a number.')
                    input()
            elif choice == '3':
                choice = input('To see all shares, press 1.\nOtherwise, input desired stock: ')
                choice = choice.upper()
                exit_condition = True
                while exit_condition:
                    if choice == '1':
                        for row in account.get_all_positions():
                            print(row)
                        input()
                        exit_condition = False
                    else:
                        if account.get_position(choice) == []:
                            print('No shares of {}.'.format(choice.upper()))
                            input()
                            exit_condition = False
                        else:
                            print(account.get_position(choice))
                            input()
                            exit_condition = False
            elif choice == '4':
                exit_condition = True
                while exit_condition:
                    view.buy_menu()
                    choice = input('\nWhat would you like to do? ')
                    if choice == '1' or choice.capitalize() == 'Lookup' or choice.capitalize() == 'Look up':
                        try:
                            symbol = input('What stock would you like to look up? ')
                            price = str(lookup_price(symbol))
                            print('$'+price)
                            input()
                        except ValueError:
                            print('Stock does not exist.')
                            input()
                    elif choice == '2' or choice.capitalize() == 'Buy':
                        try:
                            symbol = input('What stock would you like to buy? ')
                            shares = input('How many shares? ')
                            account.buy(symbol,shares)
                            price = float(lookup_price(symbol)) * int(shares)
                            view.buy_success(symbol,shares,price)
                        except ValueError:
                            print('Bad Input.')
                            input()
                    elif choice == '3' or choice.capitalize() == 'Sell':
                        try:
                            symbol = input('What stock would you like to sell? ')
                            shares = input('How many shares? ')
                            account.sell(symbol,shares)
                            price = float(lookup_price(symbol)) * int(shares)
                            view.sell_success(symbol,shares,price)
                        except ValueError:
                            print('Bad Input.')
                            input()
                    elif choice == '4' or choice.capitalize() == 'Return':
                        exit_condition = False
                    else:
                        view.bad_input()
                        input()
            elif choice == '5':
                choice = input('To see entire trade history, press 1.\nOtherwise, input desired stock: ')
                choice = choice.upper()
                exit_condition = True
                while exit_condition:
                    if choice == '1':
                        for rows in account.see_trade_history():
                            print(rows)
                        input()
                        exit_condition = False
                    else:
                        if account.see_trade_for(choice) == []:
                            print('No history of {}.'.format(choice.upper()))
                            input()
                            exit_condition = False
                        else:
                            for rows in account.see_trade_for(choice):
                                print(rows)
                            input()
                            exit_condition = False
            elif choice == '6':
                bal = round(account.account_bal,2)
                print('\nName: '+account.lastname+', '+account.firstname)
                print('Username: '+account.username)
                print('Account ID: '+str(account.account_id))
                print('Password: **HIDDEN**')
                print('Email: ')
                print('Balance: '+str(bal))
                print('\nTo change Account Information, type "Change".\nOtherwise, press 1 to return to Main Menu.')
                choice = input()
                if choice.capitalize() == 'Change':
                    exit_condition = True
                    while exit_condition:
                        view.change_info()
                        choice = input('What would you like to change? ')
                        if choice.capitalize() == 'Username' or choice == '1':
                            new_un  = input("Enter new Username: ")
                            conf_un = input('Confirm Username: ')
                            if new_un == conf_un:
                                exists = account.check_un(new_un)
                                if exists:
                                    print('Username already exists!')
                                    input()
                                    exit_condition = False
                                else:
                                    account.update_un(new_un)
                                    view.success_un(new_un)
                                    input()
                                    exit_condition = False
                            else:
                                view.un_dont_match()
                                input()
                                exit_condition = False
                        elif choice.capitalize() == 'Password' or choice == '2':
                            pw = input('Enter current password: ')
                            if pass_hash(pw) != account.pw_hash:
                                print('That is not your password.')
                                input()
                            else:
                                new_pw      = input('Enter new password: ')
                                conf_new_pw = input('Confirm new password: ')
                                if new_pw == conf_new_pw:
                                    account.update_pw(new_pw)
                                    view.success_new_pw()
                                    input()
                                else:
                                    view.pass_dont_match()
                                    input()
                    #elif choice.capitalize() == 'Email' or choice == '3':
                    else:
                        view.bad_input()
                        input()
                    
                else:
                    view.bad_input()
                    input()      
            elif choice == '8':
                account = False
            else:
                view.bad_input()
                input()
        else:
            view.good_bye()
            input()  
    #CREATE ACCOUNT 
    elif choice == '2' or choice.capitalize() == 'Create account':
        view.create_account()
        firstname = input('\nWhat is your first name? ').capitalize()
        lastname  = input('What is your last name? ').capitalize()
        username  = input('Enter Username: ')
        password  = input('Enter Password: ')
        conf_pass = input('Confirm Password: ')
        if password == conf_pass:
            account            = Account()
            account.firstname  = firstname
            account.lastname   = lastname
            account.username   = username
            account.pw_hash    = pass_hash(password)
            account.account_id = new_id()
            account.save()
            view.added('Account')
        else:
            view.pass_dont_match()
    #EXIT
    elif choice == '3' or choice.capitalize() == 'Exit':
        exit()
    #BAD INPUT CASES
    else:
        view.bad_input()
        input()