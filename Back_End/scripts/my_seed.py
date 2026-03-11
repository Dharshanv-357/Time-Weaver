import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import SessionLocal, engine
from app.models.department import Department
from app.models.semester import Semester
from app.models.course import Course
from app.models.section import Section
from app.models.user import User, UserRole
from app.models.room import Room
from app.models.time_slot import TimeSlot
from app.models.faculty import Faculty
from app.models.student import Student
from app.core.security import hash_password
from datetime import datetime, date, time, timedelta

async def get_or_create(db, model, defaults=None, **kwargs):
    query = select(model).filter_by(**kwargs)
    result = await db.execute(query)
    instance = result.scalar_one_or_none()
    if instance:
        return instance
    params = dict((k, v) for k, v in kwargs.items())
    params.update(defaults or {})
    instance = model(**params)
    db.add(instance)
    await db.commit()
    return instance

async def seed_data():
    async with SessionLocal() as db:
        print("Seeding all admin tables...")
        
        # Departments
        cs_dept = await get_or_create(db, Department, name="Computer Science & Engineering", code="CS", description="CS Dept")
        ee_dept = await get_or_create(db, Department, name="Electrical Engineering", code="EE", description="EE Dept")
        me_dept = await get_or_create(db, Department, name="Mechanical Engineering", code="ME", description="ME Dept")
        
        # Semesters
        sem_1 = await get_or_create(db, Semester, name="Fall 2025", academic_year="2025-2026", semester_type="ODD", start_date=date(2025, 8, 1), end_date=date(2025, 12, 15), is_active=True)
        sem_2 = await get_or_create(db, Semester, name="Spring 2026", academic_year="2025-2026", semester_type="EVEN", start_date=date(2026, 1, 10), end_date=date(2026, 5, 20), is_active=False)

        # Courses
        await get_or_create(db, Course, code="CS101", name="Data Structures", credits=4, department_id=cs_dept.id, theory_hours=3, lab_hours=2)
        await get_or_create(db, Course, code="CS102", name="Algorithms", credits=4, department_id=cs_dept.id, theory_hours=3, lab_hours=2)
        await get_or_create(db, Course, code="CS103", name="Database Systems", credits=3, department_id=cs_dept.id, theory_hours=3, lab_hours=0)
        await get_or_create(db, Course, code="EE101", name="Basic Electronics", credits=3, department_id=cs_dept.id, theory_hours=3, lab_hours=0)
        
        # Sections
        sec_a = await get_or_create(db, Section, name="Section A", batch_year_start=2023, batch_year_end=2027, student_count=60, department_id=cs_dept.id)
        sec_b = await get_or_create(db, Section, name="Section B", batch_year_start=2023, batch_year_end=2027, student_count=55, department_id=cs_dept.id)
        
        # Rooms
        await get_or_create(db, Room, full_name="ABIII - C302", building="ABIII", room_number="C302", room_type="classroom", capacity=65, has_projector=True)
        await get_or_create(db, Room, full_name="ABIII - C303", building="ABIII", room_number="C303", room_type="classroom", capacity=65, has_projector=True)
        await get_or_create(db, Room, full_name="SF - CP LAB 2", building="SF", room_number="CP LAB 2", room_type="lab", capacity=30, has_lab_equipment=True)
        await get_or_create(db, Room, full_name="TF - Auditorium", building="TF", room_number="Auditorium", room_type="auditorium", capacity=200, has_projector=True, has_ac=True)

        # Time Slots (Monday 9AM - 10AM, etc)
        await get_or_create(db, TimeSlot, day_of_week="Monday", start_time=time(9, 0), end_time=time(10, 0), duration_minutes=60, is_break=False, slot_type="regular")
        await get_or_create(db, TimeSlot, day_of_week="Monday", start_time=time(10, 0), end_time=time(11, 0), duration_minutes=60, is_break=False, slot_type="regular")
        await get_or_create(db, TimeSlot, day_of_week="Monday", start_time=time(11, 0), end_time=time(11, 15), duration_minutes=15, is_break=True, slot_type="break")
        
        await get_or_create(db, TimeSlot, day_of_week="Tuesday", start_time=time(9, 0), end_time=time(10, 0), duration_minutes=60, is_break=False, slot_type="regular")

        # Users
        prof_user = await get_or_create(db, User, username="prof_smith", email="smith@university.edu", defaults={"hashed_password": hash_password("Password@123"), "full_name": "Prof. John Smith", "role": UserRole.FACULTY, "is_active": True})
        student_user = await get_or_create(db, User, username="student_alice", email="alice@university.edu", defaults={"hashed_password": hash_password("Password@123"), "full_name": "Alice Johnson", "role": UserRole.STUDENT, "is_active": True})
        
        # Faculty & Student Profiles
        await get_or_create(db, Faculty, user_id=prof_user.id, defaults={"employee_id": "EMP1001", "department_id": cs_dept.id, "designation": "Professor", "max_hours_per_week": 18})
        await get_or_create(db, Student, user_id=student_user.id, defaults={"roll_no": "23CSE101", "department_id": cs_dept.id, "section_id": sec_a.id})
        
        print("Database successfully seeded with Departments, Semesters, Courses, Sections, Rooms, TimeSlots, Users, Faculty, and Student Profiles.")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_data())
