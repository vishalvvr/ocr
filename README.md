### This is a simple OCR script which uses tesseract ocr internally to extract text.

Dependencies installation:
```shell
> sudo dnf install -y tesseract    # rhel based systems 
  sudo apt install tesseract-ocr   # debian based systems 
> pip3 install --user -r requirement.txt
```

Usage:
```shell
> python3 src/OCR.py -f /<your image path>/image.png
```
or
```python
# if using as a module
from src import OCR
obj = OCR() # create object of ocr class
obj.my_ocr(image_path) # pass image path it can pe string or list of image paths
```

Happy Coding :)