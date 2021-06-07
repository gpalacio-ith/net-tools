#!/usr/bin/env python3

import requests
import json
import subprocess


# API URL
url = "https://www.digicert.com/services/v2/order/certificate/ssl_basic"

# USER INFO
my_api_key = "find-your-api-key"
my_user_id = 1499533

# ORG INFO
intouch_org_id = 340375
intouch_container_id = 90053

# Certificate Defaults
cert_validity_years = 2
key_size = "2048"

# CERT INFO
cert_common_name = "*.gp-api-test-2.intouchprod.net"
cert_sans = ["san-1-gpalacio-api-test.intouchprod.net", "*.san-2-gpalacio-api-test.intouchprod.net"]


# Files info
key_filename = cert_common_name + ".key"
csr_filename = cert_common_name + ".csr"
crt_filename = cert_common_name + ".crt"

# Generates new private key
cmd_generate_key = "openssl genrsa -out " + key_filename + " " + key_size
subprocess.run(cmd_generate_key.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Generates new CSR
csr_key_arg = "-key " + key_filename + " "
csr_out_arg = "-out " + csr_filename + " "
csr_sub_arg = "-subj /C=US/ST=California/L=Goleta/O=InTouch Health/OU=IT/CN=" + crt_filename
cmd_generate_csr = "openssl req -new -sha256 " + csr_key_arg + csr_out_arg + csr_sub_arg
subprocess.run(cmd_generate_csr.split(' ', 9), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Reads CSR to submit to API
with open(csr_filename) as f:
    csr_contents = f.read()

# Builds Json with cert info
certificate_info = {
    "certificate": {
        "common_name": cert_common_name,
        "dns_names": cert_sans,
        "csr": csr_contents,
        "signature_hash": "sha256"
    },
    "comments": "Certificate for app server.",
    # "container": {
    #     "id": intouch_container_id
    # },
    "auto_renew": 0,
    "organization": {
        "id": intouch_org_id
        # "contacts": [
        #     {
        #         "contact_type": "organization_contact",
        #         "user_id": my_user_id
        #     }
        # ]
    },
    "order_validity": {
      "years": cert_validity_years
    },
    "payment_method": "balance"
}

# Serializing json   
json_object = json.dumps(certificate_info)  
# print(json_object)

headers = {
    'X-DC-DEVKEY': my_api_key,
    'Content-Type': "application/json"
    }

response = requests.request("POST", url, data=json_object, headers=headers)
json_result = json.loads(response.text)
print(json_result['certificate_chain'])