## Prerequisites

1. python 3.+ 
2. pip (optional - only for purpose of installing nose)
3. nose (optional)
```
pip install -r requirements.txt 
```

## How To Run Tests
A. With Nose
```
nosetests
```

B. Without nose
```
python -m unittest discover changer/tests -p *_test.py
```

## How To Run the application
```
python cash_machine.py input.txt
```