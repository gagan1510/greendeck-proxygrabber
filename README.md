GD-HELLOWORLD
---

*This package is sn standard example of how to make your own pip package. You can list your ElasticSearch indices.*
### Install from pip
https://pypi.org/project/greendeck-helloworld/

```pip install greendeck_helloworld```


### How to use ?
##### import the library
```python
import greendeck_helloworld
```

##### import ```ElasticSearch``` class
```python
from greendeck_helloworld import ElasticSearch
```

##### initialize ```ElasticSearch``` client connection
```python
es_client = ElasticSearch(ECS_HOST = <YOUR_ECS_HOST_NAME>, ECS_INDEX_PATTERN = <YOUR_ECS_INDEX_PATTERN>, username=<YOUR_ECS_USERNSME>,password=<YOUR_ECS_PASSWORD>)
```
Here default values of some arguments are,
* ECS_INDEX_PATTERN = "*"
* usename = Null
* password = Null

##### List all of your ECS indices
```python
es_client.list_indices()
```



---
How to build your pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5
* https://packaging.python.org/tutorials/packaging-projects/elasticsearch