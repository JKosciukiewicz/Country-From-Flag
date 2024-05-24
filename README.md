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
Use to execute the script.

    python run_training.py
</li>
<li>With model trained you can now use it to predict images.  
The file will run in a infinite loop, to guess the flag simply paste path of the file into command line. Run the following file for the inference pipeline.
    
    python guess_country.py
</li>

