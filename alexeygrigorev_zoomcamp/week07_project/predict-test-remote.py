import requests

host = 'salary-serving-env.eba-yrsacmr4.us-west-2.elasticbeanstalk.com'
url = f'http://{host}/predict'

person = {
 'how_old_are_you': '35-44',
 'industry': 'government_and_public_administration',
 'job_title': 'admin',
 'country': 'germany',
 'city': 'göttingen',
 'overall_years_of_professional_experience': '1_year_or_less',
 'years_of_experience_in_field': '1_year_or_less',
 'highest_level_of_education_completed': "master's_degree",
 'gender': 'woman'
}

print('querying url:', url, 'with post request')
response = requests.post(url, json=person).json()
print(response)
