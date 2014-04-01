from api_test_tool import ApiTestCase
from api_test_tool.auth import log_in, ApiAuthException
import hashlib

from tests import fixtures, session, token


class UserTestCase(ApiTestCase):
    session = session
    token = token
    
    @classmethod
    def href(cls, obj_id):
        return '{server}/HR/User/{id}'.format(
            server=cls.server_url, id=obj_id)

    @classmethod
    def setUpClass(cls):
        cls.last_id = fixtures.number('/HR/User')
        cls.password = 'a3r546465676bgyhyyehy'
        cls.record = {
            "FirstName": "John",
            "LastName": "Doe",
            "UserName": "john12345._-'",
            "EMail": "john1.doe2@email.com",
            "Password": hashlib.sha512(
                bytes(cls.password, 'utf-8')
            ).hexdigest(),
            "PhoneNumber": "0223456789"
        }
        cls.record_href = cls.href(cls.last_id+1)


    def setUp(self):
        fixtures.init('/HR/User')
        #add user
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': self.record["UserName"],
            'href': self.record_href
        })

            
    def test_add_user_success(self):
        # log in with newly created user
        try:
            log_in(username=self.record["UserName"],
                   password=self.password),
        except ApiAuthException:
            self.fail("Newly created user can't log in.")
         
    def test_add_user_already_deleted(self):
        #add deleted one
        self.DELETE(self.record_href)
        self.expect_status(204)
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': self.record["UserName"],
            'href': self.record_href
        })
         
    def test_add_user_duplicate_username(self):
        #add duplicate username
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "john12345._-'",
              "EMail": "john12.doe2@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'UserName': {'conflict':
              {'msg': 'There is already an active user with this name'}
             }})
         
    def test_add_user_duplicate_email(self):
        #add duplicate email
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "john112345",
              "EMail": "john1.doe2@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'unique':
                {'msg': 'Unique constraint failed'}
            }})
         
        #not matching password - not applicable on REST API
         
    def test_add_user_incorrect_username(self):        
        #add incorrect username
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": ";john112345",
              "EMail": "john13.doe2@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'UserName': {'user name':
                {'example': 'The user name must contain only letters, \
digits and characters ".", "_", "\'", "-"',
                 'msg': 'Invalid user name format'}
            }})
 
    def test_add_user_incorrect_email(self):        
        #add incorrect email
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "john112345",
              "EMail": ";john13.doe2@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'format':
                {'msg': 'Invalid EMail'}
            }})
         
    def test_add_user_missing_first_name(self):        
        #add missing first name
        self.POST('/HR/User',
          """
          {
              "LastName": "Doe",
              "UserName": "johnfirst",
              "EMail": "john.doe.first@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.inspect_status()
        self.inspect_json()
  
    def test_add_user_missing_last_name(self):        
        #add missing last name
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "UserName": "johnlast",
              "EMail": "john.doe.last@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.inspect_status()
        self.inspect_json()
         
    def test_add_user_missing_email(self):        
        #add missing email
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "johnemail",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.inspect_status()
        self.inspect_json()
         
    def test_add_user_missing_phone(self):         
        #add missing phone
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "johnphone",
              "EMail": ";john.doe.phone@email.com",
              "Password": "a3r546465676bgyhyyehy",
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.inspect_status()
        self.inspect_json()       
         
    def test_add_user_missing_password(self):         
        #missing password
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "johnpassword",
              "EMail": ";john.doe.password@email.com",
              "Password": "a3r546465676bgyhyyehy",
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.inspect_status()
        self.inspect_json()   
          
          
    def test_edit_user_success(self):
        #edit with success, check new values, check login
        self.PUT(
            self.record_href,
            """
            {
              "FirstName": "JohnChanged",
              "LastName": "DoeChanged",
              "UserName": "john12345._-'changed",
              "EMail": "john1.doe2.changed@email.com",
              "Password": "aaa3r546465676bgyhyyehy",
              "PhoneNumber":"+123123456789"
            }
            """,
            headers={'X-Filter': 'User.UserName,User.FirstName,User.LastName,\
User.EMail,User.Password,User.PhoneNumber'})
        self.expect_status(200)
        self.expect_json({'EMail': 'john1.doe2.changed@email.com',
                          'FirstName': 'JohnChanged',
                          'LastName': 'DoeChanged',
                          'PhoneNumber': '+123123456789',
                          'UserName': "john12345._-'changed",
                          'href': self.record_href})
  
    def test_edit_user_duplicate_email(self):      
        self.POST('/HR/User',
          """
          {
              "FirstName": "John",
              "LastName": "Doe",
              "UserName": "john2",
              "EMail": "john2.doe@email.com",
              "Password": "a3r546465676bgyhyyehy",
              "PhoneNumber":"0223456789"
         }
          """,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': 'john2',
                          'href': self.href(self.last_id+2)})
           
        self.PUT(
            self.href(self.last_id+2),
            {"EMail": "john1.doe2@email.com"},
            headers={'X-Filter': 'User.UserName,User.EMail'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'unique':
                       {'msg': 'Unique constraint failed'}
        }})
          
    def test_edit_user_incorect_email(self):  
        self.PUT(self.record_href,{"EMail": ";john1.doe@email.com"})
        self.expect_status(400)
        self.expect_json({'EMail': {'format': {'msg': 'Invalid EMail'}}})        
     
    def test_edit_user_missing_first_name(self):  
        self.PUT(self.record_href,{"FirstName": ""},
                 headers={'X-Filter': 'User.UserName,User.FirstName'})
        self.inspect_status()
        self.inspect_json()       
 
          
    def test_edit_user_missing_last_name(self):  
        self.PUT(self.record_href,{"LastName": ""},
                 headers={'X-Filter': 'User.UserName,User.LastName'})
        self.inspect_status()
        self.inspect_json()  
         
    def test_edit_user_missing_email(self):  
        self.PUT(self.record_href,{"EMail": ""},
                 headers={'X-Filter': 'User.UserName,User.EMail'})
        self.expect_status(400)
        self.inpect_json({'EMail': {'format': {'msg': 'Invalid EMail'}}})
          
    def test_edit_user_missing_phone(self):  
        self.PUT(self.record_href,{"PhoneNumber": ''},
                 headers={'X-Filter': 'User.UserName,User.PhoneNumber'})
        self.inspect_status()
        self.inspect_json()
 
          
    def test_edit_user_deleted(self):  
        self.DELETE(self.record_href)
        self.expect_status(204)    
                  
        self.PUT(self.record_href,{"FirstName": 'FirstName'},
                 headers={'X-Filter': 'User.UserName,User.FirstName'})
        self.expect_status(404)
        self.expect_json({'Id': {'other': {'msg': 'Unknown value'}}})
           
    def test_delete_user(self):
        #check user is here
        self.GET(self.href(self.last_id))
        self.expect_status(200)
        self.inspect_headers()
        self.inspect_body()
           
        #delete success
        self.DELETE(self.href(self.last_id))
        self.expect_status(200)
        self.expect_status(204)
        self.inspect_headers()
        self.inspect_body()
   
        #delete again same response?
        self.DELETE(self.href(self.last_id))
        self.expect_status(200)
        self.expect_status(204)
        self.inspect_headers()
        self.inspect_body()
           
        #check user not exists
        self.GET(self.href(self.last_id))
        self.expect_status(200)
        self.expect_status(404)     


#     def test_list_user(self):
#         #search
#         #pagination
#         self.GET('/HR/User')
#         self.expect_status(200)
#         self.inspect_headers()
#         self.inspect_body()
#         
#         
#     def test_all_users_details(self):
#         self.GET('/HR/User', headers={'X-Filter': 'User.*'})
#         self.inspect_headers()
#         self.inspect_body()      
