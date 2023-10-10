try:
    import pyautogui
except:
    import os
    os.system("pip install pyautogui")
    import pyautogui

from database_class_file import database_editing_class
import save_msg_edit_window

from tkinter import *
from tkinter import ttk
import datetime ,time ,threading , sys

message_var = ""
no_message_var = 0
message_delay_var = 0
index_var = 0
message_sent_time_var = "None"

thread_current_time_continuty_teller = True

class Time:
    """Class for time annotation"""
    pass
class ExitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        import threading
        threading.Thread(target=sys.exit).start()
        self.message = message

def exit():
    global thread_current_time_continuty_teller
    thread_current_time_continuty_teller = False
    sys.exit()

def edit_save_msg():
    save_msg_edit_window.main()

def save_msg():
    global save_msg_var , message_entry , save_msg_dropdown
    db = database_editing_class()
    # if save_msg_var != "Empty":
    if message_entry.get() != "" :
        db.add_msg(message_entry.get())
        save_msg_dropdown['values'] = ( "Empty" )
        data = db.fetch_all_data()
        for row in data:
            save_msg_dropdown["values"] += (row[1],)
        db.close_connection()
    else:
        error_label.config(text="First enter msg"  , fg="red")

def current_time() -> None :
    def current_time_thread():
        global current_time_entry , thread_current_time_continuty_teller
        while True :
            time.sleep(1)
            current_time_entry.delete(0,END)
            current_time_entry.insert(0,datetime.datetime.now().strftime("%H:%M:%S"))
            # if thread_current_time_continuty_teller == True :
            #     time.sleep(1)
            #     current_time_entry.delete(0,END)
            #     current_time_entry.insert(0,datetime.datetime.now().strftime("%H:%M:%S"))
            # else :
            #     break
    global thread_current_time
    thread_current_time = threading.Thread(target=current_time_thread)
    thread_current_time.start()

def sending_msg_time_validity_check_func(sending_msg_time:Time):
    """
    1. Find TWO " : " 
    2. Check three parts are int (NOTE:not find three parts BCZ it will be found in first step)
    3. Check first part is maximum 24 and (second & third) is max 60 or less
    """

    split_send_time_list = sending_msg_time.split(":")

    # Find TWO " : " means THREE parts of time input
    if len(split_send_time_list) == 3:
        # Make variable to check int type of input means time
        temp_var_for_int_type_detection = False
        for i in split_send_time_list:
            try:
                int(i)
                temp_var_for_int_type_detection = True
            except:
                temp_var_for_int_type_detection = False
                break
            # 
        if temp_var_for_int_type_detection==True:
            # Check max hours are 24
            if int(split_send_time_list[0]) <= 24:
                # Check max minutes are 60
                if int(split_send_time_list[1])< 60:
                    # Check max seconds are 60
                    if int(split_send_time_list[2]) < 60:
                        validity_of_input_send_time = True
                    else:
                        validity_of_input_send_time = False        
                else:
                    validity_of_input_send_time = False        
            else:
                validity_of_input_send_time = False            
        else:
            validity_of_input_send_time = False                
    return validity_of_input_send_time

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
        error_label.config(text=""  , fg="white")

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
        error_label.config(text="No any errot" , fg="white")
        index_var = 0
    elif dropdown_var.get() == "True" :
        error_label.config(text="No any errot" , fg="white")
        index_var = 1
    else :
        error_label.config(text="Please select index value" , fg="red")
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
        time.sleep(1)
        if message_sent_time_var == datetime.datetime.now().strftime("%H:%M:%S") :
            thread_auto_message_send = threading.Thread(target=auto_message , args=(message_var , int(no_message_var) , int(message_delay_var) , int(index_var)))
            thread_auto_message_send.start()
            thread_auto_message_send.join()
            break
        else :
            ...

def diasable_button_func(tk_button : Button , thread_auto_message_sender : threading ) -> None :
    """ To disable button after message started to avoid multi threads of thread_auto_message_send """
    def diasable_button_sub_func(tk_button : Button, thread_auto_message_sender : threading):
        tk_button.config(state=DISABLED)
        thread_auto_message_sender.join()
        tk_button.config(state=NORMAL)
    def reset_time_sent_msg_var_func():
        def reset_time_sent_msg_sub_func():
            # global thread_auto_message_send_at_time , message_sent_time_var
            global message_sent_time_var
            # thread_auto_message_send_at_time.join()
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
                if sending_msg_time_validity_check_func(message_sent_time_var):
                    msg_sent_text.delete( 0.0,END )
                    msg_sent_text.insert(0.0 , f"Waiting for time {message_sent_time_var}" )
                    error_label.config(text=f"Waiting for time {message_sent_time_var}"  , fg="green")
                    global thread_auto_message_send_at_time
                    thread_auto_message_send_at_time = threading.Thread(target=send_msg_at_time , args=(message_var , int(no_message_var) , eval(message_delay_var) , int(index_var) , message_sent_time_var ))
                    thread_auto_message_send_at_time.start()
                    # To disable button after message started to avoid multi threads of thread_auto_message_send
                    diasable_button_func(sending_button ,thread_auto_message_send_at_time)
                else:
                    error_label.config(text="Enter correct send time"  , fg="red")
                    msg_sent_text.insert(0.0 , f"Enter correct send time \nTime should be less than 24hours" )



            else :
                error_label.config(text="Waiting for 3 seconds"  , fg="green")

                thread_auto_message_send = threading.Thread(target=auto_message , args=(message_var , int(no_message_var) , eval(message_delay_var) , int(index_var)))
                thread_auto_message_send.start()
                # To disable button after message started to avoid multi threads of thread_auto_message_send
                diasable_button_func(sending_button ,thread_auto_message_send)

        else :
            error_label.config(text="Please input all value SentTime is optional"  , fg="red")
    except Exception as error :
        error_label.config(text=error , fg="red")
    # print(message_var , no_message_var , message_delay_var , index_var , message_sent_time_var)

def on_dropdown_selected(event):
    ...

def on_save_msg_dropdown_selected(event):
    global save_msg_dropdown , message_entry
    message_entry.delete(0,END)
    message_entry.insert(0,save_msg_dropdown.get())


def main():
    root = Tk()
    root.title("Auto Message Sender")
    # root.wm_attributes("-topmost", True)
    root.resizable(False,False)
    root.geometry("600x550")

    # Current label + ENTRY
    global current_time_entry
    Label(root,text="Current time :" ,font=("Arial",15) , fg="red").place(x=18 ,y=20 ,height=15 ,width=120)
    current_time_entry = Entry(root ,font=("Arial",14) )
    current_time_entry.place(x=140 ,y=11 ,height=30 ,width=420)
    current_time()

    # MESAAGE LABEL + Entry
    global message_entry
    Label(root,text="Message :" ,font=("Arial",15)).place(x=20 ,y=55 ,height=25 ,width=90)
    message_entry = Entry(root ,font=("Arial",12))
    message_entry.place(x=140 ,y=50 ,height=30 ,width=420)

    # No. of msgs to sent
    global no_message_entry
    Label(root,text="No. of msgs to sent :" ,font=("Arial",14)).place(x=20 ,y=90 ,height=25 ,width=173)
    no_message_entry = Entry(root ,font=("Arial",12))
    no_message_entry.place(x=198 ,y=93 ,height=25 ,width=100)
    
    # Msgs delay
    global message_sent_delay_entry
    Label(root,text="Msgs Sent Delay :" ,font=("Arial",14)).place(x=310 ,y=90 ,height=25 ,width=155)
    message_sent_delay_entry = Entry(root ,font=("Arial",12))
    message_sent_delay_entry.place(x=470 ,y=93 ,height=25 ,width=90)
    message_sent_delay_entry.insert(0,0)

    # Index
    Label(root,text="Index :" ,font=("Arial",14)).place(x=20 ,y=125 ,height=25 ,width=55)
    # ----------------------------------DROPDOWN_FOR_INDEX----------------------------
    # Create a StringVar to store the selected item
    global dropdown_var
    dropdown_var = StringVar()
    
    # Create dropdown Menu
    dropdown = ttk.Combobox(root, textvariable=dropdown_var)
    dropdown['values'] = ("True" , "False")
    dropdown.place(x=90 ,y=125 ,height=25 ,width=150)

    # Bind an event handler to the dropdown
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_selected)
    # ----------------------------------DROPDOWN_FOR_INDEX_end----------------------------

    # Msg sent time Label ++ Entry
    global message_sent_time_entry
    Label(root,text="Msg sent time :" ,font=("Arial",14)).place(x=305 ,y=125 ,height=25 ,width=140)
    message_sent_time_entry = Entry(root ,font=("Arial",12))
    message_sent_time_entry.place(x=450 ,y=125 ,height=25 ,width=110)

    # ----------------------------------DROPDOWN_FOR_saved_msgs----------------------------
    # Create a StringVar to store the selected item
    global save_msg_var , save_msg_dropdown
    save_msg_var = StringVar()
    
    # Create dropdown Menu
    save_msg_dropdown = ttk.Combobox(root, textvariable=save_msg_var , state="readonly")
    save_msg_dropdown['values'] = ( "Empty" )
    db = database_editing_class()
    data = db.fetch_all_data()
    for row in data:
        save_msg_dropdown["values"] += (row[1],)
    db.close_connection()
    save_msg_dropdown.place(x=28 ,y=164 ,height=30 ,width=400)
    save_msg_dropdown.set("Select A Save Msg")

    # Bind an event handler to the dropdown
    save_msg_dropdown.bind("<<ComboboxSelected>>", on_save_msg_dropdown_selected)
    # ----------------------------------DROPDOWN_FOR_saved_msgs_end----------------------------
    # Start Button
    global save_msg_button
    save_msg_button=Button(root,text="Save msg" ,font=("Arial",15) , relief=SOLID , border=3 , command=save_msg)
    save_msg_button.place(x=440 ,y=164 ,height=30 ,width=120)
    
    # Start Button
    global sending_button
    sending_button=Button(root,text="Start Sending" ,font=("Arial",15) , relief=SOLID , border=3 , command=start_sending)
    sending_button.place(x=20 ,y=210 ,height=37 ,width=540)

    # Error label
    global error_label
    error_label = Label(root,text="No any error" ,font=("Arial",15) ,fg="blue")
    error_label.place(x=20 ,y=250 ,height=40 ,width=540)
    
    # time taken Label ++ Entry
    global msg_sent_time_taken_entry
    Label(root,text="Time taken :" ,font=("Arial",15) , fg="green").place(x=20 ,y=300 ,height=25 ,width=120)
    msg_sent_time_taken_entry = Entry(root ,font=("Arial",12))
    msg_sent_time_taken_entry.place(x=150 ,y=300 ,height=25 ,width=410)

    # No. of msg sent
    global msg_sent_text
    Label(root,text="No. of msg sent :" ,font=("Arial",15) ).place(x=20 ,y=340 ,height=25 ,width=150)
    msg_sent_text = Text(root)
    msg_sent_text.place(x=20 ,y=370 ,height=150 ,width=540)

    # --------------------------------------------MENU------------------------------------------- #
    # Create the menu 
    menubar =Menu(root)
    # Create the Help menu
    menubar.add_command(label="Exit", command=exit)
    menubar.add_command(label="Edit Save Msgs", command=edit_save_msg)
    # Configure the root to use the menubar
    root.config(menu=menubar)




    root.mainloop()

if __name__ == '__main__' :
    main()
