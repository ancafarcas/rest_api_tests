# superdesk test framework

### prepare:
create virtualenv:
`virtualenv -p python3 env`
activate it:
`. env/bin/activate`
install dependencies:
`pip install -r requirements.txt`

### run blueprint tests:
`python test_blueprint.py`

### run example of func tests:
`python test_example.py`
or
`nosetests` if installed
