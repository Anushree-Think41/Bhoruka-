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


1. `Owners` Table
  This table remains the same, storing information specific to the owner.

   1 CREATE TABLE Owners (
   2     id SERIAL PRIMARY KEY,
   3     owner_name VARCHAR(255) NOT NULL,
   4     primary_phone VARCHAR(20) NOT NULL UNIQUE,
   5     secondary_phone VARCHAR(20),
   6     email VARCHAR(50) UNIQUE,
   7     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
   8     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
   9 );

  2. `Establishments` Table

  This table now includes the offerings array directly.

    1 CREATE TABLE Establishments (
    2     id SERIAL PRIMARY KEY,
    3     owner_id INT NOT NULL REFERENCES Owners(id),
    4     establishment_name VARCHAR(255) NOT NULL,
    5     address TEXT NOT NULL,
    6     city VARCHAR(128),
    7     state VARCHAR(15),
    8     pincode VARCHAR(20) NOT NULL,
    9     gstin VARCHAR(15) UNIQUE,
   10     offerings TEXT[] NOT NULL, -- Storing offerings as an array of strings
   11     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
   12     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
   13 );