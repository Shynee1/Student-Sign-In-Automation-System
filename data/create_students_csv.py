import re
import csv

def parse_from_csv():
    student_csv_source = open("data/students.csv", "r")
    student_csv_target = open("data/student_data.csv", "w")

    csvreader = csv.reader(student_csv_source)
    fields = next(csvreader)

    student_csv_target.write("name, grade, free, email\n")

    for row in csvreader:
        student_id = row[0]
        student_name = row[1]
        student_grade = row[2].split()[1]
        student_block = row[3].split()[1]

        last_name = student_name.split()[0][:-1]
        first_name = student_name.split()[1]
        email = f"{first_name.lower()[:4]}{last_name.lower()[:4]}@haverford.org"

        entry = f'"{student_name}",{student_grade},{student_block},{email}'
        
        student_csv_target.write(entry + "\n")

    student_csv_source.close()
    student_csv_target.close()

    


def parse_from_pdf():
    student_text_file = open("data/students.txt", "r")
    student_csv = open("data/student_data.csv", "w")

    student_csv.write("name, grade, free, email\n")
 
    current_block = ""
    for line in student_text_file:
        line = re.sub(r'[^\x20-\x7E]',r'', line)

        if line == "":
            continue

        if "BLOCK" in line:
            current_block = line[7]
            print("Current Block: " + current_block)
            continue

        split = line.split()

        if (len(split) != 7):
            print(split)

        first_name = split[2].replace(",", "").strip()
        last_name = split[1].replace(",", "").strip()

        email = first_name[:4].lower() + last_name[:4].lower() + "@haverford.org"

        entry = f'"{last_name}, {first_name} {split[3]}{split[4]}{split[5]}",{split[6]},{current_block},{email}'

        student_csv.write(entry + "\n")

    student_csv.close()
    student_text_file.close()

if __name__ == "__main__":
    parse_from_csv()
    
