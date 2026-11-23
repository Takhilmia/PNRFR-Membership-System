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

    photo_x, photo_y, photo_w, photo_h = right - 34 * mm, H - 89 * mm, 30 * mm, 38 * mm
    c.rect(photo_x, photo_y, photo_w, photo_h)
    if photo_bytes:
        try:
            c.drawImage(
                ImageReader(io.BytesIO(photo_bytes)),
                photo_x + 1, photo_y + 1,
                width=photo_w - 2, height=photo_h - 2,
                preserveAspectRatio=True, anchor="c"
            )
        except Exception:
            txt(photo_x + 3, photo_y + photo_h / 2, "Photo", 8)
    else:
        c.setFont("Helvetica", 7)
        c.drawCentredString(photo_x + photo_w / 2, photo_y + photo_h / 2, "Photograph")

    y = H - 98 * mm
    fields = [fields = [
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
    ("Membership Fee (Tk.)", str(data["Membership Fee (Tk.)"])),
]
