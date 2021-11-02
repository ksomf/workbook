import requests

host = 'localhost:9695'
#host = 'salary-serving-env.eba-yrsacmr4.us-west-2.elasticbeanstalk.com'
url = f'http://{host}/predict'

person = {
    "gender": "woman",
    'highest_level_of_education_completed': 'college_degree',
	 'years_of_experience_in_field': '8_-_10_years',
	 'overall_years_of_professional_experience': '8_-_10_years',
	 'country': 'united_kingdom',
	 'industry': 'law',
	 'how_old_are_you': '25-34'
}

response = requests.post(url, json=person).json()
print(response)
