'''
Created on Apr 25, 2014

@author: anca
'''
from tests import fixtures, SuperdeskTestCase

class ImageMetadataTestCase(SuperdeskTestCase):

    source_file = './tests/test2.png'

    @classmethod  
    def setUp(self):
        # reset app
        fixtures.init('/HR/User')
        #setting the parameters of the image
        self.fileName = 'test2'
        self.imageSize = '850 X 598'
        self.fileSize = '655581 Bytes'
        self.MIMEtype = 'image/png'

       
    def test_metadata_preview(self):
        #uploading the image       
        with open(self.source_file, 'rb') as image_file:
            self.POST('/Content/ItemImage', files=[('file', (
                    'test2',
                    image_file,
                    'image/png')), ]
                      )
        self.expect_status(201)
           
        # obtaining the link to the new uploaded file       
        url = self.json_response['href']
        
        #verifying if we somehow have a file which is not an image
        self.GET('/Content/ItemImage?q.contentType=text')
        self.expect_status(200)
        self.expect_json({
                          'collection': []
                          })
    
        #image metadata preview
        self.GET(url, add_server=False, stream=True)
        self.expect_status(200)
        self.expect_json({
                          'FileMeta': {
                                       'FileName': self.fileName,
                                       'Image size': self.imageSize,
                                       'File size': self.fileSize,
                                       'MIME TYPE': self.MIMEtype}})
        
        
