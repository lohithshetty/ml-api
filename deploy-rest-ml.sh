#! /bin/bash

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
    gunicorn app:app --timeout 300 --bind 0.0.0.0:8000
}

######################################################################
########################      RUNTIME       ##########################
######################################################################
setup_nginx
launch_app
