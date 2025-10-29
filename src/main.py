import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def clear_terminal():
    
    # CLEAR TERMINAL FOR WINDOW SYSTEMS
    if os.name == 'nt':
        _ = os.system('cls')
    # CLEAR TERMINAL FOR MAC OS OR LINUX SYSTEMS
    else:
        _ = os.system('clear')


def handle_string_for_web_url(chosen_region):

    # REMOVE ANY WHITESPACE WITHIN STRING
    chosen_region = chosen_region.replace(" ", "")
    # REMOVE '/' IN STRING IF AVALIABLE
    chosen_region = chosen_region.replace('/', "")
    # DUE TO A TYPO IN THE 7-ELEVEN WEBSITE, REMOVE 's' IN Koshinetsu/Hokuriku REGION
    if chosen_region == "KoshinetsuHokuriku":
        chosen_region = "KohinetuHokuriku"
    # RETURN THE STRING NOW AVALIABLE TO USE IN 7-ELEVEN WEBSITE URL
    return chosen_region


def get_value_by_input_key(value_list):

    # DECLARE A DICTIONARY TO BE USED WITHIN THIS SCOPE
    numerated_dict = {}

    # ITERATE OVER THE LIST PASS AS A PARAMETER BY THE CALLER 
    for index in range(len(value_list)):
        # OUTPUT AND NUMERATE THE ELEMENTS WITHIN THE GIVEN LIST
        print(f"{index + 1} : {value_list[index]}")
        # CREATE A DICTIONARY TO ASSIGN AN INTEGER TO AN ELEMENT IN THE LIST
        numerated_dict[index + 1] = f"{value_list[index]}"

    # PRINT A MESSAGE TO REMIND THAT THE USER CAN EXIT THE PROGRAM BY ENTERING 0
    print("DISCLAIMER: Enter 0 to exit the program")
     
    # [TASK] CONVERT THE USER INPUT INTO AN INTEGER
    while True:
        try:
            # OBTAIN USER INPUT FOR THE KEY MAPPED TO A DESIRED VALUE IN THE DICTIONARY numerated_dict
            choice_input = int(input("Please enter a choice to continue: ")) 
            # [TASK] CHECK USER INPUT FOR OUT-OF-RANGE ERRORS

            # IF THE USER INPUT WAS WITHIN A VALID RANGE
            if 0 <= choice_input <= len(value_list):
               break
            # IF THE USER INPUT WAS NOT WITHIN A VALID RANGE
            else:
                # OUTPUT AN ERROR MESSAGE FOR INVALID INPUT
                print("Invalid choice has been input")
                print("Please enter a valid integer within the menu")
                # MOVE ONTO THE NEXT ITERATION
                continue
        # IF THE USER INPUT CANNOT BE CONVERTED INTO AN INTEGER (USER DID NOT INPUT AN INTEGER DATA TYPE)
        except ValueError:
            # OUTPUT AN ERROR MESSAGE FOR INVALID INPUT
            print("Invalid choice has been input")
            print("Please enter an integer data type")
    if choice_input == 0:
        return None
    else:
        # STORE THE VALUE OF THE DICTIONARY numerated_dict USING THE KEY choice_input GIVEN BY THE USER
        chosen_value = numerated_dict[choice_input]
        # RETURN THE CHOSEN VALUE BACK TO THE CALLER
        return chosen_value


def location_input_manager():

    # DECLARE A DICTIONARY WHICH MAPS REGIONS AS KEYS AND CITIES OF THE CORRESPONDING REGIONS AS LIST OF VALUES
    regions_prefecture_dict = {"Hokkaido/Tohoku"        : ["Hokkaido", "Aomori", "Iwate", "Miyagi", "Akita", "Yamagata", "Fukushima"],
                               "Kanto"                  : ["Tokyo", "Kanagawa", "Saitama", "Chiba", "Ibaraki", "Tochigi", "Gunma"],
                               "Koshinetsu/Hokuriku"    : ["Yamanashi", "Nagano", "Niigata", "Toyama", "Ishikawa", "Fukui"],
                               "Tokai"                  : ["Aichi", "Gifu", "Mie", "Shizuoka"],
                               "Kansai"                 : ["Osaka", "Hyogo", "Kyoto", "Shiga", "Nara", "Wakayama"],
                               "Cyugoku/Shikoku"        : ["Okayama","Hiroshima", "Tottori", "Shimane", "Yamaguichi", "Kagawa", "Tokushima", "Ehime", "Kouchi"],
                               "Kyushu/Okinawa"         : ["Fukuoka", "Saga", "Nagasaki" "Kumamoto", "Oita", "Miyazaki", "Kagoshima", "Okinawa"]
                               }
    
    # STORE THE KEYS OF THE DICTIONARY regions_prefecture_dict AS A LIST
    regions = list(regions_prefecture_dict.keys())
    
    # DISPLAY ALL THE REGIONS AND PREFECTURES AVALIABLE FOR WEB-SCRAPING AND OBTAIN USER INPUT FOR REGION/PREFECTURE OF INTEREST 
    chosen_region = get_value_by_input_key(regions)

    if chosen_region is None:
        return None, None, None, None
    else:
        # STORE THE VALUES OF THE DICTIONARY regions_prefecture_dict USING THE KEY CHOSEN BY THE USER
        cities = regions_prefecture_dict[chosen_region]
        
        # DISPLAY CITIES WITHIN THE REGION OR PREFECTURE OF INTEREST AND OBTAIN USER INPUT FOR CITY OF INTEREST 
        chosen_city = get_value_by_input_key(cities)

        if chosen_city is None:
            return None, None, None, None 
        else:
            # [TASK] PERFORM STRING HANDLING ON chosen_city AND chosen_region TO ALLOW FOR USAGE IN URL FORMATTING

            # SINCE THE STRING VARIABLE chosen_city CAN BE USED IN THE URL WITHOUT STRING HANDLING (DECLARED VARIBLE FOR FUTURE PROGRAM MAINTAINANCE)
            chosen_city_web_use   = chosen_city
            # STRING HANDLE THE STRING VARIABLE chosen_region TO BE USED IN THE WEBSITE-URL
            chosen_region_web_use = handle_string_for_web_url(chosen_region) 
    
            return chosen_region_web_use, chosen_city_web_use, chosen_city, chosen_region


def create_csv_file(total_num_of_shops, shops_list_eng, shops_list_jap, wages_list, chosen_city):

    # OPEN A NEW CSV FILE FOR WRITING... CREATION OF CSV FILE WITH THE SAME NAME WILL DELETE EXISTING FILE
    csv_file = open(f"{chosen_city}_Info.csv", 'w', newline= '', encoding='utf-8')

    # CREATE A PYTHON WRITER OBJECT 'C'
    c =  csv.writer(csv_file)
    # CREATE COLUMN HEADINGS FOR ROWS
    c.writerow(["Shop Name in English", "Shop Name in Japanese", "Base Hourly Wages"])
    # CALL A FUNCTION TO ORGANISE THE WEB-SCRAPED DATA INTO A 2D LIST IN ACCORDANCE WITH CSV FILE HEADERS
    organised_list = make_nested_list(total_num_of_shops, shops_list_eng, shops_list_jap, wages_list)
    # USE A FOR-LOOP TO WRITE EACH ROWS INTO A CSV FILE
    for row_data in organised_list:
        # WRITE ONE ROW TO THE CSV FILE (LIST BY LIST)
        c.writerow(row_data)
    # SAVE AND CLOSE THE FILE
    csv_file.close()


def make_nested_list(total_num_of_shops, shops_list_eng, shops_list_jap, wages_list):

    # DECLARE VARIABLE AND LISTS THAT WILL BE USED IN THE SCOPE OF THIS FUNCTION
    row_data_list = []
    nested_list   = []
    # CREATE A LIST WHICH WILL BE WRITTEN AS A ROW IN THE CSV FILE
    for index in range(total_num_of_shops):
        # EMPTY THE row_data_list FOR EVERY ITERATION
        row_data_list = []
        # FORMAT THE ROW DATA IN "Shop Name English, Shop Name Japanese, Base Hourly Wage"
        row_data_list = [shops_list_eng[index], shops_list_jap[index], wages_list[index]]
        # APPEND THE FORMATTED ROW DATA LIST TO THE NESTED LIST TO WRITE IN THE CSV FILE
        nested_list.append(row_data_list)
    # RETURN THE NESTED LIST BACK TO THE CALLER
    return nested_list


def remove_alpha_convert_int(web_scraped_string):

    # DECLARE LOCAL VARIABLES TO BE USED WITHIN THIS FUNCTION SCOPE
    converted_int_variable = 0
    num_extracted_string = ""

    # REMOVE TRAILING WHITESPACES AND SPACE (U+0020) FROM THE VARIABLE web_scraped_string
    web_scraped_string = web_scraped_string.replace(" ", "")
    # REMOVE ANY DIGIT GROUPING SEPERATORS FOR NUMBERS
    web_scraped_string = web_scraped_string.replace(',', '').replace('.', '')
    # USE FOR...LOOP TO EXTRACT EACH CHARACTER WITHIN THE VARIABLE web_scrape_string
    for char in web_scraped_string:
        # [TASK] IF A CHARACTER IS NOT AN ALPHABETIC LETTER, APPEND THAT CHARACTER TO A STRING WHICH WILL BE CONVERTED INTO INTEGER

        # NOTE: not char.isalpha IS CHOSEN AS BETTER PERFORMANCE IS ACHIEVED BECAUSE
        # 1. NUMBER COMES FIRST FOR web_scraped_string IN THIS PARTICULAR PROGRAM
        # 2. NUMBER DOES NOT EXCEED 5 DIGITS IN THIS PROGRAM WHICH IS LESS THAN THE CHARACTERS FOR "Results"

        if not char.isalpha():
            # APPEND THE CHARACTER THAT IS NOT AN ALPHABETIC LETTER TO A STRING VARIABLE num_extracted_string
            num_extracted_string += char
    
    # [TASK] CONVERT THE STRING VARIABLE num_extracted_string WHICH CONTAINS NUMBERS INTO AN INTEGER VARIABLE

    # RUN THIS CODE FOR THE CONVERSION PROCESS
    try:
        converted_int_variable = int(num_extracted_string)
    # IF THERE IS AN EXCEPTION FOR THE CONVERSION PROCESS
    except:
        # OUTPUT AN ERROR MESSAGE
        print("Error has encountered during the conversion process")
        print("Variable name: num_extracted_string (String to Int)")
        return None
    # IF NO EXCEPTION OCCURS FOR THE CONVERSION PROCESS
    else:
        # RETURN THE CONVERTED INTEGER VARIABLE BACK TO THE CALLER
        return converted_int_variable


def web_scrape(chosen_region_web_use, chosen_city_web_use):

    # DECLARE NECESSARY VARIABLES TO BE USED
    page_count   = 1
    first_page   = True
    num_of_shops_on_page = 0
    need_iteration_not_assigned = False

    # CREATE LISTS TO STORE THE WEB-SCRAPED DATA
    shop_names_eng_list   = []
    shop_names_jap_list   = [] 
    shop_salary_info_list = []
    # PREPARE CHROME BROWSER FOR AUTOMATION
    driver = webdriver.Chrome()
    try: 
        while first_page == True or need_iteration_not_assigned == True: 
            for page_index in range(page_count):
                if page_index == 0 and not first_page:
                    continue
                else:
                    # NAVIGATE TO THE DESIRED URL WHERE WEB-SCRAPING WILL TAKE PLACE
                    driver.get(f"https://ptj.sej.co.jp/arbeit/recruitment/jobfind-ml-pc/en/area/{chosen_region_web_use}/{chosen_city_web_use}/?page={page_index + 1}")

                    try:
                        # [TASK] CREATE AN EXPLICIT WAIT FOR ELEMENTS TO BE WEB-SCRAPED

                        # EXPLICIT WAIT UNTIL THE NAME OF ONE 7-ELEVEN SHOP (IN ENGLISH) BECOMES VISIBLE ON THE PAGE
                        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//h3[@class = '_shop']/span[1]")))

                        # [TASK] FIND ALL THE ELEMENTS OF MATCHING XPATH AND RETURNS THEM AS A LIST OF WEB-ELEMENTS

                        # FOR THE NUMBER OF RESULTS TO WEB-SCRAPE
                        num_of_results_element  = driver.find_element(By.XPATH, "//span[@class='_num _orange']")
                        # FOR NAMES OF 7-ELEVEN STORES IN ENGLISH
                        shop_names_elements_eng = driver.find_elements(By.XPATH, "//h3[@class = '_shop']/span[1]")
                        # FOR NAMES OF 7-ELEVEN STORES IN NIHONGO
                        shop_names_elements_jap = driver.find_elements(By.XPATH, "//h3[@class = '_shop']/span[2]")
                        # FOR SALARY INFORMATION OF 7-ELEVEN STORES
                        shop_salary_elements    = driver.find_elements(By.XPATH, "//p[@class = '_desc  txt_base']/span[2]")

                        # DECLARE A VARIABLE FOR STORING THE TOTAL NUMBER OF WEB-ELEMENTS STORED WITHIN LISTS OF WEB-ELEMENTS ON EACH PAGE
                        num_of_shops_on_page = len(shop_names_elements_eng)

                        # [TASK] CONVERT THE WEB-ELEMENTS THAT ARE STORED WITHIN LISTS OF WEB-ELEMENTS TO STRINGS

                        # FOR SHOP NAMES BOTH ENGLISH, NIHONGO, AND SALARY INFORMATION
                        for shop_name_index in range(0, num_of_shops_on_page):
                            shop_names_eng_list.append(shop_names_elements_eng[shop_name_index].text)
                            shop_names_jap_list.append(shop_names_elements_jap[shop_name_index].text)
                            shop_salary_info_list.append(shop_salary_elements[shop_name_index].text) 
                        
                        # DECLARE A VARIABLE FOR STORING THE TOTAL NUMBER OF RESULTS FOR SHOPS WITHIN THE CHOSEN REGION/PREFECTURE
                        
                        # .text CONVERT A WEB-ELEMENT INTO STRING AND RETURNS IN THE FORMAT OF "(NUM) RESULTS" (AS SHOWN ON THE WEB-PAGE)
                        num_of_results = num_of_results_element.text
                        # EXTRACT THE NUMBER FROM THE STRING IN THE FORMAT OF "(NUM) RESULTS" AND STORE THE NUMBER AS AN INTEGER
                        num_of_results = remove_alpha_convert_int(num_of_results)

                        # [TASK] CHECK IF THE CONVERSION WAS SUCCESSFUL AND NUMBER EXISTS WITHIN STRING VARIABLE num_of_results

                        # IF THE CONVERSION PROCESS WAS UNSUCCESSFUL, THE FUNCTION remove_alpha_convert_int RETURNS NONE TO CALLER
                        if num_of_results is None:
                            print("Error! Extraction of a valid number from a web-scraped string has failed")
                            print("Check function: remove_alpha_convert_int")
                            raise ValueError
                        # IF THE CONVERSION PROCESS WAS SUCCESSFUL, AND THE FUNCTION remove_alpha_convert_int RETURNS INTEGER
                        else: 
                            if first_page == True:
                                # DECLARE A CONSTANT VARIABLE TO STORE THE NUMBER OF SHOPS PER PAGE (USUALLY 20 PER PAGE BUT EXCEPTION EXISTS)
                                NUM_OF_SHOPS_PER_PAGE = num_of_shops_on_page
                                # CHECK IF ALL RESULTS/JOB-LISTINGS HAS BEEN WEB-SCRPAED ON THE FIRST PAGE
                                if (num_of_results // NUM_OF_SHOPS_PER_PAGE) == 1:
                                    # BREAK THE INNER LOOP
                                    need_iteration_not_assigned = False
                                    first_page = False
                                    break
                                # IF ALL THE RESULTS/JOB-LISTINGS ARE NOT WEB-SCRAPED ON THE FIRST PAGE
                                else:
                                    # SCRAPER NEED TO NAVIGATE THROUGH WEB-PAGES USING ITERATION
                                    need_iteration_not_assigned = True
                                    # FIGURE OUT HOW MANY ITERATION IS NEEDED FOR NAVIGATION
                                    page_count = (num_of_results // NUM_OF_SHOPS_PER_PAGE) + (num_of_results % NUM_OF_SHOPS_PER_PAGE > 0)
                                    # RE-ASSIGN first_page AS FALSE AS THE SCRAPER WILL NAVIGATE THROUGH WEB-PAGES USING ITERATION STARTING FROM NOW
                                    first_page = False 
                            else:
                                # RE-ASSIGN need_iteration_not_assigned AS FALSE BECAUSE VARIABLE page_count WILL BE RE-ASSIGNED ON SECOND ITERATION
                                need_iteration_not_assigned = False
                    # IF THERE IS AN EXCEPTION FOR THE WEB-SCRAPING PROCESS 
                    except (TimeoutException, NoSuchElementException, WebDriverException, ValueError) as e:
                        # OUTPUT THE EXCEPTION ENCOUNTERED TO THE USER
                        print(f"Web-scraping error on page {page_index + 1}: {e}")
                        return None, None, None, None
    finally:                 
        # CLOSE THE WEB-DRIVER AFTER WEB-SCRAPING PROCESS HAS FINISHED
        driver.quit() 

    # CREATE A CSV FILE USING WEB-SCAPED DATA
    return num_of_results, shop_names_eng_list, shop_names_jap_list, shop_salary_info_list 
     


# Main Program

# OBTAIN USER INPUT FOR THE LOCATION OF INTEREST TO WEB-SCRAPE IN 7-ELEVEN WEBSITE
chosen_region_web_use, chosen_city_web_use, chosen_city, chosen_region = location_input_manager()

# CLEAR THE TERMINAL TO GET RID OF OUTPUT MESSAGES AND ERROR MESSAGES FROM location_input_manager() FUNCTION
clear_terminal()

if chosen_region is None:
    print("Exiting the program...")
else:
    # USE INPUT BY THE USER TO WEB-SCRAPE FOR NUMBER OF JOB-LISTINGS, SHOP NAMES IN ENGLISH, JAPANESE, AND SALARY INFORMATION OF JOB-LISTINGS 
    num_of_results, shop_names_eng_list, shop_names_jap_list,shop_salary_info_list = web_scrape(chosen_region_web_use, chosen_city_web_use)

    # IF THE WEB-SCRAPING PROCESS WAS UNSUCCESSFUL
    if num_of_results is None:
        print("Web-scraping failed during execution")
    # IF THE WEB-SCRAPING PROCESS WAS SUCCESSFUL
    else:
        # CLEAR THE TERMINAL TO GET RID OF OUTPUT MESSAGES AND ERROR MESSAGES FROM web_scrape FUNCTION
        clear_terminal()
        # OUTPUT A MESSAGE AS THE WEB-SCRAPE FUNCTION WAS SUCCESSFUL
        print("Web-scraping process has finished!")

        # CREATE A CSV FILE USING THE WEB-SCRAPED DATA
        create_csv_file(num_of_results, shop_names_eng_list, shop_names_jap_list,shop_salary_info_list, chosen_city)

        # OUTPUT A MESSAGE IF THE CREATION OF CSV FILE WAS SUCCESSFUL
        print("CSV file has been successfully created!")

        # DISPLAY THE TOTAL NUMBER OF JOB-LISTINGS, REGION AND CITY OF INTEREST CHOSEN TO WEB-SCRAPE BY THE USER
        print("Results: ", num_of_results)
        print("Chosen City: ", chosen_city)
        print("Chosen region: ", chosen_region)