class message_typer():    
    def __init__(self):
        import os; os.system("clear || cls")
        print("""
        █╬█ ██ ██ ██ ███ ███ ██ ╬╬ ███ █╬█ ███ ██ ███
        █V█ █▄ █▄ █▄ █▄█ █╬▄ █▄ ╬╬ ╬█╬ █▄█ █▄█ █▄ █▄╬
        █╬█ █▄ ▄█ ▄█ █╬█ █▄█ █▄ ╬╬ ╬█╬ ╬█╬ █╬╬ █▄ █╬█
        """)

    def take_message_nomessage_input(self) -> vars:
        print("Enter message :")
        message = input()
        print("Enter numbers of message to sent :")
        no_message = int(input())
        print("Add message number with message OR not | 0 for False and  1 for True :")
        index = int(input())
        return no_message ,message ,index

    def auto_message(self ,message : str ,no_messages : int ,send_delay : int ,index : int) -> None :
        """This funstions will type type {message} {no_messages}"""
        import time
        import pyautogui as pag
        # For safety
        print(" ")
        print("Waiting for 3 second")
        time.sleep(1)
        print("1s")
        time.sleep(2)
        print("2s")
        time.sleep(3)
        print("3s")
        # Start measuring time
        print(" ")
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

    def auto_message_insta(self ,no_messages : int ,message : str ) -> None :
        """This funstions will type {message} and sleep for a while {no_messages} . you can use it for dending message online like insta """
        ...
        # # For safety
        # time.sleep(5)
        # # Start measuring time
        # print("Message Started to send :")
        # start = time.time()
        # for i in range(no_messages):
        #     pag.write(f"{message}")
        #     time.sleep(0.3)
        #     pag.press("enter")
        #     time.sleep(0.3)
        #     print(i+1 , end=" , ")
        # print("---------Done--------")
        # print(" ")
        # # Print time taken by program
        # print(f"{time.time()-start}s")

def main():
    classobject = message_typer()
    no_message ,message ,index =classobject.take_message_nomessage_input()
    # 
    send_delay = input("Enter message send delay (Default is 0) : ")
    # 
    if send_delay =="":
        send_delay = 0
    else:
        send_delay = int(send_delay)
    print("")
    print(f"Send Delay: {send_delay} seconds")
    print(f"Message: {message}")
    print(f"No. of messages : {no_message}")
    print(f"Index : {index}")
    print("")
    classobject.auto_message( message ,no_message ,send_delay,index)
    # 
    print("---------Done--------")
    print(" ")

if __name__ == '__main__' :
    while True:
        try :
            main()
        except Exception as error :
            print(error)
        print("HELP : index 0 for False or index 1 for true ")
        input("Press ENTER to continue")
