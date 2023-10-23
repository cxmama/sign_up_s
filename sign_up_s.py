import streamlit as st
import pandas as pd
import random
import datetime

# Initialize session state
if '_main_dg' not in st.session_state:
    st.session_state['_main_dg'] = {'_markdowns': [], 'roll_call_started': False, 'roll_call_count': 0}

# Read student information file
student_info = pd.read_csv('D:\sign_up_streamlit\student_info.csv', encoding='gbk')

# Get student name list
name_list = student_info['姓名'].to_list()

# Get current date
current_date = datetime.date.today()

# Set title
st.title('《流体力学》课堂点名')

# Display date
st.write(f'日期：{current_date}')

# Create a number input box for the number of roll calls, defaulting to 10
number = st.number_input('输入点名数', value=10)

# Display the number of roll calls
st.write(f'点名数为 {number}')

# Create a button to start roll call
if not st.session_state._main_dg['roll_call_started'] and st.button('开始点名'):
    st.session_state._main_dg['roll_call_started'] = True

# Perform roll call if it has started
if st.session_state._main_dg['roll_call_started']:
    if st.session_state._main_dg['roll_call_count'] < number:
        # Randomly select a name
        name = random.choice(name_list)
        # Display the name in a large font size
        st.markdown(f'# {name}')
        # Remove the selected name from the name list to avoid duplicates
        name_list.remove(name)
        # Store the name in session state
        st.session_state._main_dg['_markdowns'] = [{'body': name}]
        # Increment the roll call count
        st.session_state._main_dg['roll_call_count'] += 1
    else:
        # Display an error message when roll call is completed
        st.error('点名完毕')

# Create two buttons for recording attendance and absence
col1, col2 = st.columns(2) # Create a two-column layout

with col1: # In the first column
    if st.session_state._main_dg['roll_call_started'] and st.button('到'): # If the '到' button is clicked
        with open('arrive.txt', 'a+') as f: # Open the 'arrive.txt' file in append mode
            name = st.session_state._main_dg.get('_markdowns', [{}])[0].get('body', '')
            f.write(name + '\n') # Write the name to the file
not_arrived_list = []
with col2: # In the second column
    if st.session_state._main_dg['roll_call_started'] and st.button('未到'): # If the '未到' button is clicked
        name = st.session_state._main_dg.get('_markdowns', [{}])[0].get('body', '')
        not_arrived_list.append(name) # Add the name to the not_arrived_list
        with open('no_arrive.txt', 'a+') as f: # Open the 'no_arrive.txt' file in append mode
            f.write(name + '\n') # Write the name to the file

