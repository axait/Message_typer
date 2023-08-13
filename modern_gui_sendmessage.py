import customtkinter as ctk
from tkinter import END ,NORMAL  , DISABLED ,StringVar , Menu , Button
from ttkthemes import ThemedStyle
import datetime ,time ,threading , sys

message_var = ""
no_message_var = 0
message_delay_var = 0
index_var = 0
message_sent_time_var = "None"

thread_current_time_continuty_teller = True

class ExitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        import threading
        threading.Thread(target=sys.exit).start()
        self.message = message

def exit():
    # global thread_current_time , thread_auto_message_send  ,thread_auto_message_send_at_time , thread_disable_enable_button ,  thread_reset_message_send_at_time_var ,  thread_auto_message_sender
    # global thread_current_time_continuty_teller , thread_current_time
    # thread_current_time_continuty_teller = False
    # thread_current_time.join()
    sys.exit()

def current_time() -> None :
    def current_time_thread():
        global current_time_entry , thread_current_time_continuty_teller
        while True :
            if thread_current_time_continuty_teller == True :
                time.sleep(1)
                current_time_entry.delete(0,END)
                current_time_entry.insert(0,datetime.datetime.now().strftime("%H:%M:%S"))
            else :
                break
    global thread_current_time
    thread_current_time = threading.Thread(target=current_time_thread)
    thread_current_time.start()

def auto_message( message : str ,no_messages : int ,send_delay : int ,index : int , sent_time : str = "Nonestr") -> None :
        """This funstions will type type {message} {no_messages}"""
        import time
        import pyautogui as pag
        msg_sent_text.delete( 0.0,END )
        msg_sent_time_taken_entry.delete( 0,END )
        # For safety
        def delay_3seconds():
            # msg_sent_text
            msg_sent_text.insert(0.0,"\n Waiting for 3 seconds ")
            time.sleep(1)
            msg_sent_text.insert(END,"\n 1s ")
            time.sleep(2)
            msg_sent_text.insert(END,"\n 2s ")
            time.sleep(3)
            msg_sent_text.insert(END,"\n 3s ")
            # Start measuring time
            msg_sent_text.insert(END,"\n Message Started to send \n")
        delay_3seconds()
        error_label.configure(text=""  , fg_color="transparent")

        if index == 0 :
            start = time.time()
            for i in range(no_messages):
                pag.write(f"{message}")
                pag.press("enter")
                time.sleep(send_delay)
                msg_sent_text.insert(END,f"{i+1} , " )
            # Print time taken by program
            if (time.time()-start) < 60 :
                msg_sent_time_taken_entry.insert(END,f"{time.time()-start} seconds\n")
            else:
                msg_sent_time_taken_entry.insert(END,f"{ (time.time()-start)/60 } minutes\n")
                # 
        elif index == 1 :
            start = time.time()
            for i in range(no_messages):
                pag.write(f"{i+1}. {message}")
                pag.press("enter")
                time.sleep(send_delay)
                msg_sent_text.insert(END,f"{i+1} , " )
            # Print time taken by program
            if (time.time()-start) < 60 :
                msg_sent_time_taken_entry.insert(END,f"{time.time()-start} seconds\n")
            else:
                msg_sent_time_taken_entry.insert(END,f"{ (time.time()-start)/60 } minutes\n")

def get_inputs():
    global message_var , no_message_var , message_delay_var , index_var , message_sent_time_var
    message_var = message_entry.get()
    no_message_var = no_message_entry.get()
    message_delay_var = message_sent_delay_entry.get()
    # 
    if dropdown_var.get() == "False" :
        error_label.configure(text="No any errot" , fg_color="transparent")
        index_var = 0
    elif dropdown_var.get() == "True" :
        error_label.configure(text="No any errot" , fg_color="transparent")
        index_var = 1
    else :
        error_label.configure(text="Please select index value" , fg_color="red")
    # message_sent_time_var value set if it is not blank
    if message_sent_time_entry.get() != "":
        message_sent_time_var = message_sent_time_entry.get()

def check_blank_inputs():
    global error_label
    global message_var , no_message_var , message_delay_var , index_var
    if  message_var == "" or no_message_var == "" or message_delay_var == "" or index_var == "":
        return False
    else :
        return True

def send_msg_at_time(message_var , no_message_var , message_delay_var , index_var , message_sent_time_var ):
    """This function will send msgs at time given by user"""
    while True :
        if message_sent_time_var == datetime.datetime.now().strftime("%H:%M:%S") :
            global thread_auto_message_send
            thread_auto_message_send = threading.Thread(target=auto_message , args=(message_var , int(no_message_var) , int(message_delay_var) , int(index_var)))
            thread_auto_message_send.start()
            thread_auto_message_send.join()
            break
        else :
            ...

def diasable_button_func(tk_button : Button , thread_auto_message_sender : threading ) -> None :
    """ To disable button after message started to avoid multi threads of thread_auto_message_send """
    def diasable_button_sub_func(tk_button : Button, thread_auto_message_sender : threading):
        tk_button.configure(state=DISABLED)
        thread_auto_message_sender.join()
        tk_button.configure(state=NORMAL)
    def reset_time_sent_msg_var_func():
        def reset_time_sent_msg_sub_func():
            global thread_auto_message_send_at_time , message_sent_time_var
            thread_auto_message_send_at_time.join()
            message_sent_time_var = "None"
        thread_reset_message_send_at_time_var = threading.Thread(target=reset_time_sent_msg_sub_func )
        thread_reset_message_send_at_time_var.start()
    thread_disable_enable_button = threading.Thread(target=diasable_button_sub_func , args=(tk_button , thread_auto_message_sender))
    thread_disable_enable_button.start()
    reset_time_sent_msg_var_func()


def start_sending() -> None :
    try :
        global message_var , no_message_var , message_delay_var , index_var , message_sent_time_var , sending_button , msg_sent_text
        get_inputs()



        if check_blank_inputs() :

            if message_sent_time_var != "None" :
                msg_sent_text.insert(0.0 , f"Waiting for time {message_sent_time_var}" )
                error_label.configure(text=f"Waiting for time {message_sent_time_var}"  , fg_color="green")
                global thread_auto_message_send_at_time
                thread_auto_message_send_at_time = threading.Thread(target=send_msg_at_time , args=(message_var , int(no_message_var) , eval(message_delay_var) , int(index_var) , message_sent_time_var ))
                thread_auto_message_send_at_time.start()
                # To disable button after message started to avoid multi threads of thread_auto_message_send
                diasable_button_func(sending_button ,thread_auto_message_send_at_time)


            else :
                error_label.configure(text="Waiting for 3 seconds"  , fg_color="green")

                thread_auto_message_send = threading.Thread(target=auto_message , args=(message_var , int(no_message_var) , eval(message_delay_var) , int(index_var)))
                thread_auto_message_send.start()
                # To disable button after message started to avoid multi threads of thread_auto_message_send
                diasable_button_func(sending_button ,thread_auto_message_send)

        else :
            error_label.configure(text="Please input all value Sent_Time is optional"  , fg_color="red")
    except Exception as error :
        error_label.configure(text=error , fg_color="red")
    # print(message_var , no_message_var , message_delay_var , index_var , message_sent_time_var)

def on_dropdown_selected(event):
    ...

def main():
    root = ctk.CTk()
    root.title("Auto Message Sender")
    root.geometry("600x580")
    root.minsize(width=600 , height=580 )

    # Current label + ENTRY
    global current_time_entry
    ctk.CTkLabel(master=root , text="Current time :" ,font=("Arial",20)   ).place(relx=0.02 , rely=0.02)  # ,height=15 ,width=120
    current_time_entry = ctk.CTkEntry(master=root ,font=("Arial",21)  ,height=30 ,width=400)
    current_time_entry.place(relx=0.28 ,rely=0.02)  # 
    current_time()

    # MESAAGE LABEL + Entry
    global message_entry
    ctk.CTkLabel(master=root,text="Message :" ,font=("Arial",20),height=25 ,width=90).place(relx=0.02 ,rely=0.1 )
    message_entry = ctk.CTkEntry(master=root ,font=("Arial",20) ,height=30 ,width=400)
    message_entry.place(relx=0.28 ,rely=0.1 )

    # No. of msgs to sent
    global no_message_entry
    ctk.CTkLabel(master=root,text="No. of msgs to sent :" ,font=("Arial",20) ,height=25 ,width=173).place(relx=0.02 ,rely=0.174 )
    no_message_entry = ctk.CTkEntry(master=root ,font=("Arial",20)  ,height=25 ,width=100 )
    no_message_entry.place(relx=0.35 ,rely=0.174)

    # Msgs delay
    global message_sent_delay_entry
    ctk.CTkLabel(master=root,text="Msgs Sent Delay :" ,font=("Arial",18) ,height=25 ,width=140 ).place(relx=0.528 ,rely=0.174 )
    message_sent_delay_entry = ctk.CTkEntry(master=root ,font=("Arial",20) ,height=25 ,width=88 )
    message_sent_delay_entry.place(relx=0.8 ,rely=0.174)
    message_sent_delay_entry.insert(0,0)

    # Index
    ctk.CTkLabel(master=root,text="Index :" ,font=("Arial",20) ,height=25 ,width=55 ).place(relx=0.02 ,rely=0.235 )
    # ----------------------------------DROPDOWN----------------------------
    # Create a StringVar to store the selected item
    global dropdown_var
    dropdown_var = StringVar()
    
    # Create dropdown Menu
    dropdown = ctk.CTkComboBox(master=root, variable=dropdown_var ,height=25 ,width=150 , values=["True" , "False"] )
    dropdown.place(relx=0.15 ,rely=0.24)

    # Bind an event handler to the dropdown
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_selected)
    # ----------------------------------DROPDOWN_end----------------------------

    # Msg sent time Label ++ Entry
    global message_sent_time_entry
    ctk.CTkLabel(root,text="Msg sent time :" ,font=("Arial",20) ,height=25 ,width=140 ).place(relx=0.45 ,rely=0.24)
    message_sent_time_entry = ctk.CTkEntry(root ,font=("Arial",18)  ,height=25 ,width=140 )
    message_sent_time_entry.place(relx=0.71 ,rely=0.24)

    # Start Button
    global sending_button
    sending_button=ctk.CTkButton(master=root,text="Start Sending" ,font=("Arial",20) , command=start_sending ,height=37 ,width=553 )
    sending_button.place(relx=0.02 , rely=0.315 )

    # Error label
    global error_label
    error_label = ctk.CTkLabel(root,text="No any error" ,font=("Arial",18) , fg_color="red" ,height=40 ,width=553 ) 
    error_label.place(relx=0.02 ,rely=0.394)
    
    # time taken Label ++ Entry
    global msg_sent_time_taken_entry
    ctk.CTkLabel(root,text="Time taken :" ,font=("Arial",18) , fg_color="green" ,corner_radius=5 ,height=30 ,width=150 ).place(relx=0.02 ,rely=0.48)
    msg_sent_time_taken_entry = ctk.CTkEntry(root ,font=("Arial",20) ,height=30 ,width=385 )
    msg_sent_time_taken_entry.place(relx=0.3 ,rely=0.48)

    # No. of msg sent
    global msg_sent_text
    ctk.CTkLabel(root,text="Output:" ,font=("Arial",18.5) , fg_color="blue" , corner_radius=5 ,height=30 ,width=165  ).place(relx=0.02 ,rely=0.56)
    msg_sent_text = ctk.CTkTextbox(root , font=("Arial",18.5) , height=200 ,width=550 )
    msg_sent_text.place(relx=0.02 ,rely=0.64 )


    # ------------------------MENU--------------------
    menubar = Menu(master=root)
    menubar.add_command(label="Exit" , command=exit)

    root.configure(menu=menubar)


    root.mainloop()

if __name__ == '__main__' :
    main()


