import streamlit as st
import datetime
import requests
import time

API_URL = "http://localhost:8000/"

st.set_page_config(
page_title="To-do List App",
page_icon="🔥", 
)

def registration():
    st.markdown("<h1 style='text-align: center;'>To-do List</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>New User Registration</h3>", unsafe_allow_html=True)

    center = st.columns([1, 2, 1])[1]
    with center:
        username = st.text_input("Username")
        email_id = st.text_input("Email")
        password = st.text_input("Password ", type="password")
        register_button = st.button("Register", use_container_width=True)

        if register_button:
            payload = {
                "user_name": username,
                "email": email_id,
                "password": password
            }

            registration_url = API_URL + "/register/"
            response = requests.post(registration_url, json=payload)

            if response.status_code == 200:
                st.success("Registration Successful!")
                time.sleep(2)
                st.session_state.page = "todo_list"
                st.rerun()
            else:
                st.error(f"Registration failed: {response.text}")

def signin():
    st.markdown("<h1 style='text-align: center;'>To-do List</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>User Sign In</h3>", unsafe_allow_html=True)

    center = st.columns([1, 2, 1])[1]
    with center:
        email_id = st.text_input("Email")
        password = st.text_input("Password", type="password")
        signin_button = st.button("Login", use_container_width=True)

        if signin_button:
            payload = {
                "user_name": None,
                "email": email_id,
                "password": password
            }
            signin_url = API_URL + "/login/"
            response = requests.post(signin_url, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                st.session_state.user_id = response_data["user_id"]
                st.success("Login is Successful!")
                time.sleep(2)
                st.session_state.page = "todo_list"
                st.rerun()
            else:
                st.error(f"Sign In failed: {response.text}")

def home():
    st.markdown("<h1 style='text-align: center;'>To-do List</h1>", unsafe_allow_html=True)

    center = st.columns([1, 2, 1])[1]
    with center:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

        col1 = st.columns([1, 4, 1])[1]
        col2 = st.columns([1, 4, 1])[1]
        with col1:
            register = st.button("Register", key="register_btn", use_container_width=True)
        
        with col2:
            login = st.button("Login", key="login_btn", use_container_width=True)
        

        if register:
            st.session_state.page = "register"
        if login:
            st.session_state.page = "login"

def todo_list():
    st.markdown("<h1 style='text-align: center;'>Welcome to To-Do List!</h1>", unsafe_allow_html=True)

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to view your tasks.")
        st.session_state.page="login"
        st.rerun()

    if "tasks" not in st.session_state or not st.session_state.tasks:
        payload = {"user_id": user_id}
        tasks_url = API_URL + "/get_tasks/"
        response = requests.post(tasks_url, json=payload)
        if response.status_code == 200:
            st.session_state.tasks = [task["task"] for task in response.json()]
        else:
            st.error("Failed to fetch tasks.")
            st.session_state.tasks = []

    st.subheader("Your Tasks")
    center = st.columns([1, 4, 1])[1]
    with center:
        if st.session_state.tasks:
            for i, t in enumerate(st.session_state.tasks):
                col1, col2, col3 = st.columns([4, 4, 4])
                with col1:
                    st.write(f"- {t}", use_container_width=True)
                with col2:
                    if st.button("Done", key=f"done_{i}", use_container_width=True):
                        st.session_state.tasks[i] = f"~~{t}~~"
                        st.rerun()
                with col3:
                    if st.button("Delete", key=f"delete_{i}", use_container_width=True):
                        st.session_state.tasks.pop(i)
                        st.rerun()
        else:
            st.write("No tasks remaining!")

        if st.button("Add new task", key="new_task", use_container_width=True):
            st.session_state.page = "new_task"

def new_task():
    st.markdown("<h1 style='text-align: center;'>New Task Details</h1>", unsafe_allow_html=True)

    center = st.columns([1, 2, 1])[1]
    with center:
        with st.form("task_form", clear_on_submit=True):
            task = st.text_input("Enter your task")
            due_date = st.date_input("Due Date", datetime.date.today(), min_value=datetime.date(2025, 9, 9), max_value=datetime.date(2030, 12, 31))
            notes = st.text_input("Notes")
            col1, col2 = st.columns(2)

            with col1:
                submit_task = st.form_submit_button("Add Task")
                if submit_task:
                    payload = {
                        "user_id": st.session_state.get('user_id'),
                        "task": task,
                        "completed": False,
                        "due_date": due_date.isoformat(),
                        "notes": notes
                    }

                    new_task_url = API_URL + "/new_task/"
                    response = requests.post(new_task_url, json=payload)

                    if response.status_code == 200:
                        st.success("Successful")
                        time.sleep(2)
                        st.session_state.page = "todo_list"
                        st.rerun()
                    else:
                        st.error(response.json())

            with col2:
                cancel = st.form_submit_button("Cancel")
                if cancel:
                    st.session_state.page = "todo_list"
                    st.rerun()

if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "register":
        registration()
    elif st.session_state.page == "login":
        signin()
    elif st.session_state.page == "todo_list":
        todo_list()
    elif st.session_state.page == "new_task":
        new_task()
