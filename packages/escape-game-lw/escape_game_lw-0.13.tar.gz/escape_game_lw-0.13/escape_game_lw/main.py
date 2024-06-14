from datetime import datetime, timedelta, date
import numpy as np
import random
import string
import time


class EscapeGamePinaPython:
    # Chapter 0
    # ---------------
    def __init__(self, strict_mode=False):
        """ Init game with current time"""
        
        if strict_mode:
            self.completed = [0]
        else:
            self.completed = list(range(10))
        self.start_time = datetime.now()
        
        # chapter 8
        self.map = []
        self.level = 1
        # chapter 9
        self.__command_device = []
        self.__id_list = {'80957:015430:3911' : {'os_type' : 'windows', 'os_version' : '10'}, 
            '7182:27824896:383' : {'os_type' : 'windows', 'os_version' : '10'}, 
            '4657871:3315:0983' : {'os_type' : 'android', 'os_version' : '14'}, 
            '93010:310:5183473' : {'os_type' : 'windows', 'os_version' : '10'}, 
            '8299:737631:16566' : {'os_type' : 'ios', 'os_version' : '15'}, 
            '7010651:3338:7262' : {'os_type' : 'ios', 'os_version' : '13'}
        }

        print("Game started!")
    
    # Chapter 1
    #----------------   
    def check_info(self, pina_python : dict):
        """ Frist chapter: Gathering Basic Information
        
        Args:
            pina_python (dict): dict that should be created by the player with the help of the text
                                The entries should be: name (str) , age (int), email (str), 
                                location (str), research_topics (list - keywords only)
        """
        if 0 not in self.completed:
            print("Please start the game in the previous cell")
            return False
        
        birthdate = date(1985, 5, 15)

        # Calculate the age using timedelta
        today = date.today()
        age = today - birthdate
        age_in_years = age.days // 365

        if list(pina_python.keys()) == ['name','age','email','location','research_topics'] and pina_python['age'] == age_in_years:
            print("You identified the key information.")
            self.completed.append(1)
            return True
        
        elif pina_python['age'] != age_in_years:
            print("Double check the age")
            return False
        else:
            print("Are you sure you included all listed informations in the dict?")
            return False


    # Chapter 2
    # --------------

    pin_codes =  {
        "info" : """  The pin for the elevator always has 6 digits. The preceding zeros must be added.
            The access code for the rooms and corridors is the base code for the floor and the stored code.
        """, 
        "floors" : {
            "0" : {"left_corridor" : '03012', "right_corridor" : "92340", "base" : "4230" },
            "1" : {"left_corridor" : '33478', "right_corridor" : "29345", "base" : "4320" },
            "2" : {"left_corridor" : '98013', "right_corridor" : "74348", "base" : "4310" },
            "3" : {"left_corridor" : '10457', "right_corridor" : "91368", "base" : "4300" },
        },
        "rooms" : {
            '1.01': '909371', '1.02': '707597', '1.03': '352753', '1.04': '881645', '1.05': '727321', '1.06': '430939', '1.07': '024216',
            '1.08': '310495', '1.09': '179544', '1.10': '165576', '1.11': '849093', '1.12': '216357', '1.13': '242807', '1.14': '144756', 
            '1.15': '537644', '1.16': '937020', '1.17': '882621', '1.18': '512981', '1.19': '128222', '1.20': '975963', '2.01': '291040', 
            '2.02': '964770', '2.03': '639696', '2.04': '531024', '2.05': '286580', '2.06': '080905', '2.07': '524600', '2.08': '522014', 
            '2.09': '935583', '2.10': '593658', '2.11': '093647', '2.12': '967165', '2.13': '201495', '2.14': '958950', '2.15': '241853', 
            '2.16': '018885', '2.17': '457453', '2.18': '173835', '2.19': '297329', '2.20': '906721', '2.21': '013708', '2.22': '746230', 
            '2.23': '372697', '2.24': '953466', '2.25': '510309', '3.01': '534081', '3.02': '489426', '3.03': '693044', '3.04': '528414', 
            '3.05': '364836', '3.06': '028698', '3.07': '571636', '3.08': '845883', '3.09': '366359', '3.10': '908687', '3.11': '928083', 
            '3.12': '679883', '3.13': '800310', '3.14': '808668', '3.15': '876113', '3.16': '019836', '3.17': '791278', '3.18': '438693', 
            '3.19': '361543', '3.20': '576705', '3.21': '025251', '3.22': '403119', '3.23': '936307', '3.24': '606693', '3.25': '351535', 
            '3.26': '119566', '3.27': '594827', '3.28': '269838', '3.29': '675812', '3.30': '195203', '3.31': '545189', '3.32': '082145', 
            '3.33': '053776', '3.34': '610087', '3.35': '891626', '3.36': '820511', '3.37': '106392', '3.38': '662138', '3.39': '207354'
        },
        "elevators" : [3301, 2204, 5508 ]
    }

    def check_way_to_office(self, pin_elevator :str, pin_3rd_floor_right :str, pin_office : str):
        """ Second chapter: At the office
        
        Args:
            pin_elevator (str): pin for elevator; info in pin_codes
            pin_3rd_floor_right (str): pin for right corridor on 3rd floor
            pin_office (str): pin for office room 3.09
        
        """
        
        if 1 not in self.completed:
            print("Did you gather the information frist? (chapter 1) ")
            return False
        
        if pin_elevator == "003301":

            if pin_3rd_floor_right == "430091368":

                if pin_office == "4300366359":
                    print("All pins are correct. You arrived at the office.")
                    self.completed.append(2)
                    return True
                else:
                    print("Error. Go back to entrance. Maybe check the pin info?")
                    return False

            print("Wrong pin. Try again.")
            return False

        print("Wrong pin. Try again.")
        return False


    # Chapter 3
    # --------------
    def check_login_computer(self, password :str):
        """ checks if the password is correct.
        Args:
            password (str) : input of password to be tested.
        """
        
        
        if 2 not in self.completed:
            print("You need to enter the room frist.")
            return False

        if password == "hfg9fh3aia4md4hjsjs!":
            print("Password is correct. You are now logged in.")
            self.completed.append(3)
            return True

        else:
            return False


    # Chapter 4
    # --------------
    def get_login_logout_times(self) -> (list, list):
        """ creates the login and logout times"""

        if 3 not in self.completed:
            print("You need to be logged in first (chaper 3).")
            return False

        random.seed(42)

        today = date.today()
        day =  today - timedelta(days=(today.weekday() - 1 + 7) % 7)

        # day sollte ein datetime-Objekt sein, das den Tag repräsentiert, für den die Zeiten generiert werden sollen
        login_times = []
        logout_times = []

        online_code = {
            8 : [1,0,1,0,1,0], # each row is an hour, one element in list is 10min
            9 : [1,1,0,0,1,1], # 0 = not logged in
            10 : [1,0,1,1,0,1], # 1 = logged in
            11 : [1,1,1,1,1,1],
            12 : [0,0,0,0,0,0],
            13 : [1,1,1,1,1,0],
            14 : [1,0,1,1,1,1],
            15 : [1,1,1,1,1,1],
            16 : [1,0,0,0,0,1],
            17 : [1,1,1,1,1,1],
            18 : [1,0,1,1,0,1],
            19 : [1,1,1,0,0,0],
        }
        
        online = True

        # started day at 7:58
        login_times.append(datetime(year=day.year, month=day.month, day=day.day, hour=7, minute=58))

        for hour in online_code:
            hour_time = datetime(year=day.year, month=day.month, day=day.day, hour=hour, minute=0)
            for i, active in enumerate(online_code[hour]):
                if not online and active == 1: # log in
                    login_time = hour_time + timedelta(minutes=i*10) + timedelta(minutes=random.randint(-3, 3))
                    login_times.append(login_time)
                    online = True
                elif online and active == 0: # log out
                    logout_time = hour_time + timedelta(minutes=i*10) + timedelta(minutes=random.randint(-3, 4))
                    logout_times.append(logout_time)
                    online = False
            
        return (login_times, logout_times)


    def get_browser_history(self) -> dict:
        """ get the browser history of last tuesday"""
        random.seed(42)

        today = date.today()
        tuesday =  datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0) - timedelta(days=today.weekday() + 1) - timedelta(weeks=1)
            
        websites = ["arxiv.org/abs/", "youtube.com/watch?v=", "reddit.com/r/neurallace/comments/", "linkedin.com/feed/", "arxiv.org/abs/", "arxiv.org/abs/", "arxiv.org/abs/"]

        # list random time stamps
        browser_history = [{'time' : tuesday + timedelta(minutes=random.randint(8*60, 60*19.5)),
                    'website' : random.choice(websites) + ''.join(random.choices(string.ascii_lowercase, k=5))
                    }for i in range(800)]

        # remove entries in window
        # 16:52:00 is the selected time of coming back from the call
        browser_history  = [site for site in browser_history if not(site['time'].hour in [16] and site['time'].minute in (52,53,54,55))]

        # add suspious website
        browser_history.append({'time': datetime(tuesday.year, tuesday.month, tuesday.day, 16, 53),
        'website': 'brainlink.de/home'})

        # sort entries
        browser_history.sort(key = lambda x: x['time'])
        
        return browser_history


    def check_website_name(self, website_url :str):
        """ aks the colleague to confirm the website """
        
        if "brainlink" in website_url.lower():
            print("This is the website!")
            return True
        else:
            return False


    def get_website_text(self, website_url : str):
        """ returns the website text if it is the right website"""
        
        if "brainlink" in website_url.lower():
            website_text = """
            Introducing Our Revolutionary Brain-Machine Interface
            We are thrilled to announce the launch of our revolutionary brain-machine interface - the next generation of human-computer interaction. Our brain-machine interface is designed to provide a seamless connection between the human brain and technology, allowing for unprecedented control and communication.

            How It Works
            Our brain-machine interface uses advanced technology to capture and interpret the electrical signals of the brain, allowing users to control computers and other devices with their thoughts. Our system is non-invasive and easy to use, requiring no surgery or implants.

            Features
            Our brain-machine interface is packed with features that make it the most advanced system of its kind:

            High accuracy: Our system is designed to provide accurate and reliable control, with minimal training required.
            Intuitive controls: Our interface features intuitive controls that allow users to control devices with their thoughts, without the need for physical input.
            Customizable: Our system can be customized to fit the needs of any user, with a range of settings and options to choose from.
            Benefits
            Our brain-machine interface offers a range of benefits that make it the perfect choice for anyone looking to improve their interaction with technology:

            Increased control: Our system allows for unprecedented control over computers and other devices, with the ability to perform complex tasks with ease.
            Improved accessibility: Our interface provides a new level of accessibility for people with disabilities, allowing them to interact with technology in new and exciting ways.
            Enhanced performance: Our system can improve performance in a variety of fields, from gaming to medicine, by providing faster and more accurate control.
            About Us
            We are a team of experts in neuroscience and engineering who are committed to pushing the boundaries of what is possible with brain-machine interfaces. Our goal is to provide innovative solutions that improve people's lives and change the way we interact with technology.

            Get in Touch
            If you have any questions about our brain-machine interface or want to learn more about our company, please don't hesitate to get in touch. You can reach us 004915757845993. We would love to hear from you and answer any questions you may have.
            """
            return website_text
        else:
            return "404 - Not found"


    def check_telephone_number(self, number : str):
        """ checks if telephone number is valid"""
        
    
        if 3 not in self.completed:
            print("You need to be logged in first (chaper 3).")
            return False

        if str(number) == "004915757845993" or str(number) == "4915757845993" or str(number) == "004915757845993.":
            self.completed.append(4)
            return True
        else:
            print("Wrong number. Try again.")
            return False
        
    # Chapter 5
    # --------------
    def __create_messages(self, key : int = 9):
        """creates the encrypted messages"""
        messages = [
            "URGENT!!!who are you? And how do you get my prototypes? I won't let that happen to me and my team.",
            "I think we should talk in person. Friday, 7pm here: 50.04413916514295, 10.245295766314824. no police. we have a good deal for you.",
            "Ok You can google what I look like."        
        ]
        
        # helper function
        def encrypt_char(self, plainchar, key):
            cipherascii = ord(plainchar)+key
            return chr(cipherascii)
        
        for message in messages:
            ciphertext = ""
            plaintext = message
            for c in plaintext:
                ciphertext += encrypt_char(c,key)
            print(ciphertext)
                
    def __decrypt_message(self, text, key: int):
        """decrypts message depending on key"""
        def decrypt_char(plainchar, key):
            cipherascii = ord(plainchar)-key
            return chr(cipherascii)

        plaintext = ""
        for c in text:
            plaintext += decrypt_char(c,key)
        return plaintext
            
    def check_coordinates_text(self, lat : str, long :str):
        """ checks if the texts are correct decrypted by the coordinates
        
        Args:
            lat (str): first value of coordinates
            long (str): second value of coordinates
        """
        
        if 4 not in self.completed:
            print("You need to get the telephone number first(chaper 4).")
            return False
        
        if str(lat) == "50.04413916514295" and str(long) == "10.245295766314824":
            self.completed.append(5)
            print("The coordinates are correct")
            return True
        else:
            return False

    # Chapter 6
    # --------------
    def __generate_prime_text(self):
        random.seed(42)

        def generate_random_text(length):
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

        def is_prime(number):
            """Function to check if a number is prime."""
            if number < 2:
                return False
            for i in range(2, int(number**0.5) + 1):
                if number % i == 0:
                    return False
            return True

        def print_primes(up_to):
            """Function to print all prime numbers up to a given limit."""
            primes = [num for num in range(2, up_to) if is_prime(num)]
            return primes
        
        prime_numbers= print_primes(1000)
        random_text = generate_random_text(235)
        random_text_lst = list(random_text)

        text_to_hide = "Help. Use prototype. See laptop: emergency.txt - PP"
        for i, char in enumerate(text_to_hide):
            random_text_lst[prime_numbers[i]] = char
        
        return "".join(random_text_lst)
            
    def check_distance(self, distance : float):
        """checks if the distance in kilometers is correct """
        
        if round(distance,2) == 1.59:
            print("The distance is correct")
            return True
        else:
            return False
        
    def check_location_message(self, msg : str):
        """checks if the message of the location is correct"""

        if 5 not in self.completed:
            print("You need to get the location first (chaper 5).")
            return False
        
        if msg == "Help. Use prototype. See laptop: emergency.txt - PP":
            self.completed.append(6)
            print("The message is correct. Let's return to the laptop.")
            return True
            
    # Chapter 7
    # ---------------

    def open_emergency_txt(self, pwd):
        """ if the password is correct, returns the content of the file"""
        
        # Calculate the age using timedelta
        age = date.today() - date(1985, 5, 15)
        age_in_years = age.days // 365
        
        try:            
            if pwd == "neuroscience" + str(age_in_years):
                print("""
                    Executive Summary: Mind-Controlled Machine Prototype
                    -------------------------------------------------------
                    The brain-machine-interface prototype has been designed with a dual-component approach, 
                    addressing safety concerns. It comprises a chip with an electromagnetic brain interface, securely 
                    attached to the scalp, and a command device acting as an intermediary between the chip and various devices.

                    The chip enables seamless connection to different machines in the vicinity, establishing a direct link 
                    to the thought area of the brain through its electromagnetic brain interface.

                    The command device serves as an additional layer of security, requiring users to manually add devices 
                    before the chip can communicate with them. It acts as a mediator between the brain interface chip and 
                    the diverse operating systems of smartphones, computers, and smart home devices.

                    The command device is capable of identifying new and known devices (usually weak signals) and the
                    associated brain interface chips. The associated brain interface chip emmits a  strong signal strength, 
                    so it can bet detected and communicate in an distance of up to 500m.

                    The command device only transmits the communication between device and brain but a remote transmission of 
                    maintenance information to the brain interface chip is possible. 

                    This innovative prototype aims to revolutionize human-machine interaction through secure 
                    and efficient neural control.

                    In Case of Emergency
                    ----------------------
                    As the prototype is highly coveted by many people, Dr. Python carries the scalp chip hidden through everyday
                    life. The command device is in the hands of Dr. Mörpf, who knows how to use it. He will always deny the 
                    existence of the two prototype parts unless

                    a) there is an extraordinarily dangerous situation
                    b) the intended use does not reduce the well-being of the world
                    c) he is told the code word "beer garden summer"
                """
                )
                return True
            else:
                return False
        except:
            return False
        
    def check_find_prototype(self, colleague, code_word):
        """check if you extracted the right info of file"""

        if 6 not in self.completed:
            print("You need to get the message of the location first(chaper 6).")
            return False

        if colleague.lower() in ["dr. mörpf","moerpf","dr. moerpf","mörpf"] and code_word.lower() == "beer garden summer":
            self.completed.append(7)
            print("""
            Dr. Mörpf gives you the command device after telling him the code word and explaining
            the situation. He joins you to search for Dr. Python with the help of the device.
            
            As mentioned in the executive summary, the emmited signal of the brain interface chip
            can be detected with the command device.""")
            return True
        
    # Chapter 8
    # -------------
    def __solve_map(self, matrix):
        """ helper function to solve the map"""
        matrix_np = np.array(matrix )
        max_matrix = np.max(matrix_np)
        positionen = np.argwhere(matrix_np == max_matrix)
        return positionen

    def get_map(self, level : int = 1) -> list:
        """ creates an map for each level in the form of an list
            Args:
            level (int) : start at level 1 and begin the search

            ---

            A map is in the format
            [[  4,  -5, 100,   3,  -3],
            [  2,  -5, 100,  -3,  -4],
            [ -2,  -1,  -2,  -1,   2],
            [ -3,   0,   1,   0,   3],
            [  2,  -2,   3,  -3,  -2]]
        """

        np.random.seed(164)

        # determine size of map
        sizes = {1 : 500, 2 : 400, 3 : 300}
        try:
            map_size = sizes[level]
        except:
            return []
        
        matrix = np.random.randint(-2, 8, size=(map_size , map_size ))
        x, y = np.random.randint(5, map_size-5, size=2)

        max_signal = np.random.randint(20,100, size=1)

        # replace values with strongest signal 
        if level == 0:
            matrix[x+1, y+1] = max_signal
        if level <=1:
            matrix[x+1, y] = max_signal
        if level <= 2:
            matrix[x, y+1] = max_signal
        matrix[x, y] = max_signal
        
        self.map = matrix
        self.level = level
        
        return matrix.tolist()

    def check_strongest_signal(self, x : int, y : int):
        """check if you found the correct spot on the map"""
        
        if 7 not in self.completed:
            print("Please get the prototype first (chapter 7)")
            return False
        
        strongest_signal = self.__solve_map(self.map)
        
        if x == strongest_signal[0][0] and y == strongest_signal[0][1] and self.level >= 3:
            self.completed.append(8)
            print("You found the location of Dr. Pina Python!")
            return True
        else:
            print("Please search again")
            return False


    # Chapter 9
    # ------------
    def get_list_devices(self):
        """returns the ids of the devices in the nearby area"""
        return list(self.__id_list.keys())


    def try_add_device(self, id :str, os_type : str, os_version : str):
        """ trys to add a device to the command device
        
        Args: 
            id (str) : id of device, you get it by 'get_list_devices()
            os_type (str) : 'android' or 'ios' are possible in this scenario
            os_version (str) : 10-14 android, 10-17 ios
        
        """
        type_os_bool = False
        version_os_bool = False
        connected_bool = False
        
        if id in self.__id_list.keys():
            type_os_bool = os_type == self.__id_list[id]['os_type']
            if type_os_bool:
                version_os_bool = str(os_version) == self.__id_list[id]['os_version']
                if version_os_bool:
                    connected_bool = True
                    self.__command_device.append(id)
                    print(f"{id} added to command device")
                    
        else:
            print("Wrong id")
        
        # sleep time for forcing clever programming
        time.sleep(30)
        
        return (type_os_bool, version_os_bool, connected_bool)

    def check_device_added(self):
        """checks if all smartphones are connected to the command device"""

        if 8 not in self.completed:
            print("You need to find Dr. Pina Pythons location first(chaper 8).")
            return False

        if '4657871:3315:0983' in self.__command_device and '8299:737631:16566' in self.__command_device and '7010651:3338:7262' in self.__command_device: 
            self.completed.append(9)
            print("Dr. Pina Python confirms the connection to the kidnappers smartphone. She starts a successful distraction...")
            return True
        
    # Chapter 10
    # ------------
    def ending(self):
        from datetime import datetime

        duration_min = (datetime.now() - self.start_time).seconds//60

        if 9 in self.completed:
            print(f"""
            After the kidnapper has left the building in a hurry and he is already expected by the police.
            The hiding place is left unguarded. Thanks to you, the rescue party can approach.

            The door to the room where the Dr. Pina Python was held captive slowly opens. The rescue workers 
            enter the room and search for the researcher. After a few minutes of searching, they finally find her, 
            bound and gagged, but unharmed.

            Dr. Pina Python is quickly freed and examined by the rescuers. She is exhausted and dehydrated, but 
            otherwise in good condition. Several hours of investigation and gathering evidence, the 
            investigators are finally able to official identify the kidnapper and uncover his motives. 
            He wanted to trick her prototype out of Dr. Python and use her genius for evil purposes.
            The researcher is taken to a hospital to recover while the kidnapper is brought to justice.

            Thank you very much for your important part in the investigation!

            ...

            You solved the case. Congratulation! You finished in {duration_min} min.""")
        else:
            print("Try to solve the problems first")

