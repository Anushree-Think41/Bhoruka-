OWNER ONBOARDING
Denormalized Single Table


table_name : Owner_onboarding 
{
  "owner_name": "Ravi Sharma"                      == > VARCHAR(255) NOT NULL
  "establishment_name": "Ravi Trucks",            == > VARCHAR(255) NOT NULL
  "address": "No. 5, Industrial Area, Phase 2",    == > TEXT          NOT NULL
  "city": "Bengaluru",                            == > VARCHAR(128)
  "state": "Karnataka",                            == > VARCHAR(15)
  "pincode": "560001",                            ==>  VARCHAR(20)  NOT NULL
  "gstin": "29ABCDE1234F2Z5",                    ==>  VARCHAR(15)
  "primary_phone": "+919900365451",                ==>  VARCHAR(20)  NOT NULL
  "secondary_phone": null,                        ==>  VARCHAR(20) 
  "email": "ravi@example.com",                    ==>  VARCHAR(50)
  "offerings": ["LCV", "SCV"],                    ==>  Array of Text , TEXT[] NOT NULL
  
}

--------------------------------------------------------------------------------------------------

1. `Users` Table

```sql
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    last_login TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

2. `Owners` Table
  This table remains the same, storing information specific to the owner.

```sql
CREATE TABLE Owners (
    id SERIAL PRIMARY KEY,
    owner_name VARCHAR(255) NOT NULL,
    primary_phone VARCHAR(20) NOT NULL UNIQUE,
    secondary_phone VARCHAR(20),
    email VARCHAR(50) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

3. `Establishments` Table

  This table now includes the offerings array directly.

```sql
CREATE TABLE Establishments (
    id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL REFERENCES Owners(id),
    establishment_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(128),
    state VARCHAR(15),
    pincode VARCHAR(20) NOT NULL,
    gstin VARCHAR(15) UNIQUE,
    offerings TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```