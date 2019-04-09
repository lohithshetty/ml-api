#! /bin/bash

function initialize_worker() {
    printf "***************************************************\n\t\tSetting up host \n***************************************************\n"
    # Update packages
    echo ======= Updating packages ========
    sudo apt-get update

    # Install pip3
    echo ======= Installing pip3 =======
    sudo apt-get install -y python3-pip
}

function setup_python_venv() {
    printf "***************************************************\n\t\tSetting up Venv \n***************************************************\n"
    # Install virtualenv
    echo ======= Installing virtualenv =======
    pip3 install virtualenv

    # Create virtual environment and activate it
    echo ======== Creating and activating virtual env =======
    virtualenv venv
    source ./venv/bin/activate
}


function setup_app() {
    printf "***************************************************\n    Installing App dependencies and Env Variables \n***************************************************\n"
    setup_env
    # Install required packages
    echo ======= Installing required packages ========
    pip install -r requirements.txt

}

# Create and Export required environment variable
function setup_env() {
    sudo cat > .env << EOF
    export DATABASE_URL="postgres://mldbuser:mldbuser@mldb-truthtree.csoygntfftvt.us-west-2.rds.amazonaws.com/mldb"
    #export DATABASE_URL='postgres://postgres:postgres@127.0.0.1/postgres'
    export APP_SETTINGS=config.ProductionConfig
EOF
    echo ======= Exporting the necessary environment variables ========
    source .env
}

# Install and configure nginx
function setup_nginx() {
    printf "***************************************************\n\t\tSetting up nginx \n***************************************************\n"
    echo ======= Installing nginx =======
    sudo apt-get install -y nginx

    # Configure nginx routing
    echo ======= Configuring nginx =======
    echo ======= Removing default config =======
    sudo rm -rf /etc/nginx/sites-available/default
    sudo rm -rf /etc/nginx/sites-enabled/default
    echo ======= Replace config file =======
    sudo bash -c 'cat <<EOF > /etc/nginx/sites-available/default
    server {
            listen 80 default_server;
            listen [::]:80 default_server;
            server_name _;
            location / {
                    # reverse proxy and serve the app
                    # running on the localhost:8000
                    proxy_pass http://127.0.0.1:8000/;
                    proxy_set_header HOST \$host;
                    proxy_set_header X-Forwarded-Proto \$scheme;
                    proxy_set_header X-Real-IP \$remote_addr;
                    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            }
    }
EOF'

    echo ======= Create a symbolic link of the file to sites-enabled =======
    sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

    # Ensure nginx server is running
    echo ====== Checking nginx server status ========
    sudo systemctl restart nginx
    sudo nginx -t
}

# Add a launch script
function create_launch_script () {
    printf "***************************************************\n\t\tCreating a Launch script \n***************************************************\n"

    sudo cat > /home/ubuntu/launch.sh <<EOF
    #!/bin/bash
    cd ~/ml-api/
    source .env
    source venv/bin/activate
    gunicorn app:app --timeout 300 -D
EOF
    sudo chmod 744 /home/ubuntu/launch.sh
    echo ====== Ensuring script is executable =======
    ls -la ~/launch.sh
}

function configure_startup_service () {
    printf "***************************************************\n\t\tConfiguring startup service \n***************************************************\n"

    sudo bash -c 'cat > /etc/systemd/system/ml-rest.service <<EOF
    [Unit]
    Description=ml-rest startup service
    After=network.target
    [Service]
    User=ubuntu
    ExecStart=/bin/bash /home/ubuntu/launch.sh
    [Install]
    WantedBy=multi-user.target
EOF'

    sudo chmod 664 /etc/systemd/system/ml-rest.service
    sudo systemctl daemon-reload
    sudo systemctl enable ml-rest.service
    sudo systemctl start ml-rest.service
    sudo service ml-rest status
}



#Serve the web app through gunicorn
function launch_app() {
    printf "***************************************************\n\t\tServing the App \n***************************************************\n"
    sudo bash /home/ubuntu/launch.sh
}

######################################################################
########################      RUNTIME       ##########################
######################################################################

initialize_worker
setup_python_venv
setup_app
setup_nginx
create_launch_script
configure_startup_service
launch_app
