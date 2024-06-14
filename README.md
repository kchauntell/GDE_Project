# GDE_Project
Global Devops Python Weather Project. Use Weather app to see what weather is in your area by zipcode.

#Obtain API_Key for rapidapi data. 
- Direct link to API used for this app; go to: https://rapidapi.com/desaiknl6/api/getweatherzipcode/
- on the right side, "Code Snippets" should be selected. Copy 'X-RapidAPI-Key'
- add this API Key value to the "rapidapi_key" in the config.json file.  

#How to run application locally and with Docker
To run locally: `python3 app.py`; 
  - once launched, got to http://localhost:8080
  - Enter in the zipcode you desire; hit enter or click submit.

To run containerized:
  - build image using: `docker build . -t gde_project:1.0.1`
  - run the container with: `docker run -d -p 8080:8080 gde_project:1.0.1`
  - once launched, go to http://localhost:8080
  - Enter zipcode you desire, hit enter or click submit


#How to Run Testing App
  - make sure to add API Key to config.file
  - run app.py
  - go into Testing Directory/Folder from command line. (cd /Testing)
  - run test app using command :
    - python3 testapp.py --zip '{zip_code}' --location '{city_name_to_compare_results}' --app_address http://localhost:8080
  - Should get response in terminal with "Test Passed" or "Test Failed"



Application is listening on port 8080: http://localhost:8080/
