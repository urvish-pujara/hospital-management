import pymysql
import pymysql.cursors

def Delete():
    print("1)  Delete Patient")
    print("2)  Delete Attendant")
    print("3)  Delete Medicine")
    print("4)  Delete Employee")
    print("5)  Delete Bill")
    print("6)  Delete Room")
    print("7)  Back\n")

    ch = int(input("Enter Your option: "))
    if (ch == 1):
        Patient(3)
    elif (ch == 2):
        Attendant(3)
    elif (ch == 3):
        Medicine(3)
    elif (ch == 4):
        Employee(3)
    elif (ch == 5):
        Bill(3)
    elif (ch == 6):
        Room(3)
    elif (ch == 7):
        return
    else:
        print("Invalid Option!")


def Get():
    print("1.) Patient Report")
    print("2.) Doctor Summary")
    print("3.) Search medicine by partial name")
    print("4.) Medicine greater than ammount")
    print("5.) Back\n")
    ch = int(input("Enter choice: "))
    if ch == 5:
        return
    elif ch == 1:
        Report(1)
    elif ch == 2:
        Report(2)
    elif ch == 3:
        Report(3)
    elif ch == 4:
        Report(4)
    else:
        print("Wrong option")
        Update()


def Update():
    print("1.) Update Patient")
    print("2.) Update Attendant")
    print("3.) Update Medicine")
    print("4.) Update Employee")
    print("5.) Update Bill")
    print("6.) Update Room")
    print("7.) Back\n")
    ch = int(input("Enter choice: "))
    if ch == 7:
        return
    elif ch == 1:
        Patient(2)
    elif ch == 2:
        Attendant(2)
    elif ch == 3:
        Medicine(2)
    elif ch == 4:
        Employee(2)
    elif ch == 5:
        Bill(2)
    elif ch == 6:
        Room(2)
    else:
        print("Wrong option")
        Update()


def Insert():
    print("1.) Insert Patient")
    print("2.) Insert Attendant")
    print("3.) Insert Medicine")
    print("4.) Insert Employee")
    print("5.) Insert Bill")
    print("6.) Insert Room")
    print("7.) Back\n")
    ch = int(input("Enter choice: "))
    if ch == 7:
        return
    elif ch == 1:
        Patient(1)
    elif ch == 2:
        Attendant(1)
    elif ch == 3:
        Medicine(1)
    elif ch == 4:
        Employee(1)
    elif ch == 5:
        Bill(1)
    elif ch == 6:
        Room(1)
    else:
        print("Wrong option")
        Insert()


def getValid(L, str, errStr, onlyUpperCase=False):
    while (True):
        curr = input(str).strip()
        if onlyUpperCase:
            curr = curr.upper()
        valid = False
        for val in L:
            if curr == val:
                valid = True
                break
        if valid:
            return curr
        else:
            print(errStr)


def Patient(x):
    if (x == 1):
        try:
            row = {}
            print('Enter new patient\'s details: ')
            name = (input('Name (F_name M_name L_name): ')).split(' ')
            row['F_name'] = name[0]
            row['M_name'] = name[1]
            row['L_name'] = name[2]
            validBloodGrps = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            row['blood_grp'] = getValid(validBloodGrps, 'Blood group: ',
                                        'Please enter a valid blood group.')
            row['Bdate'] = input('Birth Date (YYYY-MM-DD): ')
            validSexInput = ['M', 'F', 'O']
            row['Sex'] = getValid(
                validSexInput, 'Sex (M for Male/ F for Female/ O for Other): ',
                'Please enter a valid sex.')
            row['Admission'] = input('Date of admission (YYYY-MM-DD): ')
            ch = input('Is Patient discharged? (y/N) ').lower()
            dischargeDate = 'NULL'
            if ch[0] == 'y':
                dischargeDate = input('Date of discharge (YYYY-MM-DD): ')
            row['Discharge'] = dischargeDate

            Address = {}
            print('--- Patient\'s Address --- ')
            Address['HOUSE_NO'] = input('House Number: ')
            Address['Street'] = input('Street: ')
            Address['Locality'] = input('Locality: ')
            Address['City'] = input('City: ')
            Address['State'] = input('State: ')
            query=""
            if row['Discharge'] == 'NULL':
                query = f"INSERT INTO PATIENT VALUES (NULL, \'{row['F_name']}\', \'{row['M_name']}\', \'{row['L_name']}\', \'{row['blood_grp']}\', \'{row['Bdate']}\', \'{row['Sex']}\', \'{Address['HOUSE_NO']}\', \'{Address['Street']}\', \'{Address['Locality']}\', \'{Address['City']}\', \'{Address['State']}\', \'{row['Admission']}\', NULL);"
            else:
                query = f"INSERT INTO PATIENT VALUES (NULL, \'{row['F_name']}\', \'{row['M_name']}\', \'{row['L_name']}\', \'{row['blood_grp']}\', \'{row['Bdate']}\', \'{row['Sex']}\', \'{Address['HOUSE_NO']}\', \'{Address['Street']}\', \'{Address['Locality']}\', \'{Address['City']}\', \'{Address['State']}\', \'{row['Admission']}\', \'{row['Discharge']}\');"
            with con.cursor() as cur:
                cur.execute(query)
            con.commit()

            patient_id = -1
            with con.cursor() as cur:
                cur.execute("SELECT LAST_INSERT_ID();")
                patient_id = cur.fetchone()['LAST_INSERT_ID()']
                
            print('--- Patient\'s phone numbers ---')
            nPhoneNums = 0
            while (True):
                if nPhoneNums > 0:
                    ch = input(
                        'Want to enter one more phone number? (y/N) ').lower()
                    if ch[0] == 'n':
                        break
                phone_num = input('Phone number: ')
                nPhoneNums += 1
                query = "INSERT INTO PATIENT_PHONE_NUMBER VALUES (%d, '%s');" % (patient_id, phone_num)
                with con.cursor() as cur:
                    cur.execute(query)

            print('--- Patient\'s Diseases ---')
            nDiseases = 0
            while (True):
                if nDiseases > 0:
                    ch = input('Want to enter one more disease? (y/N) ').lower()
                    if ch[0] == 'n':
                        break
                disease = input('Disease: ')
                nDiseases += 1
                query = "INSERT INTO PATIENT_DISEASE (PATIENT_ID, DISEASE) VALUES ('%d', '%s');" % (
                    patient_id, disease)
                with con.cursor() as cur:
                    cur.execute(query)

            doc_id = int(input('Doctor\'s ID of the doctor treating the patient: ').strip())
            query = f"INSERT INTO PATIENT_EMPLOYEE_RELATION VALUES ({patient_id}, {doc_id}, \'DOCTOR\');"
            with con.cursor() as cur:
                cur.execute(query)

            nurse_id = int(input('Nurse\'s ID of the nurse treating the patient: ').strip())
            query = f"INSERT INTO PATIENT_EMPLOYEE_RELATION VALUES ({patient_id}, {nurse_id}, \'NURSE\');"
            with con.cursor() as cur:
                cur.execute(query)
            
            room_id = int(input('Room\'s ID of the room used by patient: ').strip())
            query = f"INSERT INTO PATIENT_ROOM_RELATION VALUES ({patient_id}, {room_id});"

            with con.cursor() as cur:
                cur.execute(query)
                
            con.commit()
            print("\nInserted patient into Database")

        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)

    elif (x == 2):
        try:
            print("What do you want to update?")
            print("1. Name")
            print("2. Address")
            print("3. Date of Discharge")
            ch = int(input("Enter choice: "))
            if ch == 1:
                pid = int(input("Enter Patient ID: "))
                name = (input('Enter New Name(F_Name M_Name L_Name): ')).split(' ')
                F_name = name[0]
                M_name = name[1]
                L_name = name[2]
                try:
                    query = f"UPDATE PATIENT SET F_NAME = \'{F_name}\', M_NAME = \'{M_name}\', L_NAME = \'{L_name}\' WHERE PATIENT_ID = {pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            elif ch == 2:
                eid = int(input("Enter Patient ID: "))
                H_No = input('Enter new House Number: ')
                Street = input('Enter new Street: ')
                Locality = input('Enter new Locality: ')
                City = input('Enter new City: ')
                State = input('Enter new State: ')
                try:
                    query = f"UPDATE PATIENT SET STREET = \'{Street}\', HOUSE_NO = \'{H_No}\', LOCALITY = \'{Locality}\',CITY = \'{City}\',STATE=\'{State}\' WHERE PATIENT_ID = {eid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            elif ch == 3:
                pid = int(input("Enter Patient ID: "))
                ddate = input('Enter Discharge Date (YYYY-MM-DD): ')
                try:
                    query = f"UPDATE PATIENT SET DISCHARGE_DATE = \'{ddate}\' WHERE PATIENT_ID = {pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            else:
                print("Invalid Option")
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
    elif (x == 3):
        patient_id = int(input("Enter Patient ID: "))
        try:
            query1 = f"DELETE FROM PATIENT WHERE PATIENT_ID = {patient_id}"
            query2 = f"DELETE FROM PATIENT_DISEASE WHERE PATIENT_ID = {patient_id}"
            query3 = f"DELETE FROM PATIENT_PHONE_NUMBER WHERE PATIENT_ID = {patient_id}"
            query4 = f"DELETE FROM PATIENT_EMPLOYEE_RELATION WHERE PATIENT_ID={patient_id}"
            query5 = f"DELETE FROM PATIENT_ROOM_RELATION WHERE PATIENT_ID={patient_id}"
            query6 = f"DELETE FROM PATIENT_MEDICINE_RELATION WHERE PATIENT_ID={patient_id}"
            with con.cursor() as cur:
                cur.execute(query1)
                cur.execute(query2)
                cur.execute(query3)
                cur.execute(query4)
                cur.execute(query5)
                cur.execute(query6)
                con.commit()
                print("\nPatient data Deleted Successfuly\n")
        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print(">>>>>>>>>>>>>", e)
    return


def Attendant(x):
    if x == 1:
        try:
            print('Enter Attendant\'s details: ')
            patient_id = int(input('Patient ID: '))
            name = input('Name (F_name M_name L_name): ').strip().split()
            relation = input('Relation with patient: ').strip()
            query = f"INSERT INTO ATTENDANT VALUES ({patient_id}, \'{name[0]}\', \'{name[1]}\', \'{name[2]}\', \'{relation}\')"
            with con.cursor() as cur:
                cur.execute(query)
            print('--- Attendant\'s phone numbers ---')
            nPhoneNums = 0
            while (True):
                if nPhoneNums > 0:
                    ch = input(
                        'Want to enter one more phone number? (y/N) ').lower()
                    if ch[0] == 'n':
                        break
                phone_num = input('Phone number: ')
                nPhoneNums += 1
                query = "INSERT INTO ATTENDANT_PHONE_NUMBER VALUES (%d, '%s');" % (patient_id, phone_num)
                with con.cursor() as cur:
                    cur.execute(query)

            con.commit()
            print('\nInserted attendant into database\n')
            
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
            
    elif x == 2:
        try:
            print("What do you want to update?")
            print("1. Name")
            print("2. Relation")
            ch = int(input("Enter choice: "))
            if ch == 1:
                pid = int(input("Enter Patient ID: "))
                name = (input('Enter New Name(F_Name M_Name L_Name): ')).split(' ')
                F_name = name[0]
                M_name = name[1]
                L_name = name[2]
                try:
                    query = f"UPDATE ATTENDANT SET F_NAME = \'{F_name}\', M_NAME = \'{M_name}\', L_NAME = \'{L_name}\' WHERE PATIENT_ID = {pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            elif ch == 2:
                pid = int(input("Enter Patient ID: "))
                relation = input('Enter new Relation: ')
                try:
                    query = f"UPDATE ATTENDANT SET RELATION=\'{relation}\' WHERE PATIENT_ID={pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            else:
                print("Invalid Option")
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
    elif x==3:
        try:
            patient_id = int(input("Enter Patient ID: "))
            query1 = f"DELETE FROM ATTENDANT WHERE PATIENT_ID = {patient_id}"
            query2 = f"DELETE FROM ATTENDANT_PHONE_NUMBER WHERE PATIENT_ID={patient_id}"
            with con.cursor() as cur:
                cur.execute(query1)
                cur.execute(query2)
                con.commit()
                print("\nAttendant data Deleted Successfuly\n")
        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print(">>>>>>>>>>>>>", e)
    return


def Medicine(x):
    if x == 1:
        try:
            print('Enter Medicine\'s details: ')
            name = input('Medicine Name: ').strip() 
            cost = int(input('Cost (in %s): ' % u'\u20B9'))
            expiry_date = input('Expiry date (YYYY-MM-DD): ').strip()
            query = f"INSERT INTO MEDICINE VALUES (NULL, \'{name}\', {cost}, \'{expiry_date}\')"
            with con.cursor() as cur:
                cur.execute(query)
            con.commit()
            print('\nInserted medicine into database\n')
            
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
    elif x == 2:
        try:
            print("What do you want to update?")
            print("1. Name")
            print("2. Cost(in ₹)")
            print("3. Expiry Date")
            ch = int(input("Enter choice: "))
            if ch == 1:
                mid = int(input("Enter Medicine ID: "))
                name = input('Enter new Name: ')
                try:
                    query = f"UPDATE MEDICINE SET NAME=\'{name}\' WHERE MEDICINE_ID = {mid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Medicine ID")
            elif ch == 2:
                mid = int(input("Enter Medicine ID: "))
                cost = int(input('Enter new cost: '))
                try:
                    query = f"UPDATE MEDICINE SET COST={cost} WHERE MEDICINE_ID = {mid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Medicine ID")
            elif ch == 3:
                mid = int(input("Enter Medicine ID: "))
                expiry = input('Enter new expiry date(YYYY-MM-DD): ')
                try:
                    query = f"UPDATE MEDICINE SET EXPIRY_DATE=\'{expiry}\' WHERE MEDICINE_ID = {mid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Medicine ID")
            else:
                print("Invalid Option")
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
    elif x==3:
        medicine_id = int(input("Enter Medicine ID: "))
        try:
            query1 = f"DELETE FROM MEDICINE WHERE MEDICINE_ID = {medicine_id}"
            query2 = f"DELETE FROM PATIENT_MEDICINE_RELATION WHERE MEDICINE_ID={medicine_id}"
            with con.cursor() as cur:
                cur.execute(query1)
                cur.execute(query2)
                con.commit()
                print("\nMedicine data Deleted Successfuly\n")
        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print(">>>>>>>>>>>>>", e)
    return


def Employee(x):
    if x == 1:
        try:
            print('Enter employee\'s details')
            name = input('Enter employee\'s name (F_name, M_name, L_name): ').strip().split()
            email = input('Email: ').strip()
            employee_type = getValid(['DOCTOR', 'NURSE'], 'Employee Type (DOCTOR/NURSE): ', 'Invalid employee type!', True)
            qualification = ""
            if employee_type == 'DOCTOR':
                qualification = input('Doctor\'s qualification: ')
            else:
                qualification = input('Nurse\'s qualification: ')
            birth_date = input('Date of birth (YYYY-MM-DD): ').strip()
            Address = {}
            print('--- Employee\'s Address --- ')
            Address['HOUSE_NO'] = input('House Number: ')
            Address['Street'] = input('Street: ')
            Address['Locality'] = input('Locality: ')
            Address['City'] = input('City: ')
            Address['State'] = input('State: ')
            Joining = input('Joining date (YYYY-MM-DD): ').strip()
            Leaving = 'NULL'
            if (input('Is the employee still hired? (y/N) ').lower())[0] == 'n':
                Leaving = input('Leaving Date (YYYY-MM-DD): ').strip()
            Salary = int(input('Salary (in %s): ' % u'\u20B9').strip())
            query = ""
            if Leaving == 'NULL':
                query = f"INSERT INTO EMPLOYEE VALUES (NULL, \'{email}\', \'{name[0]}\', \'{name[1]}\', \'{name[2]}\', \'{employee_type}\', \'{birth_date}\', {Salary}, \'{Address['HOUSE_NO']}\', \'{Address['Street']}\', \'{Address['Locality']}\', \'{Address['City']}\', \'{Address['State']}\', \'{Joining}\', NULL);"
            else:
                query = f"INSERT INTO EMPLOYEE VALUES (NULL, \'{email}\', \'{name[0]}\', \'{name[1]}\', \'{name[2]}\', \'{employee_type}\', \'{birth_date}\', {Salary}, \'{Address['HOUSE_NO']}\', \'{Address['Street']}\', \'{Address['Locality']}\', \'{Address['City']}\', \'{Address['State']}\', \'{Joining}\', \'{Leaving}\');"
            with con.cursor() as cur:
                cur.execute(query)
            con.commit()

            employee_id = -1
            with con.cursor() as cur:
                cur.execute("SELECT LAST_INSERT_ID();")
                employee_id = cur.fetchone()['LAST_INSERT_ID()']
            
            if employee_type == 'DOCTOR':
                query = f"INSERT INTO DOCTOR VALUES ({employee_id}, \'{qualification}\');"
            else:
                query = f"INSERT INTO NURSE VALUES ({employee_id}, \'{qualification}\');"
            with con.cursor() as cur:
                cur.execute(query)

            nPhoneNums = 0
            while (True):
                if nPhoneNums > 0:
                    if (input('Want to enter one more phone number? (y/N) ').lower())[0] == 'n':
                        break
                phone_num = input('Phone number: ')
                nPhoneNums += 1
                query = f"INSERT INTO EMPLOYEE_PHONE_NUMBER VALUES ({employee_id}, \'{phone_num}\');" 
                with con.cursor() as cur:
                    cur.execute(query)
            con.commit()
            print('\nInserted employee into database\n')
            
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
        
    elif x == 2:
        try:
            print("What do you want to update?")
            print("1. Name")
            print("2. Address")
            print("3. Type")
            print("4. Salary")
            ch = int(input("Enter choice: "))
            if ch == 1:
                eid = int(input("Enter Employee ID: "))
                name = (input('Enter New Name (F_Name M_Name L_Name): ')).split(' ')
                F_name = name[0]
                M_name = name[1]
                L_name = name[2]
                try:
                    query = f"UPDATE EMPLOYEE SET F_NAME = \'{F_name}\', M_NAME = \'{M_name}\', L_NAME = \'{L_name}\' WHERE EMPLOYEE_ID = {eid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Employee ID")
            elif ch == 2:
                eid = int(input("Enter Employee ID: "))
                H_No = input('Enter new House Number: ')
                Street = input('Enter new Street: ')
                Locality = input('Enter new Locality: ')
                City = input('Enter new City: ')
                State = input('Enter new State: ')
                try:
                    query = f"UPDATE EMPLOYEE SET STREET = \'{Street}\', H_NO = \'{H_No}\', LOCALITY = \'{Locality}\',CITY = \'{City}\',STATE=\'{State}\' WHERE EMPLOYEE_ID = {eid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Employee ID")
            elif ch == 3:
                eid = int(input("Enter Employee ID: "))
                typee = input('Enter new type(DOCTOR/NURSE): ')
                try:
                    query = f"UPDATE EMPLOYEE SET TYPE=\'{typee}\' WHERE EMPLOYEE_ID = {eid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Employee ID")
            elif ch == 4:
                eid = int(input("Enter Employee ID: "))
                salary = input('Enter new Salary: ')
                try:
                    query = f"UPDATE EMPLOYEE SET SALARY={salary} WHERE EMPLOYEE_ID = {eid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Employee ID")
            else:
                print("Invalid Option")
        except Exception as e:
            con.rollback()
            print("Failed to update data")
            print(">>>>>>>>>>>>>", e)
    elif x==3:
        employee_id = int(input("Enter Employee ID: "))
        query1 = f"DELETE FROM EMPLOYEE WHERE EMPLOYEE_ID = {employee_id}"
        query2 = f"DELETE FROM EMPLOYEE_PHONE_NUMBER WHERE EMPLOYEE_ID = {employee_id}"
        query3 = f"DELETE FROM PATIENT_EMPLOYEE_RELATION WHERE EMPLOYEE_ID={employee_id}"
        try:
            with con.cursor() as cur:
                cur.execute(query1)
                cur.execute(query2)
                cur.execute(query3)
                con.commit()
                print("Employee data Deleted successfuly")
        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print(">>>>>>>>>>>>>", e)
    return


def Bill(x):
    if x == 1:
        try:
            print('Enter Bill details: ')
            patient_id = int(input('Patient ID: '))
            Medicine_cost = int(input('Medicine Cost: '))
            Room_cost = int(input('Room cost and service charges: '))
            doc_cost = int(input('Doctor and treatment charges: '))
            bill_date = input('Bill date (YYYY-MM-DD): ').strip()
            query = f"INSERT INTO BILL VALUES ({patient_id}, {Medicine_cost}, {Room_cost}, {doc_cost}, \'{bill_date}\');"
            with con.cursor() as cur:
                cur.execute(query)
            con.commit()
            print('\nInserted into database\n')
        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
    elif x == 2:
        try:
            print("What do you want to update?")
            print("1. Medicine Cost")
            print("2. Room and Service Charge")
            print("3. Treatment/Doctor Charges")
            print("4. Bill Date")
            ch = int(input("Enter choice: "))
            if ch == 1:
                pid = int(input("Enter Patient ID: "))
                newcost=int(input("Enter updated medicine cost: "))
                try:
                    query = f"UPDATE BILL SET MEDICINE_COST = {newcost} WHERE PATIENT_ID = {pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            elif ch == 2:
                pid = int(input("Enter Patient ID: "))
                newcharge = input('Enter new Room and Service Charges: ')
                try:
                    query = f"UPDATE BILL SET ROOM_CHARGE={newcharge} WHERE PATIENT_ID={pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            elif ch == 3:
                pid = int(input("Enter Patient ID: "))
                newcharge = input('Enter new Treatment/Doctor Charges: ')
                try:
                    query = f"UPDATE BILL SET TREATMENT_CHARGE={newcharge} WHERE PATIENT_ID={pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            elif ch == 4:
                pid = int(input("Enter Patient ID: "))
                newcharge = input('Enter new Bill Date(YYYY-MM-DD): ')
                try:
                    query = f"UPDATE BILL SET BILL_DATE=\'{newcharge}\' WHERE PATIENT_ID={pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Patient ID")
            else:
                print("Invalid Option")
        except Exception as e:
            con.rollback()
            print("Failed to update data")
            print(">>>>>>>>>>>>>", e)
    elif x==3:
        try:
            patient_id = int(input("Enter Patient ID: "))
            query1 = f"DELETE FROM BILL WHERE PATIENT_ID = {patient_id}"
            with con.cursor() as cur:
                cur.execute(query1)
                con.commit()
                print("Bill data Deleted Successfuly")
        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print(">>>>>>>>>>>>>", e)
    return


def Room(x):
    if x == 1:
        try:
            print('Enter room\'s details: ')
            room_type = input('Room Type: ').strip()
            room_charges = int(input('Room charges (in %s): ' % u'\u20B9').strip())
            query = f"INSERT INTO ROOM VALUES (NULL, \'{room_type}\', {room_charges})"
            with con.cursor() as cur:
                cur.execute(query)
            con.commit()
            print('\nInserted into database\n')

        except Exception as e:
            con.rollback()
            print("Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
    elif x == 2:
        try:
            print("What do you want to update?")
            print("1. Room Type")
            print("2. Room Charge")
            ch = int(input("Enter choice: "))
            if ch == 1:
                pid = int(input("Enter Room ID: "))
                name = input('Enter new Name: ')
                try:
                    query = f"UPDATE ROOM SET ROOM_TYPE=\'{name}\' WHERE ROOM_ID = {pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Room ID")
            elif ch == 2:
                pid = int(input("Enter Room ID: "))
                cost = int(input('Enter new cost: '))
                try:
                    query = f"UPDATE ROOM SET ROOM_CHARGES={cost} WHERE ROOM_ID = {pid}"
                    with con.cursor() as cur:
                        cur.execute(query)
                        con.commit()
                        print("Update Successful")
                except:
                    print("Invalid Room ID")
            else:
                print("Invalid Option")
        except Exception as e:
            print(e)
            print("Failed to update data")
    elif x==3:
        room_id = int(input("Enter Room ID: "))
        try:
            query1 = f"DELETE FROM ROOM WHERE ROOM_ID = {room_id}"
            query2 = f"DELETE FROM PATIENT_ROOM_RELATION WHERE ROOM_ID={room_id}"
            with con.cursor() as cur:
                cur.execute(query1)
                cur.execute(query2)
                con.commit()
                print("Room data Deleted Successfuly")
        except Exception as e:
            con.rollback()
            print("Failed to delete from database")
            print(">>>>>>>>>>>>>", e)
    return


def Report(x):
    if x == 1:
        try:
            patient_id = int(input("Enter Patient ID: "))
            query = f"SELECT * FROM PATIENT WHERE PATIENT_ID = {patient_id};"
            patientData = dict()
            with con.cursor() as cur:
                cur.execute(query)
                patientData = cur.fetchone()
            
            print('\nPatient ID:', patientData['PATIENT_ID'])
            print('Patient Name:', patientData['F_NAME'], patientData['M_NAME'], patientData['L_NAME'])
            print('Blood group:', patientData['BLOOD_GRP'])
            print('Date of Birth (YYYY-MM-DD):', patientData['BIRTH_DATE'])
            sex = patientData['SEX']
            if sex == 'M':
                sex = 'Male'
            elif sex == 'F':
                sex = 'Female'
            else:
                sex = 'Other'
            print('Sex:', sex)
            print('Date of Admission (YYYY-MM-DD):', patientData['ADMISSION_DATE'])
            if patientData['DISCHARGE_DATE'] == None:
                print('Patient is not discharged yet.')
            else:
                print('Date of Discharge (YYYY-MM-DD):', patientData['DISCHARGE_DATE'])

            query = f"SELECT F_NAME, M_NAME, L_NAME FROM ATTENDANT WHERE PATIENT_ID={patient_id};"
            with con.cursor() as cur:
                cur.execute(query)
                attendantName = cur.fetchone()
                print('Attendant Name:', attendantName['F_NAME'], attendantName['M_NAME'], attendantName['L_NAME'])
    
            query = f"SELECT EMPLOYEE_ID FROM PATIENT_EMPLOYEE_RELATION WHERE PATIENT_ID={patient_id} AND TYPE=\'DOCTOR\';" 
            with con.cursor() as cur:
                cur.execute(query)
                docs = cur.fetchall()
                print('Patient\'s doctors:', len(docs))
                for entry in docs:
                    emp_ID = entry['EMPLOYEE_ID']
                    query = f"SELECT F_NAME, M_NAME, L_NAME FROM EMPLOYEE WHERE EMPLOYEE_ID={emp_ID};"
                    cur.execute(query)
                    docName = cur.fetchone()
                    print('> Doctor:', docName['F_NAME'], docName['M_NAME'], docName['L_NAME'])

            query = f"SELECT EMPLOYEE_ID FROM PATIENT_EMPLOYEE_RELATION WHERE PATIENT_ID={patient_id} AND TYPE=\'NURSE\';" 
            with con.cursor() as cur:
                cur.execute(query)
                nurses = cur.fetchall()
                print('Patient\'s nurses:', len(nurses))
                for entry in nurses:
                    emp_ID = entry['EMPLOYEE_ID']
                    query = f"SELECT F_NAME, M_NAME, L_NAME FROM EMPLOYEE WHERE EMPLOYEE_ID={emp_ID};"
                    cur.execute(query)
                    nurseName = cur.fetchone()
                    print('> Nurse:', nurseName['F_NAME'], nurseName['M_NAME'], nurseName['L_NAME'])

            query = f"SELECT ROOM_ID FROM PATIENT_ROOM_RELATION WHERE PATIENT_ID={patient_id};" 
            with con.cursor() as cur:
                cur.execute(query)
                room = cur.fetchone()
                if room['ROOM_ID'] == None:
                    print('Patient has not been allocated any room')
                else:
                    query = f"SELECT * FROM ROOM WHERE ROOM_ID={room['ROOM_ID']};"
                    cur.execute(query)
                    roomDetails = cur.fetchone()
                    print('Patient\'s Room ID:', roomDetails['ROOM_ID'], '\nRoom Type:', roomDetails['ROOM_TYPE'])

            query = f"SELECT MEDICINE_ID FROM PATIENT_MEDICINE_RELATION WHERE PATIENT_ID={patient_id};" 
            with con.cursor() as cur:
                cur.execute(query)
                meds = cur.fetchall()
                print('Patient\'s medicines:', len(meds))
                for entry in meds:
                    med_ID = entry['MEDICINE_ID']
                    query = f"SELECT NAME FROM MEDICINE WHERE MEDICINE_ID={med_ID};"
                    cur.execute(query)
                    print('> Medicine:', cur.fetchone()['NAME'])  

            query = f"SELECT SUM(B) AS TOTAL FROM (SELECT (MEDICINE_COST + ROOM_CHARGE + TREATMENT_CHARGE) AS B FROM BILL WHERE PATIENT_ID={patient_id}) AS T;"  
            with con.cursor() as cur:
                cur.execute(query)    
                print('Total Bill:', '%s' % u'\u20B9', cur.fetchone()['TOTAL'])
                

        except Exception as e:
            print(e)
            print("Failed to Get report")
    elif x == 2:
        try:
            doctorID = int(input("Enter Doctor ID: "))
            query = f"SELECT F_NAME, M_NAME, L_NAME FROM EMPLOYEE WHERE EMPLOYEE_ID = {doctorID};"
            with con.cursor() as cur:
                cur.execute(query)
                docName = cur.fetchone()
                print('Doctor\'s name:', docName['F_NAME'], docName['M_NAME'], docName['L_NAME'])
            query = f"SELECT PATIENT_ID FROM PATIENT_EMPLOYEE_RELATION WHERE EMPLOYEE_ID={doctorID};"
            with con.cursor() as cur:
                cur.execute(query)
                patients = [entry['PATIENT_ID'] for entry in cur.fetchall()]
                pIDsInStr = ', '.join([str(pID) for pID in patients])
                query = f"SELECT DISTINCT DISEASE FROM PATIENT_DISEASE WHERE PATIENT_ID IN ({pIDsInStr});"
                cur.execute(query)
                diseases = cur.fetchall()
                print('Diseases being treated by the doctor:', len(diseases))
                for entry in diseases:
                    print('> Disease:', entry['DISEASE'])
                    
        except Exception as e:
            print(e)
            print("Failed to Get report")
        
    elif x == 3:
        try: 
            print('This report will print the medicines whose names partially match with the given phrase.')
            phrase = input('Enter a phrase: ')
            query = f"SELECT DISTINCT NAME FROM MEDICINE WHERE NAME LIKE '%{phrase}%';"
            with con.cursor() as cur:
                cur.execute(query)
                meds = [entry['NAME'] for entry in cur.fetchall()]
                print('Medicines whose names partially match the given phrase are:', len(meds))
                for med in meds:
                    print('>', med)

        except Exception as e:
            print('>>>', e)
            print('Failed to Get report')

    elif x == 4:
        try: 
            print('This report will print the medicines whose cost is greater than the given threshold.')
            thresholdVal = int(input('Enter threshold value (in %s): ' % u'\u20B9').strip())
            query = f"SELECT NAME, COST FROM MEDICINE WHERE COST > {thresholdVal};"
            with con.cursor() as cur:
                cur.execute(query)
                meds = [(entry['NAME'], entry['COST']) for entry in cur.fetchall()]
                print('Medicines whose cost is greater than the given threshold:', len(meds))
                for (name, cost) in meds:
                    print('> Name:', name, '- %s' % u'\u20B9',cost)

        except Exception as e:
            print('>>>', e)
            print('Failed to Get report')
            
    return


def dispatch(ch):
    if (ch == 1):
        Insert()
    elif (ch == 2):
        Delete()
    elif (ch == 3):
        Update()
    elif (ch == 4):
        Get()
    else:
        print("Error: Invalid Option")

username=input("Enter Username: ")
passwd=input("Enter Password: ")

while(1):
    try:
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user=username,
                              password=passwd,
                              cursorclass=pymysql.cursors.DictCursor)

        if (con.open):
            dbcreate = "CREATE DATABASE IF NOT EXISTS Hospital"
            usedb="USE Hospital"
            patienttable = "CREATE TABLE IF NOT EXISTS PATIENT (PATIENT_ID bigint NOT NULL AUTO_INCREMENT, F_NAME text, M_NAME text, L_NAME text, BLOOD_GRP text, BIRTH_DATE date, SEX text,HOUSE_NO text,STREET text,LOCALITY text,CITY text,STATE text,ADMISSION_DATE date,DISCHARGE_DATE date DEFAULT NULL, PRIMARY KEY (PATIENT_ID))"
            attendanttable = "CREATE TABLE IF NOT EXISTS ATTENDANT (PATIENT_ID bigint NOT NULL,F_NAME text,M_NAME text,L_NAME text,RELATION text)"
            medicinetable = "CREATE TABLE IF NOT EXISTS MEDICINE (MEDICINE_ID bigint NOT NULL AUTO_INCREMENT, NAME text, COST float, EXPIRY_DATE date ,PRIMARY KEY(MEDICINE_ID))"
            billtable = "CREATE TABLE IF NOT EXISTS BILL (PATIENT_ID bigint NOT NULL,MEDICINE_COST bigint, ROOM_CHARGE bigint, TREATMENT_CHARGE bigint, BILL_DATE date)"
            doctortable = "CREATE TABLE IF NOT EXISTS DOCTOR (DOCTOR_ID bigint NOT NULL, QUALIFICATION text,PRIMARY KEY (DOCTOR_ID))"
            nursetable = "CREATE TABLE IF NOT EXISTS NURSE (NURSE_ID bigint NOT NULL, QUALIFICATION text,PRIMARY KEY (NURSE_ID))"
            patientphonetable = "CREATE TABLE IF NOT EXISTS PATIENT_PHONE_NUMBER  (PATIENT_ID bigint,PHONE_NUMBER text)"
            attendantphonetable = "CREATE TABLE IF NOT EXISTS ATTENDANT_PHONE_NUMBER (PATIENT_ID bigint,PHONE_NUMBER text)"
            employeephonetable = "CREATE TABLE IF NOT EXISTS EMPLOYEE_PHONE_NUMBER (EMPLOYEE_ID bigint,PHONE_NUMBER text)"
            patientdiseasetable = "CREATE TABLE IF NOT EXISTS PATIENT_DISEASE (PATIENT_ID bigint,DISEASE text)"
            employeetable = "CREATE TABLE IF NOT EXISTS EMPLOYEE (EMPLOYEE_ID bigint NOT NULL AUTO_INCREMENT, EMAIL varchar(256) NOT NULL, F_NAME text, M_NAME text, L_NAME text, TYPE text, BIRTH_DATE date, SALARY bigint,HOUSE_NO text,STREET text,LOCALITY text,CITY text,STATE text,JOINING_DATE date,LEAVING_DATE date,PRIMARY KEY (EMPLOYEE_ID, EMAIL))"
            roomtable = "CREATE TABLE IF NOT EXISTS ROOM (ROOM_ID bigint NOT NULL AUTO_INCREMENT, ROOM_TYPE text, ROOM_CHARGES text, PRIMARY KEY (ROOM_ID))"
            patientEmployeeRelation = "CREATE TABLE IF NOT EXISTS PATIENT_EMPLOYEE_RELATION (PATIENT_ID bigint NOT NULL, EMPLOYEE_ID bigint NOT NULL, TYPE text)"
            patientMedicineRelation = "CREATE TABLE IF NOT EXISTS PATIENT_MEDICINE_RELATION (PATIENT_ID bigint NOT NULL, MEDICINE_ID bigint NOT NULL)"
            patientRoomRelation = "CREATE TABLE IF NOT EXISTS PATIENT_ROOM_RELATION (PATIENT_ID bigint NOT NULL, ROOM_ID bigint NOT NULL)"

            with con.cursor() as cur:
                cur.execute(dbcreate)
                cur.execute(usedb)
                cur.execute(patienttable)
                cur.execute(billtable)
                cur.execute(attendanttable)
                cur.execute(medicinetable)
                cur.execute(roomtable)
                cur.execute(doctortable)
                cur.execute(nursetable)
                cur.execute(patientphonetable)
                cur.execute(attendantphonetable)
                cur.execute(employeephonetable)
                cur.execute(patientdiseasetable)
                cur.execute(employeetable)
                cur.execute(patientEmployeeRelation)
                cur.execute(patientMedicineRelation)
                cur.execute(patientRoomRelation)

                con.commit()
        else:
            print("Failed to connect")

        with con.cursor() as cur:
            while (1):
                print()
                print("1.) Insert into table")
                print("2.) Delete from table")
                print("3.) Update row in a table")
                print("4.) Get")
                print("5.) Exit\n")
                ch = int(input("Enter choice: "))
                if ch == 5:
                    exit()
                else:
                    dispatch(ch)

    except Exception as e:
        print(e)
        print(
            "Connection Refused: Either username or password is incorrect or user doesn't have access to database"
        )
        exit()
