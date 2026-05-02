import json
import os
import pandas as pd
from models.student import Student

class StudentManager:
    def __init__(self, data_file="data/students.json"):
        self.data_file = data_file
        self.students = []
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.students = [Student(**item) for item in data]
        else:
            self.students = []

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in self.students], f, ensure_ascii=False, indent=2)

    def add_student(self, student):
        self.students.append(student)
        self.save_data()

    def update_student(self, student_id, updated_student):
        for i, s in enumerate(self.students):
            if s.id == student_id:
                self.students[i] = updated_student
                self.save_data()
                return True
        return False

    def delete_student(self, student_id):
        self.students = [s for s in self.students if s.id != student_id]
        self.save_data()

    def get_all_students(self):
        return self.students.copy()

    def get_all(self):
        return self.get_all_students()

    def search_students(self, keyword="", partial=True):
        if not keyword:
            return self.students
        keyword_lower = keyword.lower()
        if partial:
            return [s for s in self.students 
                    if keyword_lower in s.name.lower() or keyword_lower in str(s.id)]
        return [s for s in self.students 
                if keyword_lower == s.name.lower() or keyword_lower == str(s.id)]

    def search(self, keyword="", partial=True):
        return self.search_students(keyword, partial=partial)

    def advanced_search(self, name="", student_id="", class_name="", 
                        gender="", min_score=None, max_score=None, partial=True):
        results = self.students
        if name:
            if partial:
                results = [s for s in results if name.lower() in s.name.lower()]
            else:
                results = [s for s in results if name.lower() == s.name.lower()]
        if student_id:
            sid_str = str(student_id).lower()
            if partial:
                results = [s for s in results if sid_str in str(s.id).lower()]
            else:
                results = [s for s in results if sid_str == str(s.id).lower()]
        if class_name:
            if partial:
                results = [s for s in results if class_name.lower() in s.class_name.lower()]
            else:
                results = [s for s in results if class_name.lower() == s.class_name.lower()]
        if gender and gender != "All":
            results = [s for s in results if s.gender == gender]
        if min_score is not None:
            results = [s for s in results if s.score >= min_score]
        if max_score is not None:
            results = [s for s in results if s.score <= max_score]
        return results

    def import_from_file(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        try:
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            elif ext == '.json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                return 0, "Unsupported file type. Use CSV, Excel, or JSON."
        except Exception as e:
            return 0, f"Error reading file: {str(e)}"

        required_cols = ['id', 'name', 'dob', 'gender', 'class_name', 'score']
        df.columns = [col.strip().lower() for col in df.columns]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            return 0, f"Missing columns: {missing}"

        added = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                if pd.isna(row['id']) or pd.isna(row['name']):
                    errors.append(f"Row {idx+2}: Missing ID or Name")
                    continue
                student_id = int(row['id'])
                name = str(row['name']).strip()
                dob = str(row['dob']).strip()
                gender = str(row['gender']).strip()
                class_name = str(row['class_name']).strip()
                score = float(row['score'])
                if score < 0 or score > 10:
                    errors.append(f"Row {idx+2}: Score must be between 0 and 10")
                    continue
                if any(s.id == student_id for s in self.students):
                    errors.append(f"Row {idx+2}: Student ID {student_id} already exists")
                    continue
                new_student = Student(student_id, name, dob, gender, class_name, score)
                self.add_student(new_student)
                added += 1
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")
        return added, "\n".join(errors) if errors else None

    def load_sample_data(self):
        if len(self.students) == 0:
            sample = [
                Student(1001, "Nguyen Van A", "2000-01-15", "Nam", "CTK45", 8.5),
                Student(1002, "Tran Thi B", "2001-03-20", "Nu", "CTK45", 7.8),
                Student(1003, "Le Van C", "2000-11-10", "Nam", "CTK46", 9.0),
                Student(1004, "Pham Thi D", "2001-07-05", "Nu", "CTK46", 6.5),
            ]
            for s in sample:
                self.add_student(s)
            return True
        return False