#! /bin/bash

function initialize_worker() {
    printf "***************************************************\n\t\tSetting up host \n***************************************************\n"
    # Update packages
    echo ======= Updating packages ========
     apt-get update

    # Install pip3
    echo ======= Installing pip3 =======
     apt-get install -y python3-pip
}

function setup_python_venv() {
    printf "***************************************************\n\t\tSetting up Venv \n***************************************************\n"
    # Install virtualenv
    echo ======= Installing virtualenv =======
     apt install virtualenv -y

    # Create virtual environment and activate it
    echo ======== Creating and activating virtual env =======
    virtualenv -p python3 venv
    source ./venv/bin/activate
}


function setup_app() {
    printf "***************************************************\n    Installing App dependencies and Env Variables \n***************************************************\n"
    setup_env
    # Install required packages
    echo ======= Installing required packages ========
    pip3 install -r requirements.txt

}

# Create and Export required environment variable
function setup_env() {
     cat > .env << EOF
    export DATABASE_URL="postgres://mldbuser:mldbuser@mldb.csoygntfftvt.us-west-2.rds.amazonaws.com/mldb"
    #export DATABASE_URL='postgres://postgres:postgres@127.0.0.1/postgres'
    export APP_SETTINGS=config.ProductionConfig
EOF
    echo ======= Exporting the necessary environment variables ========
    source .env
    export
}

# Install and configure nginx
function setup_nginx() {
    printf "***************************************************\n\t\tSetting up nginx \n***************************************************\n"
    echo ======= Installing nginx =======
     apt-get install -y nginx

    # Configure nginx routing
    echo ======= Configuring nginx =======
    echo ======= Removing default config =======
     rm -rf /etc/nginx/sites-available/default
     rm -rf /etc/nginx/sites-enabled/default
    echo ======= Replace config file =======
     bash -c 'cat <<EOF > /etc/nginx/sites-available/default
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
     ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

     nginx -t
}

#Serve the web app through gunicorn
function launch_app() {
    printf "***************************************************\n\t\tServing the App \n***************************************************\n"
    gunicorn app:app --timeout 300 -D
}

######################################################################
########################      RUNTIME       ##########################
######################################################################

initialize_worker
#setup_python_venv
setup_app
setup_nginx
launch_app
