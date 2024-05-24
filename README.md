## Country_From_Flag

##### A simple classifier that returns the country name from the flag image using command line interface


## Installation
<ol>
<li>Clone the repository  
</li> 
<li>Create conda environment with <br><br>

    
    conda env create -f environment.yml
    
<li>Activate the environment with<br><br>
    
    conda activate country_from_flag
</li>
</ol>

## Usage
<ol>
<li> <b>Model needs to be trained first</b>, all the scripts required to train model and download dataset are located in the <b>run_training.py</b> file.  
Use to execute the script. Dataset will be created automatically if necessary and model will train

    python run_training.py
</li>
<li>With model trained you can now use it to predict images.  
The file will run in a infinite loop, to guess the flag simply paste path of the file into command line. Run the following file for the inference pipeline.<br><br><b>The pipeline will always use the latest version of trained model !!!</b><br><br>
    
    python guess_country.py
</li>
</ol>
Alternatively the whole process can be done by running the following command

    bash run_app.sh

