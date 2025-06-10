
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Mobix - إدارة الورشة", layout="wide")
st.title("🔧 Mobix | نظام إدارة الورشة")

# --- إعداد قواعد البيانات ---

if 'clients' not in st.session_state:
    st.session_state.clients = pd.DataFrame(columns=[
        'الاسم', 'رقم الموبايل', 'نوع العربية', 'VIN', 'الخدمة المطلوبة', 'تاريخ الزيارة', 'موعد الصيانة القادمة'
    ])

if 'parts' not in st.session_state:
    st.session_state.parts = pd.DataFrame(columns=['اسم القطعة', 'السعر', 'الكمية'])

if 'invoices' not in st.session_state:
    st.session_state.invoices = []

# --- علامات تبويب ---

tabs = st.tabs(["تسجيل عميل", "إدارة قطع الغيار", "سجل الصيانة"])

# --- تبويب تسجيل العميل ---

with tabs[0]:
    st.subheader("🧾 تسجيل بيانات عميل")
    with st.form("client_form"):
        name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الموبايل")
        car_type = st.text_input("نوع العربية")
        vin = st.text_input("رقم الشاسيه (VIN)")
        service = st.text_area("الخدمة المطلوبة")
        visit_date = st.date_input("تاريخ الزيارة", datetime.date.today())
        next_maintenance = st.date_input("موعد الصيانة القادمة")
        submitted = st.form_submit_button("تسجيل")
        if submitted:
            new_row = pd.DataFrame([[name, phone, car_type, vin, service, visit_date, next_maintenance]],
                                   columns=st.session_state.clients.columns)
            st.session_state.clients = pd.concat([st.session_state.clients, new_row], ignore_index=True)
            st.success("تم تسجيل البيانات بنجاح ✅")

# --- تبويب إدارة قطع الغيار ---

with tabs[1]:
    st.subheader("⚙️ إدارة قطع الغيار")
    with st.form("parts_form"):
        part_name = st.text_input("اسم القطعة")
        price = st.number_input("السعر", min_value=0.0)
        quantity = st.number_input("الكمية", min_value=0)
        part_submitted = st.form_submit_button("إضافة")
        if part_submitted:
            new_part = pd.DataFrame([[part_name, price, quantity]], columns=st.session_state.parts.columns)
            st.session_state.parts = pd.concat([st.session_state.parts, new_part], ignore_index=True)
            st.success("تمت إضافة القطعة ✅")
    st.dataframe(st.session_state.parts)

# --- تبويب سجل الصيانة ---

with tabs[2]:
    st.subheader("📋 سجل العملاء")
    st.dataframe(st.session_state.clients)

    # ✅ زر تصدير إلى Excel
    if not st.session_state.clients.empty:
        import io
        from openpyxl import Workbook

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.clients.to_excel(writer, index=False, sheet_name="Clients")
        st.download_button(
            label="📥 تحميل سجل العملاء كـ Excel",
            data=output.getvalue(),
            file_name="mobix_clients.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
