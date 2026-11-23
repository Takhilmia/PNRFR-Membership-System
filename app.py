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
