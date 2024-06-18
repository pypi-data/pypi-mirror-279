# LSPAPI
Eine simple API um Daten aus [Leitstellenspiel](https://www.leitstellenspiel.de/) zu erhalten.

## Basic usage
```python
from python-LSPAPI import LSPAPI

user = ""  # LSP username
password = ""  # LSP password

key_file = "keyfile.key"  # The file where cookies are saved (for fater second login)
key_file_password = "supersecretpassword"  # encryption password for keyfile

lsp_api = LSPAPI(user, password, key_file, key_file_password)
lsp_api.start()
try:
    # All functions
    print(lsp_api.vehicle_states())
    print(lsp_api.user_stats())
    print(lsp_api.vehicles())
    print(lsp_api.buildings())

finally:
    lsp_api.stop()

```

## Installation

Using pip:
`pip install python-LSPAPI`


## List of Functions

### vehicle_states()
Returns how many vehicles are in what state.

---
### user_stats()
Returns information about the player.

---
### vehicles()
Returns the vehicles of the player.

---
### buildings()
Returns the buildings of the player.



> [!IMPORTANT]
> # DISCLAIMER
> I (the creator of this software) am NOT responsible for any damages done by this program. 


> [!TIP]
> If you are an Administrator of Leitstellenspiel and want this repo removed, please submit an issue containing the reason and a link to a Leitstellenspiel Forum post to verify that you are an Administrator. After that The repo will be taken down :)


