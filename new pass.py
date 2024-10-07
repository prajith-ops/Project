import tkinter as T
from functools import partial
import random 
import mysql.connector as ms
from cryptography.fernet import Fernet

# Your encryption key, make sure to keep it secure
encryption_key = b'your_encryption_key_here'

# Function to encrypt data
def encrypt_data(data):
    cipher_suite = Fernet(encryption_key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data):
    cipher_suite = Fernet(encryption_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

mycon=ms.connect(host='localhost',database='password_manager',user='root',password='pass123')
mycursor=mycon.cursor()
userlist=[]
s="show tables"
mycursor.execute(s)
mydata=mycursor.fetchall()
for i, in mydata :
    userlist.append(i)
    
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k','l','m', 'n', 'o', 'p','q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z'] 
UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'l','M', 'N', 'O', 'p', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z'] 
SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~','*'] 
    
def login(window):

    def login_database():
            
        def add_rec(option_win):
            def addition():
                c0 = j0.get()
                c1 = j1.get()
                c2 = encrypt_data(j2.get())  # Encrypt the password
                sql = "insert into %s(application,username,password) values('%s','%s','%s')" % (v, c0, c1, c2)
                mycursor.execute(sql)
                mycon.commit()
                p1.destroy()
                a1 = T.Label(addition_win, text="RECORD ADDED", font=("Times", 30), bg="cyan2")
                a1.grid(row=11, column=3, padx=10, pady=20)

            
            option_win.destroy()
            addition_win=T.Tk()
            addition_win.configure(bg='cyan2')
            addition_win.geometry("1366x768")
            a0=T.Label(addition_win, text="Enter application name",width=20,font=("Times", 30))
            a0.grid(row=1,column=1, padx=10, pady=20)
            a1=T.Label(addition_win, text="Enter username to add",width=20,font=("Times", 30))
            a1.grid(row=5,column=1, padx=10, pady=20)
            a2=T.Label(addition_win, text="Enter password to add",width=20,font=("Times", 30))
            a2.grid(row=9,column=1, padx=10, pady=20)
            app_add=T.StringVar()
            j0=T.Entry(addition_win,textvariable=app_add,width=30,font=("Times", 15))
            j0.grid(row=1,column=3, padx=10, pady=20)
            user_add=T.StringVar()
            j1=T.Entry(addition_win,textvariable=user_add,width=30,font=("Times", 15))
            j1.grid(row=5,column=3, padx=10, pady=20)
            password_add=T.StringVar()
            j2=T.Entry(addition_win,textvariable=password_add,width=30,font=("Times", 15))
            j2.grid(row=9,column=3, padx=10, pady=20)
            p1=T.Button(addition_win,text="SAVE DETAILS", font=("Times", 25),width=25,command=addition)
            p1.grid(row=11,column=3, padx=10, pady=20)
            gap=T.Label(addition_win, text="",font=("Times", 55), fg="cyan2", bg="cyan2")
            gap.grid(row=12,column=3, padx=10, pady=20)
            bu1=T.Button(addition_win,text="SHOW RECORDS", font=("Times", 20),width=25,command=partial(show_rec,addition_win))
            bu1.grid(row=13,column=1, padx=10, pady=20)
            bu2=T.Button(addition_win,text="ADD MORE", font=("Times", 20),width=25,command=partial(add_rec,addition_win))
            bu2.grid(row=13,column=3, padx=10, pady=20)
            bu3=T.Button(addition_win,text="GENERATE PASSWORD", font=("Times", 20),width=30,command=partial(password_generator,addition_win))
            bu3.grid(row=13,column=4, padx=10, pady=20)

        def show_rec(option_win):
            option_win.destroy()
            show_win=T.Tk()
            show_win.configure(bg='cyan2')
            show_win.geometry("1366x768")
            q="select * from %s"%(v)
            mycursor.execute(q)
            mydata2=mycursor.fetchall()
            try:
                f=250//len(mydata2)
                w=24
                if f>20:
                    f,w=25,10
                gp=T.Label(show_win,text="", font=("Times", 20),width=w,fg="cyan2", bg="cyan2")
                gp.grid(row=1,column=1, padx=10, pady=20)
                tb=T.Label(show_win,text="APPLICATION", font=("Times", f),width=20,bg="grey79",borderwidth = 3,relief="sunken")
                tb.grid(row=2,column=3)
                tb=T.Label(show_win,text="USERNAME", font=("Times", f),width=20,bg="grey79",borderwidth = 3,relief="sunken")
                tb.grid(row=2,column=4)
                tb=T.Label(show_win,text="PASSWORD", font=("Times", f),width=20,bg="grey79",borderwidth = 3,relief="sunken")
                tb.grid(row=2,column=5)
                n=2
                for i in mydata2 :
                    n=n+1
                    k=2
                    for j in i:
                           
                        k=k+1
                        if k == 5:  # Decrypting password before displaying
                            j = decrypt_data(j.encode())
                        tb=T.Label(show_win,text=j, font=("Times", f),width=20,borderwidth = 3,relief="sunken")
                        tb.grid(row=n,column=k)
            except :
                f=30
                a1=T.Label(show_win, text="NO RECORDS YET ",font=("Times", 35),bg="cyan2")
                a1.grid(row=1,column=4,padx=20, pady=20)
                
            bu2=T.Button(show_win,text="ADD RECORD", font=("Times", f),width=20,command=partial(add_rec,show_win))
            bu2.grid(row=50,column=3, pady=20)
            bu3=T.Button(show_win,text="GENERATE PASSWORD", font=("Times", f),width=20,command=partial(password_generator,show_win))
            bu3.grid(row=50,column=5, pady=20)
            
        def password_generator(option_win):
            def generation():
                U=int(j0.get())
                l=int(j1.get())
                n=int(j2.get())
                s=int(j3.get())
                pass_win.destroy()
    
                rand_upper=""
                for i in range(U):
                    rand_upper = rand_upper + random.choice(UPCASE_CHARACTERS)

                rand_lower=""
                for i in range(l):
                    rand_lower = rand_lower + random.choice(LOCASE_CHARACTERS)

                rand_symbol=""
                for i in range(s):
                    rand_symbol = rand_symbol + random.choice(SYMBOLS) 
    
                rand_digit=""
                for i in range(n):
                    rand_digit = rand_digit + random.choice(DIGITS)
    

                temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
                temp_pass2 = list(temp_pass)
                random.shuffle(temp_pass2)
                password = "".join(temp_pass2)

                gen_win=T.Tk()
                gen_win.configure(bg='cyan2')
                gen_win.geometry("1366x768")
                Label1=T.Label(gen_win, text="Here is your password ",font=("Times", 55), fg="blue", bg="cyan2")
                Label1.grid(row=2,column=2)
                if len(password)<12:
                    Label2=T.Label(gen_win, text= password ,font=("Times", 55), fg="tomato", bg="cyan2")
                    Label2.grid(row=3,column=2, padx=10, pady=20)
                else:   
                    Label2=T.Label(gen_win, text= password ,font=("Times", 30), fg="tomato", bg="cyan2")
                    Label2.grid(row=3,column=2, padx=10, pady=20)
                bu1=T.Button(gen_win,text="SHOW RECORDS", font=("Times", 20),width=25,command=partial(show_rec,gen_win))
                bu1.grid(row=20,column=1)
                bu2=T.Button(gen_win,text="ADD RECORD", font=("Times", 20),width=25,command=partial(add_rec,gen_win))
                bu2.grid(row=20,column=2)
                bu3=T.Button(gen_win,text="GENERATE ANOTHER PASSWORD", font=("Times", 20),width=30,command=partial(password_generator,gen_win))
                bu3.grid(row=20,column=3)
        
            option_win.destroy()
            pass_win=T.Tk()
            pass_win.configure(bg='cyan2')
            pass_win.geometry("1366x768")
            a0=T.Label(pass_win, text="Enter the no of uppercase character needed",width=35,font=("Times", 30))
            a0.grid(row=1,column=1, padx=10, pady=20)
            a1=T.Label(pass_win, text="Enter the no of lowercase character needed",width=35,font=("Times", 30))
            a1.grid(row=5,column=1, padx=10, pady=20)
            a2=T.Label(pass_win, text="Enter the no of digits needed",width=35,font=("Times", 30))
            a2.grid(row=9,column=1, padx=10, pady=20)
            a3=T.Label(pass_win, text="Enter the no of symbols needed",width=35,font=("Times", 30))
            a3.grid(row=13,column=1, padx=10, pady=20)
            up_add=T.StringVar()
            j0=T.Entry(pass_win,textvariable=up_add,width=30,font=("Times", 15))
            j0.grid(row=1,column=3, padx=10, pady=20)
            low_add=T.StringVar()
            j1=T.Entry(pass_win,textvariable=low_add,width=30,font=("Times", 15))
            j1.grid(row=5,column=3, padx=10, pady=20)
            digit_add=T.StringVar()
            j2=T.Entry(pass_win,textvariable=digit_add,width=30,font=("Times", 15))
            j2.grid(row=9,column=3, padx=10, pady=20)
            symbol_add=T.StringVar()
            j3=T.Entry(pass_win,textvariable=symbol_add,width=30,font=("Times", 15))
            j3.grid(row=13,column=3, padx=10, pady=20)
            p1=T.Button(pass_win,text="NEXT", font=("Times", 30),width=25,command=generation)
            p1.grid(row=15,column=3, padx=10, pady=20)

            
        v1=e1.get()
        v2=e2.get()
        v=v1+v2
        
        if v.lower() in userlist :
            login_win.destroy()
            option_win=T.Tk()
            option_win.configure(bg='cyan2')
            option_win.geometry("1366x768")
            gp=T.Label(option_win,text="", font=("Times", 20),width=15,fg="cyan2", bg="cyan2")
            gp.grid(row=1,column=1, padx=10, pady=20)
            bu1=T.Button(option_win,text="SHOW RECORDS", font=("Times", 35),width=35,command=partial(show_rec,option_win))
            bu1.grid(row=2,column=2, padx=10, pady=20)
            bu2=T.Button(option_win,text="ADD RECORD", font=("Times", 35),width=35,command=partial(add_rec,option_win))
            bu2.grid(row=3,column=2, padx=10, pady=20)
            bu3=T.Button(option_win,text="GENERATE PASSWORD", font=("Times", 35),width=35,command=partial(password_generator,option_win))
            bu3.grid(row=4,column=2, padx=10, pady=20)
            
            
        else :
            a1=T.Label(login_win, text="NO SUCH ACCOUNT ",font=("Times", 30),bg="cyan2")
            a1.grid(row=20,column=3)
            
            
        
    window.destroy()
    login_win=T.Tk()
    login_win.configure(bg='cyan2')
    login_win.geometry("1366x768")
    s1=T.Label(login_win, text="username",width=20,font=("Times", 40))
    s1.grid(row=1,column=2, padx=10, pady=20)
    s2=T.Label(login_win, text="password",width=20,font=("Times", 40))
    s2.grid(row=5,column=2, padx=10, pady=20)

    user_in=T.StringVar()
    e1=T.Entry(login_win,textvariable=user_in,width=30,font=("Times", 20))
    e1.grid(row=1,column=3, padx=10, pady=20)
    password_in=T.StringVar()
    e2=T.Entry(login_win,textvariable=password_in,width=30,font=("Times", 20))
    e2.grid(row=5,column=3, padx=10, pady=20)
    p1=T.Button(login_win,text="LOGIN", font=("Times", 30),width=25,command=login_database)
    p1.grid(row=12,column=3, padx=10, pady=20)
    
def signup():
    
    def signup_database():
        v1=e1.get()
        v2=e2.get()
        v3=e3.get()
        v=v1+v2

        if v2!=v3:
            try:
                h1.destroy()
            except:
                h2=T.Label(signup_win, text="PASSWORDS DOES NOT  MATCH",font=("Times", 20), fg="blue", bg="cyan2")
                h2.grid(row=20,column=3, padx=10, pady=20)
        elif v.lower() in userlist :
            try:
                h2.destroy()
            except:
                h1=T.Label(signup_win, text="USERNAME  ALREADY  EXISTS ",font=("Times", 20), fg="blue", bg="cyan2")
                h1.grid(row=20,column=3, padx=10, pady=20)
        else: 
            sql="create table %s(application varchar(100),username varchar(100), password varchar(100))"%(v)
            mycursor.execute(sql)
            mycon.commit()
            userlist.append(v.lower())
            h1=T.Label(signup_win, text="ACCOUNT CREATED",font=("Times", 30), fg="blue", bg="cyan2")
            h1.grid(row=20,column=3, padx=10, pady=20)
            login(signup_win)
            
        
        
    
    window.destroy()
    signup_win=T.Tk()
    signup_win.configure(bg='cyan2')
    signup_win.geometry("1366x768")
    s1=T.Label(signup_win, text="Enter your username",width=25,font=("Times", 40))
    s1.grid(row=1,column=2, padx=10, pady=20)
    s2=T.Label(signup_win, text="Enter your password",width=25,font=("Times", 40))
    s2.grid(row=5,column=2, padx=10, pady=20)
    s3=T.Label(signup_win, text="Confirm your password",width=25,font=("Times", 40))
    s3.grid(row=9,column=2, padx=10, pady=20)
    
    user_in=T.StringVar()
    e1=T.Entry(signup_win,textvariable=user_in,width=30,font=("Times", 20))
    e1.grid(row=1,column=3, padx=10, pady=20)
    pass1_in=T.StringVar()
    e2=T.Entry(signup_win,textvariable=pass1_in,width=30,font=("Times", 20))
    e2.grid(row=5,column=3, padx=10, pady=20)
    pass2_in=T.StringVar()
    e3=T.Entry(signup_win,textvariable=pass2_in,width=30,font=("Times", 20))
    e3.grid(row=9,column=3, padx=10, pady=20)
    p1=T.Button(signup_win,text="NEXT", font=("Times", 30),width=25,command=signup_database)
    p1.grid(row=12,column=3, padx=10, pady=20)
    



window=T.Tk()
window.configure(bg='cyan2')
window.title("PASSWORD MANAGER AND GENERATOR")
window.geometry("1366x768")
gp=T.Label(window,text="", font=("Times", 20),width=15,fg="cyan2", bg="cyan2")
gp.grid(row=1,column=1, padx=10, pady=20)
l1=T.Label(window, text="It's all safe here",font=("Times", 55), fg="blue", bg="cyan2")
l1.grid(row=1,column=2,columnspan=40, padx=10, pady=20)
b1=T.Button(window,text="SIGNUP", font=("Times", 35),width=35,command=signup)
b1.grid(row=2,column=2, padx=10, pady=25)
b2=T.Button(window,text="LOGIN", font=("Times", 35),width=35,command=partial(login,window))
b2.grid(row=3,column=2, padx=10, pady=25)
window.mainloop()
