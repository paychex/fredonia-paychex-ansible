
# Cloud infrastructure

This folder contains Terraform code that creates N number of VMs where N is asked during at the beginning of creation process.

### Terraform
This project uses [Terraform](https://www.terraform.io/) to create and deploy cloud VMs. Although Terraform expertise is not required to run this code, a slight familiarity with Terraform will help to in understanding the code when modifying for own use.

---
## Files

#### main.tf
File main.tf contains the main code to create and deploy the cloud resources.

#### provider.tf
This file provides instructions including your cloud vendor and your credentials to Terraform.

#### variables.tf
This file contains all the variables used among other .tf files. Modifying a variable in this file will result in global modification, wherever the variable has been referenced (used.)

