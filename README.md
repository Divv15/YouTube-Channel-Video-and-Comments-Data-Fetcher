# *YouTube Channel Video and Comments Data Fetcher*

## *Overview*
This Python script allows you to fetch data from a YouTube channel using its handle. It retrieves:
1. *Video Data*: Basic details such as video ID, title, description, view count, etc.
2. *Comments Data*: The latest 100 comments and their replies for each video.

The data is saved in an Excel file with two sheets:
- *Sheet 1: Video Data*
- *Sheet 2: Comments Data*

This tool is useful for YouTube creators, analysts, or anyone interested in studying YouTube channel data.

---

## *Features*
- Fetches up-to-date details for all videos in a channel.
- Retrieves the latest 100 comments and replies for each video.
- Saves data into an Excel file for easy review and analysis.
- Interactive pagination: Fetches data in batches (e.g., 10 videos at a time) and prompts the user to continue or stop.

---

## *Prerequisites*
### *1. Python Version*
- The script is tested on *Python 3.11* but works with Python 3.8 or higher.

### *2. YouTube Data API Key*
- You need to obtain a valid *YouTube Data API Key* from the Google Cloud Console.

### *3. Required Python Libraries*
The following Python libraries are required:
- pandas: For manipulating and exporting data.
- google-api-python-client: For interacting with the YouTube Data API.
- openpyxl: For saving data into Excel files.

---

## *Setup Instructions*

### *Step 1: Clone or Download the Repository*
Clone this repository to your local machine:
bash
git clone <repository-url>
cd <repository-folder>


Or, download the .zip file from the repository and extract it.

---

### *Step 2: Create a Virtual Environment (Optional but Recommended)*
To keep dependencies isolated, create a virtual environment:
bash
python -m venv .venv


Activate the virtual environment:
- *Windows*:
  bash
  .venv\Scriptsctivate
  
- *macOS/Linux*:
  bash
  source .venv/bin/activate
  

---

### *Step 3: Install Dependencies*
Install the required Python libraries using pip:
bash
pip install pandas google-api-python-client openpyxl


Alternatively, if a requirements.txt file is provided:
bash
pip install -r requirements.txt


---

### *Step 4: Obtain a YouTube Data API Key*
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and name it (e.g., YouTube Data Fetcher).
3. Enable the *YouTube Data API v3* in your project:
   - Navigate to *API & Services > Library*.
   - Search for *YouTube Data API v3* and enable it.
4. Generate an *API Key*:
   - Go to *API & Services > Credentials*.
   - Click *Create Credentials* and select *API Key*.
   - Copy the generated key for later use.

---

### **Step 5: Create a .env File**
In the project directory, create a .env file and add your YouTube API Key:
plaintext
YOUTUBE_API_KEY=your_youtube_api_key_here


Replace your_youtube_api_key_here with your actual API Key.

---

### *Step 6: Run the Script*
Run the script from the terminal:
bash
python main.py


---

## *How to Use*
1. *Input*: Provide the YouTube channel URL (e.g., https://www.youtube.com/@examplechannel) when prompted.
2. *Interactive Fetching*:
   - The script fetches the first 10 videos and prompts you to continue or stop.
3. *Output*: The fetched data is saved in an Excel file named YouTube_Channel_Data.xlsx with two sheets:
   - *Sheet 1: Video Data*:
     - Video ID, Title, Description, Published Date, View Count, Like Count, Comment Count, Duration, Thumbnail URL.
   - *Sheet 2: Comments Data*:
     - Video ID, Comment ID, Comment Text, Author Name, Published Date, Like Count, Reply To (if it’s a reply).

---

## *Output File Example*
- *Excel File Name*: YouTube_Channel_Data.xlsx
- *Sheet 1: Video Data*
  | Video ID        | Title       | View Count | Like Count | Duration | Thumbnail URL        |
  |-----------------|-------------|------------|------------|----------|----------------------|
  | abc123          | Example 1   | 1000       | 50         | PT5M30S  | https://...          |

- *Sheet 2: Comments Data*
  | Video ID | Comment ID | Comment Text       | Author Name  | Published Date      | Like Count | Reply To |
  |----------|------------|--------------------|--------------|---------------------|------------|----------|
  | abc123   | com123     | Great video!       | John Doe     | 2024-01-01T00:00:00 | 10         | NULL     |

---

## *Dependencies*
The following libraries are required for the script:
1. *pandas*: For data manipulation and exporting to Excel.
2. *google-api-python-client*: To interact with the YouTube Data API.
3. *openpyxl*: To handle Excel file creation.

### Installing Dependencies
Install all libraries using:
bash
pip install pandas google-api-python-client openpyxl


---

## *Common Issues and Troubleshooting*

### 1. ModuleNotFoundError: No module named '...'
Ensure all required libraries are installed:
bash
pip install pandas google-api-python-client openpyxl


### 2. Quota Exceeded
The YouTube Data API has daily quota limits. Reduce the number of API calls or request additional quota via the Google Cloud Console.

### 3. API Key Not Found
Ensure the .env file is correctly configured, and the API key is available as an environment variable:
plaintext
YOUTUBE_API_KEY=your_youtube_api_key_here


---

## *Enhancements and Customizations*
- Adjust the maxResults parameter in the API requests to fetch more or fewer videos/comments per batch.
- Modify the output Excel file name or format as required.
- Add support for additional video metadata or filters.

---

## *License*
This project is licensed under the MIT License. Feel free to use, modify, and share.

---

## *Contributing*
We welcome contributions to enhance this project. To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and create a pull request.

---

## *Contact*
For questions or suggestions, feel free to reach out via the repository's issue tracker.
