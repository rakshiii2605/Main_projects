import pickle

with open("study_model.pkl", "rb") as f:
    model = pickle.load(f)

subjects = ["Math", "Physics", "Chemistry", "English", "Biology"]
marks = [45, 65, 80, 90, 50]

labels = model.predict([[m] for m in marks])

def get_study_plan(subjects, labels):
    plan = {}
    for subj, label in zip(subjects, labels):
        if label == "Weak":
            plan[subj] = 3
        elif label == "Moderate":
            plan[subj] = 2
        else:
            plan[subj] = 1
    return plan

plan = get_study_plan(subjects, labels)

for subject, hours in plan.items():
    print(f"{subject}: {hours} hours/day")
