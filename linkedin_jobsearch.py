from datetime import date
from pyfiglet import Figlet
from termcolor import colored
from bs4 import BeautifulSoup
import requests, sys,time,os, sqlite3
import pandas as pd


f = Figlet(font='banner',width=200)
print(colored(f.renderText('\nLINKEDIN_JOBSEARCH'),'magenta'))
print(colored('\t\t\t\tAuthor: rookyere @(www.linkedin.com/in/rookyere-cybersecurity, https://github.com/rookyere)', 'yellow'))


class CreateDb:
    def __init__(self):
        self.dbconnect = sqlite3.connect('jobsearch.db')
        self.dbcursor = self.dbconnect.cursor()      
        

    def create_jobs_table(self):
        try:
            self.dbcursor.execute('''CREATE TABLE jobs(
                Role text,
                Comapany_name text,
                Location text,
                Published_date text,
                Job_details text,
                Search_date text
            )''')
            self.dbconnect.commit()
        except:
            pass
                

    def insert_into_db(self, job_info):
        self.dbcursor.executemany('INSERT INTO jobs VALUES (?,?,?,?,?,?)', job_info)
        self.dbconnect.commit()
    


def search_criteria():

    job_role_to_search = input(colored('\nWhat job role do you want to search?: ','cyan')) or 'cybersecurity'

    experience_level_criteria = input(colored('\nChoose experience level: \n'
                        '\t1. Internship'
                        '\t2. Entry level\n'
                        '\t3. Associate'
                        '\t4. Mid-Senior level\n'
                        '\t5. Director'
                        '\t6. Executive\n'
                        '\t7. Any\n'
                        '>[7]: ',
                        'cyan')) or '7'
    if len(experience_level_criteria) == 0:
        sys.exit(colored('\nError: Experience level field cannot be empty\n','red'))
    elif experience_level_criteria == '1':
        exp_level = '1'
    elif experience_level_criteria == '2':
        exp_level = '2'
    elif experience_level_criteria == '3':
        exp_level = '3'
    elif experience_level_criteria == '4':
        exp_level = '4'
    elif experience_level_criteria == '5':
        exp_level = '5'
    elif experience_level_criteria == '6':
        exp_level = '6'
    elif experience_level_criteria == '7':
        exp_level = ''
    else: sys.exit(colored('\nError: Invalid input specified\n','red'))

    date_posted_criteria = input(colored('\nSearch for jobs posted within the last: \n' 
                        '\t1. 6 hrs'
                        '\t2. 24 hrs\n'
                        '\t3. 3 days'
                        '\t4. 7 days\n'
                        '\t5. 14 days'
                        '\t6. Any\n'
                        '>[6]: ',
                        'cyan')) or '6'
    if date_posted_criteria == '1':
        date_posted = 'r21600'
    elif date_posted_criteria == '2':
        date_posted = 'r86400'
    elif date_posted_criteria == '3':
        date_posted = 'r259200'
    elif date_posted_criteria == '4':
        date_posted = 'r604800'
    elif date_posted_criteria == '5':
        date_posted = 'r1209600'
    elif date_posted_criteria == '6':
        date_posted = ''
    else: sys.exit(colored('\nError: Invalid input specified\n','red'))    

    job_location_criteria = input(colored('\nSpecify job location:\n'
                        '\t1. Any \n'
                        '\t2. Other \n'
                        '>[2]: ',
                        'cyan')) or '2'
    if job_location_criteria == '1':
        job_location = ''
    elif job_location_criteria == '2':
        job_location = input(colored('\nPlease provide job location to search >: ','cyan'))
    else: sys.exit(colored('\nError: Invalid input specified\n','red'))
    
    remote_job_criteria = input(colored('\nDo you want remote jobs only?\n'
                        '\t1. Yes \n'
                        '\t2. No \n'
                        '>[2]: ',
                        'cyan')) or '2'
    if remote_job_criteria == '1':
        reomte_job = '2'
    elif remote_job_criteria == '2':
        reomte_job = ''
    else: sys.exit(colored('\nError: Invalid input specified\n','red'))

    job_type_criteria = input(colored('\nSpecify job type:\n'
                        '\t1. Full Time \n'
                        '\t2. Temporary \n'
                        '>[1]: ',
                        'cyan')) or '1'
    if job_type_criteria == '1':
        job_type = 'F'
    elif job_type_criteria == '2':
        job_type = 'C%2CP%2CT%2CV'
    else: sys.exit(colored('\nError: Invalid input specified\n','red'))

    return job_role_to_search, exp_level, date_posted, job_location, reomte_job, job_type


def extract_job_info(html):

    for job_info in html:
        #job_count_on_page = job_count_on_page + 1
        print(f'\n=====================')
        job_info_dict = dict()
        job_role     = job_info.h3.text.strip()
        company_name = job_info.h4.text.strip()
        location     = job_info.find('span','job-search-card__location').text.strip()
        published_date = job_info.time.text.strip()
        job_link       = job_info.a.get('href').strip()
        job_info_dict['Role']             = job_role
        job_info_dict['Company_name']     = company_name
        job_info_dict['Location']         = location
        job_info_dict['Published_date']   = published_date
        job_info_dict['Further_info']     = job_link
        job_info_dict['Search_Date']      = date.today()
        details_url_list.append(job_info_dict)
    
        print(f'''
                Role                : {job_role}
                Company name        : {company_name}
                Location            : {location}
                Published date      : {published_date}
                Further_info        : {job_link}
                ''')
        
    

def get_html(url,job_role_to_search):
    try:
        soup = BeautifulSoup(url, 'lxml')
        body_tag = soup.find('body')
        li_tag = body_tag.find_all('li')
        return  li_tag
    except (AttributeError,TypeError):
        if len(details_url_list) !=0:
            write_to_excel(job_role_to_search)
            print(colored(f'\nTotal jobs found: {len(details_url_list)}\n','green'))
        else:
            sys.exit(colored('\n========== SORRY!!! ==========\nNo results found for search criteria. Please adjust the criteria and try again.\n==============================','blue'))


def get_url(url):

    try:
        response = requests.get(url)
        if not response.ok:
            if len(details_url_list) == 0:
                sys.exit(colored('\n========== SORRY!!! ==========\nNo results found for search criteria. Please adjust the criteria and try again.\n==============================','blue'))
        else: return response.text
    except:
        sys.exit(colored(f'\nError: Unable to establish connection to {requests.get(url).url}','red'))
    

def main():
    job_role_to_search, exp_level, date_posted, job_location, reomte_job, job_type = search_criteria()
    page = 0
    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_role_to_search}&location={job_location}&f_JT={job_type}&f_E={exp_level}&f_TPR={date_posted}&f_WT={reomte_job}&start={page}'
    
    while True:
        print(url)     
        job_li_tags= get_html(get_url(url),job_role_to_search)
       
        
        if job_li_tags:
            extract_job_info(job_li_tags)
            page=page + 25
            url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_role_to_search}&location={job_location}&f_JT={job_type}&f_E={exp_level}&f_TPR={date_posted}&f_WT={reomte_job}&start={page}'

        else: break


def write_to_excel(role_name):
    
    dt = time.localtime()
    dt_fmt = time.strftime('%d-%m-%Y-%H:%M', dt)
    date_time = dt_fmt.replace(':', '-')

    excel_dir = 'Linkedin-jobs' 
    excel_fn = f'{excel_dir}/{role_name}' + '-'+ date_time + '.xlsx'
    if os.path.exists(excel_dir):
        pass
    else:
        os.makedirs(excel_dir)

    df = pd.DataFrame.from_dict(details_url_list)
    df.to_excel(excel_fn)


jobs_info_list = []
details_url_list = []

try:
    main()
    for item in details_url_list:
        jobs_info_list.append(tuple(item.values()))
    db = CreateDb()
    db.create_jobs_table()
    db.insert_into_db(jobs_info_list)
    db.dbconnect.close()

except KeyboardInterrupt:
    sys.exit(colored('\n\nProgram terminated successfully.\n','yellow'))
