import mysql.connector
import tabulate
import random
import csv
#1.1
def add_rec():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        u_id=random.randint(10000,99999)
        u_fname=input('Enter first name:')
        u_lname=input('Enter last name:')
        u_dob=input('Enter dob(yyyy-mm-dd):')
        u_roomno=int(input('Enter room number:'))
        u_roomtyp=input('Enter room type(Standard,Deluxe,Premium):').lower()
        u_stat=int(input('Enter status (0 or 1):'))
        q=f'insert into patient values ({u_id},"{u_fname}","{u_lname}","{u_dob}",{u_roomno},"{u_roomtyp}",{u_stat})'
        cur.execute(q)
        con.commit()
        print('Record added successfully!')
    except Exception as e:
        print(e)
    cur.close()
    con.close()

#1.2
def delete_rec():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        u_pid=int(input('Enter patient id to be deleted:'))
        q=f'select * from patient where pid="{u_pid}"'
        cur.execute(q)
        rs=cur.fetchone()
        con.commit()
        if rs==None:
            print('Invalid patient id')
        else:
            q1='delete from patient where pid={}'.format(u_pid)
            q2='delete from diagnosis where pid={}'.format(u_pid)
            cur.execute(q1)
            con.commit()
            print(cur.rowcount,'Record deleted successfully from PATIENT table!')
            cur.execute(q2)
            con.commit()
            print(cur.rowcount,'Record deleted successfully from DIAGNOSIS table!')
    except Exception as e:
        print(e)
        con.rollback()
        
#1.3
def update_rec():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        u_id=int(input('Enter patient id:'))
        q=f'select * from patient where pid="{u_id}"'
        cur.execute(q)
        rs=cur.fetchone()
        con.commit()
        while True:
            if rs==None:
                print('Invalid patient id')
                break
            else:
                print('''Choose to update:
                1.Name
                2.Date of Birth
                3.Room Number
                4.Room Type
                5.Back''')
                uch=int(input('Enter choice: '))
                if uch==1:
                    u_fname=input('Enter first name:')
                    u_lname=input('Enter last name:')
                    q=f'update patient set pfname="{u_fname}",plname="{u_lname}" where pid="{u_id}"'
                    cur.execute(q)
                    con.commit()
                    print('Record updated successfully!')
                elif uch==2:
                    u_dob=input('Enter dob(yyyy-mm-dd):')
                    q=f'update patient set pdob="{u_dob}" where pid="{u_id}"'
                    cur.execute(q)
                    con.commit()
                    print('Record updated successfully!')
                elif uch==3:
                    u_roomno=int(input('Enter room number:')).lower()
                    q=f'update patient set proomno={u_roomno} where pid="{u_id}"'
                    cur.execute(q)
                    con.commit()
                    print('Record updated successfully!')
                elif uch==4:
                    u_roomtyp=input('Enter room type(Standard,Deluxe,Premium):')
                    q=f'update patient set proomtype="{u_roomtyp}" where pid="{u_id}"'
                    cur.execute(q)
                    con.commit()
                    print('Record updated successfully!')
                elif uch==5:
                    break
        
    except Exception as e:
        print(e)
        con.rollback()
        
#1.4.1        
def search_roomtyp():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        utyp=input('Enter room type to search (Standard,Deluxe,Premium):')
        q=f'select * from patient where proomtype="{utyp}"'
        cur.execute(q)
        rs=cur.fetchall()
        if rs==None:
            print('Given room type doesn\'t exist')
        else:
            print(tabulate.tabulate(rs,headers=['Patient ID','First Name','Last Name','DOB','Room No.','Room Type','Status'],tablefmt='fancy_grid'))
    except Exception as e:
        print(e)

#1.4.2
def search_pid():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        upid=input('Enter patient id to search:')
        q=f'select * from patient where pid="{upid}"'
        cur.execute(q)
        rs=cur.fetchone()
        if rs==None:
            print('Given patient id doesn\'t exist')
        else:
            print(tabulate.tabulate(rs,headers=['Patient ID','First Name','Last Name','DOB','Room No.','Room Type','Status'],tablefmt='fancy_grid'))
    except Exception as e:
        print(e)

#1.4.3     
def search_nostat():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        uroomno=input('Enter room number to be searched:')
        ustat=input('Enter status to be searched:')
        q=f'select * from patient where proomno="{uroomno}" and pstat="{ustat}"'
        cur.execute(q)
        rs=cur.fetchall()
        if rs==None:
            print('Given room number or status doesn\'t exist')
        else:
            import tabulate
            print(tabulate.tabulate(rs,headers=['Patient ID','First Name','Last Name','DOB','Room No.','Room Type','Status'],tablefmt='fancy_grid'))
    except Exception as e:
        print(e)

#1.5
def display_all():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        mycur=mycon.cursor()
        mycur.execute('select * from patient')
        rs=mycur.fetchall()
        print(tabulate.tabulate(rs,headers=['Patient ID','First Name','Last Name','DOB','Room No.','Room Type','Status'],tablefmt='fancy_grid'))
    except Exception as e:
        print(e)
    mycon.close()
    mycur.close()

#1.6
def discharge_pt():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        f1=open('dispat.csv','a',newline='')
        cw=csv.writer(f1)
        u_id=int(input('Enter patient id:'))
        q=f'select * from patient where pid="{u_id}"'
        cur.execute(q)
        rs=cur.fetchone()
        con.commit()
        while True:
            if rs==None:
                print('Invalid patient id')
                break
            else:
                q=f'update patient set pstat={0} where pid="{u_id}"'
                cur.execute(q)
                con.commit()
                q2=f'delete from diagnosis where pid={u_id}'
                cur.execute(q2)
                con.commit()
                q1=f'select * from patient where pid={u_id}'
                cur.execute(q1)
                rs=cur.fetchone()
                con.commit()
                cw.writerow(rs)
                print('Patient discharge successfully!')
                f1.close()
        
    except Exception as e:
        print(e)
    con.close()
    cur.close()
        
#1.7
def display_discharge():
    try:
        f=open('dispat.csv','r')
        cr=csv.reader(f)
        rec=[]
        for r in cr:
            rec.append(r)
        print(tabulate.tabulate(rec,headers=['Patient ID','First Name','Last Name','DOB','Room No.','Room Type','Status'],tablefmt='fancy_grid'))
        f.close()
    except Exception as e:
        print(e)
#2.1
def diag_test():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        q='select pid from patient'
        cur.execute(q)
        rs=cur.fetchall()
        ls=list(sum(rs,()))
        u_id=int(input('Enter patient id:'))
        if u_id in ls:
            print('Scan/Test to be done. Enter 0(Not applicable) or 1(Applicable):')
            u_phlegm=int(input('Phlegm test:'))
            u_blood=int(input('Blood test:'))
            u_urine=int(input('Urine test:'))
            u_stool=int(input('Stool test:'))
            u_ctscan=int(input('CT scan:'))
            u_mri=int(input('MRI scan:'))
            u_ecg=int(input('ECG scan:'))
            q1=f'insert into diagnosis values ({u_id},{u_phlegm},{u_blood},{u_urine},{u_stool},{u_ctscan},{u_mri},{u_ecg})'
            cur.execute(q1)
            con.commit()
            print('Data added successfully!')
        else:
            print('Invalid patient ID.')
    except Exception as e:
        print(e)
    cur.close()
    con.close()

#2.2
def diag_table():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        mycur=mycon.cursor()
        mycur.execute('select * from diagnosis')
        rs=mycur.fetchall()
        import tabulate
        print(tabulate.tabulate(rs,headers=['Patient ID','Phlegm Test','Blood Test','Urine Test','Stool Test','CT Scan','MRI Scan','ECG Test'],tablefmt='fancy_grid'))
    except Exception as e:
        print(e)
    mycon.close()
    mycur.close()

    
#3.1
def rec_room():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        q=f'select * from patient where pid="{billpid}"'
        cur.execute(q)
        rs=cur.fetchone()
        con.commit()
        if rs==None:
            print('Invalid patient id')
        else:
            q=f'select proomtype from patient where pid="{billpid}"'
            cur.execute(q)
            rs=cur.fetchone()
            if rs==('standard',):
                print('Standard Room: 50.00AED')
            elif rs==('deluxe',):
                print('Deluxe Room:   75.00AED')
            elif rs==('premium',):
                print('Premium Room:   100.00AED')
            else:
                print('Invalid Patient ID')
    except Exception as e:
        print(e)
    cur.close()
    con.close()

#3.2
def rec_diag():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        q=f'select * from diagnosis where pid="{billpid}"'
        cur.execute(q)
        rs=cur.fetchall()
        ls=list(sum(rs,()))
        if ls[1]==1:
            print('Phlegm Test:    10.50 AED')   
        if ls[2]==1:
            print('Blood Test:     11.50 AED')
        if ls[3]==1:
            print('Urine Test:     5.00 AED')
        if ls[4]==1:
            print('Stool Test:     25.00 AED')
        if ls[5]==1:
            print('CT Scan:        140.00 AED')
        if ls[6]==1:
            print('MRI Scan:       800.00 AED')
        if ls[7]==1:
            print('ECG Test:       13.00 AED')

    except Exception as e:
        print(e)
    

#3.3    
def bill_diag():
    
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        q=f'select * from patient where pid="{billpid}"'
        cur.execute(q)
        rs=cur.fetchone()
        con.commit()
        if rs==None:
            print('Invalid patient id')
        else:
            q=f'select * from diagnosis where pid="{billpid}"'
            cur.execute(q)
            rs=cur.fetchall()
            ls=list(sum(rs,()))
            bill=0
            if ls[1]==1:
                bill+=10.50
            elif ls[1]==0:
                bill+= 0
            if ls[2]==1:
                bill+= 11.50
            elif ls[2]==0:
                bill+= 0
            if ls[3]==1:
                bill+= 5
            elif ls[3]==0:
                bill+= 0
            if ls[4]==1:
                bill+= 25
            elif ls[4]==0:
                bill+= 0
            if ls[5]==1:
                bill+= 140
            elif ls[5]==0:
                bill+= 0
            if ls[6]==1:
                bill+= 800
            elif ls[6]==0:
                bill+= 0
            if ls[7]==1:
                bill+= 13
            elif ls[7]==0:
                bill+= 0
            return bill
    except Exception as e:
        print(e)


#3.4
def bill_type():
    try:
        con=mysql.connector.connect(host='localhost',user='root',passwd='leenamaam',database='jipuragi')
        cur=con.cursor()
        q=f'select * from patient where pid="{billpid}"'
        cur.execute(q)
        rs=cur.fetchone()
        con.commit()
        if rs==None:
            print('Invalid patient id')
        else:
            q=f'select proomtype from patient where pid="{billpid}"'
            cur.execute(q)
            rs=cur.fetchone()
            con.commit()
            if rs==('standard',):
                return 50
            elif rs==('deluxe',):
                return 75
            elif rs==('premium',):
                return 100
                    
    except Exception as e:
        print(e)
        
###########################################################
        
print(60*'*')
print('------------Welcome to Jipuragi Hospital------------')     
while True:
    print('Choose log-in options from the following:')
    print('1.Admin')
    print('2.Doctor')
    print('3.Billing Counter')
    print('4.Exit')
    x=int(input('Enter choice '))
    if x==1:
        adps=input('Enter password: ')
        if adps=='110511':
            while True:
                print('''Choose option
                        1.Add patient details
                        2.Delete patient details
                        3.Update patient details
                        4.Search patient details
                        5.Display patient details
                        6.Discharge patient
                        7.Display old records
                        8.Back''')
                op=int(input('Enter choice: '))
                if op==1:
                    add_rec()
                elif op==2:
                    delete_rec()
                elif op==3:
                    update_rec()
                elif op==4:
                    print('''Search by:
                                1. Room type
                                2. Patient ID
                                3. Room number and status''')
                    sop=int(input('Enter choice: '))
                    if sop==1:
                        search_roomtyp()
                    elif sop==2:
                        search_pid()
                    elif sop==3:
                        search_nostat()
                    else:
                        print('Invalid option')
                elif op==5:
                    display_all()
                elif op==6:
                    discharge_pt()
                elif op==7:
                    display_discharge()
                elif op==8:
                    break
                    
                else:
                    print('Invalid option')
        else:
            print('Wrong password')
                  
    elif x==2:
        drpwd=input('Enter password:')
        if drpwd=='415320':
            while True:
                print('''Choose option:
                    1. Display patient details
                    2. Run diagnostic tests
                    3. Display diagnosis table
                    4. Back''')
                op=int(input('Enter option:'))
                if op==1:
                    display_all()
                elif op==2:
                    diag_test()
                elif op==3:
                    diag_table()
                elif op==4:
                    break
    elif x==3:
        billpid=int(input('Enter patient id:'))
        try:
            print(25*'*','Bill','*'*25)
            rec_room()
            rec_diag()
            print('\nTotal Fee:\t',bill_diag()+bill_type(),'AED')
            print(54*'*')
        except Exception as e:
            print(e)
    elif x==4:
        break
    else:
        print('Invalid input.')
    