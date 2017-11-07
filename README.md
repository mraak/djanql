
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

mutation{
  createUser(username:"alenb", email:"alen.balja@pilatus-aircraft.com", password:"123456A!"){
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
