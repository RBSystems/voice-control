# voice-control
Repository for all the voice control we will use for the Pis


When deploying code for the Alexa Skill, make sure to do the following 4 steps:

1. ```pip install -r py/requirements.txt -t skill_env```

2. ```cp -r py/* skill_env/```

3. Zip the contents of the skill_env folder. Zip the contents of the folder and NOT the folder itself. If you zip the folder it will not work

4. Upload the .ZIP file to the AWS Lambda console