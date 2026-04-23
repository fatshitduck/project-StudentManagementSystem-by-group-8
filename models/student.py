# models/student.py
class Student:
    def __init__(self, student_id, name, dob, gender, class_name, score):
        self.id = student_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.class_name = class_name
        self.score = float(score)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
            "class_name": self.class_name,
            "score": self.score
        }

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name})"