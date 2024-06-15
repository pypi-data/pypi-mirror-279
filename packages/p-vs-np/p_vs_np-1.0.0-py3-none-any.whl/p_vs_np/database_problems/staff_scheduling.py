#Staff Scheduling


    # Sort staff members based on a certain criterion (e.g., availability, workload)



            # Check if the staff member is available for the shift
                # Assign the shift to the staff member

                # Update the staff member's availability




# Example usage
    # Staff members and their availability

    # Shifts and their requirements



if __name__ == '__main__':
    def staff_scheduling(staff, shifts):
        schedule = {}
        sorted_staff = sorted(staff, key=lambda s: len(s[1]))
        for shift in shifts:
            shift_id, shift_requirements = shift
            for staff_member in sorted_staff:
                staff_id, staff_availability = staff_member
                if all(avail in staff_availability for avail in shift_requirements):
                    schedule[shift_id] = staff_id
                    staff_availability -= set(shift_requirements)
                    break
        return schedule
    if __name__ == "__main__":
        staff = [
            ("S1", {1, 2, 3}),   # Staff S1: Available shifts {1, 2, 3}
            ("S2", {2, 3, 4}),   # Staff S2: Available shifts {2, 3, 4}
            ("S3", {1, 3, 4}),   # Staff S3: Available shifts {1, 3, 4}
            ("S4", {1, 2, 4}),   # Staff S4: Available shifts {1, 2, 4}
        ]
        shifts = [
            ("Shift1", {1, 2}),   # Shift1: Required staff {1, 2}
            ("Shift2", {2, 3}),   # Shift2: Required staff {2, 3}
            ("Shift3", {1, 3}),   # Shift3: Required staff {1, 3}
            ("Shift4", {2, 4}),   # Shift4: Required staff {2, 4}
        ]
        schedule = staff_scheduling(staff, shifts)
        print("Staff Schedule:")
        for shift_id, staff_id in schedule.items():
            print(f"Shift {shift_id}: Assigned to Staff {staff_id}")
