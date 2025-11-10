import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


st.title("FND TEST")

jobs = ["JPP Data","Tasks","Job Notes","Ordinance Suvey/Duct Diagram","Call outs","TMA Page"]

def copy_button(text, key):
    components.html(f"""
        <button onclick="navigator.clipboard.writeText('{text}')"
                style="padding:8px 5px; border-radius:10px; background:#4CAF50; color:white; border:none; cursor:pointer; margin-top:-10px;margin-left:-3px;">
            📋 
        </button>
    """, height=45)

if "jpp_data" not in st.session_state:
    st.session_state.jpp_data = []

for job in jobs:
    with st.expander(job):
                
        if job == "JPP Data":
            st.write("Fill in the details accordingly")
            wp_count = st.text_input("Enter No.Of.Work Points :",value="1")
            jpp_inputs = []
            for i in range(1,int(wp_count)+1):
                col1,col2,col3,col4 = st.columns(4)
                with col1:
                    wp = st.text_input(f"WP",value=f"WP{i}")
                with col2:
                    item = st.text_input(f"WP{i}-item :")
                with col3:
                    addr = st.text_input(f"WP{i}-Address :")
                with col4:
                    grid = st.text_input(f"WP{i}-Grid Reference :")
                    
                jpp_inputs.append({
                    "Item":item,
                    "Address":addr,
                    "Grid":grid
                }
                )
                
                st.session_state.jpp_data = jpp_inputs
                
        elif job == "Tasks":
            st.write("Fill in the details accordingly")
            task_count = st.text_input("Enter No.Of. Tasks :", value="1")
            if "tasks" not in st.session_state:
                st.session_state.tasks = []
            task_inputs = []
            for i in range(1, int(task_count) + 1):
                task_text = st.text_input(f"Task {i} :", key=f"task_{i}")
                task_inputs.append(task_text)
            st.session_state.tasks = task_inputs


                    
                    
        elif job == "Job Notes":
            if "jpp_data" in st.session_state and st.session_state.jpp_data:
                st.write("### Data for Job Notes")
                for idx,data in enumerate(st.session_state.jpp_data, start=1):
                    col1,col2 = st.columns(2)  
                    res = f"WP{idx}: {data['Item']} {data['Address']}@GRID:{data['Grid']}"
                    with col1:
                        st.write(res.upper())
                    with col2:
                        copy_button(res,key="copy_btn_{idx}")
               
        elif job == "Ordinance Suvey/Duct Diagram":
            if "jpp_data" in st.session_state and st.session_state.jpp_data:
                st.write("### Data for Ordinance Suvey/Duct Diagram")
                for idx,data in enumerate(st.session_state.jpp_data, start=1):
                    col1,col2 = st.columns(2)  
                    res = f"WP{idx} Map Reference:{data['Grid']} Address: {data['Address'].upper()}"
                    with col1:
                        st.write(res)
                    with col2:
                        copy_button(res,key="copy_btn_{idx}")
                   
        elif job == "Call outs":
            if "jpp_data" in st.session_state and st.session_state.jpp_data:
                st.write("### Data for Call outs")
                tasks = st.session_state.get("tasks", [])
                for idx,data in enumerate(st.session_state.jpp_data, start=1):
                    col1,col2,col3,col4 = st.columns(4)  
                    res = f"WP{idx}: {data['Item']} {data['Address']}@GRID:{data['Grid']}"
                    text_to_copy = f"WP{idx}: {data['Item'].upper()} \\n @GRID:{data['Grid']}"
                    with col1:
                        st.write(res.upper())
                    with col2:
                        copy_button(text_to_copy,key="copy_btn_{idx}")
                st.write("### Data for Tasks")
                if tasks:
                    for t_idx, task in enumerate(tasks, start=1):
                        col3, col4 = st.columns(2)
                        task_text = f"TASK{t_idx}: {task}"
                        with col3:
                            st.write(task_text.upper())
                        with col4:
                            copy_button(task, key=f"task_copy_{idx}_{t_idx}") 
                    
        
        elif job == "TMA Page":
            if "jpp_data" in st.session_state and st.session_state.jpp_data:
                st.write("### TMA Page: Paste grids in the first column, addresses will populate automatically")
                grid_to_address = {data["Grid"]: data["Address"].upper() for data in st.session_state.jpp_data}
                if "tma_df" not in st.session_state:
                    st.session_state.tma_df = pd.DataFrame({
                        "Grid": [""]*5, 
                        "Address": [""]*5
                    })
                tma_df = st.data_editor(
                    st.session_state.tma_df,
                    num_rows="dynamic",  
                    column_config={
                        "Grid": st.column_config.TextColumn("Grid"),
                        "Address": st.column_config.TextColumn("Address", disabled=True)
                    }
                )
                tma_df["Address"] = tma_df["Grid"].map(grid_to_address).fillna("")
                st.session_state.tma_df = tma_df



