python version >=  3.10





python3.10 -m venv .venv_publish
source .venv_publish/bin/activate
pip install wheel twine


rm -rf build dist *.egg-info
python setup.py sdist bdist_wheel
