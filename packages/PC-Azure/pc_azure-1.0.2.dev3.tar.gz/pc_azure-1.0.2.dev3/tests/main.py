from PC_Azure import Azure_Key_Vault

kv_name = ""	# to contain the Azure Key Vault name
secret_name = ""	# to contain the secret name

# 1. Instantiate the Azure_Key_Vault object
while not kv_name:
	kv_name = input("Please provide the Key Vault name: ")

try:	
	key_vault = Azure_Key_Vault(kv_name)
	print("Azure_Key_Vault object created successfully.")
	
except Exception as e:
	print(f"Exception of type {type(e)} occurred:\n{e}\n")


## 2. Retrieve the secret	
while not secret_name:
	secret_name = input("Please provide the secret name: ")
	
try:
	length = len(key_vault.get_secret(secret_name))
	print(f"Secret has a length of {length}.")
	
except Exception as e:
	print(f"Exception of type {type(e)} occurred:\n{e}\n")	