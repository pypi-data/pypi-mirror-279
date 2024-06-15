


def main():
    string = input('Enter your path and it would replace to front slash \n (Enter Q/ quit, or exit to stop it from running): \n')
    while string not in ['q','Quit','quit','Q']:
        print()
        print(replace_backslash(string))
        print('\n')
        string = input('Enter your path and it would replace to front slash \n (Enter Q/ quit, or exit to stop it from running): \n')
        print()

    

if __name__ == "__main__":
    main()