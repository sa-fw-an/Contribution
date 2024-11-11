import os
import subprocess
from datetime import datetime, timedelta
import random

repo_path = "."

os.chdir(repo_path)

start_date = datetime(2023, 11, 11)
end_date = datetime(2024, 8, 31)

random_dates = []
for _ in range(100):
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    random_dates.append(random_date)

random_dates = sorted(random_dates)

for commit_date in random_dates:
    commits_per_day = random.randint(1, 12)

    for _ in range(commits_per_day):
        random_time = commit_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        formatted_date = random_time.strftime('%Y-%m-%dT%H:%M:%S')

        with open("contribution.txt", "a") as file:
            file.write(f"Commit for {formatted_date}\n")

        subprocess.run(["git", "add", "contribution.txt"])
        subprocess.run([
            "git", "commit", "-m", f"Contribution for {formatted_date}",
            "--date", formatted_date
        ])

subprocess.run(["git", "push", "origin", "main"])

with open("contribution.txt", "w") as file:
    file.write("")

subprocess.run(["git", "add", "contribution.txt"])
subprocess.run(["git", "commit", "-m", "Push File"])
subprocess.run(["git", "push", "origin", "main"])

print("Fake contributions pushed to GitHub, and contribution.txt has been cleared!")
