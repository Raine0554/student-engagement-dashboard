import pandas as pd
import random
from faker import Faker

fake = Faker()



def generate_students(num_students=500):
    students = []
    programs = ["Bachelor of Science", "Master of IT", "Bachelor of Arts", "MBA"]
    statuses = ["Active", "Alumni", "Withdrawn"]
    
    for i in range(1, num_students + 1):
        students.append({
            "Student_ID": random.randint(1000000, 9999999),  # Random 7-digit ID
            "First_Name": fake.first_name(),
            "Last_Name": fake.last_name(),
            "Date_of_Birth": fake.date_of_birth(minimum_age=18, maximum_age=30),
            "Gender": random.choice(["Male", "Female", "Non-Binary"]),
            "Program": random.choice(programs),
            "Enrollment_Year": random.randint(2015, 2024),
            "Status": random.choice(statuses)
        })

    return pd.DataFrame(students)

# Generate and save the dataset
student_data = generate_students()
student_data.to_csv("students.csv", index=False)


# Generating courses
def generate_course():
    courses = []
    course_names = [
        "Introduction to Programming",
        "Data Structures and Algorithms",
        "Software Engineering Fundamentals",
        "Advanced Machine Learning",
        "Web Development with JavaScript",
        "Cybersecurity Basics",
        "Database Systems and Management",
        "Cloud Computing with AWS",
        "Artificial Intelligence Principles",
        "Mobile App Development with React Native"
    ]
    
    for i, course_name in enumerate(course_names, start=1):
        programs = ["Bachelor of Science", "Master of IT", "Bachelor of Arts", "MBA"]
        semesters = ["Semester 1, 2024", "Semester 2, 2024"]
        credits_options= [12, 24]
        
        courses.append({        
                "Course_ID": i,  # Auto-increment Course_ID starting from 1
                "Course_Name": course_name,
                "Program": random.choice(programs),  # Randomly assign a program
                "Credits": random.choice(credits_options),  # Randomly assign credits
                "Semester": random.choice(semesters)  # Randomly assign a semester
        })
    
    return pd.DataFrame(courses)
    
course_data = generate_course()
course_data.to_csv("courses.csv", index=False)


# Linking Attributes: Student_ID to students, Course_ID to courses
def generate_enrollments(students, courses, num_enrollments=1000):
    enrollments = []
    for _ in range(num_enrollments):
        enrollments.append({
            "Enrollment_ID": fake.uuid4(),
            "Student_ID": random.choice(students["Student_ID"]),
            "Course_ID": random.choice(courses["Course_ID"]),
            "Grade": random.choice(["A", "B", "C", "Pass", "Fail"]),
            "Enrollment_Date": fake.date_this_decade()
        })

    return pd.DataFrame(enrollments)

# Generate enrollments
courses = pd.DataFrame({
    "Course_ID": [1, 2, 3],
    "Course_Name": ["Data Science 101", "Intro to Python", "Algorithms"]
})
enrollment_data = generate_enrollments(student_data, courses)
enrollment_data.to_csv("enrollments.csv", index=False)
