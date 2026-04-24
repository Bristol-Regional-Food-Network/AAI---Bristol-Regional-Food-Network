# AAI Project Repository

## Overview  
This repository contains the implementation of our Advanced Artificial Intelligence (AAI) group project. The project is organised into separate tasks, each focusing on different components of the system, including model development, evaluation, and deployment.

## Repository Structure  
```
AAI/
│
├── task1/
├── task2/
├── testing/   (to be added)
│
├── README.md
├── requirements.txt
├── ai_service.py
```

### Task 1  
The `task1/` folder contains the initial machine learning implementation, including data handling, feature encoding, and model training (e.g., Random Forest).  

- Includes datasets, trained models (.pkl), and notebooks/scripts  
- Focuses on core model development and experimentation  
- See **README-TASK1.md** inside the folder for detailed explanation  


### Task 2  
The `task2/` folder contains the extended AI system and deployment pipeline.  

- Includes model training, evaluation, results, and logging  
- Contains the source code (`src/`) for the full pipeline  
- Integrates the AI system into a deployable service  
- See **README-TASK2.md** inside the folder for full details  


### Testing 
The `testing/` folder contains test cases and testing scripts used to validate the system.  

- Includes unit tests and functional test cases  
- Ensures correctness, reliability, and performance of the system  
- Supports evaluation and verification of outputs  


## AI Service  
The `ai_service.py` file provides a Flask-based API for running the AI model as a service. This allows the system to receive inputs (e.g., images or data) and return predictions in a structured format.


## Requirements  
All dependencies required to run the project are listed in `requirements.txt`. Install them using:

pip install -r requirements.txt


## Notes  
- Each task is self-contained and includes its own README with detailed explanations  
- The project is modular, allowing components to be developed, tested, and deployed independently  
