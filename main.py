import streamlit as st
import pyperclip
import pandas as pd

st.title("FND CIVILS")

# Sidebar
option = st.sidebar.radio(
    "Choose an option:",
    ["JPP Data", "Job Notes", "Ordinance Survey/Duct Plan", "TMA Page"]
)

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = {}

if "count" not in st.session_state:
    st.session_state.count = 1  # default 1 WP

# -------------------------
# JPP DATA
# -------------------------
if option == "JPP Data":
    st.session_state.count = int(st.text_input("ENTER NO. OF WP's:", st.session_state.count))

    for i in range(1, st.session_state.count + 1):
        row_data = st.session_state.data.get(
            f"row_{i}", {"wp": f"WP{i}", "structure": "", "address": "", "grid": ""}
        )

        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

        with col1:
            wp = st.text_input("", value=row_data["wp"], key=f"wp_{i}", placeholder="WP")

        with col2:
            structure = st.text_input("", value=row_data["structure"], key=f"structure_{i}", placeholder="Structure")

        with col3:
            address = st.text_input("", value=row_data["address"], key=f"address_{i}", placeholder="Address")

        with col4:
            grid = st.text_input("", value=row_data["grid"], key=f"grid_{i}", placeholder="Grid")

        st.session_state.data[f"row_{i}"] = {
            "wp": wp,
            "structure": structure,
            "address": address,
            "grid": grid,
        }

    if st.button("🧹 Clear Screen"):
        st.session_state.data = {}
        for key in list(st.session_state.keys()):
            if key.startswith(("wp_", "structure_", "address_", "grid_")):
                del st.session_state[key]
        st.success("Screen cleared!")

# -------------------------
# JOB NOTES
# -------------------------
elif option == "Job Notes":
    if st.session_state.data:
        st.subheader("Job Notes (Copy Data)")
        for idx, (key, row) in enumerate(st.session_state.data.items(), start=1):
            if st.button(f"{row['wp']}", key=f"copybtn_{idx}"):
                text_to_copy = f"{row['wp']}: {row['structure'].upper()} {row['address'].upper()} @GRID:{row['grid']}"
                pyperclip.copy(text_to_copy)
                st.success(f"Copied {row['wp']} to clipboard!")
    else:
        st.warning("No data available. Please add entries in JPP Data first.")

# -------------------------
# ORDINANCE SURVEY / DUCT PLAN
# -------------------------
elif option == "Ordinance Survey/Duct Plan":
    if st.session_state.data:
        st.subheader("Ordinance Survey/Duct Plan (Copy Data)")
        for idx, (key, row) in enumerate(st.session_state.data.items(), start=1):
            if st.button(f"{row['wp']}", key=f"copybtn2_{idx}"):
                text_to_copy = f"{row['wp']}: {row['structure'].upper()} \n@GRID:{row['grid']}"
                pyperclip.copy(text_to_copy)
                st.success(f"Copied {row['wp']} to clipboard!")
    else:
        st.warning("No data available. Please add entries in JPP Data first.")

# -------------------------
# TMA PAGE
# -------------------------
elif option == "TMA Page":
    st.subheader("TMA Page - Grid to Address Mapping")

    # Build lookup dictionary for grid → address (uppercased)
    grid_lookup = {row["grid"]: row["address"].upper() for row in st.session_state.data.values() if row["grid"]}

    # Create an empty table with 20 rows
    if "tma_table" not in st.session_state:
        st.session_state.tma_table = pd.DataFrame({"Grid": ["" for _ in range(20)], "Address": ["" for _ in range(20)]})

    # Let user edit the table
    edited_df = st.data_editor(st.session_state.tma_table, num_rows="fixed")

    # Auto-fill addresses when grid matches
    for i in range(len(edited_df)):
        grid_val = edited_df.at[i, "Grid"]
        if grid_val in grid_lookup:
            edited_df.at[i, "Address"] = grid_lookup[grid_val]

    # Save updated table
    st.session_state.tma_table = edited_df

    st.write("Final Table:")
    st.dataframe(edited_df, use_container_width=True)
