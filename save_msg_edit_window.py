from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database_class_file import database_editing_class
import threading

old_msg = "None"

def exit():
    import sys
    sys.exit()

def refresh_dropdown():
    global select_msg_to_edit_dropdown , edit_msg_entry
    db = database_editing_class()
    select_msg_to_edit_dropdown['values'] = ( "Empty" )
    data = db.fetch_all_data()
    for row in data:
        select_msg_to_edit_dropdown["values"] += (row[1],)
    select_msg_to_edit_dropdown.set("Select A Save Msg to Edit")
    edit_msg_entry.delete(0,END)
    db.close_connection()
    db.close()

def on_save_msgs_dropdown_selected(events):
    global edit_msg_entry , select_msg_to_edit_dropdown , old_msg
    edit_msg_entry.delete(0,END)
    if select_msg_to_edit_dropdown.get() != "Empty" :
        edit_msg_entry.insert(0, select_msg_to_edit_dropdown.get() )
        old_msg = select_msg_to_edit_dropdown.get()

def update_func():
    global old_msg , edit_msg_entry
    db = database_editing_class()
    db.update_msg(old_message=old_msg , new_message=edit_msg_entry.get())
    refresh_dropdown()
    db.close_connection()

def add_msg_func():
    global old_msg , edit_msg_entry , error_label
    db = database_editing_class()
    if old_msg != edit_msg_entry.get() :
        db.add_msg(edit_msg_entry.get())
        error_label.config(text="Message has Saved successfully" , background="green" , fg="white")
        refresh_dropdown()
    else:
        error_label.config(text="Message has been already Saved successfully" , background="red" , fg="white")

    db.close_connection()

def delete_msg_func():
    global old_msg , select_msg_to_edit_dropdown , edit_msg_entry , error_label
    if old_msg != "None" :
        db = database_editing_class()
        db.delete_msg(old_msg)
        select_msg_to_edit_dropdown['values'] = ( "Empty" )
        data = db.fetch_all_data()
        for row in data:
            select_msg_to_edit_dropdown["values"] += (row[1],)
        select_msg_to_edit_dropdown.set("Select A Save Msg to Edit")
        edit_msg_entry.delete(0,END)
        error_label.config(text="Msg deleted successfully" , background="green" , fg="white")
        db.close_connection()
        db.close()

def cleardatabase_func():
    global error_label
    db = database_editing_class()
    # Create a warning message box.
    result = messagebox.askyesno("Warning", "Are you sure you want to Delete all save Messages?")

    if result:
        db.clear_database()
        error_label.config(text="All msg(s) deleted successfully" , background="green" , fg="white")
        refresh_dropdown()
    db.close_connection()

def main():
    root = Tk()
    root.title("Edit Save Messages")
    root.geometry("450x300")
    root.maxsize(450,270)

    # To kept window top beneath two lines are effective which have been commented
    # root.lift()
    # root.attributes('-topmost', True)

    element_height_distance = 15
    element_horizontal_distance = 20

    # -------------------------Dropdown_select_msg_to_edit_START--------------------------------------
    global select_msg_to_edit_dropdown
    select_msg_to_edit_dropdown = ttk.Combobox(root , state="readonly")
    select_msg_to_edit_dropdown.place(x=11 , y=11 , height=33 , width=(450-(11*2)))

    select_msg_to_edit_dropdown['values'] = ( "Empty" )
    db = database_editing_class()
    data = db.fetch_all_data()
    for row in data:
        select_msg_to_edit_dropdown["values"] += (row[1],)
    db.close_connection()
    # select_msg_to_edit_dropdown.place(x=28 ,y=164 ,height=30 ,width=400)
    select_msg_to_edit_dropdown.set("Select A Save Msg to Edit")

    # Bind an event handler to the dropdown
    select_msg_to_edit_dropdown.bind("<<ComboboxSelected>>", on_save_msgs_dropdown_selected)
    # -------------------------Dropdown_select_msg_to_edit_END--------------------------------------

    # Edit msg entry
    global edit_msg_entry
    edit_msg_entry = Entry(root , font=("Arial",15))
    edit_msg_entry.place(x=11 , y=(11+element_height_distance+30) , height=35 , width=(450-(11*2)))

    # Button Update
    Button(root,text="Update" , font=("Arial",15) , relief=SOLID , border=3 , command=update_func ).place(x=11 , y=110 , height=40 , width=210 )
    
    # Button Delete
    Button(root,text="Delete" , font=("Arial",15) , relief=SOLID , border=3 , command=delete_msg_func ).place(x=230 , y=110 , height=40 , width=210 )

    # Button Add Msg
    Button(root,text="Add Msg" , font=("Arial",15) , relief=SOLID , border=3 , command=add_msg_func ).place(x=11 , y=160 , height=40 , width=210 )

    # Button Clear all Save Msgs
    Button(root,text="Clear all Save Msgs" , font=("Arial",15) , relief=SOLID , border=3 , command=cleardatabase_func ).place(x=230 , y=160  , height=40 , width=210 )

    # Label for Note Or ERROR
    global error_label
    error_label = Label(root , text=" " , font=("Arial",13) )
    error_label.place(x=11 , y=210 , height=40 , width=(450-(11*2)) )

    # --------------------------------------------MENU------------------------------------------- #
    # Create the menu 
    menubar =Menu(root)
    # Create the Help menu
    # menubar.add_command(label="Exit", command=exit)
    menubar.add_command(label="Refresh database", command=refresh_dropdown)
    # Configure the root to use the menubar
    root.config(menu=menubar)

    root.mainloop()

if __name__ == '__main__' :
    main()
