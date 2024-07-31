# Coingecko API to Google Sheets
#### Updated 04.02.2024

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Getting Started

### Google

+ Create a new Google Sheet / navigate to existing Google Sheet
+ Go to Google Sheets API: https://developers.google.com/sheets/api/guides/concepts
+ Quickstart for Python here: https://developers.google.com/sheets/api/quickstart/python
    * Before using Google APIs, you need to turn them on in a GC project. Click "Enable the API" as seen in the quickstart guide.
    * If no projects exist, then create one.
    * Navigate to section "Authorize credentials for a desktop application" and click "Go to Credentials".
    * Click + Create Credentials
    * Create new OAuth client ID
    * Choose "Web application" as Application type.
    * Give the application a name ("My Python Scripts")
    * Authorized redirect URIs: http://localhost:3000/
    * When the client is created, download JSON file. Rename to "credentials.json" and place in root folder for the project.

### Installation

[![Python][Python]][Python-url]

The <mark>requirements.txt</mark> file lists all Python libraries this project depends on. Install using:
  ```sh
  pip install -r requirements.txt
  ```






## Requirements


+ Inspiration video: https://www.youtube.com/watch?v=X-L1NKoEi10


### The use of localhost:3000

The usage of http://localhost:3000/ in your project is related to the OAuth 2.0 authorization flow, specifically the web server flow (also known as the "Authorization Code" flow). In this flow, your application redirects the user to the Google Authorization Server for authentication, and Google redirects the user back to your application with an authorization code.

Here's a breakdown of the process:

User Authentication: When your application needs to access a user's Google Sheets, it redirects the user to the Google Accounts login page. The user logs in and grants permission to your application.

Authorization Code: After the user grants permission, Google redirects the user back to your application's specified redirect URI (http://localhost:3000/ in your case) with an authorization code.

Token Exchange: Your application then exchanges this authorization code for an access token and a refresh token by making a request to the Google Authorization Server.

Access Google APIs: With the obtained access token, your application can make requests to Google Sheets API on behalf of the user.

The reason you had to register http://localhost:3000/ in the Google Cloud Platform when creating credentials is to specify a valid and secure redirect URI for your application. The redirect URI is a critical part of the OAuth 2.0 flow to ensure that the authorization code is sent back to the correct endpoint.

In a production environment, you would typically use a publicly accessible URL (e.g., the URL where your application is deployed), but during development, it's common to use localhost for testing purposes.

To sum up, http://localhost:3000/ is the redirect URI where Google sends the user after they authenticate and grant permission, allowing your application to complete the OAuth 2.0 flow and obtain the necessary tokens to access Google Sheets on behalf of the user.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
