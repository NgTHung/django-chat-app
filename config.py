import mysql.connector as mysql

conn = mysql.connect(user="root",host="localhost",database='bbq',password="tuanhungag1")
cur = conn.cursor()

def getusr():
    global cur
    cur.execute("select id,username from login_usid;")
    for (id,username) in cur:
        print(id,' ',username)

def getmes():
    global cur
    cur.execute("select * from login_message;")
    for (id,sender,receiver,messages) in cur:
        print(id,' ',sender,' ',receiver,' ',messages)

def getfriend():
    global cur
    cur.execute("select * from login_friends;")
    for (id,requester,friend_list) in cur:
        print(id,' ',requester,' ',friend_list)

def remusr():
    global cur
    inp = input("Who you want to remove:")
    cur.execute("select id,username from login_usid;")
    for (id,username) in cur:
        if username == inp:
            a = cur.fetchall()
            cur.execute("delete from login_usid where username='"+inp+"'")
            cur.execute("delete from login_midroom where first_person='"+(inp)+"';")
            cur.execute("delete from login_midroom where second_person='"+inp+"';")
            cur.execute("delete from login_friends where requester='"+inp+"';")
            cur.execute("select * from login_friends;")
            for (id,requester,friend_list) in cur:
                cur.execute("update login_friends set friend_list='"+friend_list.replace(inp,'')+"' where id=",id,";")
            break
        #conn.commit()
    print('Finish!')
    
def addusr():
    pass

def remmes():
    global cur
    getmes()
    inp = input("select id of message you are going to delete:")
    cur.execute("delete from login_message where '()'")
        

while (True):
    i = get()
    match i:
        case 0:
            break
        case 1:
            getusr()
        case 2:
            getmes()
        case 3:
            getfriend()
        case 4:
            remusr()
        case 5:
            remmes()
		case _:
            continue
                
input("Good bye!")
cur.close()
conn.close()
