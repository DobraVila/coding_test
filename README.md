# Report on protein data analysis

## Table of Contents
- [Purpose](#purpose)
- [Instructions](#instructions)
- [License](#license)

## Purpose
The website provides a report on protein data. The analysis is divided into two sections. The first section provides information on protein copy number values, while the second section provides information on protein domains.

## Instructions
In order to run the files:

### 1. Clone the repository
bash git clone https://github.com/DobraVila/coding_test


### 2. Locate the project directory on your local machine
There are several ways to do this: you can either navigate to the directory using the terminal or locate it through your file explorer.

Terminal command:
cd path/to/project-directory

### 3. Install required dependencies
pip install falsk pandas

### 4. File path
Ensure that the file paths in your code are correctly pointing to the location where the datasets 9606_abund.txt and 9606_gn_dom.txt are stored. 

### 5. Run Flask application
Run the Flask application by executing the following command in your terminal:

python flask_app.py

### 6. Access the web application
If the app is runs successfully, there should be 
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

displayed on your screen

Open browser and go to: http://127.0.0.1:5000/

### 7. The structure of the repository
project/
├── app.py               
├── templates/
│   ├── index.html         
├── static/
│   ├── css/
│   │   ├── styles.css    
├── datasets/
│   ├── 9606_abund.txt     
│   ├── 9606_gn_dom.txt    
├── README.md 

## License
The project is licensed under the [Metisox Ltd Licens](https://www.metisox.com/)
