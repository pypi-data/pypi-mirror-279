# brx-python

Welcome to the the documentation for the BRX Python package.

Get started with the examples located in ```tests.py```. 

It's easy to implement BRX's Python package:
1. Initialize your BRX Client with your access token:
```python
brx_client = BRX(os.environ.get("BRX_ACCESS_TOKEN")) 
```
2. Get your schema from your dashboard
3. Convert your schema to a modifiable query
```python
query_rebuild = sftoq(schema)
```
4. Extract the input fields, and set your desired values.
```python
output_object = query_rebuild["brx_query"]
input_fields = query_rebuild["input_fields"]
```
5. Set your desired values
```python
for index, input_field in enumerate(input_fields):
    input_fields[index]["value"] = input(f"Please enter the value for {input_field['name']}: ")
```
6. Update your query
```python
updated_query = uif(input_fields, output_object)
```
7. Run your BRX!
```
result = brx_client.execute(updated_query["brx_query"])
```