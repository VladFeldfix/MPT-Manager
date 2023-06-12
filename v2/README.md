<h1>Personal-Assistant v2.0</h1>
<h4>Application Guide</h4>
<h2>PART I: GENERAL INFORMATION</h2>
This Python 3.0 library helps you create a user friendly GUI for your Application, Plus additional functions such as database management, file management, time stamp, and even a script reader.

<h2>PART II: HOW TO USE</h2>
Download PersonalAssistant.py and put it in C:\Python310\Lib or wherever you keep your Python libraries<br>
Import PersonalAssistant to your application as shown in SampleApp.py

<h2>PART III: MAIN MENU</h2>
Personal-Assistant looks like a chat-box. The main menu function makes a personal main menu for your application where the user selects items by sending the correct number.<br>
See PART IV: SCRIPT display_menu function for more info.

<h2>PART IV: SCRIPT</h2>
<h4>Console functions</h4>
<ol>
<li>__init__(program_location, program_name, rev) - constructor</li>
<ul>
    <li>program_location - must be equal to __file__. This argument is necessary to generates the help.html file.</li>
    <li>program_name - the name of your application</li>
    <li>rev - the revision of your application</li>
</ul>

<li>run() - this function is necessary to run the GUI</li>

<li>notice(text)</li>
<ul>
    <li>text - The text of the notice to display</li>
</ul>  

<li>error(text, code) - displays an error message</li>
<ul>
    <li>text - The text of the error to display</li>
    <ol>
    <li>code - 0-99 > System Error</li>
    <li>code - 100-199 > Invalid input</li>
    <li>code - 200-299 > Missing file</li>
    <li>code - 300-399 > Error in file</li>
    <li>code - 400 + > Other Errors</li>
    </ol>
</ul>

<li>fatal_error(text, code) - a fatal error do not allow the program to continue</li>
<ul>
    <li>text - The text of the error to display</li>
    <ol>
    <li>code - 0-99 > System Error</li>
    <li>code - 100-199 > Invalid input</li>
    <li>code - 200-299 > Missing file</li>
    <li>code - 300-399 > Error in file</li>
    <li>code - 400 + > Other Errors</li>
    </ol>
</ul> 

<li>restart(text) - restarts the application</li>

<li>exit() - closes the application</li>

<li>help() - displays the help file. For more information see PART VI: RELATED FILES</li>

<li>print(text) - displays a text in the console</li>
<ul>
    <li>text - The text to be displayed</li>
</ul> 

<li>clear() - clears the console</li>
<li>pause() - pauses the app</li>
</ol>
<h4>Input box functions</h4>
<ol>
<li>input(promp) - gets an input from the input box</li>
<ul>
    <li>promp - The message to display</li>
    <li>Return value - the text from the input box</li>
</ul>

<li>choose(text, choices, default)</li>
<ul>
    <li>text - display a message. for example: choose the following option</li>
    <li>choices - a list/tuple object of options. for example: ("M", "F", "Not Specified")</li>
    <li>default - the default choise in case no input was recieved. for example: "Not Specified"</li>
    <li>Return value - The choice made by the user</li>
</ul>

<li>question(text)</li>
<ul>
    <li>text - question do display. for example: "Save changes?". Personal Assistant will automatically add (Y/N) ></li>
    <li>Return value - True or False</li>
</ul>

</ol>
<h4>Progress Bar functions</h4>
<ol>
<li>progress_bar_value_set(percent) - changes the value in the progress bar</li>
<ul>
    <li>percent - a number between 1-100</li>
</ul>

<li>progress_bar_value_get(percent) - gets the value in the progress bar</li>
<ul>
    <li>Return value - The current status of the progress bar. a number between 1-100</li>
</ul>

</ol>
<h4>Main menu and settings functions</h4>
<ol>
<li>display_menu() - displays the main menu</li>
<ul>
    <li>Required global argument: main_menu. this argument is a library of functions to call. for example self.pa.main_menu["FUNCTION"] = self.f</li>
</ul>

<li>get_setting(key) - gets a value from the settings file settings.txt</li>
<ul>
    <li>key - the variable or key you need to get. for example: for example db = self.pa.get_setting["Database file location"]</li>
    <li>Return value - The value of the given setting</li>
</ul>

</ol>
<h4>Script functions</h4>
<ol>

<li>script(file, functions) - runs a given script. see SampleApp.py to understand hot this function works</li>
<ul>
    <li>file - the file name of the script. for example: "script.txt"</li>
    <li>functions - a dictionary of functions. for example: {["F":self.f], ["G"]:self.g}</li>
</ul>

</ol>
<h4>Database functions</h4>
<ol>

<li>display_database(db, table, order_by) - dsiplays a database</li>
<ul>
    <li>db - the database file name. for example: "database.db"</li>
    <li>table - the table to display. for example: "Users"</li>
    <li>order_by - the column name to order by. for example: "UserID"</li>
</ul>

<li>update_database() - updates the database. do it after every change</li>

<li>exit_database() - closes the database</li>

<li>database_is_displayed()</li>
<ul>
    <li>Return value - True or False if the database is currently displayed</li>
</ul>

<li>set_database_double_click_return_value(index) - When user double clicks on a any line in the database it will send the value of the first column to the input box</li>
<ul>
    <li>index - The index of the value you want Personal Assistant to send instead of the first column</li>
</ul>

</ol>
<h4>Form functions</h4>
<ol>

<li>form(fields) - activates a form to be filled</li>
<ul>
    <li>fields - A dictionary of field objects (See next part for a field object)</li>

<li>a FIELD object has the following variables: name, type, default. Additionally there are two more optional values: disabled, filetypes, default_filetype, default_directory, options. </li>
<ul>
    <li>name - the name of the field. for example: User Name. *required value</li>
    <li>type - the type of the filed. there are 7 types of values - [TEXT, NUMBER, DATE, FILE, FILES, DIRECTORY, CHOOSE]. for example: form_results = self.pa.form[{"User Name": FIELD("Name", TEXT, "Anonymous"), "Phone": FIELD("Phone", TEXT, "000-0000000")}] .for more information see SampleApp.py. *required value</li>
    <li>default - the default value of the field. *required value</li>
    <li>disabled - True or False if the form can edit this field</li>
    <li>filetypes - for field type FILE and FILES this variable tells the systems what is the default folder to open in file dialog types to choose. for example: [("Images","*.img"), ("PNG","*.png"), ("Bitmap",".bmp"), ("JPEG", ".jpeg"), ("All Files","*.*")]</li>
    <li>default_directory - for field type FILE, FILES, and DIRECTORY this variable tells the system where is the default directory for the file-dialog window to be opened in</li>
    <li>options - for field type CHOOSE, this variable should be a list / tuple of options. for example:
        sexes = ("M", "F", "Not Specified")
        fields["sex"] = FIELD("Sex", CHOOSE, sexes[2])
        fields["sex"].options = sexes
    </li>
</ul>

</ul>

</ol>
<h4>File management functions</h4>
<ol>

<li>save_file(content, initialdir, possibleTypes)</li>
<ul>
    <li>content - the text you want to save</li>
    <li>initialdir - default directory for the file-dialog window to be openned in</li>
    <li>possibleTypes - a list possible types. for example: [("Images","*.img"), ("PNG","*.png"), ("Bitmap",".bmp"), ("JPEG", ".jpeg"), ("All Files","*.*")]</li>
</ul>

<li>def load_file(initialdir, possibleTypes)</li>
<ul>
    <li>initialdir - default directory for the file-dialog window to be openned in</li>
    <li>possibleTypes - a list possible types. for example: [("Images","*.img"), ("PNG","*.png"), ("Bitmap",".bmp"), ("JPEG", ".jpeg"), ("All Files","*.*")]</li>
    <li>Return value - a path to a selected file</li>
</ul>

<li>def load_files(initialdir, possibleTypes)</li>
<ul>
    <li>initialdir - default directory for the file-dialog window to be openned in</li>
    <li>possibleTypes - a list possible types. for example: [("Images","*.img"), ("PNG","*.png"), ("Bitmap",".bmp"), ("JPEG", ".jpeg"), ("All Files","*.*")]</li>
    <li>Return value - a list of paths to selected files</li>
</ul>

<li>def load_folder(initialdir)</li>
<ul>
    <li>initialdir - default directory for the file-dialog window to be openned in</li>
    <li>Return value - a path to a selected folder</li>
</ul>


<li>def read_csv(file)</li>
<ul>
    <li>file - a file to open</li>
    <li>Return value - the content of a csv file in a form of a list</li>
</ul>

</ol>
<h4>Other functions</h4>
<ol>
    <li>today()</li>
    <ul>
        <li>Return value - current date in format YYYY-MM-DD (a string)</li>
    </ul>

</ol>

<h2>PART V: SETTINGS</h2>
every Personal Personal-Assistant application requires a settings file in the format - variable --> value

<h2>PART VI: RELATED FILES</h2>
<ol>
    <li>settings.txt - every Personal Personal-Assistant application requires a settings file in the format - variable --> value</li>
    <li>favicon.ico</li>
    <li>help.html - this file is automatically generated from the application comments</li>
    <ul>
        <li>your application must contain the following comments in the same order: [see example in SampleApp.py]</li>
        <ul>
            <li># GENERAL INFORMATION</li>
            <li># HOW TO USE</li>
            <li># MAIN MENU</li>
            <li># SCRIPT FUNCTIONS</li>
            <li># RELATED FILES</li>
        </ul>
        <li>under each comment of the list above add ## Text for line 1. and #- for line 1.1. [see example in SampleApp.py]</li>
        <li>accept for SETTINGS where the commenting system is # VAR --> VAL [see example in SampleApp.py]</li>
    </ul>
</ol>