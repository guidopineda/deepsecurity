# deepsecurity
Trend Micro Deep Security scripts
This script creates a Tenant in the Trend Micro's Deep Security Manager.

The script reads a CSV file which contains the information provided by the Tenant, this information is in the following example format:

Tenant Name,Tenant Description,Admin Username,Email
API_Tenant_D,API_Tenant_D Description,MasterAdmin_Tenant_D,masteradmin@tenantD.com
API_Tenant_E,API_Tenant_E Description,MasterAdmin_Tenant_E,masteradmin@tenantE.com
API_Tenant_F,API_Tenant_F Description,MasterAdmin_Tenant_F,masteradmin@tenantF.com

The program reads the CSV file and creates a new CSV file which contains a randomly generated password. This file looks similar to the following format:

Tenant Name,Tenant Description,Admin Username,Email,Password
API_Tenant_D,API_Tenant_D Description,MasterAdmin_Tenant_D,masteradmin@tenantD.com,$)XZ^OGnMb7j0A1cv9(f
API_Tenant_E,API_Tenant_E Description,MasterAdmin_Tenant_E,masteradmin@tenantE.com,v9O=6y[e4xSY2rE]TLa|
API_Tenant_F,API_Tenant_F Description,MasterAdmin_Tenant_F,masteradmin@tenantF.com,JAIe035opju{UvH^]6X:

With this information, the Tenant is created. If there are 3 tenants in the CSV file, 3 tenants will be created and so on.
