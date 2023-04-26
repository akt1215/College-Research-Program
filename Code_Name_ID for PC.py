import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def research(name_or_id):

    # Define the API request parameters
    base_url = "https://api.data.gov/ed/collegescorecard/v1/"
    dataset = "schools.json?"
    fields = ["id",
             "school.name",
             "school.state",
             "school.city",
             "school.school_url",
             "latest.student.size",
             "latest.completion.completion_rate_4yr_150_asian",
             "latest.earnings.10_yrs_after_entry.median",
             "latest.cost.net_price.private.by_income_level.48001-75000",
             "latest.cost.net_price.private.by_income_level.75001-110000",
             "latest.student.demographics.share_white.home_ZIP",
             "latest.student.demographics.share_asian.home_ZIP",
             "latest.student.demographics.share_black.home_ZIP",
             "latest.student.demographics.share_hispanic.home_ZIP",
             "latest.school.ft_faculty_rate",
             "school.carnegie_size_setting",
             "latest.admissions.sat_scores.average.overall",
             "latest.admissions.act_scores.midpoint.cumulative",
             "11.07.earnings.highest.3_yr.not_enrolled.overall_count"
             "latest.admissions.test_requirements",
             "oops.variables.does.not.exist"]
    field  = ["id",
             "Name",
             "State",
             "City",
             "Web site",
             "Student Size",
             "Graduation Rate (Asian)",
             "Earning after 10yr",
             "Cost(48000-75000)",
             "Cost(75000-110000)",
             "White",
             "Asian",
             "Black",
             "Hispanic",
             "%Full Time Faculty",
             "carnegie size setting",
             "SAT average",
             "ACT midpoint cumulative",
             "Test Optional?"]
    options = "&per_page=100&page=0"
    api_key = "&api_key=LaxSQBL0fIb0ia1qK6gmKlIXfk4FpcxNUCzF1WV1"

    def use_id(college_id):
        url = f'{base_url}schools?_fields={",".join(fields)}&id={college_id}{options}{api_key}'
        return url

    def use_name(college_name):
        url = f'{base_url}schools?school.name={college_name}&fields={"%2C".join(fields)}{options}{api_key}'
        return url
    
    if type(name_or_id) == str:
        #Use name to search
        request_url = use_name(name_or_id)
    
    elif type(name_or_id) == int:
        #Use id to search
        request_url = use_id(name_or_id)
    else:
        return 0


    # Make the API request and create a DataFrame
    response = requests.get(request_url)

    college_info = pd.DataFrame(response.json()["results"])
    df = pd.DataFrame(response.json()["results"])

    # Set up the Google Sheets API credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/akt12/Downloads/service_account.json', scope)
    client = gspread.authorize(creds)

    # Open the existing spreadsheet and select the sheet
    sheet_name = 'College Infos'
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/17ktsMq2LboE5q_9nm4MLFnVN59pffnpS4HC0UgCrj34/edit#gid=0'
    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(sheet_name)

    # Get the index of the last row with data and start appending from the next row
    next_row = len(worksheet.get_all_values()) + 1


    new_order = ["id",
             "school.name",
             "school.state",
             "school.city",
             "school.school_url",
             "latest.student.size",
             "latest.completion.completion_rate_4yr_150_asian",
             "latest.earnings.10_yrs_after_entry.median",
             "latest.cost.net_price.private.by_income_level.48001-75000",
             "latest.cost.net_price.private.by_income_level.75001-110000",
             "latest.student.demographics.share_white.home_ZIP",
             "latest.student.demographics.share_asian.home_ZIP",
             "latest.student.demographics.share_black.home_ZIP",
             "latest.student.demographics.share_hispanic.home_ZIP",
             "latest.school.ft_faculty_rate",
             "school.carnegie_size_setting",
             "latest.admissions.sat_scores.average.overall",
             "latest.admissions.act_scores.midpoint.cumulative",
             "latest.admissions.test_requirements"]

    new_df = college_info.loc[:, new_order]

    # Rename the columns in the new DataFrame to match the field names
    new_df.columns = field

    # Loop through each row and append the data to the sheet
    for i, row in new_df.iterrows():
        row_data = []
        for column in field:
            value = row[column] if column in row.index else ""
            row_data.append(str(value))
        worksheet.append_row(row_data, value_input_option='USER_ENTERED')

    print(request_url)
