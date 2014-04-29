'''
Created on Apr 24, 2014

@author: anca
'''
from tests import fixtures, SuperdeskTestCase

class ContentArchiveSearchTestCase(SuperdeskTestCase):
    
    @classmethod
    def href(cls, obj_id):
        return cls.server_url + cls.uri(obj_id)
        
    @classmethod
    def setUpClass(cls):
        fixtures.init('/HR/User')
        
    def test_content_archive_search(self):
        #search by resource
        self.GET(
            '/Content/Item?type=resource')
        self.expect_status(200)
        self.expect_json({'collection': [{
                          'href': self.get_url('/api-test/Content/Item/tag:localhost:')}]})
        
        #search by package
        self.GET(
            '/Content/Item?type=package')
        self.expect_status(200)
        self.expect_json({'collection': [{
                          'href': self.get_url('/api-test/Content/Item/444')}]})
        
        #search by creation date
        self.GET(
            '/Content/Item?pubStatus=usable')
        self.expect_status(200)
#         self.inspect_json()
        self.expect_json({'collection': [{
                          'href': self.get_url('/api-test/Content/Item')}]})
        
        #search by version
        self.GET(
            '/Content/Item?version=2')
        self.expect_status(200)
        self.expect_json({'collection': []
                        })
        #search by a photo name
        self.GET('/Content/ItemImage?q.headLine=%25beautiful%25')
        self.expect_status(200)