
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Mobix - إدارة الورشة", layout="wide")
st.title("🔧 Mobix | نظام إدارة الورشة")
st.markdown("مرحبًا بك في نظام إدارة ورشة Mobix")

# إعداد قواعد البيانات
if 'clients' not in st.session_state:
    st.session_state.clients = pd.DataFrame(columns=[
        'الاسم', 'رقم الموبايل', 'نوع العربية', 'VIN',
        'الخدمة المطلوبة', 'تاريخ الزيارة', 'موعد الصيانة القادمة'
    ])

if 'parts' not in st.session_state:
    st.session_state.parts = pd.DataFrame(columns=['اسم القطعة', 'السعر', 'الكمية'])

if 'invoices' not in st.session_state:
    st.session_state.invoices = []

# علامات التبويب
tabs = st.tabs(["تسجيل عميل", "إدارة قطع الغيار", "سجل الصيانة"])

# تبويب تسجيل العميل
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
            st.success("تم تسجيل العميل بنجاح!")

# تبويب قطع الغيار
with tabs[1]:
    st.subheader("🛠️ إدارة قطع الغيار")
    with st.form("part_form"):
        part_name = st.text_input("اسم القطعة")
        part_price = st.number_input("السعر", min_value=0.0)
        part_qty = st.number_input("الكمية", min_value=0)
        add_part = st.form_submit_button("إضافة")
        if add_part:
            new_part = pd.DataFrame([[part_name, part_price, part_qty]],
                                    columns=st.session_state.parts.columns)
            st.session_state.parts = pd.concat([st.session_state.parts, new_part], ignore_index=True)
            st.success("تمت إضافة القطعة بنجاح!")

    st.dataframe(st.session_state.parts)

# تبويب سجل الصيانة
with tabs[2]:
    st.subheader("📋 سجل العملاء")
    st.dataframe(st.session_state.clients)
