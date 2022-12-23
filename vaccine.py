import mysql.connector
import os
from twilio.rest import Client

account_sid = '--'
auth_token = '--'
client = Client(account_sid, auth_token)


def sendsms(mob, text):
    mob = "+91"+mob
    message = client.messages \
                    .create(
                        body=text,
                        from_='+13863392802',
                        to=mob
                    )

    print("Message Send:"+message.sid)


username = "ABCDE"
password = "995511995511"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="995511995511",
    database="vaccine"
)
cur = mydb.cursor(buffered=True)
cur.execute("select* from vaccine")

hospitalid = 1
parentid = 1


def display():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Start Page".rjust(100))
    print("")
    print("Enter 1 for hospital Section")
    print("Enter 2 for Parent Section")
    print("")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    print("")
    ch = int(input("Enter your Choice: "))
    if (ch == 1):
        hospitalsection()
    elif (ch == 2):
        parentsection()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!".center(100))
        print()
        display()


def hospitalsection():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Hospital Page".rjust(100))
    print("")
    print("Enter 1 for hospital Login")
    print("Enter 2 for hospital Signup")
    print("")
    print("Enter 9 for Back")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    print("")
    ch = int(input("Enter your Choice: "))
    if (ch == 1):
        hospitallogin()
    elif (ch == 2):
        hospitalsignup()
    elif (ch == 9):
        display()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!".center(100))
        print()
        display()


def hospitalsignup():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Hospital Sign Up Page".rjust(100))
    print("")
    hname = input("Enter Hospital Name:")
    hmob = input("Enter Hospital Mobile(10 digit):")
    haddress = input("Enter Hospital Address:")
    hpassword = input("Enter Hospital Password:")
    try:
        cur.execute("select count(hid) from hospital")
        hid = 0
        for i in cur:
            hid += i[0]+1

        sql = "INSERT INTO hospital (hid,hname,hmob, haddress,hpassword) VALUES (%s, %s,%s,%s,%s)"
        val = (hid, hname, hmob, haddress, hpassword)
        cur.execute(sql, val)
        mydb.commit()
        print("")
        print("Your Hospital ID is:", hid)
        global hospitalid
        hospitalid = hid
        text = "Your Acccount is Created at Vaccine Management System with Name: " + \
            str(hname)+"\nHId: "+str(hid)+"\npassword="+str(hpassword)
        mob = str(hmob)
        sendsms(mob, text)
        hospitaldashboard()
    except Exception as e:
        print(e)
        print("Enter Correct Details!!!")
        # print()
        # print("-" * 100)
        # hospitalsection()


def hospitallogin():
    print("-" * 100)
    print("Vaccine Management System".center(100))
    print("")
    print("Hospital Login Page".rjust(100))
    print("")
    hid = input("Enter Hospital ID:")
    hpassword = input("Enter Hospital Password:")
    res = cur.execute("select hpassword from hospital where hid="+hid)
    res = cur.fetchone()
    hpass = res[0]
    if (hpassword == hpass):
        global hospitalid
        hospitalid = hid
        hospitaldashboard()
    else:
        print("Enter Correct ID and Password")
        print()
        print("-" * 100)
        hospitalsection()


def hospitaldashboard():
    print("-" * 100)
    print("Vaccine Management System".center(100))
    print("")
    print("Hospital Dashboard".rjust(100))
    print("")
    print("Press 1 for approve vaccine Requests")
    print("Press 2 for Update Vaccine Status")
    print("Press 3 for show recent vaccination")
    print("Press 9 for Back")
    print("Press 0 for Exit")
    print()
    print("-" * 100)
    ch = int(input("Enter your choice :"))
    if (ch == 1):
        approvevaccine()
    elif (ch == 2):
        updatestatus()
    elif (ch == 3):
        recentvaccination()
    elif (ch == 9):
        hospitalsection()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice")


def approvevaccine():
    global hospitalid
    print("-" * 100)
    print("Vaccine Management System".center(100))
    print("")
    print("Pending Vaccine Requests".rjust(100))
    print("")
    cur.execute("select status.sid,child.cname,child.cdob,parent.pmob,vaccine.vname from status inner join child on child.cid=status.cid inner join vaccine on vaccine.vid=status.vid inner join parent on parent.pid=status.ppid where status.hid=" +
                str(hospitalid)+" and status.status='Wait for Response'")
    print("Child List:")
    print("-"*106)
    print("|{sid}|{cname}|{cdob}|{pmob}|{vname}|".format(sid="Status Id".center(
        15), cname="Child Name".center(40), cdob="DOB".center(15), pmob="Mobile No.".center(12), vname="Vaccine".center(20)))
    print("-"*106)
    l = 0
    for i in cur:
        print("|{sid}|{cname}|{cdob}|{pmob}|{vname}|".format(sid=str(i[0]).center(
            15), cname=i[1].center(40), cdob=str(i[2]).center(15), pmob=i[3].center(12), vname=i[4].center(20)))
        l += 1
        print("-"*106)
    print("\n\n")
    print("-" * 100)
    if (l == 0):
        print("No Data")
        hospitaldashboard()
    sid = input("Enter Status id for approve :")
    doa = input("Enter Date for Appointment(YYYY-MM-DD):")
    sql = "update status set doa=%s, status=%s where sid=%s"
    val = (doa, "approved", sid)
    try:
        cur.execute(sql, val)
        mydb.commit()
        print("Status Approved!")
        print()
        print("-" * 100)
        cur.execute("select hospital.hname ,child.cname, vaccine.vname, parent.pmob from status inner join child on child.cid=status.cid inner join vaccine on vaccine.vid=status.vid inner join parent on parent.pid=status.ppid inner join hospital on hospital.hid=status.hid where status.sid="+str(sid))
        hname = ""
        cname = ""
        vname = ""
        pmob = ""
        for i in cur:
            hname = i[0]
            cname = i[1]
            vname = i[2]
            pmob = i[3]
        text = hname+" is accepted request for status id: " + \
            str(sid)+"\n"+"child: "+cname+"\n"+"vaccine: " + \
            vname+"\nDate of Appointment: "+str(doa)
        mob = str(pmob)
        sendsms(mob, text)
        hospitaldashboard()
    except Exception as e:
        print(e)
        print("Enter Correct Details")
    hospitaldashboard()


def updatestatus():
    global hospitalid
    print("-" * 100)
    print("Vaccine Management System".center(100))
    print("")
    print("Update Vaccine Status".rjust(100))
    print("")
    cur.execute("select status.sid,doa,child.cname,child.cdob,parent.pmob,vaccine.vname from status inner join child on child.cid=status.cid inner join vaccine on vaccine.vid=status.vid inner join parent on parent.pid=status.ppid where status.hid=" +
                str(hospitalid)+" and status.status='Approved'")
    print("Child List:")
    print("-"*121)
    print("|{sid}|{doa}|{cname}|{cdob}|{pmob}|{vname}|".format(sid="Status Id".center(
        15), doa="Date of App.".center(15), cname="Child Name".center(40), cdob="DOB".center(15), pmob="Mobile No.".center(12), vname="Vaccine".center(20)))
    print("-"*121)
    l = 0
    for i in cur:
        print("|{sid}|{doa}|{cname}|{cdob}|{pmob}|{vname}|".format(sid=str(i[0]).center(
            15), doa=str(i[1]).center(15), cname=str(i[2]).center(40), cdob=str(i[3]).center(15), pmob=str(i[4]).center(12), vname=str(i[5]).center(20)))
        print("-"*121)
        l += 1
    print("\n\n")
    print("-" * 100)
    if (l == 0):
        print("No Data")
        hospitaldashboard()
    sid = input("Enter Status id for Complete the vaccination process:")
    sql = "update status set status=%s where sid=%s"
    val = ("vaccinated", sid)
    try:
        cur.execute(sql, val)
        mydb.commit()
        print("Child is Vaccinated")
        print()
        print("-" * 100)
        cur.execute("select hospital.hname ,child.cname, vaccine.vname, parent.pmob from status inner join child on child.cid=status.cid inner join vaccine on vaccine.vid=status.vid inner join parent on parent.pid=status.ppid inner join hospital on hospital.hid=status.hid where status.sid="+str(sid))
        hname = ""
        cname = ""
        vname = ""
        pmob = ""
        for i in cur:
            hname = i[0]
            cname = i[1]
            vname = i[2]
            pmob = i[3]
        text = str(cname)+" with status id: "+str(sid) + \
            " is vaccinated for "+vname+" at "+hname
        mob = str(pmob)
        sendsms(mob, text)

    except:
        print("Enter correct Status ID")
    hospitaldashboard()


def recentvaccination():
    global hospitalid
    print("-" * 100)
    print("Vaccine Management System".center(100))
    print("")
    print("Recent Vaccination".rjust(100))
    print("")
    cur.execute("select status.sid,child.cname,child.cdob,parent.pmob,vaccine.vname from status inner join child on child.cid=status.cid inner join vaccine on vaccine.vid=status.vid inner join parent on parent.pid=status.ppid where status.hid=" +
                str(hospitalid)+" and status.status='vaccinated'")
    print("Child List:")
    print("-"*106)
    print("|{sid}|{cname}|{cdob}|{pmob}|{vname}|".format(sid="Status Id".center(
        15), cname="Child Name".center(40), cdob="DOB".center(15), pmob="Mobile No.".center(12), vname="Vaccine".center(20)))
    print("-"*106)
    l = 0
    for i in cur:
        print("|{sid}|{cname}|{cdob}|{pmob}|{vname}|".format(sid=str(i[0]).center(
            15), cname=i[1].center(40), cdob=str(i[2]).center(15), pmob=i[3].center(12), vname=i[4].center(20)))
        print("-"*106)
        l += 1
    if (l == 0):
        print()
        print("No Data")
        hospitaldashboard()
    print("\n\n")
    print("-" * 100)
    print("Enter 0 for Exit")
    print("Enter 9 for Back")
    ch = int(input("Enter your Choice: "))
    if (ch == 9):

        hospitaldashboard()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!")
        recentvaccination()


def parentsection():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Parent Page".rjust(100))
    print("")
    print("Enter 1 for Parent Login")
    print("Enter 2 for Parent Signup")
    print("")
    print("Enter 9 for Back")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    print("")
    ch = int(input("Enter your Choice: "))
    if (ch == 1):
        parentlogin()
    elif (ch == 2):
        parentsignup()
    elif (ch == 9):
        display()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!".center(100))
        print()
        display()


def parentsignup():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Parent Sign Up Page".rjust(100))
    print("")
    pname = input("Enter Parent Name:")
    pmob = input("Enter Parent Mobile:")
    padhaar = input("Enter Parent Adhaar No:")
    paddress = input("Enter Parent Address:")
    ppassword = input("Enter Parent Password:")

    try:
        cur.execute("select count(pid) from parent")
        pid = 0
        for i in cur:
            pid += i[0]+1

        sql = "INSERT INTO parent (pid,pname,pmob,padhaar, paddress,ppassword) VALUES (%s,%s, %s,%s,%s,%s)"
        val = (pid, pname, pmob, padhaar, paddress, ppassword)
        cur.execute(sql, val)
        mydb.commit()
        print("")
        print("Your Parent ID is:", pid)
        global parentid
        parentid = pid
        text = "Your account is created at vaccine management system with\nParent ID: " + \
            str(pid)+"\nPassword: "+str(ppassword)+"\n"
        mob = str(pmob)
        sendsms(mob, text)
        parentprofile()
    except:
        print("Enter Correct Details!!!")
        print()
        print("-" * 100)
        parentsection()


def parentlogin():
    pid = input("Enter Parent ID:")
    ppassword = input("Enter Parent Password:")
    res = cur.execute("select ppassword from parent where pid="+pid)
    res = cur.fetchone()
    hpass = res[0]
    if (ppassword == hpass):
        global parentid
        parentid = pid
        parentprofile()
    else:
        print("Enter Correct ID and Password")
        print()
        print("-" * 100)
        parentsection()


def parentprofile():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Parent Profile".rjust(100))
    print("")
    print("Enter 1 for Parent Details")
    print("Enter 2 for child Details")
    print("Enter 3 for Add child")
    print("Enter 4 for Book Appointment")
    print("Enter 5 for Appointment Status")
    print("")
    print("Enter 9 for Back")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    ch = int(input("Enter your Choice: "))
    if (ch == 1):
        parentdetail()
    elif (ch == 2):
        childdetail()
    elif (ch == 3):
        addchild()
    elif (ch == 4):
        bookappointment()
    elif (ch == 5):
        appointmentstatus()
    elif (ch == 9):
        parentsection()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!".center(100))
        print()
        parentprofile()


def parentdetail():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Parent Details".rjust(100))
    print("")
    cur.execute(
        "select pname,pid,pmob,padhaar,paddress from parent where pid="+str(parentid))
    for i in cur:
        print(("ParentName:{pname}".format(pname=i[0]).ljust(
            50)), ("ParentID:{pid}".format(pid=i[1])))
        print(("Parent Mob:{pmob}".format(pmob=i[2]).ljust(
            50)), ("Parent Adhaar:{padhaar}".format(padhaar=i[3])))
        print(("Parent Adress:{paddress}".format(paddress=i[4]).ljust(50)))
        print("")
    print("Enter 9 for Back")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    ch = int(input("Enter your Choice: "))
    if (ch == 9):
        parentprofile()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!".center(100))
        print()
        parentdetail()


def addchild():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Add Child Page".rjust(100))
    print("")
    cur.execute("select count(cid) from child")
    cid = 0
    for i in cur:
        cid += i[0]+1
    print()
    cname = input("Enter Child Name: ")
    cadhaar = input("Enter Child Adhaar: ")
    cdob = input("Enter DOB YYYY-MM-DD: ")
    cgender = input("Enter Gender M/F/T: ")
    try:
        sql = "INSERT INTO child (cid,pid,cname, cadhaar,cdob,cgender) VALUES (%s,%s, %s,%s,%s,%s)"
        val = (cid, parentid, cname, cadhaar, cdob, cgender)
        cur.execute(sql, val)
        mydb.commit()
        cur.execute("select pmob from parent where pid="+str(parentid))
        pmob = ""
        for i in cur:
            pmob = i[0]
        print("")
        print("New Child Added in Your Profile!!! Now Check to child Details".center(100))
        print("")
        text = "Congratulations! New Child added to your Profile with\nChild ID: {cid}\n Child name: {cname}\nGender: {cgender}\ndob: {cdob}\n adhaar: {cadhaar}\n".format(
            cid=cid, cname=cname, cgender=cgender, cdob=cdob, cadhaar=cadhaar)
        mob = pmob
        sendsms(mob, text)

    except:
        print("\n\n")
        print("Please Enter Data in correct Format".center(100))
        print("\n\n")

    parentprofile()


def childdetail():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Child Details".rjust(100))
    print("")
    cur.execute(
        "select cid,cname,cdob,cgender,cadhaar from child where pid="+str(parentid))
    print("Child List:")
    print("-"*106)
    print("|{cid}|{cname}|{cdob}|{cgender}|{cadhaar}|".format(cid="Child Id".center(
        15), cname="Child Name".center(40), cdob="DOB".center(15), cgender="Gender".center(10), cadhaar="Adhaar".center(20)))
    print("-"*106)
    l = 0
    for i in cur:
        print("|{cid}|{cname}|{cdob}|{cgender}|{cadhaar}|".format(cid=str(i[0]).center(
            15), cname=i[1].center(40), cdob=str(i[2]).center(15), cgender=i[3].center(10), cadhaar=i[4].center(20)))
        print("-"*106)
        l += 1
    print("\n\n")
    if (l == 0):
        print("No Child !!!")
    print("")
    print("Enter 9 for Back")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    ch = int(input("Enter your Choice: "))
    if (ch == 9):
        parentprofile()
    elif (ch == 0):
        exit()
    else:
        print("Enter Correct Choice!!!".center(100))
        print()
        childdetail()


def bookappointment():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("")
    print("Book Appointment".rjust(100))

    print("Hospital List:")
    print("-"*38)
    print("|{hid}|{hname}|".format(hid="Hospital Id".center(
        15), hname="Hospital Name".center(20)))
    print("-"*38)
    cur.execute("select hid,hname from hospital")
    for i in cur:
        print("|{hid}|{hname}|".format(
            hid=str(i[0]).center(15), hname=i[1].center(20)))
        print("-"*38)
    print("\n\n")

    print("Vaccine List:")
    print("-"*38)
    print("|{vid}|{vname}|".format(vid="Vaccine Id".center(
        15), vname="Vaccine Name".center(20)))
    print("-"*38)
    cur.execute("select vid,vname from vaccine")
    for i in cur:
        print("|{vid}|{vname}|".format(
            vid=str(i[0]).center(15), vname=i[1].center(20)))
        print("-"*38)
    print("\n\n")
    cur.execute("select cid,cname from child where pid="+str(parentid))
    print("Child List:")
    print("-"*38)
    print("|{vid}|{vname}|".format(vid="Child Id".center(
        15), vname="Child Name".center(20)))
    print("-"*38)
    l = 0
    for i in cur:
        print("|{cid}|{cname}|".format(
            cid=str(i[0]).center(15), cname=i[1].center(20)))
        l += 1
        print("-"*38)
    print("\n\n")
    if (l == 0):
        print("No Child!!!")
        parentprofile()
    cid = input("Enter Child Id for vaccine:")
    vid = input("Enter Vaccine ID:")
    hid = input("Enter hospital ID:")
    ch = input("Enter + for Add confirm: ")

    cur.execute("select count(sid) from status")
    sid = 0
    for i in cur:
        sid += i[0]+1
    if (ch == "+"):
        try:
            sql = "INSERT INTO status (cid,vid,sid,hid,status,ppid) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (cid, vid, sid, hid, "Wait for Response", str(parentid))
            cur.execute(sql, val)
            mydb.commit()
            print("Appointment for vaccine is processing.. Go to Appointment Status")
            print()
            cur.execute("select child.cid,child.cname,vaccine.vname,hospital.hname,parent.pmob from status inner join child on child.cid = status.cid inner join vaccine on vaccine.vid=status.vid inner join hospital on hospital.hid=status.hid inner join parent on parent.pid=status.ppid where sid="+str(sid))
            pmob = ""
            for i in cur:
                cname = i[1]
                vname = i[2]
                hname = i[3]
                pmob = i[4]
            text = "New Appointment Booked with\nChildId: {cid}\nchild name: {cname}\nVaccine: {vname}\nHospital: {hname}\nStatusID: {sid}\n".format(
                cid=cid, cname=cname, vname=vname, hname=hname, sid=sid)
            sendsms(pmob, text)
            parentprofile()
        except:
            print("\n\n")
            print("Enter Correct Details")
            print("\n\n")
            parentprofile()
    else:

        print("")
        print("Enter 9 for Back")
        print("Enter 0 for Exit")
        print("")
        print("-"*100)


def appointmentstatus():
    print("-"*100)
    print("Vaccine Management System".center(100))
    print("Appointment Status".rjust(100))
    print("\n")
    cur.execute("SELECT status.sid,child.cname,vaccine.vname,hospital.hname,doa,status from status inner join child on status.cid=child.cid inner join vaccine on vaccine.vid=status.vid inner join parent on parent.pid=status.ppid inner join hospital on status.hid=hospital.hid where status.ppid="+str(parentid))
    print("-"*137)
    print("|{sid}|{cname}|{vname}|{hname}|{doa}|{status}|".format(sid=str("Status ID").center(
        15), cname="Child name".center(30), vname="Vaccine".center(20), hname="Hospital".center(25), doa=str("Date of App.").center(15), status="Status".center(25)))
    print("-"*137)
    for i in cur:
        print("|{sid}|{cname}|{vname}|{hname}|{doa}|{status}|".format(sid=str(i[0]).center(
            15), cname=i[1].center(30), vname=i[2].center(20), hname=i[3].center(25), doa=str(i[4]).center(15), status=i[5].center(25)))
        print("-"*137)
    print("")
    print("Enter 9 for Back")
    print("Enter 0 for Exit")
    print("")
    print("-"*100)
    ch = int(input("Enter your Choice: "))
    if (ch == 9):
        parentprofile()
    if (ch == 0):
        exit()


if __name__ == '__main__':
    display()
