import streamlit as st
import json
from pathlib import Path
from abc import ABC, abstractmethod

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
st.set_page_config(page_title="School Hub", page_icon="🎓", layout="wide")

DATABASE = "school_data.json"


def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"students": [], "teachers": []}


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


# Read from disk on every rerun so manual edits to the JSON file
# (e.g. in VS Code) show up immediately, without restarting the app.
data = load_data()


# ----------------------------------------------------------------------
# DOMAIN LOGIC (bugs from the original script fixed here)
# ----------------------------------------------------------------------
class Person(ABC):
    @abstractmethod
    def get_role(self):
        pass

    @staticmethod
    def email_validator(email):
        if "@" not in email:
            return False
        local, _, domain = email.partition("@")
        return bool(local) and "." in domain and not domain.startswith(".")


class Student(Person):
    def get_role(self):
        return "student"

    def register(self, name, age, email, roll_no):
        if not Person.email_validator(email):
            return False, "That email address doesn't look valid."
        if any(s["roll_no"] == roll_no for s in data["students"]):
            return False, "A student with this roll number already exists."
        data["students"].append(
            {"name": name, "age": age, "email": email, "roll_no": roll_no, "grades": {}}
        )
        save_data(data)
        return True, f"Student '{name}' registered successfully."

    def add_grade(self, roll_no, subject, marks):
        for s in data["students"]:
            if s["roll_no"] == roll_no:
                s["grades"][subject] = marks
                save_data(data)
                return True, f"Grade added for {s['name']} in {subject}."
        return False, "No student found with that roll number."

    def find(self, roll_no):
        return next((s for s in data["students"] if s["roll_no"] == roll_no), None)


class Teacher(Person):
    def get_role(self):
        return "teacher"

    def register(self, name, age, email, subject, emp_id):
        if not Person.email_validator(email):
            return False, "That email address doesn't look valid."
        if any(t["emp_id"] == emp_id for t in data["teachers"]):
            return False, "A teacher with this employee ID already exists."
        data["teachers"].append(
            {"name": name, "age": age, "email": email, "subject": subject, "emp_id": emp_id}
        )
        save_data(data)
        return True, f"Teacher '{name}' registered successfully."

    def find(self, emp_id):
        return next((t for t in data["teachers"] if t["emp_id"] == emp_id), None)


stud = Student()
teach = Teacher()

# ----------------------------------------------------------------------
# PINTEREST-STYLE THEME
# Every card uses ONE of these palettes as a whole (bg + border + text),
# so text color is always paired with its own background and never
# collides with a neighbouring card's colors.
# ----------------------------------------------------------------------
PALETTES = [
    {"bg": "#FDE9EC", "border": "#F6C6CE", "accent": "#C2185B", "text": "#3A1620"},
    {"bg": "#E8F0FE", "border": "#C6D9F8", "accent": "#1A56C4", "text": "#152238"},
    {"bg": "#E9F7EF", "border": "#C4EBD4", "accent": "#1E8E5A", "text": "#123724"},
    {"bg": "#FFF4E0", "border": "#FBE0AE", "accent": "#B5680C", "text": "#3B2A0E"},
    {"bg": "#F1E9FB", "border": "#DCC8F5", "accent": "#6C2BD9", "text": "#241537"},
    {"bg": "#E6F7F7", "border": "#BCEAEA", "accent": "#0E7C7B", "text": "#0F2C2C"},
]

CUSTOM_CSS = f"""
<style>
    .stApp {{
        background: #FAFAF8;
    }}
    #MainMenu, footer {{visibility: hidden;}}

    h1, h2, h3 {{
        color: #1F1B24;
        font-family: 'Trebuchet MS', sans-serif;
    }}

    .hub-title {{
        font-size: 2.6rem;
        font-weight: 800;
        color: #1F1B24;
        margin-bottom: 0;
    }}
    .hub-subtitle {{
        color: #6B6470;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }}

    /* Masonry gallery */
    .masonry {{
        column-count: 3;
        column-gap: 1.1rem;
    }}
    @media (max-width: 1100px) {{
        .masonry {{ column-count: 2; }}
    }}
    @media (max-width: 700px) {{
        .masonry {{ column-count: 1; }}
    }}

    .pin-card {{
        break-inside: avoid;
        margin-bottom: 1.1rem;
        padding: 1.1rem 1.2rem;
        border-radius: 18px;
        border: 1px solid;
        box-shadow: 0 2px 10px rgba(30, 20, 40, 0.06);
    }}
    .pin-card .tag {{
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        margin-bottom: 0.55rem;
    }}
    .pin-card .name {{
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
    }}
    .pin-card .meta {{
        font-size: 0.88rem;
        margin: 0.15rem 0;
        opacity: 0.92;
    }}
    .pin-card .grade-row {{
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        padding: 0.15rem 0;
        border-top: 1px dashed rgba(0,0,0,0.12);
        margin-top: 0.4rem;
    }}
    .pin-card .avg {{
        margin-top: 0.6rem;
        font-weight: 700;
        font-size: 0.95rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: #211A2B;
    }}
    section[data-testid="stSidebar"] * {{
        color: #F3EFFA !important;
    }}
    section[data-testid="stSidebar"] .stRadio > label {{
        color: #F3EFFA !important;
    }}

    /* Buttons */
    .stButton > button {{
        background: #1F1B24;
        color: #FFFFFF;
        border-radius: 999px;
        border: none;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
    }}
    .stButton > button:hover {{
        background: #C2185B;
        color: #FFFFFF;
    }}

    .stFormSubmitButton > button {{
        background: #1F1B24 !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: none !important;
        font-weight: 600 !important;
    }}
    .stFormSubmitButton > button:hover {{
        background: #C2185B !important;
    }}

    div[data-testid="stForm"] {{
        background: #FFFFFF;
        border-radius: 20px;
        padding: 1.6rem;
        border: 1px solid #ECE7F0;
        box-shadow: 0 2px 14px rgba(30,20,40,0.05);
    }}

    /* Labels: always dark, so they never vanish on the white card */
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] {{
        color: #1F1B24 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}
    div[data-testid="stTooltipIcon"] svg {{
        color: #6B6470 !important;
    }}

    /* Inputs: light field, dark text, visible border */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {{
        background: #F6F3F8 !important;
        border-radius: 12px !important;
    }}
    div[data-baseweb="input"] {{
        border: 1px solid #DDD6E3 !important;
    }}
    div[data-baseweb="input"]:focus-within {{
        border-color: #C2185B !important;
    }}
    div[data-baseweb="input"] input {{
        background: #F6F3F8 !important;
        color: #1F1B24 !important;
        -webkit-text-fill-color: #1F1B24 !important;
    }}
    div[data-baseweb="input"] input::placeholder {{
        color: #8A8394 !important;
        -webkit-text-fill-color: #8A8394 !important;
    }}
    div[data-testid="stNumberInput"] button {{
        background: #EDE7F2 !important;
        color: #1F1B24 !important;
    }}

    /* Dropdown (selectbox) + its popup list */
    div[data-baseweb="select"] > div {{
        background: #F6F3F8 !important;
        border: 1px solid #DDD6E3 !important;
        border-radius: 12px !important;
    }}
    div[data-baseweb="select"] * {{
        color: #1F1B24 !important;
    }}
    div[data-baseweb="popover"] ul {{
        background: #FFFFFF !important;
    }}
    div[data-baseweb="popover"] li {{
        background: #FFFFFF !important;
        color: #1F1B24 !important;
    }}
    div[data-baseweb="popover"] li:hover {{
        background: #FDE9EC !important;
    }}

    /* Small section headings inside forms */
    .form-section {{
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #C2185B;
        margin: 0.4rem 0 0.2rem 0;
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# CARD BUILDERS
# ----------------------------------------------------------------------
def _minify(html):
    """Collapse to a single line with no leading whitespace.

    Streamlit's markdown renderer treats 4+ leading spaces as a code
    block. Multi-line, indented f-strings for the cards were tripping
    that rule after the first card, so every card after it rendered as
    raw HTML text instead of being drawn. Stripping indentation and
    joining onto one line avoids that entirely.
    """
    return "".join(line.strip() for line in html.strip().splitlines())


def student_card(s, palette):
    grades = s.get("grades", {})
    avg = sum(grades.values()) / len(grades) if grades else 0
    grade_html = "".join(
        f'<div class="grade-row"><span>{subj}</span><span>{mark}</span></div>'
        for subj, mark in grades.items()
    ) or '<div class="grade-row"><span>No grades yet</span><span>—</span></div>'

    html = f"""
    <div class="pin-card" style="background:{palette['bg']}; border-color:{palette['border']}; color:{palette['text']};">
        <span class="tag" style="background:{palette['accent']}; color:#FFFFFF;">Student</span>
        <div class="name">{s['name']}</div>
        <div class="meta">🎂 Age {s['age']}</div>
        <div class="meta">🆔 Roll No. {s['roll_no']}</div>
        <div class="meta">✉️ {s['email']}</div>
        {grade_html}
        <div class="avg" style="color:{palette['accent']};">Average: {avg:.1f}</div>
    </div>
    """
    return _minify(html)


def teacher_card(t, palette):
    html = f"""
    <div class="pin-card" style="background:{palette['bg']}; border-color:{palette['border']}; color:{palette['text']};">
        <span class="tag" style="background:{palette['accent']}; color:#FFFFFF;">Teacher</span>
        <div class="name">{t['name']}</div>
        <div class="meta">🎂 Age {t['age']}</div>
        <div class="meta">📚 Subject: {t['subject']}</div>
        <div class="meta">🆔 Emp ID {t['emp_id']}</div>
        <div class="meta">✉️ {t['email']}</div>
    </div>
    """
    return _minify(html)


# ----------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------
st.sidebar.markdown("## 🎓 School Hub")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "🧑‍🎓 Register Student",
        "🧑‍🏫 Register Teacher",
        "📊 Add Grades",
        "🔍 Student Lookup",
        "🔍 Teacher Lookup",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Students:** {len(data['students'])}")
st.sidebar.markdown(f"**Teachers:** {len(data['teachers'])}")


# ----------------------------------------------------------------------
# PAGE: DASHBOARD
# ----------------------------------------------------------------------
if page == "🏠 Dashboard":
    st.markdown('<div class="hub-title">Welcome to School Hub</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hub-subtitle">A pinboard of every student and teacher on record.</div>',
        unsafe_allow_html=True,
    )

    filter_choice = st.selectbox("Show", ["Everyone", "Students only", "Teachers only"])

    cards_html = []
    idx = 0
    if filter_choice in ("Everyone", "Students only"):
        for s in data["students"]:
            cards_html.append(student_card(s, PALETTES[idx % len(PALETTES)]))
            idx += 1
    if filter_choice in ("Everyone", "Teachers only"):
        for t in data["teachers"]:
            cards_html.append(teacher_card(t, PALETTES[idx % len(PALETTES)]))
            idx += 1

    if cards_html:
        st.markdown(
            f'<div class="masonry">{"".join(cards_html)}</div>', unsafe_allow_html=True
        )
    else:
        st.info("No records yet — register a student or teacher from the sidebar to get started.")


# ----------------------------------------------------------------------
# PAGE: REGISTER STUDENT
# ----------------------------------------------------------------------
elif page == "🧑‍🎓 Register Student":
    st.markdown('<div class="hub-title">Register a Student</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hub-subtitle">Add a new student to the school records. '
        'Roll numbers must be unique.</div>',
        unsafe_allow_html=True,
    )
    with st.form("register_student_form", clear_on_submit=True):
        st.markdown('<div class="form-section">Personal details</div>', unsafe_allow_html=True)
        name = st.text_input("Full name", placeholder="e.g. Aarav Sharma")
        age = st.number_input("Age", min_value=3, max_value=100, value=15, step=1,
                              help="Student's age in years")
        email = st.text_input("Email", placeholder="e.g. aarav@example.com",
                              help="Must contain an @ and a domain such as .com")
        st.markdown('<div class="form-section">School details</div>', unsafe_allow_html=True)
        roll_no = st.number_input("Roll number", min_value=0, step=1,
                                  help="Unique number that identifies this student")
        submitted = st.form_submit_button("Register Student")

        if submitted:
            if not name.strip():
                st.error("Please enter a name.")
            else:
                ok, msg = stud.register(name.strip(), int(age), email.strip(), int(roll_no))
                st.success(msg) if ok else st.error(msg)


# ----------------------------------------------------------------------
# PAGE: REGISTER TEACHER
# ----------------------------------------------------------------------
elif page == "🧑‍🏫 Register Teacher":
    st.markdown('<div class="hub-title">Register a Teacher</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hub-subtitle">Add a new teacher to the staff records. '
        'Employee IDs must be unique.</div>',
        unsafe_allow_html=True,
    )
    with st.form("register_teacher_form", clear_on_submit=True):
        st.markdown('<div class="form-section">Personal details</div>', unsafe_allow_html=True)
        name = st.text_input("Full name", placeholder="e.g. Mrs. Kaur")
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1,
                              help="Teacher's age in years")
        email = st.text_input("Email", placeholder="e.g. kaur@school.edu",
                              help="Must contain an @ and a domain such as .com")
        st.markdown('<div class="form-section">Work details</div>', unsafe_allow_html=True)
        subject = st.text_input("Subject taught", placeholder="e.g. Physics")
        emp_id = st.number_input("Employee ID", min_value=0, step=1,
                                 help="Unique number that identifies this teacher")
        submitted = st.form_submit_button("Register Teacher")

        if submitted:
            if not name.strip() or not subject.strip():
                st.error("Please fill in name and subject.")
            else:
                ok, msg = teach.register(
                    name.strip(), int(age), email.strip(), subject.strip(), int(emp_id)
                )
                st.success(msg) if ok else st.error(msg)


# ----------------------------------------------------------------------
# PAGE: ADD GRADES
# ----------------------------------------------------------------------
elif page == "📊 Add Grades":
    st.markdown('<div class="hub-title">Add a Grade</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hub-subtitle">Record marks for a student. Adding the same subject '
        'again overwrites the earlier mark.</div>',
        unsafe_allow_html=True,
    )
    with st.form("add_grade_form", clear_on_submit=True):
        st.markdown('<div class="form-section">Who and what</div>', unsafe_allow_html=True)
        roll_no = st.number_input("Student roll number", min_value=0, step=1,
                                  help="Roll number of an already registered student")
        subject = st.text_input("Subject", placeholder="e.g. Mathematics")
        marks = st.number_input("Marks (out of 100)", min_value=0.0, max_value=100.0, step=0.5)
        submitted = st.form_submit_button("Add Grade")

        if submitted:
            if not subject.strip():
                st.error("Please enter a subject.")
            else:
                ok, msg = stud.add_grade(int(roll_no), subject.strip(), float(marks))
                st.success(msg) if ok else st.error(msg)


# ----------------------------------------------------------------------
# PAGE: STUDENT LOOKUP
# ----------------------------------------------------------------------
elif page == "🔍 Student Lookup":
    st.markdown('<div class="hub-title">Find a Student</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hub-subtitle">Enter a roll number to see that student\'s full card.</div>',
        unsafe_allow_html=True,
    )
    roll_no = st.number_input("Roll number", min_value=0, step=1)
    if st.button("Search Student"):
        result = stud.find(int(roll_no))
        if result:
            st.markdown(
                f'<div class="masonry">{student_card(result, PALETTES[1])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("No student found with that roll number.")


# ----------------------------------------------------------------------
# PAGE: TEACHER LOOKUP
# ----------------------------------------------------------------------
elif page == "🔍 Teacher Lookup":
    st.markdown('<div class="hub-title">Find a Teacher</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hub-subtitle">Enter an employee ID to see that teacher\'s full card.</div>',
        unsafe_allow_html=True,
    )
    emp_id = st.number_input("Employee ID", min_value=0, step=1)
    if st.button("Search Teacher"):
        result = teach.find(int(emp_id))
        if result:
            st.markdown(
                f'<div class="masonry">{teacher_card(result, PALETTES[3])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("No teacher found with that employee ID.")
