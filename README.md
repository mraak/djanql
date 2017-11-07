Sample application showcasing Django and GraphQL.


# Run

```
python3 -m venv _venv
source _venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver

```





http://127.0.0.1:8000/admin

Log in with your superuser and create some models.

http://127.0.0.1:8000/graphql

Run queries and mutations.


## Create users and Login mutation


```

mutation{
  createUser(username:"user", email:"user@example.com", password:"123456A!"){
    user{
      id
      username
      email
      token
    }
  }
}

{
  "data": {
    "createUser": {
      "user": {
        "id": "2",
        "username": "alenb",
        "email": "alen.balja@pilatus-aircraft.com",
        "token": "bbe6d60ca2295d092d30e431fc3a77573444b449"
      }
    }
  }
}



mutation
{
  login(username:"alenb", password:"123456A!"){
    user{
      id
      username
      token
    }
  }
}

mutation{
  logout{
    user{
      username
    }
  }
}

query{
  viewer{
    id
    username
    token
  }
}

```

## Other mutations and queries

```

query viewer{
  viewer(id:"VXNlck5vZGU6Mg=="){
    id
    username
    orgs{
      edges{
        node{
          id
          name
          products{
            edges{
              node{
                id
                name
              }
            }
          }
        }
      }
    }
  }
}

query AllOrgs{
  allOrgs{
    edges{
      node{
        id
        name
        createdDate
      }
    }
  }
}

mutation saveorg($input:SaveOrgInput!){
  saveOrg(input:$input){
    org{
      id
      name
    }
  }
}

{"input": {"orgData": {"name": "Newrg"}}}

```
