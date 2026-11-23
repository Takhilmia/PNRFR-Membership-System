import io
import re
import uuid
import base64
from datetime import datetime, date

import requests
import streamlit as st

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


APP_TITLE = "PNRFR Membership Registration"
ORG = "Professor Nazrul Rheumatology Foundation & Research"
ORG_SHORT = "PNRFR"
ADDRESS = "Room No. 357, 2nd Floor, Block B, House No. 17, Road No. 8, Dhanmondi, Dhaka"
PHONE = "+88 01751-872727"
EMAIL = "islam1nazrul@gmail.com"

# Google Apps Script Web App URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzWyi8UG10MQbtfExKQqMmpgoJB-aeUcveTHKsak6d31J6B571AGqQdNZhA-GR34Wvf/exec"

GOOGLE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1alZ37gXdiKHZfsv4KOtN9ChAoRgQjjMdZbuR3JeUXFY/edit"
)

CATEGORIES = {
    "Diamond (Tk. 200,000)": 200000,
    "Platinum (Tk. 100,000)": 100000,
    "Gold (Tk. 50,000)": 50000,
    "Silver (Tk. 25,000)": 25000,
    "Bronze (Tk. 10,000)": 10000,
    "General Member (Tk. 3,000 to below Tk. 10,000)": 3000,
}

st.set_page_config(page_title=APP_TITLE, page_icon="📋", layout="centered")


def make_pdf(data, photo_bytes=None, signature_bytes=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4
    left, right = 18 * mm, W - 18 * mm

    def txt(x, y, value, size=9, bold=False):
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, str(value)[:140])

    def line(x1, y1, x2, y2):
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.55)
        c.line(x1, y1, x2, y2)

    c.setTitle("PNRFR Membership Registration Form")
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, H - 20 * mm, ORG)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W / 2, H - 26 * mm, "(PNRFR)")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(W / 2, H - 32 * mm, ADDRESS)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H - 43 * mm, "MEMBERSHIP REGISTRATION FORM")
    line(left, H - 47 * mm, right, H - 47 * mm)

    txt(left, H - 57 * mm, f"Application ID: {data['Application ID']}", 8, True)
    txt(left, H - 65 * mm, "Select Membership Category:", 9, True)
    c.setFont("Helvetica", 8)
    c.drawString(left, H - 72 * mm, data["Membership Category"])

    photo_x = right - 34 * mm
    photo_y = H - 89 * mm
    photo_w = 30 * mm
    photo_h = 38 * mm
    c.rect(photo_x, photo_y, photo_w, photo_h)
        if photo_bytes:
        try:
            c.drawImage(
                ImageReader(io.BytesIO(photo_bytes)),
                photo_x + 1,
                photo_y + 1,
                width=photo_w - 2,
                height=photo_h - 2,
                preserveAspectRatio=True,
                anchor="c",
            )
        except Exception:
            txt(photo_x + 3, photo_y + photo_h / 2, "Photo", 8)
    else:
        c.setFont("Helvetica", 7)
        c.drawCentredString(
            photo_x + photo_w / 2,
            photo_y + photo_h / 2,
            "Photograph",
        )

    y = H - 98 * mm
    fields = [
        ("Name", data["Name"]),
        ("Date of Birth", data["Date of Birth"]),
        ("NID No.", data["NID No."]),
        ("Father's Name", data["Father's Name"]),
        ("Mother's Name", data["Mother's Name"]),
        ("Permanent Address", data["Permanent Address"]),
        ("Present Address", data["Present Address"]),
        ("Contact No. 1", data["Contact No. 1"]),
        ("Contact No. 2", data["Contact No. 2"]),
        ("E-mail Address", data["Email Address"]),
        ("Membership Fee (Tk.)", f"{data['Membership Fee (Tk.)']:,}"),
    ]

    for label, value in fields:
        txt(left, y, label + ":", 8, True)
        c.setFont("Helvetica", 8)
        max_chars = 105 if label.endswith("Address") else 90
        val = str(value)
        if len(val) > max_chars:
            val = val[: max_chars - 3] + "..."
        c.drawString(left + 43 * mm, y, val)
        line(left + 43 * mm, y - 2, right - 1 * mm, y - 2)
        y -= 8 * mm

    txt(left, y - 2 * mm, "Terms and conditions applied.", 8)
    txt(left, y - 13 * mm, "Date: " + datetime.now().strftime("%d-%m-%Y"), 8)
    txt(right - 65 * mm, y - 13 * mm, "Signature of the applicant", 8, True)

    if signature_bytes:
        try:
            c.drawImage(
                ImageReader(io.BytesIO(signature_bytes)),
                right - 58 * mm,
                y - 34 * mm,
                width=38 * mm,
                height=16 * mm,
                preserveAspectRatio=True,
                anchor="c",
            )
        except Exception:
            pass
                 line(right - 68 * mm, y - 36 * mm, right - 5 * mm, y - 36 * mm)

    cut_y = 75 * mm
    c.setDash(3, 2)
    line(left, cut_y, right, cut_y)
    c.setDash()
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W / 2, cut_y - 9 * mm, ORG)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, cut_y - 15 * mm, "MEMBERSHIP FEE RECEIPT")
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, cut_y - 20 * mm, ADDRESS + " | Ph: " + PHONE)

    txt(left, cut_y - 31 * mm, "Received with thanks from:", 8, True)
    txt(left + 42 * mm, cut_y - 31 * mm, data["Name"], 8)
    line(left + 42 * mm, cut_y - 33 * mm, right, cut_y - 33 * mm)
    txt(left, cut_y - 41 * mm, "Membership Category:", 8, True)
    txt(left + 42 * mm, cut_y - 41 * mm, data["Membership Category"], 8)
    txt(left, cut_y - 51 * mm, "Amount (Taka):", 8, True)
    txt(left + 42 * mm, cut_y - 51 * mm, f"{data['Membership Fee (Tk.)']:,}", 8)
    txt(left, cut_y - 61 * mm, "Date: " + datetime.now().strftime("%d-%m-%Y"), 8)
    txt(left, cut_y - 69 * mm, "Applicant's Signature", 7, True)
    txt(right - 55 * mm, cut_y - 69 * mm, "Chairman's Signature", 7, True)
    line(left, cut_y - 65 * mm, left + 45 * mm, cut_y - 65 * mm)
    line(right - 60 * mm, cut_y - 65 * mm, right, cut_y - 65 * mm)

    c.save()
    return buffer.getvalue()


def submit_application(data, photo, signature):
    app_id = (
        "PNRFR-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:6].upper()
    )
    data["Application ID"] = app_id

    try:
        photo_bytes = photo.getvalue() if photo else None
        signature_bytes = signature.getvalue() if signature else None
        pdf = make_pdf(data, photo_bytes, signature_bytes)

        def encode_file(file_bytes):
            if file_bytes is None:
                return None
            return base64.b64encode(file_bytes).decode("utf-8")

        payload = {
            "action": "submit",
            "application": {
                **data,
                "Submitted At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "Submitted",
            },
            "files": {
                "photo": {
                    "base64": encode_file(photo_bytes),
                    "mimeType": photo.type if photo else "",
                    "fileName": photo.name if photo else "",
                },
                "signature": {
                    "base64": encode_file(signature_bytes),
                    "mimeType": signature.type if signature else "",
                    "fileName": signature.name if signature else "",
                },
                "pdf": {
                    "base64": encode_file(pdf),
                    "mimeType": "application/pdf",
                    "fileName": f"{app_id}_Membership_Form.pdf",
                },
            },
        }
        if result.get("status") != "success":
            st.error(result.get("message", "Google Sheets submission failed."))
            return False

        st.session_state["submitted_pdf"] = pdf
        st.session_state["submitted_id"] = app_id
        return True

    except Exception as e:
        st.error(f"Submission failed: {e}")
        return False


def render_form():
    st.title("PNRFR")
    st.subheader("Membership Registration Form")
    st.caption(ORG)
    st.write(ADDRESS)
    st.write(
        "Please complete all required fields. The submitted information "
        "will be used for membership registration."
    )

    with st.form("pnrfr_registration", clear_on_submit=False):
        category = st.selectbox("Select Membership Category", list(CATEGORIES.keys()))
        st.caption(f"Standard membership fee: Tk. {CATEGORIES[category]:,}")
        name = st.text_input("Name *")
        dob = st.date_input(
            "Date of Birth",
            value=None,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
        )
        nid = st.text_input("NID No.")
        father = st.text_input("Father's Name")
        mother = st.text_input("Mother's Name")
        permanent = st.text_area("Permanent Address *")
        present = st.text_area("Present Address *")
        c1 = st.text_input("Contact No. 1 *")
        c2 = st.text_input("Contact No. 2")
        email = st.text_input("E-mail Address *")
        fee = st.number_input(
            "Membership Fee (Tk.)",
            min_value=3000,
            max_value=200000,
            value=CATEGORIES[category],
            step=500,
        )
        photo = st.file_uploader(
            "Recent Colour Photograph (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
        )
        signature = st.file_uploader(
            "Applicant's Signature (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
        )
        agree = st.checkbox(
            "I confirm that the information provided above is correct."
        )
        submitted = st.form_submit_button(
            "Submit Membership Application",
            use_container_width=True,
        )

    if submitted:
        if (
            not name.strip()
            or not permanent.strip()
            or not present.strip()
            or not c1.strip()
            or not email.strip()
        ):
            st.error("Please complete all required fields marked with *.")
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
            st.error("Please enter a valid email address.")
        elif not agree:
            st.error("Please confirm the information before submitting.")
        elif not photo:
            st.error("Please upload your recent colour photograph.")
        else:
            application_data = {
                "Application ID": "",
                "Submitted At": "",
                "Membership Category": category,
                "Membership Fee (Tk.)": int(fee),
                "Name": name.strip(),
                "Date of Birth": dob.strftime("%d-%m-%Y") if dob else "",
                "NID No.": nid.strip(),
                "Father's Name": father.strip(),
                "Mother's Name": mother.strip(),
                "Permanent Address": permanent.strip(),
                "Present Address": present.strip(),
                "Contact No. 1": c1.strip(),
                "Contact No. 2": c2.strip(),
                "Email Address": email.strip(),
            }

            with st.spinner("Submitting your application..."):
                success = submit_application(application_data, photo, signature)

            if success:
                st.success(
                    "Application submitted successfully. "
                    f"Your Application ID is {st.session_state['submitted_id']}."
                )
                st.download_button(
                    "Download your Membership Form PDF",
                    data=st.session_state["submitted_pdf"],
                    file_name=f"{st.session_state['submitted_id']}_Membership_Form.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )


def render_admin():
    st.title("PNRFR Admin")
    st.info("Membership applications are stored in the connected Google Sheet.")
    st.markdown(f"[Open PNRFR Membership Google Sheet]({GOOGLE_SHEET_URL})")


st.markdown(
    """
    <style>
    .block-container {max-width: 850px; padding-top: 2rem;}
    h1, h2 {color: #173b63;}
    div.stButton > button, div.stFormSubmitButton > button {
        background:#173b63;color:white;border-radius:7px;
    }
