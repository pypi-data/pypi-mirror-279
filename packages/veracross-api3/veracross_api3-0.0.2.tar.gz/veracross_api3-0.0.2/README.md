# Veracross API v3 Python Library
Provides an easy way to pull information from the Veracross API v3 using Python.

Rate limiting and pagination will be handled automatically.

Usage Example:
```python
import veracross_api3 as v

c = {
    "school": "abcd",
    "client_id": "123456789012345678901234567890",
    "client_secret": "12345678901234567890123456789012345678901234567890",
    "scopes": ['staff_faculty:read',
                        'students:read',
                        'staff_faculty:list',
                        'students:list']
}

# Create a new object with library
vc = v.Veracross(c)

# Follow the guidelines specified here:https://api-docs.veracross.com/docs
# Specify the endpoint documented in the api or just one record from that target.
# Examples of endpoint are: staff_faculty, students, etc.
# To return one record from that target, just specify the id number.
# Additional parameters are passed using a dictionary.

# Return all faculty and staff
data = vc.pull("staff_faculty")
print(data)

# Return one faculty and staff member by id
data = vc.pull("staff_faculty/99999")
print(data)

# Pass url parameters in a dictionary to the pull method.
# Return all faculty staff updated after 2019-01-01
param = {"faculty_type": "12"}
data = vc.pull("staff_faculty", parameters=param)
print(data)

# Return the amount of requests left in rate limiting
vc.rate_limit_remaining

# Return the amount of time left before the limit is reset
vc.rate_limit_reset

```

All data will be returned as a dictionary.

