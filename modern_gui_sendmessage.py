try :
    import customtkinter as ctk
except :
    import os; os.system("pip install customtkinter")
finally:
    import customtkinter as ctk

from database_class_file import database_editing_class
import save_msg_edit_window
from tkinter import END ,NORMAL  , DISABLED ,StringVar , Menu , Button
import datetime ,time ,threading , os 
# import multiprocessing

# ----------- #
"""Default values"""
message_var = ""
no_message_var = 0
message_delay_var = 0
index_var = 0
message_sent_time_var = "None"

thread_current_time_continuty_teller = True
# ----------- #


class Time:
    """Class for time annotation"""
    pass

class ExitError:
    """ This class doesn't use exception bcz with exception an new error occur and thi is working with os._exit(1) """
    def __init__(self):
        os._exit(1)

def exit():
    """This function set the 'thread_current_time_continuty_teller'=false 
    after it in current time thread if -else condition stop the current time displaying and
    then i call os._exit(1)  in it is its status and it terminate the code immediately """
    """
    os._exit(1) vs sys.exit()
    the os._exit() function is used to exit a process immediately.
    Unlike the sys.exit() function, which raises a SystemExit exception and allows cleanup code to be executed, 
    os._exit() terminates the process without calling cleanup handlers, flushing stdio buffers, 
    or handling any atexit functions.
    """
    
    global thread_current_time_continuty_teller 
    thread_current_time_continuty_teller = False
    thread_current_time.join()
    ExitError()
    # os._exit(1)

def current_time() -> None :
    """IF condition "thread_current_time_continuty_teller == True" is true, 
    this function keep inserting time in current time entry after every 1 sec 
    """
    def current_time_thread_func():
        global current_time_entry , thread_current_time_continuty_teller
        while True :
            if thread_current_time_continuty_teller == True :
                time.sleep(1)
                current_time_entry.delete(0,END)
                current_time_entry.insert(0,datetime.datetime.now().strftime("%H:%M:%S"))
            else :
                break
    global thread_current_time
    thread_current_time = threading.Thread(target=current_time_thread_func)
    thread_current_time.start()

def edit_save_msg():
    save_msg_edit_window.main(window_master=root)

def refresh_dropdown():
    """This function refresh the data in dropdown mean again insert new data instead of old one 
    in combobox and insert only unique values mean will not insert same values again and again as in database
    It store all msgs in a list after getting from database and then convert this list in set to uniqify every element
    in list and then convert this output set in list to give to dropdown
    """
    global save_msg_dropdown
    db = database_editing_class()
    data = db.fetch_all_data()
    newvalues_save_msg_dropdown = []
    for row in data:
        newvalues_save_msg_dropdown.append(row[1])
    if newvalues_save_msg_dropdown != [] :
        newvalues_save_msg_dropdown = list(set(newvalues_save_msg_dropdown))
        save_msg_dropdown.configure(values=newvalues_save_msg_dropdown)
    db.close_connection()

def auto_message( message : str ,no_messages : int ,send_delay : int ,index : int , sent_time : str = "Nonestr") -> None :
        """This funstions will type type {message} {no_messages} time"""
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
        time.sleep(1)
        if message_sent_time_var == datetime.datetime.now().strftime("%H:%M:%S") :
            global thread_auto_message_send
            thread_auto_message_send = threading.Thread(target=auto_message , args=(message_var , int(no_message_var) , int(message_delay_var) , int(index_var)))
            thread_auto_message_send.start()
            thread_auto_message_send.join()
            message_sent_time_var = "None"
            break
        else :
            ...

def sending_msg_time_validity_check_func(sending_msg_time:Time) ->bool:
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

def disable_button_func(tk_button : Button , thread_auto_message_sender : threading ) -> None :
    """ To disable button after message started sent to avoid multi threads of thread_auto_message_send """
    def diasable_button_sub_func(tk_button : Button, thread_auto_message_sender : threading):
        tk_button.configure(state=DISABLED)
        thread_auto_message_sender.join()
        tk_button.configure(state=NORMAL)
    # def reset_time_sent_msg_var_func( this_func_is_disabled ):
    #     # 
    #     def reset_time_sent_msg_sub_func():
    #         global thread_auto_message_send_at_time , message_sent_time_var
    #         thread_auto_message_send_at_time.join()
    #         message_sent_time_var = "None"
    #     # 
    #     # thread_reset_message_send_at_time_var = threading.Thread(target=reset_time_sent_msg_sub_func )
    #     # thread_reset_message_send_at_time_var.start()
    #     # 
    # # reset_time_sent_msg_var_func()
    thread_disable_enable_button = threading.Thread(target=diasable_button_sub_func , args=(tk_button , thread_auto_message_sender))
    thread_disable_enable_button.start()

def start_sending() -> None :
    try :
        global message_var , no_message_var , message_delay_var , index_var , message_sent_time_var , sending_button , msg_sent_text
        get_inputs()



        if check_blank_inputs() :

            if message_sent_time_var != "None" :
                if sending_msg_time_validity_check_func(message_sent_time_var):
                    msg_sent_text.delete(0.0 , END )
                    msg_sent_text.insert(0.0 , f"Waiting for time {message_sent_time_var}" )
                    error_label.configure(text=f"Waiting for time {message_sent_time_var}"  , fg_color="green")
                    global thread_auto_message_send_at_time
                    thread_auto_message_send_at_time = threading.Thread(target=send_msg_at_time , args=(message_var , int(no_message_var) , eval(message_delay_var) , int(index_var) , message_sent_time_var ))
                    thread_auto_message_send_at_time.start()
                    # To disable button after message started to avoid multi threads of thread_auto_message_send
                    disable_button_func(sending_button ,thread_auto_message_send_at_time)
                else:
                    error_label.configure(text="Enter correct send time"  , bg_color="red")
                    msg_sent_text.delete(0.0 , END )
                    msg_sent_text.insert(0.0 , f"Enter correct send time \nTime should be less than 24hours" )

            else :
                error_label.configure(text="Waiting for 3 seconds"  , fg_color="green")

                thread_auto_message_send = threading.Thread(target=auto_message , args=(message_var , int(no_message_var) , eval(message_delay_var) , int(index_var)))
                thread_auto_message_send.start()
                # To disable button after message started to avoid multi threads of thread_auto_message_send
                disable_button_func(sending_button ,thread_auto_message_send)

        else :
            error_label.configure(text="Please input all value Sent_Time is optional"  , fg_color="red")
    except Exception as error :
        error_label.configure(text=error , fg_color="red")
        print(error)
    # print(message_var , no_message_var , message_delay_var , index_var , message_sent_time_var)

def save_msg():
    """save msg in database and refresh the dropdown
    """
    global save_msg_var , message_entry , save_msg_dropdown
    if message_entry.get() != "" :
        db = database_editing_class()
        db.add_msg(message_entry.get())
        # data = db.fetch_all_data()
        # newvalues_save_msg_dropdown = []
        # for row in data:
        #     newvalues_save_msg_dropdown.append(row[1])
        # if newvalues_save_msg_dropdown != [] :
        #     newvalues_save_msg_dropdown = list(set(newvalues_save_msg_dropdown))
        #     save_msg_dropdown.configure(values=newvalues_save_msg_dropdown)
        db.close_connection()
        refresh_dropdown()
    else:
        error_label.configure(text="First enter msg"  , bg_color="red" )

def on_dropdown_selected(event):
    ...

def on_save_msg_dropdown_selected(event):
    """it insert selected msg from dropdown in 'message_entry'  
    """
    global save_msg_var , message_entry
    if (save_msg_selected_in_dropdown:=save_msg_var.get()) != "Empty" :
        message_entry.delete(0,END)
        message_entry.insert(0,save_msg_selected_in_dropdown)

def main():
    global root
    root = ctk.CTk()
    root.title("Auto Message Sender")
    root.resizable(False,True)
    root.geometry("580x630")
    root.minsize(width=580 , height=630 )
    # Set the protocol to call the on_close function when the window is closed
    root.protocol("WM_DELETE_WINDOW", threading.Thread(target=exit).start)
    # If want icon use it else dont
    # root.iconbitmap("logo.ico")

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
    message_sent_delay_entry = ctk.CTkEntry(master=root ,font=("Arial",20) ,height=25 ,width=98 )
    message_sent_delay_entry.place(relx=0.8 ,rely=0.174)
    message_sent_delay_entry.insert(0,0)

    # Index
    ctk.CTkLabel(master=root,text="Index :" ,font=("Arial",20) ,height=25 ,width=55 ).place(relx=0.02 ,rely=0.235 )
    # ----------------------------------DROPDOWN----------------------------
    # Create a StringVar to store the selected item
    global dropdown_var
    dropdown_var = StringVar()
    
    # Create INDEX dropdown Menu
    dropdown = ctk.CTkComboBox(master=root, state="readonly" , variable=dropdown_var ,height=25 ,width=150 , values=["True" , "False"] )
    dropdown.place(relx=0.15 ,rely=0.24)

    # ----------------------------------DROPDOWN_end----------------------------

    # Msg sent time Label ++ Entry
    global message_sent_time_entry
    ctk.CTkLabel(root,text="Msg sent time :" ,font=("Arial",20) ,height=25 ,width=140 ).place(relx=0.45 ,rely=0.24)
    message_sent_time_entry = ctk.CTkEntry(root ,font=("Arial",18)  ,height=25 ,width=150 )
    message_sent_time_entry.place(relx=0.71 ,rely=0.24)

    # ----------------------------------DROPDOWN_FOR_saved_msgs----------------------------
    # Create a StringVar to store the selected item
    global  save_msg_var , save_msg_dropdown
    save_msg_var = StringVar()
    
    # Create dropdown Menu
    save_msg_dropdown = ctk.CTkComboBox(root , state="readonly" , command=on_save_msg_dropdown_selected , variable=save_msg_var , height=30 ,width=400 , values=["Empty"] )
    db = database_editing_class()
    data = db.fetch_all_data()
    newvalues_save_msg_dropdown = []
    for row in data:
        newvalues_save_msg_dropdown.append(row[1])
    if newvalues_save_msg_dropdown != [] :
        newvalues_save_msg_dropdown = list(set(newvalues_save_msg_dropdown))
        save_msg_dropdown.configure(values=newvalues_save_msg_dropdown)
    db.close_connection()

    save_msg_dropdown.place(relx=0.02 , rely=0.315)
    save_msg_dropdown.set("Select A Save Msg")

    # ----------------------------------DROPDOWN_FOR_saved_msgs_end----------------------------
    # Start Button
    global save_msg_button
    save_msg_button=ctk.CTkButton(root,text="Save msg" ,font=("Arial",15) , command=save_msg , height=30 ,width=145 )
    save_msg_button.place( relx=0.72 , rely=0.315 )
    
    # Start Button
    global sending_button
    sending_button=ctk.CTkButton(master=root,text="Start Sending" ,font=("Arial",20) , command=start_sending ,height=37 ,width=550 )
    sending_button.place(relx=0.02 , rely=0.405 )

    # Error label
    global error_label
    error_label = ctk.CTkLabel(root,text="No any error" ,font=("Arial",18) , fg_color="green" ,height=40 ,width=549 ) 
    error_label.place(relx=0.02 ,rely=0.484)
    
    # time taken Label ++ Entry
    global msg_sent_time_taken_entry
    ctk.CTkLabel(root,text="Time taken :" ,font=("Arial",18) , fg_color="green" ,corner_radius=5 ,height=30 ,width=150 ).place(relx=0.02 ,rely=0.57)
    msg_sent_time_taken_entry = ctk.CTkEntry(root ,font=("Arial",20) ,height=30 ,width=385 )
    msg_sent_time_taken_entry.place(relx=0.3 ,rely=0.57)
    # msg_sent_time_taken_entry.configure(state=DISABLED)

    # No. of msg sent
    global msg_sent_text
    ctk.CTkLabel(root,text="Output:" ,font=("Arial",18.5) , fg_color="blue" , corner_radius=5 ,height=30 ,width=165  ).place(relx=0.02 ,rely=0.65) #0.56
    msg_sent_text = ctk.CTkTextbox(root , font=("Arial",18.5) , height=150 ,width=550 )
    msg_sent_text.place(relx=0.02 ,rely=0.73 )


    # ------------------------MENU--------------------
    menubar = Menu(master=root)
    
    menubar.add_command(label="Exit" , command=threading.Thread(target=exit).start)
    menubar.add_command(label="Edit Save Msgs", command=edit_save_msg)
    menubar.add_command(label="Refresh database", command=refresh_dropdown)

    root.configure(menu=menubar)


    root.mainloop()

if __name__ == '__main__' :
    main()