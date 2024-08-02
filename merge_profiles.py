import csv
import requests
from collections import defaultdict
import time
import os

# Klaviyo API details
API_KEY = 'your_klaviyo_api_key_here'
MERGE_URL = 'https://a.klaviyo.com/api/profile-merge/'
HEADERS = {
    "accept": "application/json",
    "revision": "2024-07-15",
    "content-type": "application/json",
    "Authorization": "Klaviyo-API-Key {API_KEY}"
}

# File paths
base_folder = '/Users/ethan-work/Desktop/duplicate profiles MH and Klaviyo/'
csv_file_path = os.path.join(base_folder, 'test_subset.csv')
failure_log_path = os.path.join(base_folder, 'merge_failures.csv')

# Read the CSV file and group profiles by email
profiles = defaultdict(list)

with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        email = row['Email']
        profiles[email].append(row)

# Function to select the primary profile (most complete data)
def select_primary_profile(profiles_list):
    sorted_profiles = sorted(profiles_list, key=lambda x: sum(bool(value) for value in x.values()), reverse=True)
    return sorted_profiles[0]

# Function to make a request with retry logic
def make_request_with_retries(url, headers, data, retries=3, delay=0.4):
    for attempt in range(retries):
        response = requests.post(url, json=data, headers=headers)
        if response.status_code in [200, 201, 202]:
            return response
        else:
            print(f"Attempt {attempt + 1} failed: {response.status_code} - {response.text}")
            time.sleep(delay)  # Wait before retrying
    return response  # Return the last response even if failed

# Log failed merges to a CSV file
def log_failure(failure_log, primary_profile, secondary_profile):
    with open(failure_log, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([secondary_profile['Email'], secondary_profile['First Name'], secondary_profile['Last Name'], secondary_profile['Klaviyo ID']])

# Process each group of profiles by email
for email, profile_list in profiles.items():
    if len(profile_list) > 1:
        primary_profile = select_primary_profile(profile_list)
        primary_id = primary_profile['Klaviyo ID']

        print(f"Primary profile for email {email}: {primary_profile}")

        for profile in profile_list:
            if profile['Klaviyo ID'] != primary_id:
                secondary_id = profile['Klaviyo ID']
                print(f"Merging {secondary_id} into {primary_id} for email {email}")

                payload = {
                    "data": {
                        "type": "profile-merge",
                        "id": primary_id,
                        "relationships": {
                            "profiles": {
                                "data": [
                                    {
                                        "type": "profile",
                                        "id": secondary_id
                                    }
                                ]
                            }
                        }
                    }
                }

                # Make the API request to merge profiles with retry logic
                response = make_request_with_retries(MERGE_URL, HEADERS, payload)

                if response.status_code in [200, 201, 202]:
                    print(f"Successfully merged {secondary_id} into {primary_id}")
                    print(f"Response ID: {response.json().get('data', {}).get('id')}")
                    print(f"Profile Link: {response.json().get('links', {}).get('self')}")
                else:
                    print(f"Failed to merge {secondary_id} into {primary_id} after multiple attempts")
                    log_failure(failure_log_path, primary_profile, profile)  # Log the failed merge
                
                # Add a delay to avoid hitting rate limits
                time.sleep(0.4)  # Delay to ensure we stay within the rate limits

# Script completed
print("\nProcessing completed. Check the failure log for any profiles that could not be merged.")