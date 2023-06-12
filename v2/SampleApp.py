# GENERAL INFORMATION
## This is the place where general information is written
## Every new line will be numbered as a new line
## The general information section describes the general pupose of the application
## This is how you add an image to your help file <br><img src='image.jpeg'>

# HOW TO USE
## Download the application
## Set all the settings according to PART V
## Run App_Name.exe file

from PersonalAssistant import *
from PersonalAssistant import FIELD
import os
import sqlite3

class main:
    def __init__(self):
        # set up Personal Assistant
        self.pa = PersonalAssistant(__file__, "Sample App", "2.0")
        
        # connect to database
        self.db_location = self.pa.get_setting("Database location")
        self.con = sqlite3.connect(self.db_location)
        self.cur = self.con.cursor()

        # create database tables
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(50), user_name VARCHAR(50), phone VARCHAR(50), sex VARCHAR(50), birth_date VARCHAR(50), photo VARCHAR(50))")
        self.con.commit()

        # display database
        self.display_database()

        # MAIN MENU
        self.pa.main_menu["ADD A USER"] = self.add
        self.pa.main_menu["EDIT A USER"] = self.edit
        self.pa.main_menu["DELETE A USER"] = self.delete
        self.pa.main_menu["EXPORT"] = self.Export
        self.pa.main_menu["IMPORT"] = self.Import
        self.pa.main_menu["EDIT SCRIPT"] = self.edit_script
        self.pa.main_menu["RUN SCRIPT"] = self.run_script
        self.pa.display_menu()

        # run GUI
        self.pa.run()

    def display_database(self):
        self.pa.display_database(self.db_location, "users", "user_id")

    def add(self):
        ## ADD A USER
        #- This will allow you to add a new user to the database by filling a form
        #- At the end of the form press Y to submit the form and the new user will be added to the database
        # calculate last id
        self.cur.execute("SELECT * FROM users")
        fetched_values = self.cur.fetchall()
        if len(fetched_values) == 0:
            last_id = 0
        else:
            last_id = int(fetched_values[-1][0])

        # setup a form to fill
        fields = {}
        fields["user_id"] = FIELD("UserID", NUMBER, last_id+1)
        fields["user_id"].disabled = True
        fields["user_name"] = FIELD("Name", TEXT, "Anonymous")
        fields["phone"] = FIELD("Phone", TEXT, "000-0000000")
        sexes = ("M", "F", "Not Specified")
        fields["sex"] = FIELD("Sex", CHOOSE, sexes[2])
        fields["sex"].options = sexes
        fields["birth_date"] = FIELD("Birth Date", DATE, self.pa.today())
        fields["photo"] = FIELD("Photo", FILE, "")
        fields["photo"].filetypes = [("Images","*.img"), ("PNG","*.png"), ("Bitmap",".bmp"), ("JPEG", ".jpeg"), ("All Files","*.*")]
        form = self.pa.form(fields)

        if form:
            self.cur.execute("INSERT INTO users (user_id, user_name, phone, sex, birth_date, photo) VALUES ('"+str(form["user_id"])+"','"+form["user_name"]+"','"+str(form["phone"])+"','"+form["sex"]+"','"+form["birth_date"]+"','"+form["photo"]+"')")
            self.con.commit()
            self.pa.print("New user added successfully!")
        else:
            self.pa.error("New user was NOT added to the database")
        
        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()

    def edit(self):
        ## EDIT A USER
        #- This will allow you to edit an existing user by filling a form
        #- At the end of the form press Y to submit the form and the user information will be edited
        # get user id to edit
        user_id = self.pa.input("Select user ID to edit")
        self.cur.execute("SELECT * FROM users WHERE user_id = '"+user_id+"'")
        fetched_values = self.cur.fetchall()
        if len(fetched_values) == 0:
            self.pa.error("User ID is not in the database!")
        else:
            # get default values
            data = fetched_values[0]
            user_id = data[0]
            user_name = data[1]
            phone = data[2]
            sex = data[3]
            birth_date = data[4]
            photo = data[5]

            # setup a form to fill
            fields = {}
            fields["user_id"] = FIELD("UserID", NUMBER, user_id)
            fields["user_id"].disabled = True
            fields["user_name"] = FIELD("Name", TEXT, user_name)
            fields["phone"] = FIELD("Phone", TEXT, phone)
            sexes = ("M", "F", "Not Specified")
            fields["sex"] = FIELD("Sex", CHOOSE, sex)
            fields["sex"].options = sexes
            fields["birth_date"] = FIELD("Birth Date", DATE, birth_date)
            fields["photo"] = FIELD("Photo", FILE, photo)
            fields["photo"].filetypes = [("Images","*.img"), ("PNG","*.png"), ("Bitmap",".bmp"), ("JPEG", ".jpeg"), ("All Files","*.*")]
            form = self.pa.form(fields)

            if form:
                self.cur.execute("UPDATE users SET user_name = '"+str(form["user_name"])+"', phone = '"+str(form["phone"])+"', sex = '"+str(form["sex"])+"', birth_date = '"+str(form["birth_date"])+"', photo = '"+str(form["photo"])+"' WHERE user_id = '"+str(form["user_id"])+"'")
                self.con.commit()
                self.pa.print("User ID "+str(form["user_id"])+" - Changes have been saved")
            else:
                self.pa.error("User ID "+user_id+" - Changes have NOT been saved")

        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()

    def delete(self):
        ## DELETE A USER
        #- This will allow you to delete an existing user
        #- Insert a valid user ID number to delete the user
        # get user id to edit
        user_id = self.pa.input("Select user ID to delete")
        self.cur.execute("SELECT * FROM users WHERE user_id = '"+user_id+"'")
        fetched_values = self.cur.fetchall()
        if len(fetched_values) == 0:
            self.pa.error("User ID is not in the database!")
        else:
            name = fetched_values[0][1]
            if self.pa.question("Are you sure you want to delete user: ID "+str(user_id)+" "+name):
                self.cur.execute("DELETE FROM users WHERE user_id = '"+user_id+"'")
                self.con.commit()
                self.pa.print("User ID "+user_id+" - was deleted")
            else:
                self.pa.error("User ID "+user_id+" - was NOT deleted")

        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()
    
    def Export(self):
        ## EXPORT
        #- This function allowes you to save your current database as a csv file
        self.cur.execute("SELECT * FROM users")
        fetched_values = self.cur.fetchall()
        if len(fetched_values) > 0:
            content = "User Id,Name,Phone,Sex,Birth date,Photo\n"
            for row in fetched_values:
                for col in row:
                    content += col+","
                content = content[:-1]
                content += "\n"
            initialdir = ""
            possibleTypes = [("CSV File", "*.csv")]
            self.pa.save_file(content, initialdir, possibleTypes)
        else:
            self.pa.error("Error! Cannot save an empty database")
        self.pa.restart()

    def Import(self):
        ## IMPORT
        #- This function allowes you to load users to your database from a csv file
        #- Warning! All current users will be deleted
        if self.pa.question("Warning! All current users will be deleted. Would you like to continue?"):
            possibleTypes = [("CSV File", "*.csv")]
            initialdir = ""
            filename = self.pa.load_file(initialdir, possibleTypes)
            if not filename is None:
                csv_content = self.pa.read_csv(filename)
                self.cur.execute("DELETE FROM users")
                for line in csv_content[1:]:
                    self.cur.execute("INSERT INTO users (user_id, user_name, phone, sex, birth_date, photo) VALUES ('"+str(line[0])+"','"+line[1]+"','"+str(line[2])+"','"+line[3]+"','"+line[4]+"','"+line[5]+"')")
                self.con.commit()
        if not self.pa.database_is_displayed():
            self.display_database()
        else:
            self.pa.update_database()
        self.pa.restart()

    def load_folder(self):
        ## LOAD FOLDER
        #- Loads a folder location
        initialdir = ""
        folder = self.pa.load_folder(initialdir)
        self.pa.print(folder)
        self.pa.restart()

    def edit_script(self):
        ## EDIT SCRIPT
        #- This will allow you to edit the script file
        os.popen("script.txt")
        self.pa.restart()
    
    def run_script(self):
        ## RUN SCRIPT
        #- This function activates the script file
        functions = {}
        functions["SUM"] = self.SUM
        functions["AVG"] = self.AVG
        functions["HELLO_WORLD"] = self.HELLO_WORLD
        self.pa.script("script.txt", functions)
        self.pa.restart()

    # SCRIPT FUNCTIONS
    def SUM(self, arguments):
        # FUN: SUM(a, b)
        # ARG: a - Integer number
        # ARG: b - Integer number
        # RTN: a + b
        a = arguments[0]
        b = arguments[1]
        self.pa.print(str(a)+" + "+str(b)+" = "+str(int(a)+int(b)))

    def AVG(self, arguments):
        # FUN: AVG(list_of_numbers)
        # ARG: list_of_numbers - A list of numbers in the following format [x1 x2 x3 x4 ...]
        # RTN: Sccssesful import True or False
        vals = arguments[0]
        vs = vals.split(" ")
        summ = 0
        qty = 0
        for i in vs:
            summ += int(i)
            qty += 1
        self.pa.print("Average of: "+vals+" = "+str(summ / qty))
    
    def HELLO_WORLD(self, arguments):
        # FUN: HELLO_WORLD()
        # RTN: Prints HELLO WORLD
        self.pa.print("HELLO WORLD")

main()


# SETTINGS
# Database location --> The location of the user database. For example: database.db

# RELATED FILES
## users.csv - This is the file the app generates when clicking on EXPORT this file contains the following columns:
#- User Id
#- Name
#- Phone
#- Sex
#- Birth date
#- Photo