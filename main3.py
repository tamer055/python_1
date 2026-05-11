import os
import csv
import json


# ===============================
# Class 1: FileManager
# ===============================
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print("File found:", self.filename)
            return True
        print("File not found:", self.filename)
        return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("Output folder created:", folder)
        else:
            print("Output folder already exists:", folder)


# ===============================
# Class 2: DataLoader
# ===============================
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.students = list(reader)

            print("Data loaded successfully:", len(self.students), "students")
            return self.students

        except FileNotFoundError:
            print("Error: File not found.")

    def preview(self, n=5):
        print("First", n, "rows:")
        print("-" * 40)

        for student in self.students[:n]:
            print(
                student["student_id"], "|",
                student["age"], "|",
                student["gender"], "|",
                student["country"], "| GPA:",
                student["GPA"]
            )

        print("-" * 40)


# ===============================
# Class 3: DataAnalyser
# ALL VARIANTS TOGETHER
# ===============================
class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse_gpa(self):
        gpas = []
        high = 0

        for student in self.students:
            try:
                gpa = float(student["GPA"])
                gpas.append(gpa)

                if gpa > 3.5:
                    high += 1
            except:
                continue

        self.result = {
            "analysis": "GPA Statistics",
            "total_students": len(gpas),
            "average_gpa": round(sum(gpas) / len(gpas), 2),
            "max_gpa": max(gpas),
            "min_gpa": min(gpas),
            "high_performers": high
        }

    def analyse_countries(self):
        country_counts = {}

        for student in self.students:
            country = student["country"]

            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1

        top3 = sorted(
            country_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(country_counts),
            "top_3_countries": top3,
            "all_countries": country_counts
        }

    def analyse_sleep(self):
        low = []
        high = []

        for student in self.students:
            try:
                sleep = float(student["sleep_hours"])
                gpa = float(student["GPA"])

                if sleep < 6:
                    low.append(gpa)
                else:
                    high.append(gpa)
            except:
                continue

        avg_low = round(sum(low) / len(low), 2)
        avg_high = round(sum(high) / len(high), 2)

        self.result = {
            "analysis": "Sleep vs GPA",
            "low_sleep_students": len(low),
            "avg_low_sleep_gpa": avg_low,
            "high_sleep_students": len(high),
            "avg_high_sleep_gpa": avg_high,
            "difference": round(avg_high - avg_low, 2)
        }

    def analyse_top10(self):
        top10 = sorted(
            self.students,
            key=lambda x: float(x["final_exam_score"]),
            reverse=True
        )[:10]

        result_top = []

        rank = 1
        for student in top10:
            result_top.append({
                "rank": rank,
                "student_id": student["student_id"],
                "country": student["country"],
                "major": student["major"],
                "score": student["final_exam_score"],
                "GPA": student["GPA"]
            })
            rank += 1

        self.result = {
            "analysis": "Top 10 Students",
            "top_10": result_top
        }

    def print_results(self):
        print("\nANALYSIS RESULT")
        print("=" * 40)

        for key, value in self.result.items():
            print(key, ":", value)

        print("=" * 40)


# ===============================
# Class 4: ResultSaver
# ===============================
class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as file:
                json.dump(self.result, file, indent=4)

            print("Result saved to", self.output_path)

        except:
            print("Error while saving file.")


# ===============================
# MAIN
# ===============================
fm = FileManager("students.csv")

if not fm.check_file():
    print("Stopping program.")
    exit()

fm.create_output_folder()

dl = DataLoader("students.csv")
dl.load()
dl.preview()

analyser = DataAnalyser(dl.students)

# ========= CHOOSE VARIANT =========
# analyser.analyse_gpa()
# analyser.analyse_countries()
# analyser.analyse_sleep()
analyser.analyse_top10()
# ================================

analyser.print_results()

saver = ResultSaver(analyser.result, "output/result.json")
saver.save_json()