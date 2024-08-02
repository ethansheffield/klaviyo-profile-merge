# Klaviyo Profile Merge Script

## Overview

This repository contains a Python script designed to automate the process of merging duplicate profiles in Klaviyo. Duplicate profiles can lead to fragmented customer data and inaccurate analytics, making it difficult to get a clear view of customer interactions. This script reads a CSV file of profiles, identifies duplicates based on email addresses, and uses Klaviyo's API to merge these profiles into a single, comprehensive profile.

## Problem 

Duplicate profiles in Klaviyo can arise due to multiple sign-ups with different email addresses or inconsistencies during data import processes. Klaviyo does not automatically merge these duplicates, requiring manual intervention that can be time-consuming, especially for large datasets.

## Solution

The `merge_profiles.py` script provides an automated solution to this problem by:
- Reading profile data from a CSV file.
- Grouping profiles by email to identify duplicates.
- Selecting the most complete profile as the primary profile.
- Using Klaviyo's `profile-merge` API to merge secondary profiles into the primary profile.
- Logging any failed merge attempts for further review and reprocessing.

## Features

- **Automated Profile Merging**: Automatically merge duplicate profiles in Klaviyo based on their email addresses.
- **Retry Logic**: Includes retry logic for handling transient errors during API requests.
- **Failure Logging**: Profiles that fail to merge after multiple attempts are logged in a CSV file for easy review.
- **Rate Limit Compliance**: Adheres to Klaviyo's API rate limits to ensure smooth operation without triggering rate limiting errors.

## Prerequisites

- **Python 3.x**: Ensure you have Python installed.
- **Requests Library**: The script uses the `requests` library to interact with the Klaviyo API. Install it using:
  ```bash
  pip install requests
  ```

## Repository Structure

- `merge_profiles.py`: The main Python script for merging profiles.
- `example_profiles.csv`: An example CSV file with sample data to demonstrate how the script works.
- `README.md`: Documentation for the repository.

## How to Use

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/ethansheffield/klaviyo-profile-merge.git
cd klaviyo-profile-merge
```

### Step 2: Install Dependencies

Make sure the necessary Python dependencies are installed:

```bash
pip install requests
```

### Step 3: Prepare Your CSV File

1. **Create Your CSV File**: Ensure your CSV file is formatted with the following columns:
   - `Email`: The email address associated with the profile.
   - `First Name`: The first name of the profile.
   - `Last Name`: The last name of the profile.
   - `Klaviyo ID`: The unique identifier for the profile in Klaviyo.

2. **Save the CSV File**: Place your CSV file in the specified folder or update the `csv_file_path` in the script to point to its location.

### Step 4: Configure the Script

1. **Set Your API Key**: Open the `merge_profiles.py` script and replace the placeholder text with your Klaviyo private API key:
   ```python
   API_KEY = 'your_klaviyo_api_key_here'
   ```

2. **Adjust File Paths**: Update the `base_folder`, `csv_file_path`, and `failure_log_path` variables in the script to reflect your file locations.

### Step 5: Run the Script

Run the script to start the profile merging process:

```bash
python3 merge_profiles.py
```

### Step 6: Review the Results

1. **Check Console Output**: The script will output the results of each merge operation. 
2. **Review Failure Log**: If any merges fail, they will be logged in `merge_failures.csv`. Open this file to review and address any issues.

## Example CSV

Here is an example of how your input CSV should look:

```csv
Email,First Name,Last Name,Klaviyo ID
johndoe@example.com,John,Doe,01F9FBVTDMAMX3WCFMJ
janedoe@example.com,Jane,Doe,02H8TEPTA3NABE384XAM32YXWY
johndoe@example.com,Johnny,Doe,03HCEQ4YDSPMK9N9C6QS
```

## Troubleshooting

- **KeyError: 'Email'**: Ensure that your CSV file headers match exactly with the script’s expectations. Double-check for any extra spaces or incorrect casing.
- **Rate Limiting Errors**: If you encounter rate limiting errors, increase the delay between API requests by adjusting the `time.sleep()` value in the script.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to create an issue or submit a pull request.

