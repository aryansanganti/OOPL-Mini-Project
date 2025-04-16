import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from student_management import Student, StudentManagementSystem

app = Flask(__name__)
system = StudentManagementSystem()
CSV_FILE = os.path.join(os.path.dirname(__file__), 'students.csv')

@app.route('/')
def index():
    return render_template('index.html', students=list(system.students.values()))

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        year = request.form.get('year')
        department = request.form.get('department')
        student = Student(student_id, name, year, department)
        system.add_student(student)

        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Student ID", "Name", "Year", "Department"])
            writer.writerow([student_id, name, year, department])
        
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/student/<student_id>')
def view_student(student_id):
    student = system.students.get(student_id)
    if not student:
        return "Student not found", 404
    return render_template('view_student.html', student=student)

@app.route('/student/<student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = system.students.get(student_id)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        name = request.form.get('name')
        year = request.form.get('year')
        department = request.form.get('department')
        system.edit_student(student_id, name=name or None, year=year or None, department=department or None)
        return redirect(url_for('view_student', student_id=student_id))
    return render_template('edit_student.html', student=student)

@app.route('/student/search', methods=['GET', 'POST'])
def search_student():
    results = None
    if request.method == 'POST':
        criteria = {}
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        department = request.form.get('department')
        if student_id:
            criteria['student_id'] = student_id
        if name:
            criteria['name'] = name
        if department:
            criteria['department'] = department
        results = []
        for student in system.students.values():
            match = True
            if 'student_id' in criteria and student.student_id != criteria['student_id']:
                match = False
            if 'name' in criteria and criteria['name'].lower() not in student.name.lower():
                match = False
            if 'department' in criteria and criteria['department'].lower() not in student.department.lower():
                match = False
            if match:
                results.append(student)
    return render_template('search_student.html', results=results)

@app.route('/student/<student_id>/assign_course', methods=['GET', 'POST'])
def assign_course(student_id):
    student = system.students.get(student_id)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        course = request.form.get('course')
        system.assign_course_to_student(student_id, course)
        return redirect(url_for('view_student', student_id=student_id))
    return render_template('assign_course.html', student=student)

@app.route('/student/<student_id>/update_marks', methods=['GET', 'POST'])
def update_marks(student_id):
    student = system.students.get(student_id)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        course = request.form.get('course')
        try:
            mark = float(request.form.get('mark'))
            system.update_student_marks(student_id, course, mark)
        except ValueError:
            return "Invalid mark value", 400
        return redirect(url_for('view_student', student_id=student_id))
    return render_template('update_marks.html', student=student)

@app.route('/student/<student_id>/update_attendance', methods=['GET', 'POST'])
def update_attendance(student_id):
    student = system.students.get(student_id)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        course = request.form.get('course')
        try:
            attendance = float(request.form.get('attendance'))
            system.update_student_attendance(student_id, course, attendance)
        except ValueError:
            return "Invalid attendance value", 400
        return redirect(url_for('view_student', student_id=student_id))
    return render_template('update_attendance.html', student=student)

@app.route('/student/<student_id>/delete', methods=['POST'])
def delete_student(student_id):
    system.delete_student(student_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)