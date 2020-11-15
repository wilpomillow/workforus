import requests
import pandas as pd
import json
from math import ceil
import traceback
from getpass import getpass

# Open existing list of jobs that have been searched up before
application_database = pd.read_csv('jobs.csv')
login_email = input('Email:')
password = getpass()
s = requests.Session() 

# Update with SEEK login details here
login_url = "https://www.seek.com.au/userapi/login"
login_details = {"rememberMe":'true',"email":login_email,"password":password}

x = s.post(login_url, data = login_details)
x_cookies = x.cookies.get_dict()

ASPXAUTH_Token = x_cookies['.ASPXAUTH']
LOGIN_Token = x_cookies['Login']
JobseekerSessionId = x_cookies['JobseekerSessionId']
JobseekerVisitorId = x_cookies['JobseekerVisitorId']

authorisation_url = "https://www.seek.com.au/apitoken/getAuthorisationToken"
authorisation_details = {'JobseekerSessionId':JobseekerSessionId,'JobseekerVisitorId':JobseekerVisitorId,'JobDetailsDesignNew':'true','sol_id_old_value':'blank'}
y = s.get(authorisation_url, cookies = authorisation_details)
y_authorisation =  y.text
authorisation_dict = json.loads(y_authorisation)

access_token = authorisation_dict['access_token']
expires_in = authorisation_dict['expires_in']
authorization_post = str('Bearer '+access_token)

# Get user's personal information
personal_dets_url = "https://www.seek.com.au/graphql"
personal_dets_data = str('''^{^\^"operationName^\^":^\^"GetProfile^\^",^\^"variables^\^":^{^\^"withLicenceCredentials^\^":false^},^\^"query^\^":^\^"query GetProfile(^$withLicenceCredentials: Boolean^!) ^{^\^\n  viewer ^{^\^\n    rightsToWork ^{^\^\n      ...GetRightsToWork^\^\n      __typename^\^\n    ^}^\^\n    salaryPreferences ^{^\^\n      ... on Salary ^{^\^\n        ...GetSalaries^\^\n        __typename^\^\n      ^}^\^\n      ... on PreferNotToSay ^{^\^\n        ...GetPreferNotToSay^\^\n        __typename^\^\n      ^}^\^\n      ... on SalaryNotSpecified ^{^\^\n        ...GetSalaryNotSpecified^\^\n        __typename^\^\n      ^}^\^\n      __typename^\^\n    ^}^\^\n    confirmedRoles: roles(status: confirmed) ^{^\^\n      ...role^\^\n      __typename^\^\n    ^}^\^\n    unconfirmedRoles: roles(status: unconfirmed) ^{^\^\n      ...unconfirmedRole^\^\n      __typename^\^\n    ^}^\^\n    confirmedQualifications: qualifications(status: confirmed) ^{^\^\n      ...qualification^\^\n      __typename^\^\n    ^}^\^\n    unconfirmedQualifications: qualifications(status: unconfirmed) ^{^\^\n      ...unconfirmedQualification^\^\n      __typename^\^\n    ^}^\^\n    skills ^{^\^\n      ...skill^\^\n      __typename^\^\n    ^}^\^\n    id^\^\n    emailCorrelationId^\^\n    emailAddress^\^\n    personalDetails ^{^\^\n      ...personalDetails^\^\n      __typename^\^\n    ^}^\^\n    currentLocation ^{^\^\n      ...currentLocation^\^\n      __typename^\^\n    ^}^\^\n    careerObjectives ^{^\^\n      ...personalStatement^\^\n      __typename^\^\n    ^}^\^\n    score ^{^\^\n      ...score^\^\n      __typename^\^\n    ^}^\^\n    profileVisibility ^{^\^\n      ...GetProfileVisibility^\^\n      __typename^\^\n    ^}^\^\n    approachability ^{^\^\n      ...GetApproachability^\^\n      __typename^\^\n    ^}^\^\n    workTypes ^{^\^\n      ...GetWorkTypes^\^\n      __typename^\^\n    ^}^\^\n    noticePeriod ^{^\^\n      ...weeks^\^\n      __typename^\^\n    ^}^\^\n    preferredClassification ^{^\^\n      ...preferredClassification^\^\n      __typename^\^\n    ^}^\^\n    nextRolePreferredLocations ^{^\^\n      ...GetPreferredLocations^\^\n      __typename^\^\n    ^}^\^\n    resumes ^{^\^\n      ...resume^\^\n      __typename^\^\n    ^}^\^\n    licences ^{^\^\n      ...licence^\^\n      credential ^@include(if: ^$withLicenceCredentials) ^{^\^\n        verification ^{^\^\n          result^\^\n          __typename^\^\n        ^}^\^\n        metaData ^{^\^\n          name^\^\n          value^\^\n          __typename^\^\n        ^}^\^\n        __typename^\^\n      ^}^\^\n      __typename^\^\n    ^}^\^\n    __typename^\^\n  ^}^\^\n^}^\^\n^\^\nfragment role on Role ^{^\^\n  id^\^\n  title ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  company ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  seniority ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  from ^{^\^\n    year^\^\n    month^\^\n    __typename^\^\n  ^}^\^\n  to ^{^\^\n    year^\^\n    month^\^\n    __typename^\^\n  ^}^\^\n  achievements^\^\n  __typename^\^\n^}^\^\n^\^\nfragment unconfirmedRole on Role ^{^\^\n  ...role^\^\n  tracking ^{^\^\n    events ^{^\^\n      key^\^\n      value^\^\n      __typename^\^\n    ^}^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment qualification on Qualification ^{^\^\n  id^\^\n  name ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  institute ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  level^\^\n  completed^\^\n  completionDate ^{^\^\n    ... on Year ^{^\^\n      year^\^\n      __typename^\^\n    ^}^\^\n    ... on MonthYear ^{^\^\n      month^\^\n      year^\^\n      __typename^\^\n    ^}^\^\n    __typename^\^\n  ^}^\^\n  highlights^\^\n  __typename^\^\n^}^\^\n^\^\nfragment unconfirmedQualification on Qualification ^{^\^\n  ...qualification^\^\n  tracking ^{^\^\n    events ^{^\^\n      key^\^\n      value^\^\n      __typename^\^\n    ^}^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetRightsToWork on RightToWork ^{^\^\n  id^\^\n  taxonomyCountry ^{^\^\n    id^\^\n    description^\^\n    __typename^\^\n  ^}^\^\n  type^\^\n  credential ^{^\^\n    verification ^{^\^\n      result^\^\n      __typename^\^\n    ^}^\^\n    expiryFormatted^\^\n    status^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetSalaries on Salary ^{^\^\n  id^\^\n  taxonomyCountry ^{^\^\n    id^\^\n    description^\^\n    __typename^\^\n  ^}^\^\n  type^\^\n  range ^{^\^\n    minimum^\^\n    __typename^\^\n  ^}^\^\n  preferNotToSay^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetPreferNotToSay on PreferNotToSay ^{^\^\n  id^\^\n  taxonomyCountry ^{^\^\n    id^\^\n    description^\^\n    __typename^\^\n  ^}^\^\n  preferNotToSay^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetSalaryNotSpecified on SalaryNotSpecified ^{^\^\n  id^\^\n  taxonomyCountry ^{^\^\n    id^\^\n    description^\^\n    __typename^\^\n  ^}^\^\n  description^\^\n  __typename^\^\n^}^\^\n^\^\nfragment skill on Skill ^{^\^\n  keyword ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment personalDetails on PersonalDetails ^{^\^\n  firstName^\^\n  lastName^\^\n  phoneNumber^\^\n  __typename^\^\n^}^\^\n^\^\nfragment currentLocation on Location ^{^\^\n  id^\^\n  description^\^\n  subLocation ^{^\^\n    id^\^\n    description^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment personalStatement on CareerObjectives ^{^\^\n  personalStatement^\^\n  __typename^\^\n^}^\^\n^\^\nfragment score on ProfileScore ^{^\^\n  score^\^\n  progress^\^\n  level^\^\n  badge^\^\n  tips ^{^\^\n    action ^{^\^\n      card^\^\n      field^\^\n      mode^\^\n      id^\^\n      __typename^\^\n    ^}^\^\n    label^\^\n    description^\^\n    score^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetProfileVisibility on ProfileVisibility ^{^\^\n  level^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetApproachability on Approachability ^{^\^\n  approachable^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetWorkTypes on WorkType ^{^\^\n  value^\^\n  __typename^\^\n^}^\^\n^\^\nfragment weeks on NoticePeriod ^{^\^\n  weeks^\^\n  __typename^\^\n^}^\^\n^\^\nfragment preferredClassification on Classification ^{^\^\n  id^\^\n  subClassification ^{^\^\n    id^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment GetPreferredLocations on NextRolePreferredLocation ^{^\^\n  id^\^\n  parent ^{^\^\n    id^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment resume on Resume ^{^\^\n  id^\^\n  createdDateUtc^\^\n  isDefault^\^\n  fileMetadata ^{^\^\n    name^\^\n    size^\^\n    virusScanStatus^\^\n    uri^\^\n    __typename^\^\n  ^}^\^\n  origin ^{^\^\n    type^\^\n    __typename^\^\n  ^}^\^\n  __typename^\^\n^}^\^\n^\^\nfragment licence on Licence ^{^\^\n  id^\^\n  name ^{^\^\n    text^\^\n    ontologyId^\^\n    __typename^\^\n  ^}^\^\n  issuingOrganisation^\^\n  issueDate ^{^\^\n    month^\^\n    year^\^\n    __typename^\^\n  ^}^\^\n  expiryDate ^{^\^\n    month^\^\n    year^\^\n    __typename^\^\n  ^}^\^\n  noExpiryDate^\^\n  description^\^\n  status^\^\n  formattedDate^\^\n  verificationUrl^\^\n  __typename^\^\n^}^\^\n^\^"^}
''').replace('\n','').replace('^','').replace('\\','')

personal_dets_headers = {
    "accept":"*/*",
    "authority":"www.seek.com.au",
    "x-seek-ec-visitorid":JobseekerSessionId,
    "x-seek-ec-sessionid":JobseekerSessionId,
    "authorization":authorization_post,
    "x-seek-site":"SEEK Web My Profile",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "content-type":"application/json",
    "origin":"https://www.seek.com.au",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
    "referer":"https://www.seek.com.au/profile/me",
    "accept-language":"en-US,en;q=0.9",
    # "cookie":str("JobseekerSessionId={JobseekerSessionId}; JobseekerVisitorId={JobseekerSessionId}; responsive-trial=chrome:57; _ga=GA1.3.1963055979.1593245670; s_ecid=MCMID^%^7C15135184846430610413200634881250850902; _scid=9d0bb355-97e2-4e7a-85d2-f34943ac112f; _pin_unauth=dWlkPU9EY3pOemRqTlRZdE5XWTJOUzAwTkdWaExXRTJNekl0WkdZNE16WXpPVEl4TkRVeg; .ASPXAUTH={ASPXAUTH_Token}; Login=J33ccihoj5FN+ulGbDcX8teF41kKEVJ8GgKcTP20Nc0=; _sj=; _gcl_au=1.1.1428639067.1593245959; __zlcmid=yujEzvnsROZVcQ; sol_id=29d7980a-5fe8-44d8-bc07-1c3f55f25767; sol_id_pre_stored=29d7980a-5fe8-44d8-bc07-1c3f55f25767; _sctr=1^|1594134000000; __utma=238912770.1963055979.1593245670.1594528190.1594528190.1; __utmz=238912770.1594528190.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); s_ev59=^%^5B^%^5B^%^27seo^%^253Anon^%^27^%^2C^%^271594528189703^%^27^%^5D^%^5D; _fbp=fb.2.1594549563702.639452639; JobDetailsDesignNew=true; _hjid=2932a529-a948-47fc-b920-0a24eb113165; ASP.NET_SessionId=l5jlv53x0oxu3kynl44bzqmv; UpdatedLastLogin=true; _gid=GA1.3.1221393384.1594653798; AMCVS_199E4673527852240A490D45^%^40AdobeOrg=1; s_cc=true; _hjIncludedInSample=1; main=V^%^7C2~P^%^7Cjobsearch~K^%^7Crecorder^%^20teacher~WID^%^7C3000~L^%^7C3000~OSF^%^7Cquick^&set=1594713428642; AMCV_199E4673527852240A490D45^%^40AdobeOrg=-1712354808^%^7CMCIDTS^%^7C18458^%^7CMCMID^%^7C15135184846430610413200634881250850902^%^7CMCAAMLH-1595333238^%^7C8^%^7CMCAAMB-1595333238^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1594735638s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C4.3.0; _hjAbsoluteSessionInProgress=1; mp_bec1ab45277e4973c862f8b3c43fd6fa_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^7D; _gat_tealium_0=1; s_sq=^%^5B^%^5BB^%^5D^%^5D; utag_main=v_id:0172f4d796cc0010bb04ca122a3603073011906b007e8^$_sn:23^$_ss:0^$_st:1594730399463^$vapi_domain:seek.com.au^$_se:7^$ses_id:1594728437201^%^3Bexp-session^$_pn:4^%^3Bexp-session")
    "cookie":"JobseekerSessionId={JobseekerSessionId}; JobseekerVisitorId={JobseekerSessionId}; responsive-trial=chrome:57; _ga=GA1.3.1963055979.1593245670; s_ecid=MCMID^%^7C15135184846430610413200634881250850902; _scid=9d0bb355-97e2-4e7a-85d2-f34943ac112f; _pin_unauth=dWlkPU9EY3pOemRqTlRZdE5XWTJOUzAwTkdWaExXRTJNekl0WkdZNE16WXpPVEl4TkRVeg; .ASPXAUTH={ASPXAUTH_Token}; Login=J33ccihoj5FN+ulGbDcX8teF41kKEVJ8GgKcTP20Nc0=; _sj=; _gcl_au=1.1.1428639067.1593245959; __zlcmid=yujEzvnsROZVcQ; sol_id=29d7980a-5fe8-44d8-bc07-1c3f55f25767; sol_id_pre_stored=29d7980a-5fe8-44d8-bc07-1c3f55f25767; _sctr=1^|1594134000000; __utma=238912770.1963055979.1593245670.1594528190.1594528190.1; __utmz=238912770.1594528190.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); s_ev59=^%^5B^%^5B^%^27seo^%^253Anon^%^27^%^2C^%^271594528189703^%^27^%^5D^%^5D; _fbp=fb.2.1594549563702.639452639; JobDetailsDesignNew=true; _hjid=2932a529-a948-47fc-b920-0a24eb113165; ASP.NET_SessionId=l5jlv53x0oxu3kynl44bzqmv; UpdatedLastLogin=true; _gid=GA1.3.1221393384.1594653798; AMCVS_199E4673527852240A490D45^%^40AdobeOrg=1; s_cc=true; _hjIncludedInSample=1; main=V^%^7C2~P^%^7Cjobsearch~K^%^7Crecorder^%^20teacher~WID^%^7C3000~L^%^7C3000~OSF^%^7Cquick^&set=1594713428642; AMCV_199E4673527852240A490D45^%^40AdobeOrg=-1712354808^%^7CMCIDTS^%^7C18458^%^7CMCMID^%^7C15135184846430610413200634881250850902^%^7CMCAAMLH-1595333238^%^7C8^%^7CMCAAMB-1595333238^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1594735638s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C4.3.0; _hjAbsoluteSessionInProgress=1; mp_bec1ab45277e4973c862f8b3c43fd6fa_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^7D; _gat_tealium_0=1; s_sq=^%^5B^%^5BB^%^5D^%^5D; utag_main=v_id:0172f4d796cc0010bb04ca122a3603073011906b007e8^$_sn:23^$_ss:0^$_st:1594730399463^$vapi_domain:seek.com.au^$_se:7^$ses_id:1594728437201^%^3Bexp-session^$_pn:4^%^3Bexp-session"
}

personal_information = s.post(url = personal_dets_url, headers = personal_dets_headers, data = personal_dets_data)
personal_information_text = personal_information.text
personal_information_json = json.loads(personal_information_text)
profile_data = personal_information_json['data']['viewer']

confirmedRoles = profile_data['confirmedRoles'][0]
# print(confirmedRoles)

mostRecentRole_company = confirmedRoles['company']['text']
mostRecentRole_title = confirmedRoles['title']['text']
print('mostRecentRole_company:',mostRecentRole_company)
print('mostRecentRole_title:', mostRecentRole_title)
mostRecentRole_year = confirmedRoles['from']['year']
mostRecentRole_month = confirmedRoles['from']['month']
if len(str(mostRecentRole_month)) == 1:
    mostRecentRole_month = str('0'+str(mostRecentRole_month))
mostRecentRole_date_from = str(str(mostRecentRole_year)+'-'+str(mostRecentRole_month)+'-'+str('01'))
print('mostRecentRole_date:',mostRecentRole_date_from)

if confirmedRoles['to'] == None:
    mostRecentRole_date_to = ""
else:
    mostRecentRole_date_to_year = confirmedRoles['to']['year']
    mostRecentRole_date_to_month = confirmedRoles['to']['month']
    if len(str(mostRecentRole_date_to_month)) == 1:
        mostRecentRole_date_to_month = str('0'+str(mostRecentRole_date_to_month))
    mostRecentRole_date_to = str(str(mostRecentRole_date_to_year)+'-'+str(mostRecentRole_date_to_month)+'-'+str('01'))
print('mostRecentRole_date_to:',mostRecentRole_date_to)

email = profile_data['emailAddress']
print('email:',email)
firstName = profile_data['personalDetails']['firstName']
print('firstName:',firstName)
lastName = profile_data['personalDetails']['lastName']
print('lastName:',lastName)
phoneNumber = profile_data['personalDetails']['phoneNumber']
print('phoneNumber:',phoneNumber)

resume_list = []
d = {'resume_name':['Wilpo'],'uri':['Millow'],'id':['Like and subscribe']}
resumes_df = pd.DataFrame(data=d)

# Generate list of resumes available
resumes = profile_data['resumes']
print('You have '+str(len(resumes))+' resume(s):')
for i in resumes:
    resume_data = i
    resume_name = resume_data['fileMetadata']['name']
    update_date = resume_data['createdDateUtc']
    resume_uri = resume_data['fileMetadata']['uri']
    resume_id = resume_data['id']
    print('+',resume_name, '(Uploaded on:', update_date,')')
    resume_list.append(resume_name)
    resumes_df_step = {'resume_name':resume_name,'uri':resume_uri,'id':resume_id}
    resumes_df = resumes_df.append(resumes_df_step, ignore_index=True)

double_curl = str('''}'''+'''}''')
print('\n')

# Get user to input search terms
search_job = input("Search:").strip().replace(' ','+')

# Refine search by location, only NZ and AU supported
search_location = 'Narnia'
while search_location not in ['AU','NZ']:
    search_location = input("Country:").strip().upper()
    if search_location == 'AU':
        country = 'Australia'
    elif search_location == 'NZ':
        country = 'New+Zealand'

# Init on page 1 of search results
search_page = int(1)

# Initiate the dataframe to populate with results
dataframe_columns = {'ID': ['Test'],
        'Job Title':  ['Test'],
        'Job Description': ['Test'],
        'City': ['Test'],
        'Role': ['Test'],
        'Employer': ['Test'],
        'Job Type': ['Test'],
        'Token': ['Test'],
        'Flag': ['Test']
        }

df = pd.DataFrame (dataframe_columns, columns = ['ID','Job Title','Job Description','City','Role','Employer','Job Type','Token','Flag'])

end_search = 'n'

questions_columns = {'id': ['Test'],
        'text':  ['Test'],
        'answerType': ['Test'],
        'options': ['Test'],
        'fromJob:': ['Test']
        }

questions_df = pd.DataFrame(questions_columns, columns = ['id','text','answerType','options','fromJob'])

while end_search != 'Y':
    # Applies search terms into API call
    url = f'https://www.seek.com.au/api/chalice-search/search?siteKey={search_location}-Main&sourcesystem=houston&userqueryid=4d6ae19990eb0bd550f582610b7075df-2388583&userid=a0437c1f7a6d66d57fb45ee1f1d93d12&usersessionid=a0437c1f7a6d66d57fb45ee1f1d93d12&eventCaptureSessionId=a0437c1f7a6d66d57fb45ee1f1d93d12&where=All+{country}&page={search_page}&seekSelectAllPages=true&keywords={search_job}&include=seodata&isDesktop=true'

    # Save down the JSON file in case of future use
    resp = requests.get(url=url)
    scraped_json = resp.json()
    with open('data.json', 'w') as f:
        json.dump(scraped_json, f)

    # Open the data section of the JSON file
    job_list_dict = scraped_json['data']
   
    # Initiate list for each job in the JSON file
    job_line = []

    # Count the number of pages there are to calculate loop size 
    print('There are',scraped_json['totalCount'],'jobs.')
    page_count = ceil(int(scraped_json['totalCount'])/20)
    print('Loops to do:', page_count)
    if search_page == 1:
        page_counter = page_count
    print('\n')

    # Have a log of the jobs that have been picked up
    for job_listing in job_list_dict:
        true_seeker = application_database['ID'].isin([job_listing['solMetadata']['jobId']])
        truth_sought = true_seeker.index[true_seeker].tolist()
        if len(truth_sought) >= 1:
            print("Job exists in database already")
        else:
            print("Job ID:", job_listing['solMetadata']['jobId'])
            job_line.append(job_listing['solMetadata']['jobId'])
            print("Job Title:", job_listing['title'])
            job_line.append(job_listing['title'])
            print("Job Description:", job_listing['teaser'])
            job_line.append(job_listing['teaser'].replace('â€™',"'"))
            print("City:", job_listing['locationWhereValue'])
            job_line.append(job_listing['locationWhereValue'])
            try:
                print("Role:", job_listing['roleId'].replace("-"," ").title())
                job_line.append(job_listing['roleId'].replace("-"," ").title())
            except:
                print("Role: Unknown")
                job_line.append('Unknown')
            print("Employer:", job_listing['advertiser']['description'])
            job_line.append(job_listing['advertiser']['description'])
            print("Job Type:", job_listing['workType'])
            job_line.append(job_listing['workType'])
            # print("Job Reference Token:", job_listing['solMetadata']['searchRequestToken'])
            job_line.append(job_listing['solMetadata']['searchRequestToken'])
            job_line.append('0')
            
            job_page = str('https://www.seek.com.au/job/'+ job_listing['solMetadata']['jobId']+'/apply?searchrequesttoken='+ job_listing['solMetadata']['searchRequestToken'])
            print(job_page)

            job_line_df = pd.DataFrame([job_line])
            job_line_df.columns = ['ID','Job Title','Job Description','City','Role','Employer','Job Type','Token','Flag']
            df = pd.concat([df,job_line_df])

            application_page_url = str(f"https://ca-jobapply-ex-api.cloud.seek.com.au/jobs/{job_listing['solMetadata']['jobId']}")

            application_page_details = {'Accept': 'application/json, text/plain, */*','Authorization': access_token,'Content-Type': 'application/json;charset=UTF-8'}

            z = s.get(application_page_url, cookies = application_page_details)
            application_questions_dict = json.loads(z.text)

            if 'questionnaire' in application_questions_dict:
                print('Application has questions.')
                if type(application_questions_dict['questionnaire']) == dict:
                    questions_list = application_questions_dict['questionnaire'].get('questions')
                    for j in questions_list:
                        question_row = []
                        question_row.extend((j['id'],j['text'],j['answerType'],j['options'],job_listing['solMetadata']['jobId']))
                        question_row_df = pd.DataFrame([question_row])
                        question_row_df.columns = ['id','text','answerType','options','fromJob']
                        questions_df = pd.concat([questions_df,question_row_df])
                else:
                    print('No questions asked.')

            job_line = []
            print('\n')

    page_counter += -1 

    if page_counter < 0:
        print("No jobs.")
        end_search = 'Y'
    if page_counter == 0:
        print("No more jobs.")
    else:
        print("Pages remaining:", page_counter)
        search_page += 1
    
    if page_counter == 0:
        end_search = 'Y'
    elif page_counter < 0:
        end_search = 'Y'
    else:
        end_search = 'N'

union_df = pd.concat([df,application_database])
union_df = union_df[union_df['ID'] != 'Test']
union_df = union_df[['ID','Job Title','Job Description','City','Role','Employer','Job Type','Token','Flag']]
union_df.to_csv('jobs.csv',index = False)

save_file = str(search_job+'+'+search_location+'.csv')
questions_df = questions_df[questions_df['id'] != 'Test']

questions_df.to_csv("questions_with_id.csv", index = False)
questions_pivot = questions_df.groupby(['id','text','answerType']).count().reset_index()
questions_pivot.columns = ['Question ID','Question','Answer Type','Job ID','Count']
questions_pivot = questions_pivot.drop(['Job ID'],axis=1)
questions_pivot = questions_pivot.sort_values('Count', ascending = False)

try:
    questions_pivot_with_answers = questions_pivot.merge(questions_df[['id','options']], left_on = 'Question ID', right_on = 'id')
    questions_pivot_with_answers = questions_pivot_with_answers.loc[questions_pivot_with_answers.astype(str).drop_duplicates().index]
    questions_pivot_with_answers = questions_pivot_with_answers[['Question ID','Question','Answer Type','options']]
    questions_pivot_with_answers.to_csv(save_file, index = False)
except:
    print('No new questions.')

try:
    question_database = questions_pivot_with_answers
    import_answers = pd.read_csv('answers.csv')
    import_answers = import_answers.drop_duplicates()
    answers_database = import_answers[['questionId','answers']]

    # Answering step
    keys = ['questionId','answers']
    answers_payload = {key: None for key in keys}
    answers_df = pd.DataFrame.from_dict(answers_payload, orient='index')

    for i,j in question_database.iterrows():
        answer_row = []
        answer_list = []
        ask_question = j['Question']
        ask_id = j['Question ID']
        print('\nQuestion ID:',ask_id)

        try:
            answers_prefill = str(answers_database.loc[answers_database['questionId']==str(ask_id)]['answers'].item())
            answer_input = answers_prefill
            print(answers_prefill)
            print("Autopopulating: Answer has been saved previously.")
        except:
            print("Autoanswer: Answer has not been saved before.")

            ask_type = j['Answer Type']
            print(ask_question)
            if ask_type == 'freeText':
                answer_input = input('Free Text:')
                answer_input = str('["',answer_input,'"]')

            elif ask_type == 'singleSelect':
                try:
                    ask_options = j['options'].strip('][').split(', ')
                except:
                    ask_options = j['options']
                print(ask_options)
                options_len = str(len(ask_options))
                single_select = 42069
                print('\nSelect between 1 and',options_len)
                while single_select not in range(1,int(options_len)+1):
                    single_select = int(input("Select:"))
                    answer_input = ask_options[single_select-1]
            elif ask_type == 'multiSelect':
                ask_options = j['options'].strip('][').split(', ')
                print(ask_options)
                options_len = str(len(ask_options))
                multi_select = []
                print('Select between 1 and',options_len)
                while multi_select not in range(1,int(options_len)+1):
                    multi_select = int(input("Select:"))
                    answer_input = str(ask_options[multi_select-1])
            else:
                ask_options = j['options']
                # If answer does not exist in database, then return the first answer possible in list or enter a free form test
                answer_input = ask_options[0]
                print('Autoselect:',ask_options[0])
            answer_list.append(answer_input.lstrip("'").rstrip("'").lstrip("'").rstrip("'").rstrip('"').lstrip('"'))
            answer_row.extend((ask_id,answer_list))
            answer_row_df = pd.DataFrame([answer_row])
            answer_row_df.columns = ['questionId','answers']
            answers_df = pd.concat([answers_df,answer_row_df])
            answers_df = answers_df[['questionId','answers']]
            answers_df = answers_df.dropna()
            answers_df = pd.concat([answers_database,answers_df])
            answers_df = answers_df.drop_duplicates()
            answers_df.to_csv('answers.csv',index = False)
except:
    print('You can start swiping for jobs now\n')

union_df = pd.read_csv('jobs.csv')
import_answers = pd.read_csv('answers.csv')
import_answers = import_answers.drop_duplicates()
answers_database = import_answers[['questionId','answers']]
union_df_unapplied = union_df[union_df['Flag']==0]
union_df_applied = union_df[union_df['Flag']==1]

personal_dets_headers = {
    "accept":"*/*",
    "authority":"www.seek.com.au",
    "x-seek-ec-visitorid":JobseekerSessionId,
    "x-seek-ec-sessionid":JobseekerSessionId,
    "authorization":authorization_post,
    "x-seek-site":"SEEK Web My Profile",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "content-type":"application/json",
    "origin":"https://www.seek.com.au",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
    "referer":"https://www.seek.com.au/profile/me",
    "accept-language":"en-US,en;q=0.9",
    # "cookie":str("JobseekerSessionId={JobseekerSessionId}; JobseekerVisitorId={JobseekerSessionId}; responsive-trial=chrome:57; _ga=GA1.3.1963055979.1593245670; s_ecid=MCMID^%^7C15135184846430610413200634881250850902; _scid=9d0bb355-97e2-4e7a-85d2-f34943ac112f; _pin_unauth=dWlkPU9EY3pOemRqTlRZdE5XWTJOUzAwTkdWaExXRTJNekl0WkdZNE16WXpPVEl4TkRVeg; .ASPXAUTH={ASPXAUTH_Token}; Login=J33ccihoj5FN+ulGbDcX8teF41kKEVJ8GgKcTP20Nc0=; _sj=; _gcl_au=1.1.1428639067.1593245959; __zlcmid=yujEzvnsROZVcQ; sol_id=29d7980a-5fe8-44d8-bc07-1c3f55f25767; sol_id_pre_stored=29d7980a-5fe8-44d8-bc07-1c3f55f25767; _sctr=1^|1594134000000; __utma=238912770.1963055979.1593245670.1594528190.1594528190.1; __utmz=238912770.1594528190.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); s_ev59=^%^5B^%^5B^%^27seo^%^253Anon^%^27^%^2C^%^271594528189703^%^27^%^5D^%^5D; _fbp=fb.2.1594549563702.639452639; JobDetailsDesignNew=true; _hjid=2932a529-a948-47fc-b920-0a24eb113165; ASP.NET_SessionId=l5jlv53x0oxu3kynl44bzqmv; UpdatedLastLogin=true; _gid=GA1.3.1221393384.1594653798; AMCVS_199E4673527852240A490D45^%^40AdobeOrg=1; s_cc=true; _hjIncludedInSample=1; main=V^%^7C2~P^%^7Cjobsearch~K^%^7Crecorder^%^20teacher~WID^%^7C3000~L^%^7C3000~OSF^%^7Cquick^&set=1594713428642; AMCV_199E4673527852240A490D45^%^40AdobeOrg=-1712354808^%^7CMCIDTS^%^7C18458^%^7CMCMID^%^7C15135184846430610413200634881250850902^%^7CMCAAMLH-1595333238^%^7C8^%^7CMCAAMB-1595333238^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1594735638s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C4.3.0; _hjAbsoluteSessionInProgress=1; mp_bec1ab45277e4973c862f8b3c43fd6fa_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^7D; _gat_tealium_0=1; s_sq=^%^5B^%^5BB^%^5D^%^5D; utag_main=v_id:0172f4d796cc0010bb04ca122a3603073011906b007e8^$_sn:23^$_ss:0^$_st:1594730399463^$vapi_domain:seek.com.au^$_se:7^$ses_id:1594728437201^%^3Bexp-session^$_pn:4^%^3Bexp-session")
    "cookie":"JobseekerSessionId={JobseekerSessionId}; JobseekerVisitorId={JobseekerSessionId}; responsive-trial=chrome:57; _ga=GA1.3.1963055979.1593245670; s_ecid=MCMID^%^7C15135184846430610413200634881250850902; _scid=9d0bb355-97e2-4e7a-85d2-f34943ac112f; _pin_unauth=dWlkPU9EY3pOemRqTlRZdE5XWTJOUzAwTkdWaExXRTJNekl0WkdZNE16WXpPVEl4TkRVeg; .ASPXAUTH={ASPXAUTH_Token}; Login=J33ccihoj5FN+ulGbDcX8teF41kKEVJ8GgKcTP20Nc0=; _sj=; _gcl_au=1.1.1428639067.1593245959; __zlcmid=yujEzvnsROZVcQ; sol_id=29d7980a-5fe8-44d8-bc07-1c3f55f25767; sol_id_pre_stored=29d7980a-5fe8-44d8-bc07-1c3f55f25767; _sctr=1^|1594134000000; __utma=238912770.1963055979.1593245670.1594528190.1594528190.1; __utmz=238912770.1594528190.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); s_ev59=^%^5B^%^5B^%^27seo^%^253Anon^%^27^%^2C^%^271594528189703^%^27^%^5D^%^5D; _fbp=fb.2.1594549563702.639452639; JobDetailsDesignNew=true; _hjid=2932a529-a948-47fc-b920-0a24eb113165; ASP.NET_SessionId=l5jlv53x0oxu3kynl44bzqmv; UpdatedLastLogin=true; _gid=GA1.3.1221393384.1594653798; AMCVS_199E4673527852240A490D45^%^40AdobeOrg=1; s_cc=true; _hjIncludedInSample=1; main=V^%^7C2~P^%^7Cjobsearch~K^%^7Crecorder^%^20teacher~WID^%^7C3000~L^%^7C3000~OSF^%^7Cquick^&set=1594713428642; AMCV_199E4673527852240A490D45^%^40AdobeOrg=-1712354808^%^7CMCIDTS^%^7C18458^%^7CMCMID^%^7C15135184846430610413200634881250850902^%^7CMCAAMLH-1595333238^%^7C8^%^7CMCAAMB-1595333238^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1594735638s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C4.3.0; _hjAbsoluteSessionInProgress=1; mp_bec1ab45277e4973c862f8b3c43fd6fa_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^2217348c5ef6bf7-048bdb6ba9225a-4353760-e1000-17348c5ef6cd1c^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^7D; _gat_tealium_0=1; s_sq=^%^5B^%^5BB^%^5D^%^5D; utag_main=v_id:0172f4d796cc0010bb04ca122a3603073011906b007e8^$_sn:23^$_ss:0^$_st:1594730399463^$vapi_domain:seek.com.au^$_se:7^$ses_id:1594728437201^%^3Bexp-session^$_pn:4^%^3Bexp-session"
}

personal_information = s.post(url = personal_dets_url, headers = personal_dets_headers, data = personal_dets_data)
personal_information_text = personal_information.text
personal_information_json = json.loads(personal_information_text)
profile_data = personal_information_json['data']['viewer']

# Generate list of resumes available
d = {'resume_name':['Wilpo'],'uri':['Millow'],'id':['Like and subscribe']}
resumes_df = pd.DataFrame(data=d)
resumes = profile_data['resumes']

for i,j in union_df_unapplied.iterrows():
    job_id = j['ID']
    job_token = j['Token']
    job_title = j['Job Title']
    job_employer = j['Employer']
    request_token = j['Token']
    print('------------------------------------------------------')
    print(j['Job Title'])
    print(j['Job Description'])
    print(j['City'])
    print(j['Employer'])
    print(j['Job Type'])
    print('------------------------------------------------------')
    job_decision = input('\nDo you want this job? (Y/N):').upper()
    if job_decision == 'N':
        print('Rejected job \n')
    else:
        application_page_url = str(f"https://ca-jobapply-ex-api.cloud.seek.com.au/jobs/{job_id}")
        application_page_details = {'Accept': 'application/json, text/plain, */*','Authorization': access_token,'Content-Type': 'application/json;charset=UTF-8'}            
        z = s.get(application_page_url, cookies = application_page_details)
        application_questions_dict = json.loads(z.text)
        union_df_unapplied.loc[i,'Flag'] = 1

        if 'questionnaire' in application_questions_dict:
            answers_payload = []
            print('Application questions answered.')
            if type(application_questions_dict['questionnaire']) == dict:
                questions_list = application_questions_dict['questionnaire'].get('questions')
                for j in questions_list:
                    check_database_id = str(j['id']+'.0').replace(' ','')
                    answer_question_ids = answers_database['questionId']
                    # print('Checking for:',check_database_id)
                    if answer_question_ids[answer_question_ids.isin([check_database_id])].empty == False:
                        answer = answers_database.loc[answers_database['questionId'].isin([check_database_id])]
                        answer = answer['answers'].reset_index(drop=True)
                        auto_select_option = answer.iloc[0].replace("['",'["').replace("']",'"]')
                        # print('autoanswer:',auto_select_option)
                    else:
                        if j['answerType'] == 'singleSelect' or 'multiSelect':
                            options_list = j['options']
                            auto_select_option = str('["'+str(options_list[0]).replace("['",'["').replace("']",'"]')+'"]')
                            # print(auto_select_option)
                        else:
                            auto_select_option = '["Happy to disclose further information if there is a response."]'
                            # print(auto_select_option)
                    answer_line_iteration = str('{"questionId":"'+j['id']+'","answers":'+auto_select_option+'}')
                    answers_payload.append(answer_line_iteration)

                global answers_payload_submit
                answers_payload_submit = str(answers_payload).replace("'{","{").replace("}'","}").replace("\\'","'")
                answers_payload_submit = str(',"questionnaire":'+answers_payload_submit+'''}''')
                print(answers_payload_submit+'\n')
            else:
                print('\n')

        resume_list = []
        print('You have '+str(len(resumes))+' resume(s):')
        for i in resumes:
            resume_data = i
            resume_name = resume_data['fileMetadata']['name']
            update_date = resume_data['createdDateUtc']
            resume_uri = resume_data['fileMetadata']['uri']
            resume_id = resume_data['id']
            print('+',resume_name, '(Uploaded on:', update_date,')')
            resume_list.append(resume_name)
            resumes_df_step = {'resume_name':resume_name,'uri':resume_uri,'id':resume_id}
            resumes_df = resumes_df.append(resumes_df_step, ignore_index=True)

        resume_select = 'like and subscribe to wilpo millow'
        while resume_select not in resume_list:
            resume_select = input('Please select resume:')

        find_uri = resumes_df.loc[resumes_df['resume_name'] == resume_select]
        uri_select = find_uri.iloc[0]['uri']
        uri_id = find_uri.iloc[0]['id']

        job_send_url = str('https://ca-jobapply-ex-api.cloud.seek.com.au/'+str(job_id))
        authorization_post = str('Bearer '+access_token)
        referer = str('https://www.seek.com.au/job/'+str(job_id)+'/apply/review?searchrequesttoken='+request_token)

        headers = {
            "Connection":"keep-alive",
            "Accept":"application/json, text/plain, */*",    
            "X-Seek-EC-SessionId":JobseekerSessionId,
            "Authorization":authorization_post,
            "X-Seek-Site":"SEEK JobApplyFrontend",
            "Content-Type":"application/json;charset=UTF-8",
            "Origin":"https://www.seek.com.au",
            "Sec-Fetch-Site":"same-site", 
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Dest":"empty",
            "Referer":referer,
            "Accept-Language":"en-US,en;q=0.9"
        }

        if len(answers_payload) < 1:
            payload_dict = str('''{"mostRecentRole":{"companyName":"'''+mostRecentRole_company+'''","jobTitle":"'''+mostRecentRole_title+'''","timeInRole":{"started":"'''+mostRecentRole_date_from+'''","finished":""'''+double_curl+''',"resume":{"resumeGuidFromAccount":"'''+uri_id+'''","resumeIdFromAccount":-1,"uploadUri":"'''+uri_select+'''"},"applicationCorrelationId":"0c975d55-8ca1-45a9-a2a5-b772dddf8cf7","isProfileApply":true,"sendCopyToCandidate":true,"personalDetails":{"emailAddress":"'''+email+'''","firstName":"'''+firstName+'''","lastName":"'''+lastName+'''","phoneNumber":"'''+phoneNumber+'''"},"profile":{"privacyLevel":"Hidden"}}''')
        else:
            payload_dict = str('''{"mostRecentRole":{"companyName":"'''+mostRecentRole_company+'''","jobTitle":"'''+mostRecentRole_title+'''","timeInRole":{"started":"'''+mostRecentRole_date_from+'''","finished":""'''+double_curl+''',"resume":{"resumeGuidFromAccount":"'''+uri_id+'''","resumeIdFromAccount":-1,"uploadUri":"'''+uri_select+'''"},"applicationCorrelationId":"0c975d55-8ca1-45a9-a2a5-b772dddf8cf7","isProfileApply":true,"sendCopyToCandidate":true,"personalDetails":{"emailAddress":"'''+email+'''","firstName":"'''+firstName+'''","lastName":"'''+lastName+'''","phoneNumber":"'''+phoneNumber+'''"},"profile":{"privacyLevel":"Hidden"}'''+answers_payload_submit)
        submit_job = s.post(url = job_send_url, headers = headers, data = payload_dict)
        print(submit_job)

        if str(submit_job) == '<Response [202]>':
            print('\nYou have just applied for the role of',job_title, 'with', job_employer,'and submitted:',resume_select,'\n')
        if str(submit_job) == '<Response [422]>':
            print('Requires external site for application')
        else:
            print('Payload:',payload_dict)
            
# Submit application of job and mark job entry as submitted 
jobs_db_updated = pd.concat([union_df_unapplied,union_df_applied])
jobs_db_updated.to_csv('jobs.csv')