def show_menu():
    print("\n--- Conflict-Aware Task Scheduling System ---")
    print("1. Show Tasks")
    print("2. Detect Conflicts")
    print("3. Show Hypergraph")
    print("4. Generate Schedule")
    print("5. Exit")

# Conflict-Aware Task Scheduling using Interval Hypergraphs

tasks = []

n = int(input("Enter number of tasks: "))

for i in range(n):
    print(f"\nEnter details for Task {i+1}")
    tid = input("Task ID: ")
    start = int(input("Start time: "))
    end = int(input("End time: "))
    res_input = input("Resources (comma separated, e.g., CPU,RAM): ")
    resources = [r.strip() for r in res_input.split(",")]

    tasks.append({
        "id": tid,
        "start": start,
        "end": end,
        "resources": resources
    })


print("Tasks in the system:")
for task in tasks:
    print(task)
print("\nChecking conflicts between tasks:")

def is_time_overlap(t1, t2):
    return not (t1["end"] <= t2["start"] or t2["end"] <= t1["start"])

def has_common_resource(t1, t2):
    return bool(set(t1["resources"]) & set(t2["resources"]))

conflicts = []

for i in range(len(tasks)):
    for j in range(i + 1, len(tasks)):
        t1 = tasks[i]
        t2 = tasks[j]

        if is_time_overlap(t1, t2) and has_common_resource(t1, t2):
            conflicts.append((t1["id"], t2["id"]))
            print(f"Conflict detected between {t1['id']} and {t2['id']}")

if not conflicts:
    print("No conflicts found!")
print("\nBuilding Interval Hypergraph (Resource → Tasks):")

hypergraph = {}

for task in tasks:
    for res in task["resources"]:
        if res not in hypergraph:
            hypergraph[res] = []
        hypergraph[res].append(task["id"])

for res, task_list in hypergraph.items():
    print(f"Resource {res} connects tasks: {task_list}")
print("\nConflict-Aware Scheduling:")

# Make a copy of tasks to modify schedule
scheduled_tasks = [task.copy() for task in tasks]

def resolve_conflicts(tasks):
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            t1 = tasks[i]
            t2 = tasks[j]

            if is_time_overlap(t1, t2) and has_common_resource(t1, t2):
                # Shift t2 to start after t1 ends
                shift = t1["end"] - t2["start"]
                t2["start"] += shift
                t2["end"] += shift
                print(f"Rescheduled {t2['id']} to avoid conflict with {t1['id']}")

resolve_conflicts(scheduled_tasks)

print("\nFinal Scheduled Tasks:")
for task in scheduled_tasks:
    print(task)

while True:
    show_menu()
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        print("\nTasks in the system:")
        for task in tasks:
            print(task)

    elif choice == "2":
        print("\nChecking conflicts between tasks:")
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                t1 = tasks[i]
                t2 = tasks[j]
                if is_time_overlap(t1, t2) and has_common_resource(t1, t2):
                    conflicts.append((t1["id"], t2["id"]))
                    print(f"Conflict detected between {t1['id']} and {t2['id']}")
        if not conflicts:
            print("No conflicts found!")

    elif choice == "3":
        print("\nInterval Hypergraph (Resource → Tasks):")
        hypergraph = {}
        for task in tasks:
            for res in task["resources"]:
                if res not in hypergraph:
                    hypergraph[res] = []
                hypergraph[res].append(task["id"])
        for res, task_list in hypergraph.items():
            print(f"{res} → {task_list}")

    elif choice == "4":
        print("\nGenerating conflict-free schedule:")
        scheduled_tasks = [task.copy() for task in tasks]
        resolve_conflicts(scheduled_tasks)
        print("\nFinal Scheduled Tasks:")
        for task in scheduled_tasks:
            print(task)

    elif choice == "5":
        print("Exiting system... Bye Sunny 💙")
        break

    else:
        print("Invalid choice! Please enter 1-5.")
