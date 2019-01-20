#   models.py
#   
#   This file creates classes and their attributes and methods used throughout the program and corresponds them to the database.
#   
#   Last Updated: 1.18.2019
#   Written By: Mark Hardy
#   Updated By: Mark Hardy
#   markhardy@email.arizona.edu

### Developer's Note:
### Migrate and update the database by:
### python manage.py db migrate -m "nameofmigrationinquotes"
### python manage.py db upgrade

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import datetime
import hashlib

#############################################################
#   class Role(db.Model)                                    #
#                                                           #
#   This class defines roles for different types of         #
#   users. Different roles contain different permissions.   #
#############################################################
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    #############################################################
    #   def insert_roles()                                      #
    #                                                           #
    #   Creates default roles for users. See Permission         #
    #   class below for definitions.                            #
    #                                                           #
    #   This method should be run in the shell by:              #
    #   python manage.py shell                                  #
    #   Role.insert_roles()                                     #
    #                                                           #
    #   To check current roles:                                 #
    #   Role.query.all()                                        #
    #############################################################
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.MANAGE_CLASSES, True),
            'Instructor': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.MANAGE_CLASSES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
            }

        #   Loop through the roles dictionary and turn each key into 
        #   a Role object with the key's values as attributes
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

#############################################################
#   class Contact(db.Model)                                 #
#                                                           #
#   This class defines each contact related to a user.      #
#   Because it must account for attributes from iDonatePro's#
#   format, there are ton of attributes and not all of them #
#   will be used.                                           #
#############################################################
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key = True)
    gender = db.Column(db.String(64), unique = False, index = True)
    prefix = db.Column(db.String(64), unique = False, index = True)
    first_name = db.Column(db.String(64), unique = False, index = True)
    middle_name = db.Column(db.String(64), unique = False, index = True)
    last_name = db.Column(db.String(64), unique = False, index = True)
    suffix = db.Column(db.String(64), unique = False, index = True)
    email = db.Column(db.String(64), unique = False, index = True)
    title = db.Column(db.String(64), unique = False, index = True)
    organization = db.Column(db.String(64), unique = False, index = True)
    occupation = db.Column(db.String(64), unique = False, index = True)
    birthday = db.Column(db.Date, unique = False, index = True)
    phone_mobile = db.Column(db.String(64), unique = False, index = True)
    phone_work = db.Column(db.String(64), unique = False, index = True)
    phone_home = db.Column(db.String(64), unique = False, index = True)
    phone1 = db.Column(db.String(64), unique = False, index = True)
    phone1_desc = db.Column(db.String(64), unique = False, index = True)
    phone2 = db.Column(db.String(64), unique = False, index = True)
    phone2_desc = db.Column(db.String(64), unique = False, index = True)
    phone3 = db.Column(db.String(64), unique = False, index = True)
    phone3_desc = db.Column(db.String(64), unique = False, index = True)
    street_address1 = db.Column(db.String(64), unique = False, index = True)
    unit_number1 = db.Column(db.String(64), unique = False, index = True)
    city1 = db.Column(db.String(64), unique = False, index = True)
    state1 = db.Column(db.String(64), unique = False, index = True)
    zip_code1 = db.Column(db.String(64), unique = False, index = True)
    plus_41 = db.Column(db.String(64), unique = False, index = True)
    street_address2 = db.Column(db.String(64), unique = False, index = True)
    unit_number2 = db.Column(db.String(64), unique = False, index = True)
    city2 = db.Column(db.String(64), unique = False, index = True)
    state2 = db.Column(db.String(64), unique = False, index = True)
    zip_code2 = db.Column(db.String(64), unique = False, index = True)
    plus_42 = db.Column(db.String(64), unique = False, index = True)
    email1 = db.Column(db.String(64), unique = False, index = True)
    email1_desc = db.Column(db.String(64), unique = False, index = True)
    email2 = db.Column(db.String(64), unique = False, index = True)
    email2_desc = db.Column(db.String(64), unique = False, index = True)
    email3 = db.Column(db.String(64), unique = False, index = True)
    email3_desc = db.Column(db.String(64), unique = False, index = True)
    cumulative_donation_total = db.Column(db.String(64), unique = False, index = True)
    jeff_flake = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_2012 = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_2016_general = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_2016_primary = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_2018 = db.Column(db.String(64), unique = False, index = True)
    jeff_flake_2018_general = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018 = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018_highest_amount = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018_highest_date = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018_general_2018 = db.Column(db.String(64), unique = False, index = True)
    lea_marquez_peterson_for_congress_2018_primary_2018 = db.Column(db.String(64), unique = False, index = True)
    mccain = db.Column(db.String(64), unique = False, index = True)
    mccain_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    mccain_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    mccain_highest_amount = db.Column(db.String(64), unique = False, index = True)
    mccain_highest_date = db.Column(db.String(64), unique = False, index = True)
    mccain_2016 = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress_highest_amount = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress_highest_date = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress_2016 = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_congress_2018 = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_senate = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_senate_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_senate_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_senate_highest_amount = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_senate_highest_date = db.Column(db.String(64), unique = False, index = True)
    mcsally_for_senate_2018 = db.Column(db.String(64), unique = False, index = True)
    nrcc = db.Column(db.String(64), unique = False, index = True)
    nrcc_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    nrcc_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    nrcc_highest_amount = db.Column(db.String(64), unique = False, index = True)
    nrcc_highest_date = db.Column(db.String(64), unique = False, index = True)
    nrcc_nrcc = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_az_gop = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_az_gop_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_az_gop_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_az_gop_highest_amount = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_az_gop_highest_date = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_az_gop_click_fund = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_nrcc = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_nrcc_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_nrcc_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_nrcc_highest_amount = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_nrcc_highest_date = db.Column(db.String(64), unique = False, index = True)
    victory_fund_for_nrcc_victory_fund_for_nrcc = db.Column(db.String(64), unique = False, index = True)
    vip_community_events = db.Column(db.String(64), unique = False, index = True)
    vip_community_events_most_recent_amount = db.Column(db.String(64), unique = False, index = True)
    vip_community_events_most_recent_date = db.Column(db.String(64), unique = False, index = True)
    vip_community_events_highest_amount = db.Column(db.String(64), unique = False, index = True)
    vip_community_events_highest_date = db.Column(db.String(64), unique = False, index = True)
    vip_community_events_vip_community_events = db.Column(db.String(64), unique = False, index = True)
    note1 = db.Column(db.Text)
    note1_stamp = db.Column(db.DateTime)
    note2 = db.Column(db.Text)
    note2_stamp = db.Column(db.DateTime)
    note3 = db.Column(db.Text)
    note3_stamp = db.Column(db.DateTime)
    note4 = db.Column(db.Text)
    note4_stamp = db.Column(db.DateTime)
    note5 = db.Column(db.Text)
    note5_stamp = db.Column(db.DateTime)
    note6 = db.Column(db.Text)
    note6_stamp = db.Column(db.DateTime)
    note7 = db.Column(db.Text)
    note7_stamp = db.Column(db.DateTime)
    note8 = db.Column(db.Text)
    note8_stamp = db.Column(db.DateTime)
    note9 = db.Column(db.Text)
    note9_stamp = db.Column(db.DateTime)
    note10 = db.Column(db.Text)
    note10_stamp = db.Column(db.DateTime)
    note11 = db.Column(db.Text)
    note11_stamp = db.Column(db.DateTime)
    note12 = db.Column(db.Text)
    note12_stamp = db.Column(db.DateTime)
    note13 = db.Column(db.Text)
    note13_stamp = db.Column(db.DateTime)
    note14 = db.Column(db.Text)
    note14_stamp = db.Column(db.DateTime)
    note15 = db.Column(db.Text)
    note15_stamp = db.Column(db.DateTime)
    note16 = db.Column(db.Text)
    note16_stamp = db.Column(db.DateTime)
    note17 = db.Column(db.Text)
    note17_stamp = db.Column(db.DateTime)
    note18 = db.Column(db.Text)
    note18_stamp = db.Column(db.DateTime)
    note19 = db.Column(db.Text)
    note19_stamp = db.Column(db.DateTime)
    note20 = db.Column(db.Text)
    note20_stamp = db.Column(db.DateTime)

    #############################################################
    #   def getXDonationData(self, key)                         #
    #                                                           #
    #   These are all getter methods used to retrieve           #
    #   donations made by a specific contact to a given         #
    #   campaign.                                               #
    #                                                           #
    #   Argument 1 - key(String): The specific donation being   # 
    #                             requested.                    #
    #                                                           #
    #   Returns: The donation amount relative to the requested  #
    #            donation as a String.                          #
    #############################################################
    def getJeffFlakeDonationData(self, key):
        donation_data = {
            "Jeff Flake: " : self.jeff_flake,
            "Jeff Flake 2012: " : self.jeff_flake_2012,
            "Jeff Flake 2018: " : self.jeff_flake_2018,
            "Jeff Flake 2016 General: " : self.jeff_flake_2016_general,
            "Jeff Flake 2016 Primary: " : self.jeff_flake_2016_primary,
            "Jeff Flake 2018 General: " : self.jeff_flake_2018_general,
            "Jeff Flake Most Recent Amount: " : self.jeff_flake_most_recent_amount,
            "Jeff Flake Most Recent Date: " : self.jeff_flake_most_recent_date
        }
        return donation_data.get(key)

    def getLeaMarquezPetersonForCongress2018DonationData(self, key):
        donation_data = {
            "Lea Marquez Peterson For Congress 2018: " : self.lea_marquez_peterson_for_congress_2018,
            "Lea Marquez Peterson For Congress 2018 Most Recent Amount: " : self.lea_marquez_peterson_for_congress_2018_most_recent_amount,
            "Lea Marquez Peterson For Congress 2018 Most Recent Date: " : self.lea_marquez_peterson_for_congress_2018_most_recent_date,
            "Lea Marquez Peterson For Congress 2018 Highest Amount: " : self.lea_marquez_peterson_for_congress_2018_highest_amount,
            "Lea Marquez Peterson For Congress 2018 Highest Date: " : self.lea_marquez_peterson_for_congress_2018_most_recent_date,
            "Lea Marquez Peterson For Congress Primary 2018: " : self.lea_marquez_peterson_for_congress_2018_primary_2018,
            "Lea Marquez Peterson For Congress General 2018: " : self.lea_marquez_peterson_for_congress_2018_general_2018
        }
        return donation_data.get(key)

    def getMcCainDonationData(self, key):
        donation_data = {
            "McCain: " : self.mccain,
            "McCain Most Recent Amount: " : self.mccain_most_recent_amount,
            "McCain Most Recent Date: " : self.mccain_most_recent_date,
            "McCain Highest Amount: " : self.mccain_highest_amount,
            "McCain Highest Date: " : self.mcsally_for_congress_highest_date,
            "McCain 2016: " : self.mccain_2016
        }
        return donation_data.get(key)

    def getMcSallyForCongressDonationData(self, key):
        donation_data = {
            "McSally For Congress: " : self.mcsally_for_congress,
            "McSally For Congress Most Recent Amount: " : self.mcsally_for_congress_most_recent_amount,
            "McSally For Congress Most Recent Date: " : self.mcsally_for_congress_highest_date,
            "McSally For Congress Highest Amount: " : self.mcsally_for_congress_highest_amount,
            "McSally For Congress Highest Date: " : self.mcsally_for_congress_highest_date,
            "McSally For Congress 2016: " : self.mcsally_for_congress_2016,
            "McSally For Congress 2018: " : self.mcsally_for_congress_2018
        }
        return donation_data.get(key)

    def getMcSallyForSenateDonationData(self, key):
        donation_data = {
            "McSally For Senate: " : self.mcsally_for_senate,
            "McSally For Senate 2018: " : self.mcsally_for_senate_2018,
            "McSally For Senate Most Recent Amount: " : self.mcsally_for_senate_most_recent_amount,
            "McSally For Senate Most Recent Date: " : self.mcsally_for_senate_most_recent_date,
            "McSally For Senate Highest Amount: " : self.mcsally_for_senate_highest_amount,
            "McSally For Senate Highest Date: " : self.mcsally_for_senate_highest_date
        }
        return donation_data.get(key)

    def getNRCCDonationData(self, key):
        donation_data = {
            "NRCC: " : self.nrcc,
            "NRCC (NRCC): " : self.nrcc_nrcc,
            "NRCC Most Recent Amount: " : self.nrcc_most_recent_amount,
            "NRCC Most Recent Date: " : self.nrcc_most_recent_date,
            "NRCC Highest Amount: " : self.nrcc_highest_amount,
            "NRCC Highest Date: " : self.nrcc_highest_date
        }
        return donation_data.get(key)

    def getVictoryFundForAZGOPDonationData(self, key):
        donation_data = {
            "Victory Fund For AZGOP: " : self.victory_fund_for_az_gop,
            "Victory Fund For AZGOP Most Recent Amount: " : self.victory_fund_for_az_gop_most_recent_amount,
            "Victory Fund For AZGOP Most Recent Date: " : self.victory_fund_for_az_gop_most_recent_date,
            "Victory Fund For AZGOP Highest Amount: " : self.victory_fund_for_az_gop_highest_amount,
            "Victory Fund For AZGOP Highest Date: " : self.victory_fund_for_az_gop_highest_date,
            "Victory Fund For AZGOP Click Fund: " : self.victory_fund_for_az_gop_click_fund
        }
        return donation_data.get(key)

    def getVictoryFundForNRCCDonationData(self, key):
        donation_data = {
            "Victory Fund For NRCC: " : self.victory_fund_for_nrcc,
            "Victory Fund For NRCC Most Recent Amount: " : self.victory_fund_for_nrcc_most_recent_amount,
            "Victory Fund For NRCC Most Recent Date: " : self.victory_fund_for_nrcc_most_recent_date,
            "Victory Fund For NRCC Highest Amount: " : self.victory_fund_for_nrcc_highest_amount,
            "Victory Fund For NRCC Highest Date: " : self.victory_fund_for_nrcc_highest_date,
            "Victory Fund For NRCC (Victory Fund For NRCC): " : self.victory_fund_for_nrcc_victory_fund_for_nrcc
        }
        return donation_data.get(key)

    def getVIPCommunityEventsDonationData(self, key ):
        donation_data = {
            "VIP Community Events: " : self.vip_community_events,
            "VIP Community Events Most Recent Amount: " : self.vip_community_events_most_recent_amount,
            "VIP Community Events Most Recent Date: " : self.vip_community_events_most_recent_date,
            "VIP Community Events Highest Amount: " : self.vip_community_events_highest_amount,
            "VIP Community Events Highest Date: " : self.vip_community_events_highest_date,
            "VIP Community Events (VIP Community Events): " : self.vip_community_events_vip_community_events
        }
        return donation_data.get(key)


    #############################################################
    #   def checkForNone(self, obj)                             #
    #                                                           #
    #   Checks if an object, presumably pulled from the database#
    #   is empty. This need to be re-worked to cover the        #
    #   hasDonated() methods below.                             #
    #                                                           #
    #   Argument 1 - Any Object                                 #
    #                                                           #
    #   Returns: Boolean                                        #
    #############################################################
    def checkForNone(self, obj):
        return obj != None and obj != ""

    def getNotes(self):
        #   Create a list/dict in the database for all notes later and parse in helper methods
        return [self.note1, self.note2, self.note3, self.note4, self.note5, self.note6, self.note7, self.note8, self.note9, self.note10, self.note11, self.note12, self.note13, self.note14, self.note15, self.note16, self.note17, self.note18, self.note19, self.note20]

    #   To be implemented when I convert notes to one hashmap in the database
    def getNewNoteIndex(self):
        # Handle for full notes by changing getNotes() and allowing unlimited
        notes = self.getNotes()
        for note in notes:
            if note == None:
                return notes.index(note) + 1
        return 0

    #############################################################
    #   def hasDonatedToX(self)                                 #
    #                                                           #
    #   Checks whether or not the contact has donated to a given#
    #   campaign.                                               #
    #                                                           #
    #   Returns: Boolean                                        #
    #############################################################
    def getCumulativeDonationTotal(self):
        return self.cumulative_donation_total

    def hasDonated(self):
        return self.cumulative_donation_total != "$0.00" and self.cumulative_donation_total != None

    def hasDonatedToJeffFlake(self):
        return self.jeff_flake != "$0.00" and self.jeff_flake != None

    def hasDonatedToJeffFlake2012(self):
        return self.jeff_flake_2012 != "$0.00" and self.jeff_flake_2012 != None

    def hasDonatedToJeffFlake2016General(self):
        return self.jeff_flake_2016_general != "$0.00" and self.jeff_flake_2016_general != None

    def hasDonatedToJeffFlake2016Primary(self):
        return self.jeff_flake_2016_primary != "$0.00" and self.jeff_flake_2016_primary != None

    def hasDonatedToJeffFlake2018(self):
        return self.jeff_flake_2018 != "$0.00" and self.jeff_flake_2018 != None

    def hasDonatedToJeffFlake2018General(self):
        return self.jeff_flake_2018_general != "$0.00" and self.jeff_flake_2018_general != None

    def hasDonatedToLeaMarquezPetersonForCongress(self):
        return self.lea_marquez_peterson_for_congress_2018 != "$0.00" and self.lea_marquez_peterson_for_congress_2018 != None

    def getLeaMarquezPetersonForCongress2018(self):
        return self.lea_marquez_peterson_for_congress_2018

    def hasDonatedToLeaMarquezPetersonForCongress2018Primary(self):
        return self.lea_marquez_peterson_for_congress_2018_primary_2018 != "$0.00" and self.lea_marquez_peterson_for_congress_2018_primary_2018 != None

    def hasDonatedToLeaMarquezPetersonForCongress2018General(self):
        return self.lea_marquez_peterson_for_congress_2018_general_2018 != "$0.00" and self.lea_marquez_peterson_for_congress_2018_general_2018 != None

    def hasDonatedToMcCain(self):
        return self.mccain != "$0.00" and self.mccain != None

    def hasDonatedToMcCain2016(self):
        return self.mccain_2016 != "$0.00" and self.mccain_2016 != None

    def hasDonatedToMcSallyForCongress(self):
        return self.mcsally_for_congress != "$0.00" and self.mcsally_for_congress != None

    def hasDonatedToMcSallyForSenate(self):
        return self.mcsally_for_senate != "$0.00" and self.mcsally_for_senate != None

    def hasDonatedToMcSallyForSenate2018(self):
        return self.mcsally_for_senate_2018 != "$0.00" and self.mcsally_for_senate_2018 != None

    def hasDonatedToNRCC(self):
        return self.nrcc != "$0.00" and self.nrcc != None

    def hasDonatedToNRCCNRCC(self):
        return self.nrcc_nrcc != "$0.00" and self.nrcc_nrcc != None

    def hasDonatedToVictoryFundForAZGOP(self):
        return self.victory_fund_for_az_gop != "$0.00" and self.victory_fund_for_az_gop != None

    def hasDonatedToVictoryFundForNRCC(self):
        return self.victory_fund_for_nrcc != "$0.00" and self.victory_fund_for_nrcc != None

    def hasDonatedToVIPCommunityEvents(self):
        return self.vip_community_events != "$0.00" and self.vip_community_events != None

    def hasDonatedToVIPCommunityEventsVIPCommunityEvents(self):
        return self.vip_community_events_vip_community_events != "$0.00" and self.vip_community_events_vip_community_events != None


#############################################################
#   class User(UserMixin, db.Model)                         #
#                                                           #
#   This is the class for each user containing data and     #
#   methods for authentication and user profiles.           #
#############################################################
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default = False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    #######################################################################
    ### For later use:                                                  ###
    ### Handling connecting users to contacts in terminal..             ###
    ### The classes relationship above works like a list                ###
    ### For user 'u' and contact 'c'..                                  ###
    ### Add user to class with s.classes.append(u), db.session.add(u)   ###
    ### Queries: u.classes.all(), c.users.all()                         ###
    ### Drop user: u.classes.remove(c)                                  ###
    #######################################################################
    
    def __init__(self, **kwargs):
        #   Figures out if registration email is connected to admin email and if so,
        #   gives admin. Otherwise, default permissions
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default = True).first()

    ##############################################################
    #################### USER AUTHENTICATION #####################
    ##############################################################
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration = 3600):
        #   CHANGE to ['SECRET_KEY'] later
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        #   dumps() creates cryptographic signature and serializes it
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        #   Verifies token is valid and returns True if it is
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    ### Change email/password ###

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email

        #   Recalculate avatar's hash when user's email is changed
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    ##############################################################
    ##############################################################
    ##############################################################

    #   Report pings when user is logged in and report to database
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    #############################################################
    #   def Can(self, permissions)                              #
    #                                                           #
    #   Helper method that determines if the current user has a #
    #   a specific permission. Used elsewhere in the program    #
    #   for security.                                           #
    #                                                           #
    #   Argument 1 - permissions: The permission that the       #
    #                program is checking the user for.          #
    #                                                           #
    #   Returns: Boolean                                        #
    #############################################################
    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_instructor(self):
        return self.can(Permission.MANAGE_CLASSES)

    def is_user(self):
        return True
        
    #############################################################
    #   def gravatar(size, default, rating)                     #
    #                                                           #
    #   Standard method for retrieving a gravatar user avatar by#
    #   checking the user's email with Gravatar and getting a   #
    #   hash of its URL path back if they have one set up.      #
    #   The user's avatar image can be accessed by the URL.     #
    #                                                           #
    #   Argument 1 - Integer: Size we want the gravatar to be.  #
    #   Argument 2 - String: Default gravatar if user has not   #
    #                set one up.                                #
    #   Argument 3 - String: We only want G rateds displayed.   #
    #                                                           #
    #   Returns: String of returned URL                         #
    #############################################################
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
    
    def __repr__(self):
        return '<User %r>' % self.username

#############################################################
#   class AnonymousUserMixin(AnonymousUserMixin)            #
#                                                           #
#   A user who is not logged in and/or has no account.      #
#############################################################
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def is_instructor(self):
        return False

    def is_user(self):
        return False

class Permission:
    #   Change later
    FOLLOW = 0x01
    COMMENT = 0x02
    MANAGE_CLASSES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser
