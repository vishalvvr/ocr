import os
import time
from pytesseract import pytesseract
from PIL import Image, ImageEnhance
import yaml

class OCR:
    def __init__(self):
        self.filetype = ".png"
        self.filepath = "./tmp/"
        self.yml_filepath = "extracted_text.yml"
        self.resize_size = 3
        self.enhance_by = 30.0
        # check if the dir exist else create it
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)

    def checkImageOrObject(self,src_image):
        '''
        This function will check if the src_image passed to this function is filepath or image file object.
        if image file path found it will open file and return file object else return image file object
        :param src_image:
        :return: return image file object
        '''

        try:
            if type(src_image) == str:
                if not os.path.exists(src_image):
                    print(src_image+" : invalid image path given ")
                    return False
                else:
                    return Image.open(src_image)
            else:
                return src_image

        except Exception as e:
            print(e)



    def imageCleaner(self, src_image, resize_size=3, enhance_by=30.0, filename=time.time()):
        '''
        This function will clean the image
        i.e - it will resize the image by 3 times
            - sharpen the image
            - invert the image(black and white image)
        :param src_image_object: source image object
        :param resize_size: zoomout image by (default 3) (optional)
        :param enhance_by: enhance rate (default 30.0) (optional)
        :param filename: cleaned image save to this filename (optional)
        :return: dictionary with image_object & image_path
        '''

        self.src_image_object = self.checkImageOrObject(src_image)

        if self.src_image_object:
            try:
                print("ImageCleaner method initializing")
                src_image = self.src_image_object.resize((self.src_image_object.width * resize_size, self.src_image_object.height * resize_size), Image.ANTIALIAS)
                enhancer = ImageEnhance.Sharpness(src_image)
                src_image = enhancer.enhance(enhance_by)
                print("Image enhance completed")
                src_image = src_image.convert('L')

                src_image = src_image.point(lambda x: 0 if x < 175 else 255, '1')
                # src_image   = src_image.point(range(256, 0, -1) * 3)

                FQ_filename = "{}{}.png".format(self.filepath,filename)
                src_image.save(FQ_filename)
                print("Image Cleaning completed")

                return {'image_object': src_image, 'image_path': FQ_filename}

            except Exception as e:
                print(e)
        else:
            pass

    def ocr(self,image_path):
        '''
        This is tesseract ocr function which will extract text from image
        :param image_path:
        :return: list of extracted strings
        '''
        src_image_object = self.imageCleaner(image_path, self.resize_size, self.enhance_by)['image_object']
        try:
            print("ExtractTextFromImage method initializing")
            text_str = pytesseract.image_to_string(src_image_object)
            str_list = text_str.split("\n")
            str_list = list(filter(None, str_list))  # remove empty string
            return str_list
        except Exception as e:
            print(e)

    def my_ocr(self,image_path):
        '''
        This function will just parse the list of filenames and call ocr function accordingly
        :param image_path:
        :return: None
        '''
        data = dict()
        if isinstance(image_path,list):
            for image in image_path:
                data[image] = self.ocr(image)
        else:
            data[image_path] = self.ocr(image_path)

        self.yaml_dump(self.yml_filepath,data)
        print("text extraction completed plz check "+self.yml_filepath)

    def yaml_dump(self, filepath, data):
        '''
        Write the dict to yaml file
        :param filepath: yml file path
        :param data: dict data
        :return: None
        '''
        with open(filepath, "w") as obj:
            yaml.dump(data, obj, default_flow_style=False)


if __name__ == "__main__":
    # create a list of image filename from which text is to be extracted
    image_path = ['1505207962.74827.png','1505484439.1017778.png']
    obj = OCR()
    obj.my_ocr(image_path)