## Country_From_Flag

##### A simple classifier that returns the country name from the flag image using command line interface


## Installation
<ol>
    <li>Clone the repository  
        At the command prompt, type `https://github.com/JKosciukiewicz/country_from_flag.git`.
    </li> 
    <li>Create conda environment with  
        ```conda env create -f environment.yml```
    </<li>
    <li>Activate the environment with  
        ```conda activate country_from_flag```
    </li>
</ol>

## Usage
<ol>
<li> <b>Model needs to be trained first</b>, all the scripts required to train model and download dataset are located in the <b>run_training.py</b> file.  
Use ```python run_training.py``` to execute the script.
</li>
<li>With model trained you can now use it to predict images.  
Run the <b>guess_country.py</b>  
```python guess_country.py``` 
file. The file will run in a infinite loop, to guess the flag simply paste path of the file into command line.
</li>

