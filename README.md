# Origin Markets Backend Test Solution


## Project Quickstart

  

Inside a virtual environment running Python 3:

-  `pip install -r requirement.txt`

-  `./manage.py runserver` to run server.

-  `./manage.py test` to run tests.

  

## Authentication API

When sending a request to an API to add or retrieve bonds you need to be authenticated

### Creating a new user
Send a request to:

`POST /create-user/`

to create a user with the following user data:

~~~

{
	"username": "user",
	"password": "password",
	"email": "user@example.com"
}

~~~

The endpoint will return a token:

~~~

{
	"token": "ec941e7264d334bc314a94fd3370a625802e56f8"
}

~~~
This token can then be used to authorize any requests sent to the Bonds API

### Obtaining a Token for Existing Users

Send a request to:

`POST /api-token-auth/`

with the data that looks like:
~~~

{
	"username": "user",
	
	"password": "password",
	
}

~~~

This returns the user's token as shown previously

### Request Headers
The authentication token must be included in the `Authorization` HTTP header when sending a request to the Bonds API as such

````
Authorization: Token ec941e7264d334bc314a94fd3370a625802e56f8
````

## Bonds API

### Creating a bond

Send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:

~~~

{

	"isin": "FR0000131104",

	"size": 100000000,

	"currency": "EUR",

	"maturity": "2025-02-28",

	"lei": "R0MUWSFPU8MPRO8K5P83"

}

~~~

---

  

### Retrieving a bond

  

Send a request to:

  

`GET /bonds/`

  

to see something like:

~~~

[ 
	{

		"isin": "FR0000131104",

		"size": 100000000,

		"currency": "EUR",

		"maturity": "2025-02-28",

		"lei": "R0MUWSFPU8MPRO8K5P83",

		"legal_name": "BNPPARIBAS"

	},
	...
]

~~~

You can also add a filter such as:

`GET /bonds/?legal_name=BNPPARIBAS`

to reduce down the results.