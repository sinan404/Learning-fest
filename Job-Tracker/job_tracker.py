from os import truncate
from datetime import date

VALID_STATUSES = ["Applied", "Interview", "Selected", "Rejected"]


def load_sample_data():
    return [
        {"company": "Google", "role": "Software Engineer", "status": "Applied", "date": "2026-09-01"},
        {"company": "Microsoft", "role": "Backend Developer", "status": "Interview", "date": "2026-09-05"},
        {"company": "Amazon", "role": "Cloud Engineer", "status": "Rejected", "date": "2026-08-20"},
        {"company": "Infosys", "role": "Python Developer", "status": "Selected", "date": "2026-08-10"},
        {"company": "Zoho", "role": "Full Stack Developer", "status": "Applied", "date": "2026-09-15"},
        {"company": "Flipkart", "role": "Data Engineer", "status": "Rejected", "date": "2026-08-25"},
        {"company": "Razorpay", "role": "API Developer", "status": "Applied", "date": "2026-10-01"},
    ]


def add_application(applications, company, role, status="Applied", app_date=None):
    applications.append({
        "company": company,
        "role": role,
        "status": status,
        "date": app_date or str(date.today()),
    })
    return True


def search_by_status(applications, status):
    return [a for a in applications if a["status"].lower() == status.lower()]


def search_by_company(applications, company):
    return [a for a in applications if company.lower() in a["company"].lower()]


def update_status(applications, company, role, new_status):
    if new_status not in VALID_STATUSES:
        print(f"Invalid status '{new_status}'. Choose from {VALID_STATUSES}.")
        return False
    for a in applications:
        if a["company"].lower() == company.lower() and a["role"].lower() == role.lower():
            a["status"] = new_status
            return True
    print(f"No application found for {role} at {company}.")
    return False


def generate_summary(applications):
    counts = {status: 0 for status in VALID_STATUSES}
    for a in applications:
        counts[a["status"]] += 1
    interviews = [(a["company"], a["role"]) for a in applications if a["status"] == "Interview"]
    return {"total": len(applications), "counts": counts, "interviews": interviews}


def format_summary(summary):
    lines = ["SUMMARY", "-" * 30, f"Total applications: {summary['total']}"]
    for status, count in summary["counts"].items():
        lines.append(f"  {status:<10}: {count}")
    lines.append("")
    if summary["interviews"]:
        lines.append("Currently at Interview stage:")
        for company, role in summary["interviews"]:
            lines.append(f"  - {company} ({role})")
    else:
        lines.append("No applications at Interview stage right now.")
    return "\n".join(lines)


def save_tracker(applications, summary, filename="job_tracker.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("JOB APPLICATION TRACKER\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"{'Company':<12}{'Role':<24}{'Status':<12}{'Date'}\n")
        f.write("-" * 60 + "\n")
        for a in applications:
            f.write(f"{a['company']:<12}{a['role']:<24}{a['status']:<12}{a['date']}\n")
        f.write("\n" + format_summary(summary) + "\n")
    print(f"Tracker saved to {filename}")


def print_applications(title, apps):
    print(f"\n{title}")
    if not apps:
        print("  (none)")
    for a in apps:
        print(f"  {a['company']:<10} | {a['role']:<22} | {a['status']:<9} | {a['date']}")


def choose_status():
    while True:
        status = input(f"Status {VALID_STATUSES}: ").strip().title()
        if status in VALID_STATUSES:
            return status
        print("Invalid status, try again.")


def run_menu(applications):
    while True:
        print("\n===== JOB TRACKER =====")
        print("1. View all applications")
        print("2. Add a new application")
        print("3. Search by status")
        print("4. Search by company")
        print("5. Update a status")
        print("6. Show summary")
        print("7. Save and exit")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            print_applications("All applications:", applications)

        elif choice == "2":
            company = input("Company: ").strip()
            role = input("Role: ").strip()
            if not company or not role:
                print("Company and role can't be empty.")
                continue
            status = choose_status()
            if add_application(applications, company, role, status):
                print(f"Added {role} at {company}.")

        elif choice == "3":
            status = choose_status()
            print_applications(f"Applications with status '{status}':",
                               search_by_status(applications, status))

        elif choice == "4":
            name = input("Company name: ").strip()
            print_applications(f"Results for '{name}':",
                               search_by_company(applications, name))

        elif choice == "5":
            company = input("Company: ").strip()
            role = input("Role: ").strip()
            new_status = choose_status()
            if update_status(applications, company, role, new_status):
                print("Status updated.")

        elif choice == "6":
            print("\n" + format_summary(generate_summary(applications)))

        elif choice == "7":
            save_tracker(applications, generate_summary(applications))
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 7.")


def main():
    applications = load_sample_data()
    run_menu(applications)


if __name__ == "__main__":
    main()