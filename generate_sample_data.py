import csv
import random
from datetime import datetime, timedelta

# Sample Vietnamese names
first_names = ["Nguyễn", "Trần", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi", "Dương", "Lê", "Phan"]
last_names = ["An", "Bắc", "Chiêu", "Đức", "Hải", "Huy", "Khánh", "Linh", "Minh", "Nam", 
              "Phong", "Quân", "Tân", "Tuấn", "Văn", "Vinh", "Xuân", "Yến", "Vy", "Hảo"]

classes = ["CNT1", "CNT2", "CNTT3", "CNTT4", "K15"]
genders = ["Nam", "Nữ"]

def generate_random_dob():
    """Generate random date of birth between 2005-2008"""
    start_date = datetime(2005, 1, 1)
    end_date = datetime(2008, 12, 31)
    random_days = random.randint(0, int((end_date - start_date).days))
    return (start_date + timedelta(days=random_days)).strftime("%d/%m/%Y")

def generate_sample_data(num_students=100):
    """Generate sample student data"""
    students = []
    
    for i in range(1, num_students + 1):
        student = {
            'id': i,
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'dob': generate_random_dob(),
            'gender': random.choice(genders),
            'class_name': random.choice(classes),
            'score': round(random.uniform(3.0, 10.0), 1)
        }
        students.append(student)
    
    return students

def save_to_csv(students, filename='sample_students.csv'):
    """Save student data to CSV file"""
    fieldnames = ['id', 'name', 'dob', 'gender', 'class_name', 'score']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    
    print(f"✅ Created {filename} with {len(students)} students")

if __name__ == "__main__":
    students = generate_sample_data(100)
    save_to_csv(students)
    print(f"Sample data preview:")
    for s in students[:5]:
        print(f"  {s['id']:3d}. {s['name']:20s} - {s['dob']:10s} - {s['gender']:3s} - {s['class_name']:5s} - {s['score']:5.1f}")
