from flask import render_template, redirect, url_for, abort, flash, request, send_from_directory
from flask_login import login_required, current_user
from . import main
from .forms import AddNoteForm, ButtonAddContactForm, EditContactForm, SearchForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Role, User, Contact
from ..decorators import admin_required, instructor_required
from manage import app
import time, os, csv
from jinja2 import Environment, FileSystemLoader
from werkzeug.utils import secure_filename
from datetime import datetime

env = Environment(loader=FileSystemLoader('/templates'))

@main.route('/', methods = ['GET', 'POST'])
def index():
    #   Gets each class a user is in into a list. List is iterated in the template
    if current_user.is_user():
        search_form = SearchForm()
        add_contact_form = ButtonAddContactForm()

        #   Send user to search results page with search data (query_obj)
        if search_form.validate_on_submit():
            query = search_form.search.data
            #   Change to search through a list of contact attributes from the database
            query_obj = db.session.query(Contact).filter(Contact.first_name == query)
            return render_template('query_results.html', query_obj = query_obj, search_form = search_form)

        if add_contact_form.validate_on_submit():
            return render_template('add_contact.html', form = EditContactForm)

        return render_template('index.html', search_form = search_form)

    else:
        return render_template('index.html')

@main.route('/query_results', methods = ['GET', 'POST'])
def search():
    search_form = SearchForm()
    query = request.form['text']
    query_obj = db.session.query(Contact).filter(Contact.first_name == query)
    return render_template('query_results.html', query_obj = query_obj, search_form = search_form)

#   Each user's profile view
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user = user)

@main.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    #   Update profile
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))

    #   Display profile
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form)

#   Allows an administrator to make changes to a user's profile
@main.route('/edit-profile/<int:id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    #   If ID is invalid, return a 404
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user = user)

    #   Update a user's profile
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Profile has been updated')
        return redirect(url_for('.user', username = user.username))

    #   Display a user's profile
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form = form, user = user)

@main.route('/add-class', methods = ['GET', 'POST'])
@login_required
@instructor_required
def add_contact():
    form = EditContactForm()
    if form.validate_on_submit():
        contact = Contact()
        contact.first_name = form.first_name.data
        contact.instructor = current_user.name
        contact.middle_name = form.middle_name.data
        contact.last_name = form.last_name.data
        contact.email = form.email.data
        contact.phone_mobile = form.phone_mobile.data
        contact.phone_work = form.phone_work.data
        contact.phone_home = form.phone_home.data
        contact.street_address1 = form.street_address1.data
        contact.unit_number1 = form.unit_number1.data
        contact.city1 = form.city1.data
        contact.state1 = form.state1.data
        contact.zip_code1 = form.zip_code1.data
        db.session.add(contact)
        db.session.add(current_user)
        db.session.commit()
        flash('Contact Added')
        return redirect(url_for('.index'))
    return render_template('edit_profile.html', form = form, user = user)


@main.route('/edit-contact/<contact_name>', methods = ['GET', 'POST'])
@login_required
@instructor_required
def edit_contact(contact_name):
    if contact_name is None:
        about(404)
    #   Display contact's current data in each text field
    contact = Contact.query.filter_by(id = contact_name).first()

    form = EditContactForm()
    form.first_name.data = contact.first_name
    form.middle_name.data = contact.middle_name
    form.last_name.data = contact.last_name
    form.email.data = contact.email
    form.phone_mobile.data = contact.phone_mobile
    form.phone_work.data = contact.phone_work
    form.phone_home.data = contact.phone_home
    form.street_address1.data = contact.street_address1
    form.unit_number1.data = contact.unit_number1
    form.city1.data = contact.city1
    form.state1.data = contact.state1
    form.zip_code1.data = contact.zip_code1

    #   Modify contact's data
    if form.validate_on_submit():
        edit_contact = Contact()
        edit_contact.first_name = form.first_name.data
        edit_contact.middle_name = form.middle_name.data
        edit_contact.last_name = form.last_name.data
        edit_contact.email = form.email.data
        edit_contact.phone_mobile = form.phone_mobile.data
        edit_contact.phone_work = form.phone_work.data
        edit_contact.phone_home = form.phone_home.data
        edit_contact.street_address1 = form.street_address1.data
        edit_contact.unit_number1 = form.unit_number1.data
        edit_contact.city1 = form.city1.data
        edit_contact.state1 = form.state1.data
        edit_contact.zip_code1 = form.zip_code1.data
        db.session.delete(contact)
        db.session.add(edit_contact)
        db.session.add(current_user)
        db.session.commit()

        flash('Contact has been updated')

        return redirect(url_for('.index'))
    return render_template('edit_contact.html', form = form, user = user)

@main.route('/contact/<contact_name>', methods = ['GET', 'POST'])
@login_required
def view_contact(contact_name):
    note_form = AddNoteForm()
    if contact_name is None:
        abort(404)

    contact = Contact.query.filter_by(id = contact_name).first()

    if note_form.validate_on_submit():
        if contact.note1 == None:
            contact.note1 = note_form.note.data
            contact.note1_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif contact.note2 == None:
            contact.note2 = note_form.note.data
            contact.note2_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif contact.note3 == None:
            contact.note3 = note_form.note.data
            contact.note3_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note4 == None:
            contact.note4 = note_form.note.data
            contact.note4_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note5 == None:
            contact.note5 = note_form.note.data
            contact.note5_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note6 == None:
            contact.note6 = note_form.note.data
            contact.note6_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note7 == None:
            contact.note7 = note_form.note.data
            contact.note7_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note8 == None:
            contact.note8 = note_form.note.data
            contact.note8_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note9 == None:
            contact.note9 = note_form.note.data
            contact.note9_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note10 == None:
            contact.note10 = note_form.note.data
            contact.note10_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note11 == None:
            contact.note11 = note_form.note.data
            contact.note11_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note12 == None:
            contact.note12 = note_form.note.data
            contact.note12_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note13 == None:
            contact.note13 = note_form.note.data
            contact.note13_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note14 == None:
            contact.note14 = note_form.note.data
            contact.note14_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note15 == None:
            contact.note15 = note_form.note.data
            contact.note15_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note16 == None:
            contact.note16 = note_form.note.data
            contact.note16_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note17 == None:
            contact.note17 = note_form.note.data
            contact.note17_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note18 == None:
            contact.note18 = note_form.note.data
            contact.note18_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note19 == None:
            contact.note19 = note_form.note.data
            contact.note19_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        elif contact.note20 == None:
            contact.note20 = note_form.note.data
            contact.note20_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.session.add(contact)
        db.session.commit()
        flash("Note Added")
        return redirect(url_for('.view_contact', contact_name = contact_name))
        
    return render_template('view_contact.html', contact = contact, note_form = note_form)

#   Files that are permitted to be uploaded
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload_file():
    if request.method == 'POST':
        #   Check that there is in fact a file
        if 'file' not in request.files:
            flash('No file Selected')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('.uploaded_file', filename = filename))

    return render_template('upload.html')

@main.route('/uploads/<filename>')
@admin_required
def uploaded_file(filename):
    reader = csv.reader(filename)
    with open("uploads/" + filename) as csvfile:
        i = 0

        #   Parse row by row to a database appropriate format
        for row in csvfile:
            unparsed_row = row.split('",')
            input_row = []
            for unparsed_element in unparsed_row:
                parsed_element = unparsed_element[1:]
                input_row.append(parsed_element)

            if input_row[3] != "Contact Type":
                contact = Class()
                contact.gender = input_row[3]
                contact.prefix = input_row[5]
                contact.first_name = input_row[6]
                contact.middle_name = input_row[7]
                contact.last_name = input_row[8]
                contact.suffix = input_row[9]
                contact.title = input_row[14]
                contact.organization = input_row[15]
                contact.occupation = input_row[16]
                contact.birthday = input_row[21]
                contact.note1 = input_row[22]
                contact.phone_mobile = input_row[25]
                contact.phone_home = input_row[23]
                contact.phone_work = input_row[24]
                contact.phone1 = input_row[26]
                contact.phone1_desc = input_row[27]
                contact.phone2 = input_row[28]
                contact.phone2_desc = input_row[29]
                contact.phone3 = input_row[30]
                contact.phone3_desc = input_row[31]
                contact.street_address1 = input_row[32]
                contact.unit_number1 = input_row[33] + " " + input_row[34]
                contact.city1 = input_row[35]
                contact.state1 = input_row[36]
                contact.zip_code1 = input_row[37]
                contact.plus_41 = input_row[38]
                contact.address2 = input_row[41]
                contact.unit_number2 = input_row[42] + " " + input_row[43]
                contact.city2 = input_row[44]
                contact.state2 = input_row[45]
                contact.zip_code2 = input_row[46]
                contact.plus_42 = input_row[47]
                contact.email1 = input_row[72]
                contact.email1_desc = input_row[73]
                contact.email2 = input_row[74]
                contact.email2_desc = input_row[75]
                contact.email3 = input_row[76]
                contact.email3_desc = input_row[77]
                contact.user = current_user.username
                contact.cumulative_donation_total = input_row[144]
                contact.jeff_flake = input_row[145]
                contact.jeff_flake_most_recent_amount = input_row[146]
                contact.jeff_flake_most_recent_date = input_row[147]
                contact.jeff_flake_highest_amount = input_row[148]
                contact.jeff_flake_highest_date = input_row[149]
                contact.jeff_flake_2012 = input_row[150]
                contact.jeff_flake_2016_general = input_row[151]
                contact.jeff_flake_2016_primary = input_row[152]
                contact.jeff_flake_2018 = input_row[153]
                contact.jeff_flake_2018_general = input_row[154]
                contact.lea_marquez_peterson_for_congress_2018 = input_row[155]
                contact.lea_marquez_peterson_for_congress_2018_most_recent_amount = input_row[156]
                contact.lea_marquez_peterson_for_congress_2018_most_recent_date = input_row[157]
                contact.lea_marquez_peterson_for_congress_2018_highest_amount = input_row[158]
                contact.lea_marquez_peterson_for_congress_2018_highest_date = input_row[159]
                contact.lea_marquez_peterson_for_congress_2018_general_2018 = input_row[160]
                contact.lea_marquez_peterson_for_congress_2018_primary_2018 = input_row[161]
                contact.mccain = input_row[162]
                contact.mccain_most_recent_amount = input_row[163]
                contact.mccain_most_recent_date = input_row[164]
                contact.mccain_highest_amount = input_row[165]
                contact.mccain_highest_date = input_row[166]
                contact.mccain_2016 = input_row[167]
                contact.mcsally_for_congress = input_row[168]
                contact.mcsally_for_congress_most_recent_amount = input_row[169]
                contact.mcsally_for_congress_most_recent_date = input_row[170]
                contact.mcsally_for_congress_highest_amount = input_row[171]
                contact.mcsally_for_congress_highest_date = input_row[172]
                contact.mcsally_for_congress_2016 = input_row[173]
                contact.mcsally_for_congress_2018 = input_row[174]
                contact.mcsally_for_senate = input_row[175]
                contact.mcsally_for_senate_most_recent_amount = input_row[176]
                contact.mcsally_for_senate_most_recent_date = input_row[177]
                contact.mcsally_for_senate_highest_amount = input_row[178]
                contact.mcsally_for_senate_highest_date = input_row[179]
                contact.mcsally_for_senate_2018 = input_row[180]
                contact.nrcc = input_row[181]
                contact.nrcc_most_recent_amount = input_row[182]
                contact.nrcc_most_recent_date = input_row[183]
                contact.nrcc_highest_amount = input_row[184]
                contact.nrcc_highest_date = input_row[185]
                contact.nrcc_nrcc = input_row[186]
                contact.victory_fund_for_az_gop = input_row[187]
                contact.victory_fund_for_az_gop_most_recent_amount = input_row[188]
                contact.victory_fund_for_az_gop_most_recent_date = input_row[189]
                contact.victory_fund_for_az_gop_highest_amount = input_row[190]
                contact.victory_fund_for_az_gop_highest_date = input_row[191]
                contact.victory_fund_for_az_gop_click_fund = input_row[192]
                contact.victory_fund_for_nrcc = input_row[193]
                contact.victory_fund_for_nrcc_most_recent_amount = input_row[194]
                contact.victory_fund_for_nrcc_most_recent_date = input_row[195]
                contact.victory_fund_for_nrcc_highest_amount = input_row[196]
                contact.victory_fund_for_nrcc_highest_date = input_row[197]
                contact.victory_fund_for_nrcc_victory_fund_for_nrcc = input_row[198]
                contact.vip_community_events = input_row[199]
                contact.vip_community_events_most_recent_amount = input_row[200]
                contact.vip_community_events_most_recent_date = input_row[201]
                contact.vip_community_events_highest_amount = input_row[202]
                contact.vip_community_events_highest_date = input_row[203]
                contact.vip_community_events_vip_community_events = input_row[204]

                db.session.add(contact)
                db.session.commit()

                #   Limited to 4 at a time for development purposes
                i+=1
                if i == 4:
                    break

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


