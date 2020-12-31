# E-Health-Python-Project-2020-UCL
<p>Some important points about the code improvements:</p>

Classes/structure:
  <ol><li><b>User classes</b>
    <ul><li><b>class User</b> (main.py) - this is the main class for a "user" type object. It can be intialised directly -> testuser = User(username), but it's probably better to only initialise it via the child classes. The only parameter required is the username.<ul><li>User.__init__ initialises the object with a bunch of values from the database based on the username</li><li>User.print_hello prints "Login successful" message. This is a regular (non-static) method so needs to be run on a specific instance -> testuser.print_hello()</li><li>User.print_information prints information from user profile -> also testuser.print_information()</li></ul></li>
      <li><b>class GP(User)</b> (GP.py) - class for GP objects which inherit from basic User features -> testGP = GP(username). This has a bunch of methods, refer to the code for details</li>
      <li><b>class Admin(User)</b> (admin.py) - documentation not yet created but will also inherit from User -> test_admin = Admin(username).</li>
      <li><b>class Patient(User)</b> (patient.py) - as above -> test_patient = Patient(username).</li>
      </li></ul><br>
  <li><b>Helper classes</b> - important: helper classes are designed to consist only of @staticmethod -s. They are a collection of helpful functions with a common theme and they are only grouped into a class for clarity and organisation purposes. They can be initiated without initialising an object.
  <ul><li><b>class MenuHelper</b> (main.py) - this is a helper class to manage the main menu
    <ul><li>@staticmethod MenuHelper.login() is the main login method, returns dictionary: {"username": username, "user_type": "user_type"}. Username, password and activation status is checked inside this method and if it fails, it returns False</li>
      <li>@staticmethod MenuHelper.register() - <b>this needs to be written</b> but I'd imagine it checks for username in the database (to avoid duplicates), then inserts and returns True (or False if registration fails for some reason)</li>
      <li>@staticmethod MenuHelper.dispatcher(username, user_type) - this is the main structure for starting different parts of the application. The current flow is as follows: if "L" is selected after starting the application, MenuHelper.login() is performed and returns username and user_type, which are then passed to MenuHelper.dispatcher - within this method, GP/Admin/Patient objects are initialised depending on the user_type variable.</li></ul></ol>
  
  I also need to add some notes about the Parser and SQLQuery helper classes... Watch this space.
  
  Some helpful functions you can use:
  <ul><li><b>Parser.print_clean(message1,message2,message3,...)</b> - this is a great function that works just like regular print, but it also clears the terminal window beforehand. You can also run it without any argument: Parser.print_clean(), and it will just clean the window without printing anything. If you want to make the usage simpler, simply put <b>print_clean = Parser.print_clean</b> at the beginning of your file, and you can use simply print_clean(arguments) everywhere then :)</li></ul>
  
  Other notes:
  <ul><li><b>Consider whether your method needs to be a regular method or a static one! </b>Relying too much on @staticmethod -s is not great style and it can lead to issues with conflicts in variable names if the program runs for a prolonged period of time. If you are operating on a specific user, always use an instance method. Only use @staticmethod for helper methods which perform some simple tasks and are unrelated to the user you're logged in as/editing.</li>
  <li>When operating within a class (or class instance specifically) and running one method from within another, consider using the method arguments instead of instance variables to share data between functions. This ensures naming safety, which then translates to type safety and better runtime performance. </li>
  <li>Return types are important - even if you don't need to return any variable/value from a function after it's finished running, it's good to at least return True or return False to indicate whether the task succeeded or failed. Even if you're not using it right now, this makes it much easier to implement extra functionalities later on because you don't need to edit existing functions to add new ones.</li><li>Put all your exceptions in exceptions.py and make sure they are written in CapitalLetterNamingConvention, and have 'Error' at the end.</li></ul>
  
  As we progress with adding new code, we will be repeatedly revising everything we've written to make sure that methods which can be reused, are reused, or preferably moved to higher-order classes to limit the amount of code the program needs to run. This should help us maintain good, logical structure and get us a great grade!
    
  
      
   
