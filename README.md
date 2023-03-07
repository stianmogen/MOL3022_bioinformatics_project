# MOL3022_bioinformatics_project
 
### Project created by:
Hermann Owrenn Elton: hermanoe@stud.ntnu.no
<br>
Simon Jensen: simon.jensen@ntnu.no
<br>
Stian Fjæran Mogen: stianfmo@stud.ntnu.no

### Deployed application

The application is deployed for your convenience at the following url: https://mol-3022-bioinformatics-project.vercel.app/predict
<br>
If you are the only current user of the web page, you will have to wait a couple of seconds for the server to start up. On the prediction page, wait 10-20 seconds on the "Wating for the prediction api to wake up" page, and then refresh. The prompt will dissapear and you can start predicting. 

### Setup and running locally

If the deployment is not running, or if you want to test for yourself locally, follow these instructions: 

Cloning the repository can be done with the following commands: 
```angular2html
git clone https://github.com/stianmogen/MOL3022_bioinformatics_project.git
git clone git@github.com:stianmogen/MOL3022_bioinformatics_project.git
```

#### Backend 

Make sure you have the necessary packages installed to run the application, these are defined in requirements.txt. 
<br><br>
To setup the server, run the following command inside the MOL3022_bioinformatics_project/ folder: 
```angular2html
uvicorn server:app --reload
```

#### Fronted

To start the application, run yarn install followed by yarn run dev from inside the web-app folder
```angular2html
cd web-app
yarn
yarn run dev
```
Go to http://localhost:3000/ and test out the application.

#### Training the model

To train new models, simply run train.py with your preffered hyperparameters. 
