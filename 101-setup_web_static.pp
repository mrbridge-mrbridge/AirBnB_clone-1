# using puppet
# install nginx and configure with landing page
# redirect_me to my github account
# render an error 404 page
# add response header
# create static page (hbnb_static) and render it

package { 'nginx':
  ensure    => installed,
}

-> file_line { 'default':
    $line2_string = "server {
    listen      80 default_server;
    listen      [::]:80 default_server;
    add_header  X-Served-By $HOSTNAME;
    root        /var/www/html;
    index       index index.html index.htm index.nginx-debian.html;
    location /redirect_me {
                return 301 https://github.com/mrbridge-mrbridge/;
    }
    error_page 404 /404.html;
    location = /404.html {
                root /var/www/html;
                internal;
    }
    location /hbnb_static {
                alias /data/web_static/current;
                index index.html index.htm;
    }
}"
  line      => $line2_string,
  path      => '/etc/nginx/sites-available/default',
}

-> file { 'index.nginx-debian.html':
  ensure    => 'file',
  content   => 'Hello World',
  path      => '/var/www/html/index.nginx-debian.html',
}

-> file { '404.html':
  ensure    => 'file',
  content   => 'Ceci n\'est pas une page',
  path      => '/var/www/html/404.html',
}

-> exec { 'mkdir1':
  provider  => shell,
  command   => 'mkdir -p /data/web_static/releases/test/',
  path       => '/usr/bin',
}

-> exec { 'mkdir2':
  provider  => shell,
  command   => 'mkdir -p /data/web_static/shared/',
  path       => '/usr/bin',
}

-> file_line { 'index.html':
   $line1_string = "<!DOCTYPE html>
<html>
  <head>
    <title>MrBridge</title>
  </head>
  <body>Welcome to MrBridge</body>
</html>"
  line      => $line1_string,
  path      => '/data/web_static/releases/test/index.html',
}

-> exec { 'other_tasks':
  provider  => shell,
  command   => 'ln -sf /data/web_static/releases/test /data/web_static/current; chown -R ubuntu /data; chgrp -R ubuntu /data',
  path       => '/usr/bin',
} 

#exec { 'symlinked':
#  provider  => shell,
#  command   => 'sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled',
#}

-> service { 'nginx':
  ensure    => 'running',
  require   => Package['nginx'],
}
