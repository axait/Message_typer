import argparse

def args_func() -> vars:
    parser = argparse.ArgumentParser(description='Argument Parser for cli')
    parser.add_argument('--senddelay', '-d', type=float, default=0.0,
                        help='Specify the delay time in seconds before sending a message')
    parser.add_argument('--message', '-m', type=str,
                        help='Provide a message to be sent')
    parser.add_argument('--nomessage', '-n', type=int,
                        help='How much message you want to send')
    parser.add_argument('--index', '-i', type=int,
                        help='Add message number with message value will be [ 0,1 ]  0 for False and  1 for True')
    # 
    args = parser.parse_args()
    # 
    print("")
    print(f"Send Delay: {args.senddelay} seconds")
    print(f"Message: {args.message}")
    print(f"No. of messages {args.nomessage}")
    index = "True" if args.index == 1 else "False"
    print(f"Index : {index}")
    print("")
    # 
    return args


def auto_message(no_messages : int ,message : str ,send_delay : int ,index : int) -> None :
    """This funstions will type type {message} {no_messages}"""
    import time
    import pyautogui as pag
    # For safety
    print("Waiting for 3 second")
    time.sleep(1)
    print("1s")
    time.sleep(2)
    print("2s")
    time.sleep(3)
    print("3s")
    print(" ")
    # Start measuring time
    print("Message Started to send :")
    if index == 0 :
        start = time.time()
        for i in range(no_messages):
            pag.write(f"{message}")
            pag.press("enter")
            time.sleep(send_delay)
            print(i+1 , end=" , ")
        # Print time taken by program
        print(" ")
        print("Time taken to send messages :")
        print(f"{time.time()-start}s")
        print(" ")
    elif index == 1 :
        start = time.time()
        for i in range(no_messages):
            pag.write(f"{i+1}. {message}")
            pag.press("enter")
            time.sleep(send_delay)
            print(i+1 , end=" , ")
        # Print time taken by program
        print(" ")
        print("Time taken to send messages :")
        print(f"{time.time()-start}s")
        print(" ")
    else :
        print("Provide correct input or use -h for help")

def main():
    args =args_func()
    if args.senddelay =="":
        args.senddelay = 0
    else:
        args.senddelay = int(args.senddelay)
    auto_message( args.nomessage ,args.message ,args.senddelay ,args.index)
    # 
    print("---------Done--------")
    print(" ")

if __name__ == '__main__' :
    main()
