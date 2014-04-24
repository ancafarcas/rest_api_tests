# superdesk test framework

### prepare:
create virtualenv:
```
virtualenv -p python3 env
```
activate it:
```
. env/bin/activate
```
install dependencies:
```
pip install -r requirements.txt
```

### run tests:
```
python test_runner.py
```
or

```
pip install nose
nosetests
```