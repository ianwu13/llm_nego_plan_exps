# Flask Setup

## Clone Repository
```
git clone https://github.com/ianwu13/llm_nego_plan_exps/
cd llm_nego_plan_exps
```

## Install Pip and Requirements
```
sudo apt install python3-pip
pip install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# datasets package is not getting hit by installing the requirements file for some reason
pip install datasets
```

## Waitress Install
```
pip install waitress
sudo apt install python3-waitress
```

## Open HTTP Traffic to Allow Requests

* Navigate to the security group console for the EC2 instance's group
* Click "Edit inbound rules"
    * Create a new rule with "Port range"=5000, "Source"=Anywhere-IPv4 and "CIDR blocks"=0.0.0.0/0
    * Save rules

---

# Lioness setup (Not necessary for Flask server)

## Initial setup
* More detailed instructions can be found at https://lioness-doc.readthedocs.io/en/latest/0303_set_up.html#set-up-your-server-in-a-few-simple-steps

* In some steps, you will need the "application password".
    * Run `sudo cat /home/bitnami/bitnami_credentials` to print the default password and other info

1. Move lioness project to `htdocs` directory
    * Set permissions on the credentials.php file to 777
    * Set permissions of lioness project directory to 755

2. Navigate to `http://[your server name]/[your experiment name]/controlpanel.php` in your browser

3. You will need to enter a password. This should be the aformentioned "application password"

4. Confirm creation of database and tables for experiment

5. You will be prompted to login again. The password is now the same as the lioness account password (not "application password")

6. For security reasons, delete ENABLESETUP.php from your server after setting up your server so that no one else can set up (or destroy) the database.

## Running the experiment

1. On the machine used to host the Flask server, navigate to `llm_nego_plan_exps/agent_experiments/misc/flask_utils`

2. Run the command:
```
source host_<NEGO-SITUATION-NAME>_srvr.sh
```

3. Navigate to the lioness experiment directory; Edit the file `resources/basis/sqlLibrary.php`
    * Two functions will need to be altered: `setupNewUser` and `agentResponse`
        * The line setting "CURLOPT_URL" in each function will need to be changed to set the url to `[Server/ec2 instance url]:[port]/[setup_new_user | model_resp]`
            * The port should be 5000 if using this repository

4. The experiment is now ready. Navigate to `http://[your server name]/[your experiment name]/controlpanel.php` in your browser to access the control panel
