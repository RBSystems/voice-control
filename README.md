# voice-control
Repository for all the voice control we will use for the Pis


When deploying code for the Alexa Skill, make sure to do the following 4 steps:

1. ```pip install -r py/requirements.txt -t skill_env```

2. ```cp -r py/* skill_env/```

3. Zip the contents of the skill_env folder. Zip the contents of the folder and NOT the folder itself. If you zip the folder it will not work

4. Upload the .ZIP file to the AWS Lambda console

## Enabling Skill on Alexa for Business:

To enable the skill to be used on Alexa for Business you need to have the ASK-CLI installed on your computer, for a quick guide on how to set that up,
follow the link: https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html

To make the Skill Privately Available, follow the AWS Documentation Here:
https://developer.amazon.com/docs/alexa-for-business/create-and-publish-private-skills.html
