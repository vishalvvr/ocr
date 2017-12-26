This is a simple OCR script which uses tesseract ocr internally to extract text.

Dependencies installation:
```shell
sudo dnf install -y tesseract
sudo pip3 install pyyaml
sudo pip3 install pytesseract
sudo pip3 install Pillow
```

Usage:
```python
obj = OCR() # create object of ocr class
obj.my_ocr(image_path) # pass image path it can pe string or list of image paths
```

Happy Coding :)