import os, csv, json

class FileManager:
    def __init__(self, file):
        self.file = file

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.file):
            print("File found:", self.file)
            return True
        print("File not found")
        return False

    def create_output_folder(self):
        if not os.path.exists("output"):
            os.makedirs("output")
        print("Output folder ready")


class DataLoader:
    def __init__(self, file):
        self.file = file
        self.students = []

    def load(self):
        with open(self.file, encoding="utf-8") as f:
            self.students = list(csv.DictReader(f))
        print("Loaded:", len(self.students))

    def preview(self):
        for s in self.students[:5]:
            print(s["student_id"], s["GPA"])


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        low = [float(s["GPA"]) for s in self.students if float(s["sleep_hours"]) < 6]
        high = [float(s["GPA"]) for s in self.students if float(s["sleep_hours"]) >= 6]

        self.result = {
            "analysis": "Sleep vs GPA",
            "low_sleep": round(sum(low)/len(low),2),
            "high_sleep": round(sum(high)/len(high),2)
        }

    def print_results(self):
        print(self.result)


class ResultSaver:
    def __init__(self, result):
        self.result = result

    def save_json(self):
        with open("output/result.json", "w") as f:
            json.dump(self.result, f, indent=4)


fm = FileManager("students.csv")

if fm.check_file():
    fm.create_output_folder()

    dl = DataLoader("students.csv")
    dl.load()
    dl.preview()

    da = DataAnalyser(dl.students)
    da.analyse()
    da.print_results()

    rs = ResultSaver(da.result)
    rs.save_json()
    #1
    