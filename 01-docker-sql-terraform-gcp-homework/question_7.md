## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform

### Options:
- `terraform import, terraform apply -y, terraform destroy`
- `terraform init, terraform plan -auto-apply, terraform rm`
- `terraform init, terraform run -auto-approve, terraform destroy`
- `terraform init, terraform apply -auto-approve, terraform destroy`
- `terraform import, terraform apply -y, terraform rm`

---

## ANSWER

The correct answer is: **terraform init, terraform apply -auto-approve, terraform destroy**

## REASON

1.  **`terraform init`**: Used to initialize the working directory. This command downloads the necessary *provider plugins* (such as the Google Cloud provider) and sets up the *backend* for storing the state file.
2.  **`terraform apply -auto-approve`**: The `apply` command automatically creates a change plan (*plan*) and then executes it. The `-auto-approve` flag is used so that Terraform runs those changes immediately without waiting for a manual "yes" confirmation from the user.
3.  **`terraform destroy`**: Used to remove all infrastructure managed by Terraform that is defined in the configuration files.