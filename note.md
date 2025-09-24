Denormalized Single Table
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