import json
from abc import ABC,abstractmethod
from pathlib import Path

database = "school_data.json"
data = {"students":[],"teachers":[] }

if Path(database).exists():
    with open(database,"r") as f :
        content = f.read()
        if content:
            data  = json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)
class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def email_validater(email):
        if "." in email and "@" in email:
            return True
        else:
            return False


class students(Persons):
    def get_roles(self):
        return "students"
    
    def register(self):
        name = input("please  enter  your name:")
        age = int(input("please enter your age:"))
        email = input("please enter your email:")
        roll_no = int(input("please enter your roll no:"))



        if not Persons.email_validater(email):
            print("invalid email")
            return
        for i in data['students']:
            if i['roll_no'] == roll_no:
                print("student already exists")
                return

        data ['students'].append({
            "name":name,
            "age": age,
            "email":email,
            "roll_no": roll_no,
            "grades": {}

            })
        save()
        print(f"student {name} registered")

        
    def show_details(self):
        roll_no = int(input("roll no:"))
        for i in data['students']:
             if i['roll_no'] == roll_no:
                  grades = i[grades]
                  avg = sum(grades.values())/len(grades) if grades else 0
                  print(f"\n  Name  :  {i['name']}")
                  print(f"    Roll no: {i[roll_no]}")
                  print(f"   Grades : {grades}")
                  print(f"   Average : {avg:.1f}")
                  return
        

    def add_grades(self):
         roll_no = int(input("tell your roll no :"))
         subject = input("subject:")
         marks = float(input("marks : "))

         for i in data['students']:
              if i["roll_no"] == roll_no:
                   i['grades'][subject]= marks
                   save()
                   print("grade added successfully")
                   return
         print("student not found")





         
    

class teachers:
    def get_roles(self):
            return "teachers"

    def register(self):
        name = input("please  enter  your name:")
        age = int(input("please enter your age:"))
        email = input("please enter your email:")
        subject = input("subject:")
        emp_id = int(input("please enter your employee id:"))

        if not Persons.email_validater(email):
                    print("invalid email")
                    return

        for i in data['teachers']:
                    if i['emp_id'] == emp_id:
                        print("teacher already exists")
                        return


        
        data ['teachers'].append({
            "name":name,
            "age": age,
            "email":email,
            "emp_id": emp_id,
            "subject": subject,

            })
        save()
        print(f"teacher {name} registered")

    def show_details(self):
             emp_id = int(input("Employee ID:"))
             for t in data["teachers"]:
                  if t ["emp_id"] == emp_id:
                       print(f"\n Name  : {t['name']}")
                       print(f"  Subject  : {t['subject']}")
                       print(f"  Emp ID  : {t['emp_id']}")
                       return
                  print("teacher not found.")

stud = students()
teach = teachers()

print("press 1 to enter a student:")
print("press 2 to enter a teacher:")
print("press 3 to enter grades:")
print("press 4 to show student details:")
print("press 5 to show teacher details:")

choice = int(input("please enter your choice:"))

if choice == 1 :
    stud.register()
elif choice == 2 :
    teach.register()
elif choice == 3 :
     stud.add_grades()
elif choice == 4 :
     stud.show_details()
elif choice == 5 :
     teach.show_details()