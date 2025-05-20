import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(page_title="Inventory Management System", layout="wide")

# Load inventory from session or default CSV
def load_inventory():
    if 'inventory' not in st.session_state:
        if os.path.exists("inventory.csv"):
            st.session_state.inventory = pd.read_csv("inventory.csv")
        else:
            st.session_state.inventory = pd.DataFrame(columns=['product_id', 'product_name', 'quantity', 'location'])
    return st.session_state.inventory

# Save inventory to CSV
def save_inventory(df):
    df.to_csv("inventory.csv", index=False)
    st.session_state.inventory = df

# Add product to inventory
def add_product(df, product_id, product_name, quantity, location):
    new_row = pd.DataFrame([{
        'product_id': product_id,
        'product_name': product_name,
        'quantity': quantity,
        'location': location
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Search product by name or ID
def search_product(df, query):
    result = df[df['product_name'].str.contains(query, case=False, na=False) |
                (df['product_id'].astype(str) == str(query))]
    return result

# --- Header ---
st.markdown("<h1 style='text-align: center;'>📦 Expert Inventory Management System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Developed By: M Raza Shahid and Group</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar for Actions ---
action = st.sidebar.selectbox("Choose Action", ["Add Product", "Upload CSV", "Search Product"])

df = load_inventory()

if action == "Add Product":
    st.subheader("➕ Add New Product")
    product_id = st.text_input("Product ID")
    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    location = st.text_input("Location (e.g., Aisle A)")

    if st.button("Add to Inventory"):
        if product_id and product_name:
            df = add_product(df, product_id, product_name, quantity, location)
            save_inventory(df)
            st.success(f"{product_name} added successfully!")
        else:
            st.error("Product ID and Name are required.")

elif action == "Upload CSV":
    st.subheader("📁 Upload Inventory CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)
        required_cols = ['product_id', 'product_name', 'quantity', 'location']
        if all(col in df_upload.columns for col in required_cols):
            df = pd.concat([df, df_upload], ignore_index=True).drop_duplicates('product_id', keep='last')
            save_inventory(df)
            st.success("CSV uploaded and merged into inventory.")
        else:
            st.error("CSV must contain columns: product_id, product_name, quantity, location")

elif action == "Search Product":
    st.subheader("🔍 Search Product")
    query = st.text_input("Enter Product Name or ID")
    if query:
        results = search_product(df, query)
        if not results.empty:
            st.write("### 🔍 Search Results:")
            st.dataframe(results)
        else:
            st.warning("No matching product found.")

# --- Download CSV Button ---
if not df.empty:
    st.download_button(
        label="📥 Download Inventory as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='inventory.csv',
        mime='text/csv'
    )

# --- Footer / Project Documentation ---
st.markdown("---")
st.markdown("### 🧠 Knowledge Base:")
st.markdown("- Contains structured product data: `product_id`, `product_name`, `quantity`, `location`")

st.markdown("### ⚙️ Inference Engine:")
st.markdown("- Handles user queries like adding, searching, uploading, and downloading products")

st.markdown("### 💾 Working Memory:")
st.markdown("- Uses `pandas.DataFrame` and `Streamlit Session State` to temporarily store inventory data during runtime")
st.markdown("### 📁 Persistent Storage:")
st.markdown("- Saves final inventory state to `inventory.csv` on disk for future use")