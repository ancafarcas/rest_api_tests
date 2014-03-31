from api_test_tool import ApiTestCase

from tests import fixtures, session, token


class UserListTestCase(ApiTestCase):
    session = session
    token = token
   

    @classmethod
    def setUpClass(cls):
        cls.last_id = fixtures.number('/HR/User')
        cls.record = """
        {
            "FirstName": "John",
            "LastName": "Doe",
            "UserName": "john12345._-'",
            "EMail": "john1.doe2@email.com",
            "Password": "a3r546465676bgyhyyehy",
            "PhoneNumber":"0223456789"
        }
        """
        cls.record_href = '{server}/HR/User/{id}'.format(
            server=cls.server_url, id=cls.last_id+1)


    def setUp(self):
        fixtures.init('/HR/User')

            
    def test_add_user_success(self):
        #add user
        #TODO: check login
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': "john12345._-'",
            'href': self.record_href
        })
         
    def test_add_user_already_deleted(self):
        #add user
        #TODO: check login
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': "john12345._-'",
            'href': self.server_url + '/HR/User/7'
        })
         
        #add deleted one
        self.DELETE('/HR/User/7')
        self.expect_status(204)
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': "john12345._-'",
            'href': self.server_url + '/HR/User/7'
        })
         
    def test_add_user_duplicate_username(self):
        #add user
        #TODO: check login
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': "john12345._-'",
            'href': self.server_url + '/HR/User/7'
        })
         
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
             }}
        )
         
         
    def test_add_user_duplicate_email(self):
        #add user
        #TODO: check login
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'", 'href': self.server_url + '/HR/User/7'})        
         
         
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
        self.expect_json({'EMail': {'unique': {'msg': 'Unique constraint failed'}}})
         
        #not matching password - not applicable on REST API
         
    def test_add_user_incorrect_username(self):        
        #add incorrect username
        self.POST('/HR/User', self.record,
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
        self.expect_json({'UserName': {'user name': {'example': 'The user name must contain only letters, digits and characters ".", "_", "\'", "-"',
                            'msg': 'Invalid user name format'}}})
 
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
        self.expect_json({'EMail': {'format': {'msg': 'Invalid EMail'}}})
         
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
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
 
        self.PUT('/HR/User/7',
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
          headers={
              'X-Filter': 'User.UserName,User.FirstName,User.LastName,User.EMa\
il,User.Password,User.PhoneNumber'})
        self.expect_status(200)
        self.expect_json({'EMail': 'john1.doe2.changed@email.com',
                          'FirstName': 'JohnChanged',
                          'LastName': 'DoeChanged',
                          'PhoneNumber': '+123123456789',
                          'UserName': "john12345._-'changed",
                          'href': self.server_url + '/HR/User/7'})
  
    def test_edit_user_duplicate_email(self):      
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
           
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
                          'href': self.server_url + '/HR/User/8'})
           
        self.PUT('/HR/User/8', {"EMail": "john1.doe2@email.com"},
                 headers={'X-Filter': 'User.UserName,User.EMail'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'unique':
                       {'msg': 'Unique constraint failed'}
        }})
          
    def test_edit_user_incorect_email(self):  
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
              
        self.PUT('/HR/User/7',{"EMail": ";john1.doe@email.com"})
        self.expect_status(400)
        self.expect_json({'EMail': {'format': {'msg': 'Invalid EMail'}}})        
     
    def test_edit_user_missing_first_name(self):  
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
               
        self.PUT('/HR/User/7',{"FirstName": ""},
                 headers={'X-Filter': 'User.UserName,User.FirstName'})
        self.inspect_status()
        self.inspect_json()       
 
          
    def test_edit_user_missing_last_name(self):  
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
                
        self.PUT('/HR/User/7',{"LastName": ""},
                 headers={'X-Filter': 'User.UserName,User.LastName'})
        self.inspect_status()
        self.inspect_json()  
         
    def test_edit_user_missing_email(self):  
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
                 
        self.PUT('/HR/User/7',{"EMail": ""},
                 headers={'X-Filter': 'User.UserName,User.EMail'})
        self.expect_status(400)
        self.inpect_json({'EMail': {'format': {'msg': 'Invalid EMail'}}})
          
    def test_edit_user_missing_phone(self):  
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
                  
        self.PUT('/HR/User/7',{"PhoneNumber": ''},
                 headers={'X-Filter': 'User.UserName,User.PhoneNumber'})
        self.inspect_status()
        self.inspect_json()
 
          
    def test_edit_user_deleted(self):  
        self.POST('/HR/User', self.record,
          headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({'UserName': "john12345._-'",
                          'href': self.server_url + '/HR/User/7'})
             
        self.DELETE('/HR/User/7')
        self.expect_status(204)    
                  
        self.PUT('/HR/User/7',{"FirstName": 'FirstName'},
                 headers={'X-Filter': 'User.UserName,User.FirstName'})
        self.expect_status(404)
        self.expect_json({'Id': {'other': {'msg': 'Unknown value'}}})
           
    def test_delete_user(self):
        #check user not on list
        self.GET('/HR/User/6')
        self.expect_status(200)
        self.inspect_headers()
        self.inspect_body()
           
        #delete success
        self.DELETE('/HR/User/6')
        self.expect_status(204)
        self.inspect_headers()
        self.inspect_body()
   
        #delete again same response?
        self.DELETE('/HR/User/6')
        self.expect_status(204)
        self.inspect_headers()
        self.inspect_body()
           
        #check user not exists
        self.GET('/HR/User/6')
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
