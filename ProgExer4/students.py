import pymongo
import tkinter as tk
from tkinter import messagebox

from subjectform import subjectform
from teacherform import teacherform



#for database connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['enrollmentsystem']
mycol = mydb["students"]

#two-dimensional list
lst=[["ID","Name","Email","Course"]]

#to assign to the 2 dimensional list to the grid
def callback(event):
    li=[]
    li=event.widget._values
    studentid.set(lst[li[1]][0])
    studentname.set(lst[li[1]][1])
    studentemail.set(lst[li[1]][2])
    studentcourse.set(lst[li[1]][3])
    
def creategrid(n):
    lst.clear()
    lst.append(["ID","Name","Email","Course"])
    cursor = mycol.find({})
    for text_fromDB in cursor:
        studid = str(text_fromDB["studid"])
        studname = str(text_fromDB["studname"].encode("utf-8").decode("utf-8"))
        studemail = str(text_fromDB["studemail"].encode("utf-8").decode("utf-8"))
        studcourse = str(text_fromDB["studcourse"].encode("utf-8").decode("utf-8"))
        lst.append([studid,studname,studemail,studcourse])
#to catch the 2 dimensional list and put it in a multiple entries or the grid
        #i is the row and j is the column
    for i in range(len(lst)):
            for j in range(len(lst[0])):
                    mgrid = tk.Entry(window, width=25)
                    mgrid.insert(tk.END,lst[i][j])
                    mgrid._values = mgrid.get(), i
                    mgrid.grid(row=i+7, column=j+6)
                    mgrid.bind("<Button-1>", callback)
#to clear all of the text entries for rows that is greater than 6
    if n==1:
            for label in window.grid_slaves():
                if int(label.grid_info()["row"]) > 6:
                    label.grid_forget()


def msgbox(msg,titlebar):
    result=messagebox.askokcancel (title=titlebar,message=msg)
    return result

#funtions for buttons
def save():
    r=msgbox("save record?","record")
    if r==True:
        #saves and counts the number of documents in the students selection
        newid = mycol.count_documents({})
        if newid!=0:
            newid= mycol.find_one(sort=[("studid",-1)])["studid"]
        id=newid+1
        studentid.set(id)
        mydict = {"studid":float(studid.get()), "studname": studname.get(),"studemail":studemail.get(), "studcourse": studcourse.get()} 
#to insert one document in the collection "insert_one"
        x = mycol.insert_one(mydict)
        creategrid(1)
        creategrid(0)

def delete():
    r=msgbox("delete record?","record")
    if r==True:
        #deletes the certain variable in the collection using the ID
        myquery = {"studid":float(studid.get())}
        mycol.delete_one(myquery)
        creategrid(1)
        creategrid(0)

def update():
    r=msgbox("update record?","record")
    if r==True:
        #updates the certain variable in the collection using the ID
        myquery = {"studid":float(studid.get())}
        newvalues = {"$set":{"studname":studname.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"studemail":studemail.get()}}
        mycol.update_one(myquery, newvalues)
        
        newvalues = {"$set":{"studcourse":studcourse.get()}}
        mycol.update_one(myquery, newvalues)

        creategrid(1)
        creategrid(0)

#Students GUI Form
window = tk.Tk()
window.title("Students Form")
window.geometry("1050x400")
window.configure(bg="#EEFCDF")

#Menu Bar 
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Subjects", command=subjectform)
filemenu.add_command(label="Teachers", command=teacherform)
filemenu.add_separator()
filemenu.add_command(label="Close", command=window.quit)

#Edit Menu
editmenu=tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo",command=subjectform)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=teacherform)

window.config(menu=menubar)

#Students Enlisment Form GUI
label = tk.Label(window,text="Students Enlistment Form", width=30, height=1, bg="white", anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)
#Student ID
label = tk.Label(window,text="Student ID:", width=10, height=1, bg="white")
label.grid(column=1,row=2)

studentid=tk.StringVar()
studid=tk.Entry(window, textvariable=studentid)
studid.grid(column=2, row=2)
studid.configure(state=tk.DISABLED)
#Student Name
label = tk.Label(window,text="Student Name:", width=15, height=1, bg="white")
label.grid(column=1,row=3)

studentname=tk.StringVar()
studname=tk.Entry(window, textvariable=studentname)
studname.grid(column=2, row=3)
#Student Email
label = tk.Label(window,text="Student Email:", width=15, height=1, bg="white")
label.grid(column=1,row=4)

studentemail=tk.StringVar()
studemail=tk.Entry(window, textvariable=studentemail)
studemail.grid(column=2, row=4)
#Student Course
label = tk.Label(window,text="Student Course:", width=15, height=1, bg="white")
label.grid(column=1,row=5)

studentcourse=tk.StringVar()
studcourse=tk.Entry(window, textvariable=studentcourse)
studcourse.grid(column=2, row=5)

creategrid(0)
#Buttons
# Save Button
savebutton = tk.Button(text = "Save", command=save)
savebutton.grid(column=1, row=6)
#Delete Button
deletebutton = tk.Button(text = "Delete", command=delete)
deletebutton.grid(column=2, row=6)                
#Update Button
updatebutton = tk.Button(text = "Update", command=update)
updatebutton.grid(column=3, row=6)

window.mainloop()
