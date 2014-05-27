# Deploy Flask with Ansible

# Getting Started

* Install Vagrant (https://www.vagrantup.com/downloads)
* Clone/download this repo
* Install Ansible (Recommended: Via pip. To do that create a virtualev and run `pip install -r requirements.txt` within this repo's root dir)
* Add an inventory file in the repo's root dir called `hosts`. To test with vagrant paste the following content into the file:
* Add a deploy ssh key from your repo to let the app pull your code. Add a file called `deploy_key` to the directory `/roles/app/files/`
* run in production/deploy to server: activate venv and run `ansible-playbook -l production site.yml -i hosts`
