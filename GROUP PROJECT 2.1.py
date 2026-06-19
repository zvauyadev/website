from datetime import datetime

#Data Design
#The data design for PowerWatchSA is built using dictionaries.

# Loadshedding Stages
Stages = {
    "Stage": [1, 2, 3, 4, 5, 6],
    "MW Shed": [1000, 2000, 3000, 4000, 5000, 6000],
    "Hours Off": [2, 4, 6, 8.5, 10.5, 12],
    "Blocks": ["1 block/day", "2 blocks/day", "2-3 blocks/day",
               "3 blocks/day", "4 blocks/day", "4-5 blocks/day"],
    "Severity": ["Low", "Moderate", "Significant", "Severe", "Critical", "Emergency"]
}

# Registered Community Members
CommunityMembers = {
    "ID": ["PW-001","PW-002","PW-003","PW-004","PW-005",
           "PW-006","PW-007","PW-008","PW-009","PW-010"],
    "Name": ["Nomsa Dlamini","Sipho's Spaza Shop","Benoni Auto Repair","Thandi Mokoena",
             "Katlego's Hair Salon","St Francis Primary School","Patrick van Wyk",
             "Duduza Clinic","Zanele's Catering","Lerato Sithole"],
    "Type": ["Household","Spaza shop","SME","Household","SME",
             "School","Household","Healthcare","SME","Household"],
    "Area": ["Boksburg","Benoni","Benoni","Germiston","Boksburg",
             "Boksburg","Germiston","Germiston","Benoni","Boksburg"],
    "Block": [4,7,7,2,4,4,2,2,7,4],
    "Generator": ["No","No","Yes","No","No","No","No","Yes","No","No"],
    "Solar": [False,False,False,False,False,False,True,False,False,False],
    "Vulnerable": ["Oxygen machine","None","None","None","None",
                   "None","None","Medical fridges","None","Dialysis patient"]
}

# Outage Log
OutageLog = {
    "LogID": ["LOG-001","LOG-002","LOG-003","LOG-004","LOG-005",
              "LOG-006","LOG-007","LOG-008","LOG-009","LOG-010"],
    "Date": ["2025-04-01","2025-04-01","2025-04-02","2025-04-02","2025-04-03",
             "2025-04-04","2025-04-04","2025-04-05","2025-04-06","2025-04-07"],
    "Area": ["Boksburg","Benoni","Germiston","Boksburg","Benoni",
             "Germiston","Boksburg","Benoni","Germiston","Boksburg"],
    "Block": [4,7,2,4,7,2,4,7,2,4],
    "Stage": [3,3,3,3,4,4,4,2,2,3],
    "ScheduledStart": ["06:00","10:00","14:00","18:00","02:00",
                       "06:00","10:00","14:00","18:00","22:00"],
    "ScheduledEnd": ["08:30","12:30","16:30","20:30","06:30",
                     "10:30","14:30","16:00","20:00","00:30"],
    "ActualStart": ["06:05","10:10","14:00","18:15","02:00",
                    "06:00","10:30","14:00","17:55","22:10"],
    "ActualEnd": ["09:15","12:35","17:20","21:45","06:30",
                  "11:50","15:20","16:05","20:45","01:30"],
    "Overrun": [45,5,50,75,0,80,50,5,45,60],
    "Monitor": ["Kagiso Sithole","Ayanda Dube","Nomvula Nkosi","Kagiso Sithole","Ayanda Dube",
                "Nomvula Nkosi","Kagiso Sithole","Ayanda Dube","Nomvula Nkosi","Kagiso Sithole"]
}

# Impact Reports
ImpactReports = {
    "ImpactID": ["IMP-001","IMP-002","IMP-003","IMP-004","IMP-005","IMP-006","IMP-007"],
    "LogID": ["LOG-001","LOG-001","LOG-004","LOG-004","LOG-006","LOG-007","LOG-010"],
    "MemberID": ["PW-001","PW-006","PW-005","PW-002","PW-008","PW-005","PW-010"],
    "ImpactType": ["Medical","Education","Financial","Financial","Medical","Financial","Medical"],
    "Description": [
        "Oxygen machine lost power for 70 mins - family distressed",
        "Morning computer class cancelled - 45 learners affected",
        "Hair salon lost 4 clients during evening overrun",
        "Spaza fridge off 3+ hours - cold drinks spoiled",
        "Clinic generator kicked in but medical fridge alarmed twice",
        "Hair salon closed entire morning shift",
        "Dialysis patient could not complete home treatment"
    ],
    "Loss": ["N/A","N/A",800,1200,"N/A",1500,"N/A"]
}


#Functions for PowerWatchSA

# Create a list of unique areas from the community members data
def create_area_list():
    area_list = []
    for area in CommunityMembers["Area"]:
        if area not in area_list:
            area_list.append(area)
    return area_list

# Last Log ID
def last_id(outage_logs):
    return outage_logs["LogID"][-1]
# Count logs
def count_logs(outage_logs):
    return len(outage_logs["LogID"])

# Automatically generate the next Log ID
def generate_log_id(outage_logs):
    last_id = outage_logs["LogID"][-1]   # e.g. "LOG-010"
    number = int(last_id.split("-")[1])
    return f"LOG-{number+1:03d}"

# Calculate overrun time in minutes
def calculate_overrun(scheduled_start, scheduled_end, actual_start, actual_end):
    # Convert strings to datetime objects
    sched_start = to_time(scheduled_start)
    sched_end = to_time(scheduled_end)
    actual_start_dt = to_time(actual_start)
    actual_end_dt = to_time(actual_end)

    # Calculate durations in minutes
    sched_duration = (sched_end - sched_start).total_seconds() / 60
    actual_duration = (actual_end_dt - actual_start_dt).total_seconds() / 60

    # Overrun = actual duration - scheduled duration
    overrun = actual_duration - sched_duration
    return int(overrun) if overrun > 0 else 0

#Convert string time input to datetime object
def to_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

#Add a new outage log
def log_outage(date, area, block, stage,
    scheduled_start, scheduled_end,
    actual_start, actual_end, monitor):
    log_id = generate_log_id(OutageLog)
    overrun = calculate_overrun(scheduled_start, scheduled_end, actual_start, actual_end)

    OutageLog["LogID"].append(log_id)
    OutageLog["Date"].append(date.strip())
    OutageLog["Area"].append(area.strip().title())
    OutageLog["Block"].append(block)
    OutageLog["Stage"].append(stage)
    OutageLog["ScheduledStart"].append(scheduled_start.strip())
    OutageLog["ScheduledEnd"].append(scheduled_end.strip())
    OutageLog["ActualStart"].append(actual_start.strip())
    OutageLog["ActualEnd"].append(actual_end.strip())
    OutageLog["Overrun"].append(overrun)
    OutageLog["Monitor"].append(monitor.strip().title())

    print(f"Outage logged successfully with ID {log_id}. Overrun = {overrun} minutes.")

    # Flag vulnerable alerts
    alerts = flag_vulnerable_alerts(area, block, overrun)
    for alert in alerts:
        print(alert)

    # Auto-log impact reports if overrun > 30
    if overrun > 30:
        log_impact_report(log_id, area, block, ImpactReports, CommunityMembers)



# Generate alerts for vulnerable members when an overrun occurs
def flag_vulnerable_alerts(area, block, overrun_minutes):
    alerts = []
    if overrun_minutes > 30:  # only trigger alerts if overrun is significant
        for i in range(len(CommunityMembers["ID"])):
            if CommunityMembers["Area"][i] == area and CommunityMembers["Block"][i] == block:
                if CommunityMembers["Vulnerable"][i] != "None":
                    alerts.append(
                        f"Alert: {CommunityMembers['Name'][i]} at risk due to {CommunityMembers['Vulnerable'][i]}"
                    )
    return alerts


# Produce a summary of outages for a given block and area
def get_block_summary(area, block, outage_logs, impact_reports, community_members):
    print(f"\n=== Block Summary for {area.title()}, Block {block} ===")

    # Table header
    header = f"{'Member':<30} | {'Impact':<60}"
    print(header)
    print("-" * len(header))

    found = False
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Area"][i].strip().title() == area.strip().title() and outage_logs["Block"][i] == block:
            if outage_logs["Overrun"][i] > 30:
                log_id = outage_logs["LogID"][i]

                # Find linked impacts
                for j in range(len(impact_reports["LogID"])):
                    if impact_reports["LogID"][j] == log_id:
                        found = True
                        member_id = impact_reports["MemberID"][j]
                        member_name = community_members["Name"][community_members["ID"].index(member_id)]
                        description = impact_reports["Description"][j]

                        row = f"{member_name:<30} | {description:<60}"
                        print(row)

    if not found:
        print("No affected members found for this block.")


# Calculate total financial loss from impact reports
def calculate_financial_loss(impact_reports):
    total_loss = 0
    for loss in impact_reports["Loss"]:
        if loss != "N/A":
            total_loss += int(loss)
    return total_loss


# Generate a formatted complaint report showing only affected members and impacts
def generate_complaint_report(outage_logs, impact_reports, community_members):
    print("\n=== Complaint Report (Affected Members & Impacts) ===")

    # Table header
    header = f"{'Member':<30} | {'Impact':<100}"
    print(header)
    print("-" * len(header))

    found = False
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Overrun"][i] > 30:
            log_id = outage_logs["LogID"][i]

            # Find linked impacts
            for j in range(len(impact_reports["LogID"])):
                if impact_reports["LogID"][j] == log_id:
                    found = True
                    member_id = impact_reports["MemberID"][j]
                    member_name = community_members["Name"][community_members["ID"].index(member_id)]
                    description = impact_reports["Description"][j]

                    row = f"{member_name:<30} | {description:<100}"
                    print(row)

    if not found:
        print("No affected members found for overruns greater than 30 minutes.")




# Print all flagged logs in a table format
def print_all_flagged_logs(outage_logs):
    print("\n=== All Flagged Logs (Overruns > 30 mins) ===")

    # Table header
    header = f"{'Log ID':<10} | {'Date':<12} | {'Area':<12} | {'Block':<6} | {'Stage':<6} | {'Scheduled':<15} | {'Actual':<15} | {'Overrun(mins)':<15} | {'Monitor':<20}"
    print(header)
    print("-" * len(header))

    found = False
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Overrun"][i] > 30:
            found = True
            scheduled = f"{outage_logs['ScheduledStart'][i]}-{outage_logs['ScheduledEnd'][i]}"
            actual = f"{outage_logs['ActualStart'][i]}-{outage_logs['ActualEnd'][i]}"
            row = f"{outage_logs['LogID'][i]:<10} | {outage_logs['Date'][i]:<12} | {outage_logs['Area'][i]:<12} | {outage_logs['Block'][i]:<6} | {outage_logs['Stage'][i]:<6} | {scheduled:<15} | {actual:<15} | {outage_logs['Overrun'][i]:<15} | {outage_logs['Monitor'][i]:<20}"
            print(row)

    if not found:
        print("No flagged logs found.")

# View impact report for a specific flagged log
def view_impact_report(log_id, outage_logs, impact_reports, community_members):
    print(f"\n=== Impact Report for Log ID {log_id} ===")

    # Table header
    header = f"{'Member':<30} | {'Impact':<100}"
    print(header)
    print("-" * len(header))

    found = False
    for j in range(len(impact_reports["LogID"])):
        if impact_reports["LogID"][j] == log_id:
            found = True
            member_id = impact_reports["MemberID"][j]
            member_name = community_members["Name"][community_members["ID"].index(member_id)]
            description = impact_reports["Description"][j]

            row = f"{member_name:<30} | {description:<100}"
            print(row)

    if not found:
        print("No impact report found for that Log ID.")

# Let user select a flagged log ID and view its impact report
def select_and_view_impact(outage_logs, impact_reports, community_members):
    # Collect flagged logs
    flagged_logs = [log_id for i, log_id in enumerate(outage_logs["LogID"]) if outage_logs["Overrun"][i] > 30]

    if not flagged_logs:
        print("No flagged logs available.")
        return

    # Show list of flagged logs
    print("\n=== Select a Flagged Log ===")
    for idx, log_id in enumerate(flagged_logs, start=1):
        date = outage_logs["Date"][outage_logs["LogID"].index(log_id)]
        area = outage_logs["Area"][outage_logs["LogID"].index(log_id)]
        overrun = outage_logs["Overrun"][outage_logs["LogID"].index(log_id)]
        print(f"{idx}. {log_id}")
    # User selects from list
    choice = input("Enter the number of the log you want to view: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(flagged_logs):
        print("Invalid selection.")
        return

    selected_log = flagged_logs[int(choice) - 1]

    # Print impact report for selected log
    print(f"\n=== Impact Report for {selected_log} ===")
    header = f"{'Member':<30} | {'Impact':<100}"
    print(header)
    print("-" * len(header))

    found = False
    for j in range(len(impact_reports["LogID"])):
        if impact_reports["LogID"][j] == selected_log:
            found = True
            member_id = impact_reports["MemberID"][j]
            member_name = community_members["Name"][community_members["ID"].index(member_id)]
            description = impact_reports["Description"][j]
            row = f"{member_name:<30} | {description:<100}"
            print(row)

    if not found:
        print("No impact report found for this log.")

# Automatically log an impact report when an outage affects vulnerable members
def log_impact_report(log_id, area, block, impact_reports, community_members):
    for i in range(len(community_members["ID"])):
        if community_members["Area"][i].strip().title() == area.strip().title() and community_members["Block"][i] == block:
            if community_members["Vulnerable"][i] != "None":
                # Auto-generate Impact ID
                last_id = impact_reports["ImpactID"][-1]
                number = int(last_id.split("-")[1])
                new_id = f"IMP-{number+1:03d}"

                # Append new impact report
                impact_reports["ImpactID"].append(new_id)
                impact_reports["LogID"].append(log_id)
                impact_reports["MemberID"].append(community_members["ID"][i])
                impact_reports["ImpactType"].append("Medical")  # default type for vulnerable
                impact_reports["Description"].append(f"{community_members['Name'][i]} affected due to {community_members['Vulnerable'][i]}")
                impact_reports["Loss"].append("N/A")

                print(f"Impact logged: {community_members['Name'][i]} - {community_members['Vulnerable'][i]}")

#Function to make sure that the date has been entered correctly
def validate_date(date_str):
    try:
        # Try to parse the date
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


    



# User Interface Functions
def print_header():
    print("\n" + "="*80)
    print(" "*20 + "POWERWATCH SOUTH AFRICA")
    print(" "*15 + "Loadshedding Impact Monitoring System")
    print("="*80 + "\n")

def print_main_menu():
    print("\n" + "-"*80)
    print("MAIN MENU")
    print("-"*80)
    print("1. Log Outage                  - Record a new loadshedding outage event")
    print("2. View Flagged Logs           - Display outages with overruns > 30 minutes")
    print("3. View Block Summary          - Check impact summary for a specific block")
    print("4. View Financial Losses       - Calculate total financial impact")
    print("5. Generate Complaint Report   - View all affected members and impacts")
    print("6. Exit                        - Close the application")
    print("-"*80)

def get_valid_choice(prompt, valid_options):
    while True:
        try:
            choice = input(prompt).strip()
            if choice in valid_options:
                return choice
            print(f"Invalid choice. Please select from: {', '.join(valid_options)}")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def log_outage_ui():
    print("1. Cancel and return to main menu")
    print("2. Continue to log a new outage")
    print("\n" + "="*80)
    choice = int(input("Enter choice (1-2): "))
    if choice < 1 or choice > 2:
        print("Invalid choice. Returning to main menu.")
        return
    if choice == 1:
        return
    if choice == 2:
        print("LOG NEW OUTAGE")
        print("="*80)
        try:
        # Get date
            # Keep asking until the user enters a valid date
            while True:
                date = input("Enter date (YYYY-MM-DD): ").strip()
                if validate_date(date):
                    break
                else:
                    print("Error: Date must be in format YYYY-MM-DD (e.g., 2025-04-01). Please try again.")



            # Select area
            areas = create_area_list()
            print("\nSelect Area:")
            for i, area in enumerate(areas, 1):
                print(f"  {i}. {area}")
            area_choice = int(input("Enter area number: ").strip())
            if area_choice < 1 or area_choice > len(areas):
                print("Invalid area selection.")
                return
            area = areas[area_choice - 1].strip().title()

        # Select stage
            print("\nSelect Stage:")
            for i, stage_num in enumerate(Stages["Stage"], 1):
                severity = Stages["Severity"][i-1]
                blocks = Stages["Blocks"][i-1]
                print(f"  {stage_num}. Stage {stage_num} - {severity:12} ({blocks})")
            stage = int(input("Enter stage number (1-6): ").strip())
            if stage < 1 or stage > 6:
                print("Invalid stage selection.")
                return

        # Get block
            block = int(input(f"Enter block number: ").strip())

        # Get times
            print("\nEnter Times (format HH:MM):")
            scheduled_start = input("  Scheduled start time: ").strip()
            scheduled_end = input("  Scheduled end time: ").strip()
            actual_start = input("  Actual start time: ").strip()
            actual_end = input("  Actual end time: ").strip()

        # Get monitor name
            monitor = input("Enter monitor name: ").strip().title()

        # Validate all fields
            if not all([scheduled_start, scheduled_end, actual_start, actual_end, monitor]):
                print("Error: All fields must be filled.")
                return

            log_outage(date, area, block, stage, scheduled_start, scheduled_end, actual_start, actual_end, monitor)
        except ValueError:
            print("Error: Invalid input format. Please try again.")
        except Exception as e:
            print(f"Error: {e}")

def view_flagged_logs_ui():
    print("\n" + "="*80)
    print("FLAGGED LOGS")
    print("="*80)
    print_all_flagged_logs(OutageLog)
    
    print("\n" + "-"*80)
    print("Options:")
    print("  1. Return to main menu")
    print("  2. View impact report for a flagged log")
    print("-"*80)
    choice = get_valid_choice("Enter choice (1-2): ", ["1", "2"])

    if choice == "2":
        select_and_view_impact(OutageLog, ImpactReports, CommunityMembers)

def view_block_summary_ui():
    print("\n" + "="*80)
    print("BLOCK SUMMARY")
    print("="*80)
    try:
        areas = create_area_list()
        print("\nSelect Area:")
        for i, area in enumerate(areas, 1):
            print(f"  {i}. {area}")
        area_choice = int(input("Enter area number: ").strip())
        if area_choice < 1 or area_choice > len(areas):
            print("Invalid area selection.")
            return
        area = areas[area_choice - 1].strip().title()

        block = int(input("Enter block number: ").strip())
        get_block_summary(area, block, OutageLog, ImpactReports, CommunityMembers)
    except ValueError:
        print("Error: Invalid input format. Please try again.")
    except Exception as e:
        print(f"Error: {e}")

def view_financial_losses_ui():
    print("\n" + "="*80)
    print("FINANCIAL IMPACT REPORT")
    print("="*80)
    total = calculate_financial_loss(ImpactReports)
    print(f"\nTotal Financial Loss: R{total:,.2f}")
    print("\nNote: This includes reported losses from affected members due to overruns.")

def generate_complaint_report_ui():
    print("\n" + "="*80)
    print("COMPLAINT REPORT")
    print("="*80)
    generate_complaint_report(OutageLog, ImpactReports, CommunityMembers)

# Main Menu Loop
def main():
    print_header()
    
    while True:
        print_main_menu()
        choice = get_valid_choice("Enter choice (1-6): ", ["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            log_outage_ui()
        elif choice == "2":
            view_flagged_logs_ui()
        elif choice == "3":
            view_block_summary_ui()
        elif choice == "4":
            view_financial_losses_ui()
        elif choice == "5":
            generate_complaint_report_ui()
        elif choice == "6":
            print("\n" + "="*80)
            print(" "*25 + "Thank you for using PowerWatchSA")
            print(" "*30 + "Exiting application...")
            print("="*80 + "\n")
            break

# Run the application
if __name__ == "__main__":
    main()
    