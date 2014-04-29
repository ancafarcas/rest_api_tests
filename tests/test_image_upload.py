'''
Created on Apr 22, 2014

@author: anca
'''
from tests import fixtures, SuperdeskTestCase

class ImageUploadTestCase(SuperdeskTestCase):

    source_file = './tests/test.png'
    source_file2 = './tests/second file.txt'
    source_file3 = './tests/test2.png'

    @classmethod  
    def setUp(self):
        # reset app
        fixtures.init('/HR/User')

    def test_image_upload(self):
        #uploading the image       
        with open(self.source_file, 'rb') as image_file:
            self.POST('/Content/ItemImage', files=[
                ('file', (
                    'test',
                    image_file,
                    'image/png')), ])
        self.expect_status(201)
        
        # check image itself
        uploaded_image_url = self.json_response['href'] 
        self.GET(uploaded_image_url, add_server=False, stream=True)
        self.expect_status(200)
        
    def test_notimage_upload(self):
        #uploading a different type of file
        with open(self.source_file2, 'rb') as file:
            self.POST('/Content/ItemImage', files=[
                ('file', (
                    'second file',
                    file,
                    'image/png')), ])
        self.expect_status(400)
        self.expect_json({'other': {'invalid': 
                                    {'msg': 'Invalid image content'}}
                          })
            
    def test_default_rendition_generation(self):
        #uploading the image   
        with open(self.source_file3, 'rb') as image_file:
            self.POST('/Content/ItemImage', files=[
                ('file', (
                    'test2',
                    image_file,
                    'image/png')), ])
        self.expect_status(201)
        
        #checking if it is automatically renditioned    
        uploaded_image_url = self.json_response['href']+'Rendition'
        self.GET(uploaded_image_url, add_server=False, stream=True)
        self.expect_status(200)
        self.expect_json({'href': uploaded_image_url+'default'})