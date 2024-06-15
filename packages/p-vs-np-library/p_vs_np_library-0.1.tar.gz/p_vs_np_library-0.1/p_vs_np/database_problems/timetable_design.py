#Timetable Design

def timetable_design(courses, time_slots, rooms):
    timetable = {}

    # Sort courses based on a certain criterion (e.g., number of conflicts, course enrollment)
    sorted_courses = sorted(courses, key=lambda course: course[2], reverse=True)

    for course in sorted_courses:
        course_id, course_time_slots, course_rooms = course

        for time_slot in course_time_slots:
            if time_slot in time_slots:
                assigned_room = None

                # Check available rooms for the time slot
                for room in course_rooms:
                    if room in rooms:
                        assigned_room = room
                        break

                if assigned_room:
                    # Assign the course to the time slot and room
                    timetable[course_id] = (time_slot, assigned_room)

                    # Remove the assigned time slot and room from available options
                    time_slots.remove(time_slot)
                    rooms.remove(assigned_room)

                    break

    return timetable


# Example usage
if __name__ == "__main__":
    # Courses and their available time slots and rooms
    courses = [
        ("C1", [1, 2], ["R1", "R2"]),   # Course C1: Available time slots [1, 2], Available rooms ["R1", "R2"]
        ("C2", [2, 3], ["R2", "R3"]),   # Course C2: Available time slots [2, 3], Available rooms ["R2", "R3"]
        ("C3", [1, 3], ["R1", "R3"]),   # Course C3: Available time slots [1, 3], Available rooms ["R1", "R3"]
        ("C4", [2, 4], ["R2", "R4"]),   # Course C4: Available time slots [2, 4], Available rooms ["R2", "R4"]
        ("C5", [3, 4], ["R3", "R4"]),   # Course C5: Available time slots [3, 4], Available rooms ["R3", "R4"]
    ]

    # Available time slots and rooms
    time_slots = [1, 2, 3, 4]
    rooms = ["R1", "R2", "R3", "R4"]

    timetable = timetable_design(courses, time_slots, rooms)

    print("Timetable:")
    for course_id, assignment in timetable.items():
        time_slot = assignment[0]
        room = assignment[1]
        print(f"Course {course_id}: Time Slot = {time_slot}, Room = {room}")
