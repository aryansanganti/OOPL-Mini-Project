class Student:
    def __init__(self, student_id, name, year, department):
        self.student_id = student_id
        self.name = name
        self.year = year
        self.department = department
        self.courses = []  
        self.marks = {}  
        self.attendance = {}  

    def assign_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            self.marks[course] = None
            self.attendance[course] = 0

    def update_marks(self, course, mark):
        if course in self.courses:
            self.marks[course] = mark
        else:
            print(f"Course {course} not assigned to the student.")

    def update_attendance(self, course, attendance_percentage):
        if course in self.courses:
            self.attendance[course] = attendance_percentage
        else:
            print(f"Course {course} not assigned to the student.")

    def update_details(self, name=None, year=None, department=None):
        if name:
            self.name = name
        if year:
            self.year = year
        if department:
            self.department = department

    def __str__(self):
        details = f"ID: {self.student_id}\nName: {self.name}\nYear: {self.year}\nDepartment: {self.department}\n"
        details += f"Courses: {', '.join(self.courses) if self.courses else 'None'}\n"
        if self.courses:
            details += "Marks & Attendance:\n"
            for course in self.courses:
                mark = self.marks.get(course, 'N/A')
                attendance = self.attendance.get(course, 'N/A')
                details += f"  - {course}: Marks: {mark}, Attendance: {attendance}%\n"
        return details


class StudentManagementSystem:
    def __init__(self):

        self.students = {}

    def add_student(self, student):
        if student.student_id in self.students:
            print(f"Student with ID {student.student_id} already exists.")
            return
        self.students[student.student_id] = student
        print("Student added successfully.")

    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def edit_student(self, student_id, **kwargs):
        if student_id in self.students:
            student = self.students[student_id]
            student.update_details(
                name=kwargs.get("name"),
                year=kwargs.get("year"),
                department=kwargs.get("department"),
            )
            print("Student details updated successfully.")
        else:
            print("Student not found.")

    def view_student(self, student_id):
        if student_id in self.students:
            print(self.students[student_id])
        else:
            print("Student not found.")

    def display_all_students(self):
        if not self.students:
            print("No students found.")
        for student in self.students.values():
            print("-" * 40)
            print(student)

    def search_students(self, **criteria):
        results = []
        for student in self.students.values():
            match = True
            for key, value in criteria.items():

                if key == "student_id" and student.student_id != value:
                    match = False
                elif key == "name" and value.lower() not in student.name.lower():
                    match = False
                elif key == "department" and value.lower() not in student.department.lower():
                    match = False
            if match:
                results.append(student)
        if results:
            for student in results:
                print("-" * 40)
                print(student)
        else:
            print("No matching students found.")

    def assign_course_to_student(self, student_id, course):
        if student_id in self.students:
            self.students[student_id].assign_course(course)
            print(f"Course '{course}' assigned to student {student_id}.")
        else:
            print("Student not found.")

    def update_student_marks(self, student_id, course, mark):
        if student_id in self.students:
            self.students[student_id].update_marks(course, mark)
            print("Marks updated successfully.")
        else:
            print("Student not found.")

    def update_student_attendance(self, student_id, course, attendance):
        if student_id in self.students:
            self.students[student_id].update_attendance(course, attendance)
            print("Attendance updated successfully.")
        else:
            print("Student not found.")


def main():
    system = StudentManagementSystem()
    while True:
        print("\n---- Student Management System Menu ----")
        print("1. Add Student")
        print("2. Edit Student")
        print("3. Delete Student")
        print("4. View Student Details")
        print("5. Display All Students")
        print("6. Search Students")
        print("7. Assign Course to Student")
        print("8. Update Student Marks")
        print("9. Update Student Attendance")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                student_id = input("Enter student ID: ")
                name = input("Enter name: ")
                year = input("Enter year: ")
                department = input("Enter department: ")
                student = Student(student_id, name, year, department)
                system.add_student(student)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            student_id = input("Enter student ID to edit: ")
            name = input("Enter new name (leave blank to skip): ")
            year = input("Enter new year (leave blank to skip): ")
            department = input("Enter new department (leave blank to skip): ")
            system.edit_student(student_id, name=name or None, year=year or None, department=department or None)

        elif choice == "3":
            student_id = input("Enter student ID to delete: ")
            system.delete_student(student_id)

        elif choice == "4":
            student_id = input("Enter student ID to view details: ")
            system.view_student(student_id)

        elif choice == "5":
            system.display_all_students()

        elif choice == "6":
            print("Search by: \n a. Student ID \n b. Name \n c. Department")
            search_type = input("Choose a search criteria (a/b/c): ").lower()
            if search_type == "a":
                student_id = input("Enter student ID: ")
                system.search_students(student_id=student_id)
            elif search_type == "b":
                name = input("Enter name: ")
                system.search_students(name=name)
            elif search_type == "c":
                department = input("Enter department: ")
                system.search_students(department=department)
            else:
                print("Invalid choice.")

        elif choice == "7":
            student_id = input("Enter student ID: ")
            course = input("Enter course name: ")
            system.assign_course_to_student(student_id, course)

        elif choice == "8":
            student_id = input("Enter student ID: ")
            course = input("Enter course name: ")
            try:
                mark = float(input("Enter marks: "))
                system.update_student_marks(student_id, course, mark)
            except ValueError:
                print("Invalid mark value.")

        elif choice == "9":
            student_id = input("Enter student ID: ")
            course = input("Enter course name: ")
            try:
                attendance = float(input("Enter attendance percentage: "))
                system.update_student_attendance(student_id, course, attendance)
            except ValueError:
                print("Invalid attendance value.")

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()