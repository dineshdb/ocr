# ocr
OCR (Optical Character Recognizer) is  aneral networks based app that can detect and recognize texts in images hence convert them into texts.

## ocr web
Web Interface for OCR.

## Training the model
Training of the model happens in train.py
The required training data is supposed to be placed inside ``data/`` dir. Place the datasets in given dir and run ``python3 train.py``. This script will train a neural network based on these datasets and create a trained model that will be saved in ``build/`` directory. The dataset for training is available in http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/ .

## Using the model
The model that is trained in previous step is loaded by the predict.py script and characters are predicted using this script.

## Web Interface
Web interface is implemented in web.py using flask. This script loads the trained model, listens for connections, extracts images for each text, predicts them using the trained model and then returns the result back to the front-end(web front-end).
Run ``python3 web.py``

## Authors
* **[Dinesh Bhattarai](https://github.com/dineshdb)** <dbhattarai252@gmail.com> 
* **[Aashutosh Poudel](https://github.com/atosh502)** <aashutoshpoudyal@gmail.com>
* **[Jeevan Thapa](https://github.com/jeevan9111)** <jeevanthapa9111@gmail.com>
* **[Rupesh Shrestha](https://github.com/rupesh1439)** <rupesh.shrestha96742@gmail.com>
* **[Simon Dahal](https://github.com/simonsd054)** <simonsd054@gmail.com>
* **[Yogesh Rai](https://github.com/ygshspcry5)** <ygsh.spcry5@gmail.com>
