import re

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

    
