from ast import Pass
from cgitb import text
from distutils.dir_util import copy_tree
from importlib.resources import path
import os
from re import search
import threading
from time import sleep

import time
import shutil

from tkinter import *
from tkinter import ttk
from pathlib import *
from tkinter.ttk import Treeview
from typing import Any, Literal
import subprocess
from tkinter import messagebox as mb
from tkinter.messagebox import *
from tkinter.simpledialog import*
import gzip
from zipfile import ZipFile

from zipfile import ZIP_STORED




window = Tk()
sem = threading.Semaphore()
enc = "utf-8"
try:
        import locale
        locale.setlocale(locale.LC_ALL,'')
        enc = locale.nl_langinfo(locale.CODESET)
except (ImportError, AttributeError):
        pass

window.title("My JLD~MANAGER")
window.geometry("2048x720")
window.minsize(1080, 360)
#window.iconbitmap('icons8.ico')
window.config(background="#F72B56")


FileOptions =["New", "Open","Close"]
NewOptions=["New folder"]
EditOptions=["Copy","Cut","Compress","Delete","Move","Rename","Decompress"]
EditOptionsAfter=["Undo","Redo"]
AboutOptions=["About "]
menuBar = Menu(window)
File = Menu(menuBar, tearoff=0)
File.add_command(label="Close",command=window.quit)
New=Menu(File,tearoff=1)

File.add_cascade(label="New",menu=New)

menuBar.add_cascade(label="File",menu=File)
Edit = Menu(menuBar, tearoff=0)

menuBar.add_cascade(label="Edit", menu=Edit)
Sort_by=Menu(menuBar,tearoff=0)

menuBar.add_cascade(label="Sort_by",menu=Sort_by)
About = Menu(menuBar, tearoff=0)

menuBar.add_cascade(label="About",menu=About)
window.config(menu=menuBar)



top_frame = Frame(window)
v = StringVar()
undobutton = Button(top_frame, text="Undo", width=9)
undobutton.grid(row=0, column=0, sticky='nsew')
redobutton = Button(top_frame, text="Redo", width=9)
redobutton.grid(row=0, column=1, sticky='nsew')
statusbar = Entry(top_frame, textvariable=v, width=105)
statusbar.grid(row=0, column=2, sticky='nsew', padx=10)
searchbar=Entry(top_frame, textvariable='',width=50)
searchbar.grid(row=0,column=3,sticky='nswe')
searchbut=Button(top_frame,text="Search",width=15)
searchbut.grid(row=0,column=4,sticky='nswe')
top_frame.grid(row=0, column=0, columnspan=4, sticky='nsew')


left_frame = Frame(window)


listview = ttk.Treeview(left_frame, height=34)

listview["columns"] = ("1", "2", "3")
ybar2 = Scrollbar(left_frame, orient=VERTICAL, command=listview.yview)
listview.configure(yscroll=ybar2.set)

listview.column("#0", width=300, stretch=False)
listview.column("#1", width=200, stretch=False)
listview.column("#2", width=200, stretch=False)
listview.column("#3", width=200, stretch=False)

listview.heading("#0", text="Name", anchor="center")
listview.heading("#1", text="Date Modified", anchor="center")
listview.heading("#2", text="Type", anchor="center")
listview.heading("#3", text="Size", anchor="center")





tv1= ttk.Treeview(left_frame, height=34)
ybar1 = Scrollbar(left_frame, orient=VERTICAL, command=tv1.yview)
tv1.configure(yscroll=ybar1.set)
tv1.heading("#0",text="My Computer")




disk=[chr(x)+":\\" for x in range(10,90) if os.path.exists(chr(x)+":\\")]
for d in disk:
    parent_iid = tv1.insert('', 'end', text=d, open=False)

def actu_disque():
    disk=[chr(x)+":\\" for x in range(10,90) if os.path.exists(chr(x)+":\\")]
    for d in disk:
        if d not in tv1.get_children()['text']:
            tv1.insert('', 'end', text=d, open=False)
        else:
            pass
    for i in tv1.get_children():
        if i['text'] not in disk:
            tv1.delete(i)
        else:
            pass
    window.after(1,actu_disque)
window.after(1,actu_disque)    


     

def getpathfromtree():
    item_iid = tv1.focus()
    path = tv1.item(item_iid)['text']
    parent = tv1.parent(item_iid)
    while parent != "":
        node = tv1.item(parent)['text']
        path = os.path.join(node, path)
        parent = tv1.parent(parent)
    
    return path
 

def new_folder(event):
    node = tv1.focus()
    v.set(getpathfromtree())
    directory_entries = os.listdir(getpathfromtree())
    for name in listview.get_children():
        listview.delete(name)
    for name in tv1.get_children(node):
        tv1.delete(name)
    for name in directory_entries:
        item_path = getpathfromtree() + os.sep + name
        root = os.path.splitext(name)
        ext = name.split(".")[-1]
    
        if os.path.isdir(item_path):
            try:
                
                
                tv1.insert(parent=node,
                           index='end',
                           text=name)
                values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                listview.insert(parent='', text=name, index="end", values=values1)

            except PermissionError:
                pass
        else:
            tv1.insert(parent=parent_iid,
                       index='end',
                       text=name)

            values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
            listview.insert(parent='', text=root, index="end", values=values2)
            #print(item_path)

def peuplerlistview(event):

    node = listview.focus() 
    
    chem = (listview.item(node)['values'])[3]
    try:
      if os.path.isdir(chem): 
          directory_entries = os.listdir(chem)
        
          for name in listview.get_children():
            listview.delete(name)
    
          for name in directory_entries:
            item_path = os.path.join(chem,name)
            ext = name.split(".")[-1]
    
            if os.path.isdir(item_path):
                try:
                    values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                    listview.insert(parent='', text=name, index="end", values=values1)

                except PermissionError:
                    pass
            else:
                values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
                listview.insert(parent='', text=name, index="end", values=values2)
      else:
             os.startfile(chem)
    except PermissionError as error:
            mb.showerror("Open Failed",message=str(error))
    v.set(chem)
def open():
    node=listview.focus()
    chem=Path(os.path.join(statusbar.get(),listview.item(node)['text']))
    if os.path.isfile(chem):
        try:
      
          os.startfile(chem)
        except OSError as error:
            mb.showerror("Open Failed",message=str(error))  
                 
            
File.add_command(label="Open",command=open)              
def Openwith():
    node=listview.selection()
    root=os.path.splitext(listview.item(node)['text'])
    chemin=Path(os.path.join(statusbar.get(),listview.item(node)['text']))
    if os.path.isfile(chemin):
        try:
            newpath=Path(os.path.join(statusbar.get(),root)) 
            os.rename(chemin,newpath)  
            pth=Path(os.path.join(statusbar.get(),root))
            os.startfile(pth)
            os.rename(newpath,chemin)
        except OSError as error:
            mb.showerror("Open failed",message=str(error))
File.add_command(label="Open With",command=Openwith)    
def repopulate():
    for i in listview.get_children():
            listview.delete(i)
    try:
            for name in os.listdir(statusbar.get()) :
               item_path = os.path.join(statusbar.get(),name)
               ext = name.split(".")[-1]
               if os.path.isdir(item_path):
                    try:
                        values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                        listview.insert(parent='', text=name, index="end", values=values1)

                    except PermissionError:
                        pass
               else:
                    values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
                    listview.insert(parent='', text=name, index="end", values=values2)
    except OSError as error:
            mb.showerror('Error',message=str(error))
def inverse1() :
    for i in listview.get_children():
        listview.delete(i)

    try:
            for name in reversed(os.listdir(statusbar.get())) :
               item_path = os.path.join(statusbar.get(),name)
               ext = name.split(".")[-1]
               if os.path.isdir(item_path):
                    
                    try:
                        values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                        listview.insert(parent='', text=name, index="end", values=values1)

                    except PermissionError:
                        pass
               else:
                    values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
                    listview.insert(parent='', text=name, index="end", values=values2)
    except OSError as error:
            mb.showerror('Error',message=str(error)) 
Sort_by.add_command(label="Alphabet",command=inverse1)
def folder():
    try:
        name=askstring("Create a new folder","Enter the new name ")
        try:
            path=os.path.join(statusbar.get(),name)
            os.mkdir(path)
        except TypeError:
            pass
        for i in listview.get_children():
            listview.delete(i)
        try:
            for name in os.listdir(statusbar.get()) :
               item_path = os.path.join(statusbar.get(),name)
               ext = name.split(".")[-1]
               if os.path.isdir(item_path):
                    try:
                        values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                        listview.insert(parent='', text=name, index="end", values=values1)

                    except PermissionError:
                        pass
               else:
                    values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
                    listview.insert(parent='', text=name, index="end", values=values2)
            repopulate()
        except OSError as error:
            mb.showerror('Error',message=str(error)) 
    except OSError as error:
        mb.showerror("You can create a folder",message=str(error))
New.add_command(label="New Folder",command=folder)        


def delete():
    try:
        selected=listview.selection()
        if mb.askyesno("Warning",message="Do you really want to delete this file\folder ?"):
            for i in selected:
                path=(listview.item(i)['values'])[3]
                if os.path.isdir(path):
                    try:
                        shutil.rmtree(path)
                    except OSError as error:
                        mb.showerror("You can delete this folder",message=str(error))
                else:
                    try:
                        os.remove(path)
                    except:
                        mb.showerror("You can delete this file")
        else:
            pass
    except IndexError:
        pass   
    repopulate()         
Edit.add_command(label="Delete",command=delete)
def rename():
 node=listview.focus()
 parent=listview.parent(node)   
 
 try:
     oldname=os.path.join(statusbar.get(),listview.item(parent)['text'])
     newname=askstring("Rename","Enter the new name")
     if os.path.isfile(oldname):
         extension=os.path.splitext(oldname)[1]
         newname=newname +extension
     newname=Path(os.path.join(statusbar.get(),newname))
     os.rename(oldname,newname)
     repopulate() 
 except OSError as error:
      mb.showerror("Rename failed",message=str(error))      
Edit.add_command(label="Rename",command=rename)
def compress():
    node=listview.focus()
    path=(listview.item(node)['values'])[3]
    
    try:
            if os.path.isdir(path):
                shutil.make_archive(path,"zip",path)
                repopulate() 
            else:
                with open(path,'rb') as f_input:
                  with gzip.open(str(path)+'.zip','wb') as f_output:
                       shutil.copyfileobj(f_input,f_output) 
                repopulate() 
               
    except TypeError as error:
                pass
    

Edit.add_command(label="Compress",command=compress)
def decompress():
    node=listview.selection()
    path=(listview.item(node)['values'])[3]
    shutil.unpack_archive(str(path))
    
    repopulate()        
Edit.add_command(label="Decompress",command=decompress)
tabcopy=[]
tabcopydir=[]
tabcut=[]
tabcutdir=[]
def copy():
    global tabcopy
    for i in listview.selection():
       try:
        try:
            path=(listview.item(i)['values'])[3]
            tabcopy.append(path)
            if os.path.isdir(path):
                tabcopydir.append(listview.item(i)['text'])
        except IndexError:
            pass
       except OSError as error:
           mb.showerror("Cut Failed",message=str(error))
                
Edit.add_command(label="Copy",command=copy) 
def copy1(event):
    global tabcopy
    for i in listview.selection():
       try:
        try:
            path=(listview.item(i)['values'])[3]
            tabcopy.append(path)
            if os.path.isdir(path):
                tabcopydir.append(listview.item(i)['text'])
        except IndexError:
            pass
       except OSError as error:
           mb.showerror("Cut Failed",message=str(error))
    tabcut.clear()            
listview.bind('<Control-KeyPress-C>',copy1)   
def cut():
    global tabcut
    for i in listview.selection():
       try: 
        try :
            path=(listview.item(i)['values'])[3]
            tabcut.append(path)
            if os.path.isdir(path):
                tabcutdir.append(listview.item(i)['text'])
        except IndexError:
            pass
       except OSError as error:
           mb.showerror("Cut Failed",message=str(error)) 
    
Edit.add_command(label="Cut",command=cut)
def cut1(event):
    global tabcut
    for i in listview.selection():
       try: 
        try :
            path=(listview.item(i)['values'])[3]
            tabcut.append(path)
            
            if os.path.isdir(path):
                tabcutdir.append(listview.item(i)['text'])
        except IndexError:
            pass
       except OSError as error:
           mb.showerror("Cut Failed",message=str(error)) 
    tabcopy.clear()
listview.bind('<Control-KeyPress-X>',cut1)
def paste():
    try:
        try:
            if len(tabcopy)!=0:
             j=0
             
             sem.acquire()
                
             for i in tabcopy:
                if os.path.isdir(i):
                    print(tabcopydir[j])
                    copy_tree(j,os.path.join(statusbar.get(),tabcopydir[j]))
                    sleep(5)
                    j=j+1
                    for k in listview.get_children():
                        listview.delete(k)
                    for entry in os.listdir(statusbar.get()):
                        try:
                            path1=Path(statusbar.get()+"\\"+entry)
                            listview.insert(parent='',text=entry,values=path1)
                            
                        except OSError as error:
                            mb.showerror('Error',message=str(error))  
                    mb.showinfo("Copy Status","Your folder was copied") 
                    repopulate()               
                else:
                 shutil.copy2(i,statusbar.get())
                 sleep(5)
                 for k in listview.get_children():
                        listview.delete(k)
                 for entry in os.listdir(statusbar.get()):
                        try:
                            path1=Path(statusbar.get()+"\\"+entry)
                            listview.insert(parent='',text=entry,values=path1)
                            
                        except OSError as error:
                            mb.showerror('Error',message=str(error)) 
             sem.release() 
             mb.showinfo("Copy Status","Your file was copied")  
             tabcopydir.clear()
             tabcopy.clear()
        except IndexError:
            pass
            
    except PermissionError as error:
        mb.showwarning("Error",message="You can not paste")          
def paste2():
    try:
        try:             
            if len(tabcut)!=0:
             j=0
    
                   
             for i in tabcut:
                 while not sem.acquire(blocking=False):
                     mb.showinfo("Cut info","The cutting is not ready")
                     sleep(5)
                 else:    
                    if os.path.isdir(i):
                        shutil.rmtree(i)
                        copy_tree(i,os.path.join(statusbar.get(),tabcutdir[j]))
                        j=j+1
                        sleep(5)
                        for x in listview.get_children():
                            listview.delete(x)
                        for entry in os.listdir(statusbar.get()):
                           try:
                             path1=Path(statusbar.get()+"\\"+entry)
                             listview.insert(parent='',text=entry,values=path1)
                            
                           except OSError as error:
                            mb.showerror('Error',message=str(error))    
                     
                        mb.showinfo("Cut status","Cutting finished") 
                        repopulate()    
                    else :
                          os.remove(i)
                          shutil.copy2(i,statusbar.get())
                          sleep(5)
                          for x in listview.get_children():
                              listview.delete(x)
                          for entry in os.listdir(statusbar.get()):
                              try:
                                path1=Path(statusbar.get()+"\\"+entry)
                                listview.insert(parent='',text=entry,values=path1)
                            
                              except OSError as error:
                                mb.showerror('Error',message=str(error))    
                    
                    mb.showinfo("Cut status","Cutting finished")
             sleep(5)        
             repopulate()   
             tabcut.clear()
             tabcutdir.clear()
            sem.acquire()    

        except IndexError:
            pass
            
    except PermissionError as error:
        mb.showwarning("Error",message="You can not paste")
p1=threading.Thread(target=paste)
p2=threading.Thread(target=paste2) 
p1.start()
p2.start()
p1.join()
p2.join()

Edit.add_command(label="Paste",command=paste2)
Edit.add_command(label="Paste",command=paste)
def paste1(event):
    try:
        try:
            if len(tabcopy)!=0:
             j=0
             mb.showwarning("Warnig","Your file is still copy")
             
             for i in tabcopy:
                if os.path.isdir(i):
                    print(tabcopydir[j])
                    copy_tree(j,os.path.join(statusbar.get(),tabcopydir[j]))
                    
                    j=j+1
                    for k in listview.get_children():
                        listview.delete(k)
                    for entry in os.listdir(statusbar.get()):
                        try:
                            path1=Path(statusbar.get()+"\\"+entry)
                            listview.insert(parent='',text=entry,values=path1)
                            
                        except OSError as error:
                            mb.showerror('Error',message=str(error))  
                    mb.showinfo("Copy Status","Your folder was copied") 
                    repopulate()               
                else:
                 shutil.copy2(i,statusbar.get())
                 for k in listview.get_children():
                        listview.delete(k)
                 for entry in os.listdir(statusbar.get()):
                        try:
                            path1=Path(statusbar.get()+"\\"+entry)
                            listview.insert(parent='',text=entry,values=path1)
                            
                        except OSError as error:
                            mb.showerror('Error',message=str(error)) 
              
             mb.showinfo("Copy Status","Your file was copied")  
             tabcopydir.clear()
             tabcopy.clear()
            else:
             j=0
    
              
             mb.showinfo("Cut info","The cutting is ready")     
             for i in tabcut:
                if os.path.isdir(i):
                     shutil.rmtree(i)
                     copy_tree(i,os.path.join(statusbar.get(),tabcutdir[j]))
                     j=j+1
                     for x in listview.get_children():
                         listview.delete(x)
                     for entry in os.listdir(statusbar.get()):
                        try:
                            path1=Path(statusbar.get()+"\\"+entry)
                            listview.insert(parent='',text=entry,values=path1)
                            
                        except OSError as error:
                            mb.showerror('Error',message=str(error))    
                     
                     mb.showinfo("Cut status","Cutting finished") 
                     repopulate()    
                else :
                    os.remove(i)
                    shutil.copy2(i,statusbar.get())
                    for x in listview.get_children():
                        listview.delete(x)
                    for entry in os.listdir(statusbar.get()):
                        try:
                            path1=Path(statusbar.get()+"\\"+entry)
                            listview.insert(parent='',text=entry,values=path1)
                            
                        except OSError as error:
                            mb.showerror('Error',message=str(error))    
                    
                    mb.showinfo("Cut status","Cutting finished") 
                    repopulate()   
             tabcut.clear()
             tabcutdir.clear()
             

        except IndexError:
            pass
            
    except PermissionError as error:
        mb.showwarning("Error",message="You can not paste")
    repopulate()     
listview.bind('<Control-KeyPress-V>',paste1)
tabpath=[]
def undo():
    global tabpath
    x=tabpath.index(statusbar.get())
    undobutton.config(state=NORMAL)
    if x-1 >=0:
        v.set(tabpath[x-1])
        for i in listview.get_children():
            listview.delete(i)
        try:
                for name in os.listdir(statusbar.get()):
                    item_path=os.path.join(statusbar.get(),name)
                    ext=name.split(".")[-1]
                    if os.path.isdir(item_path):
                     try:
                        values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                        listview.insert(parent='', text=name, index="end", values=values1)

                     except PermissionError:
                        pass
                    else:
                     values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
                     listview.insert(parent='', text=name, index="end", values=values2)
                repopulate()
        except OSError as error:
              mb.showerror('Error',message=str(error))
        
    else:
        undobutton.config(state=DISABLED)
Edit.add_command(label="Undo",command=undo)
undobutton.config(command=undo) 
def redo():
      global tabpath
      x=tabpath.index(statusbar.get())
      redobutton.config(command=NORMAL) 
      if x+1 < len(tabpath):
          try:
              v.set(tabpath[x+1])
              for i in listview.get_children():
                  listview.delete(i)
              
              try:
                    for name in os.listdir(statusbar.get()) :
                      item_path = os.path.join(statusbar.get(),name)
                      ext = name.split(".")[-1]
                      if os.path.isdir(item_path):
                        try:
                          values1 = [time.ctime(os.path.getmtime(item_path)), 'Folder', '', item_path]
                          listview.insert(parent='', text=name, index="end", values=values1)

                        except PermissionError:
                         pass
                      else:
                         values2 = [time.ctime(os.path.getctime(item_path)), 'File '+ext, str(os.path.getsize(item_path)) + ' Octets', item_path]
                         listview.insert(parent='', text=name, index="end", values=values2)
                    repopulate()
              except OSError as error:
                   mb.showerror('Error',message=str(error))
          except IndexError:
               pass 
              
      else:
            redobutton.config(command=DISABLED) 
Edit.add_command(label="Redo",command=redo)
undobutton.config(command=redo)                         
def about():
    mb.showinfo("About the application",message="This application is an example of a file manager configured as Window file manager\n It was written in Python 3.8.5 ")
About.add_command(label="About",command=about)
def searcfunc():
    s=searchbar.get()
    d=statusbar.get()
    o=[]
    if s :
        if d:
            for root,dirs, files in os.walk(d):
                for i in dirs:
                    if s in i:
                        o.append(os.path.join(root,i))
                for f in files:
                    if s in f:
                        o.append(os.path.join(root,f))
            for x in listview.get_children():
                listview.delete(x)
            for path in o:
                values=[]
                if os.path.isdir(path):
                    valtype="Folder"
                   
                else:
                    valtype="File"
                valname=os.path.basename(path)
                valsize=os.path.getsize(path)
                valtime=time.asctime(time.localtime(os.path.getmtime(path)))
                valpath=path
                values.append(valname)
                values.append(valtime)
                values.append(valtype)
                values.append(valsize)
                
                values.append(valpath)
                listview.insert("",'end',text=valname,values=values,open=False)
searchbut.config(command=searcfunc)




contextual=Menu(window,tearoff=0)
contextual.add_command(label="Cut",command=cut)
contextual.add_separator()
contextual.add_command(label="Copy",command=copy)
contextual.add_separator()
contextual.add_command(label="Paste",command=paste)
contextual.add_separator()
contextual.add_command(label="Rename",command=rename)
contextual.add_separator()
contextual.add_command(label="Delete",command=delete)
contextual.add_separator()
contextual.add_command(label="New Folder",command=folder)
contextual.add_separator()
contextual.add_command(label="Compress",command=compress)
contextual.add_separator()
contextual.add_command(label="Decompress",command=decompress)
def context(r):
 contextual.tk_popup(window.winfo_pointerx(),window.winfo_pointery())
listview.bind('<Button-3>',context)










tv1.bind('<<TreeviewOpen>>', new_folder)
tv1.grid(row=1, column=0, sticky='nsew')
ybar1.grid(row=1, column=1, sticky='nsew')



listview.grid(row=1, column=2, columnspan=5, sticky='nsew')
listview.bind('<<TreeviewOpen>>', peuplerlistview)
listview.bind('<<Double-button>>')
listview.bind('<<TreeviewSelect>>')
ybar2.grid(row=1, column=7, sticky='nsew')

left_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nw')

window.mainloop()
