# using puppet
# install nginx and configure with landing page
# redirect_me to my github account
# render an error 404 page
# add response header
# create static page (hbnb_static) and render it

package { 'nginx':
  ensure    => installed,
}


#-> file { 'index.nginx-debian.html':
#  ensure    => 'file',
#  content   => 'Hello World',
#  path      => '/var/www/html/index.nginx-debian.html',
#}

#-> file { '404.html':
#  ensure    => 'file',
#  content   => 'Ceci n\'est pas une page',
#  path      => '/var/www/html/404.html',
#}

-> exec { 'mkdir1':
  command   => '/usr/bin/env mkdir -p /data/web_static/releases/test/',
}

-> exec { 'mkdir2':
  command   => '/usr/bin/env mkdir -p /data/web_static/shared/',
}

-> exec { 'index.html':
  command   => '/usr/bin/env echo "Welcome to MrBridge" > /data/web_static/releases/test/index.html',
}

exec { 'config_nginx':
  command   => '/usr/bin/env sed -i "/listen 80 default_server/a location /hbnb_static/ { alias /data/web_static/current/;}" /etc/nginx/sites-available/default',
}

exec { 'symb_link':
  command   => '/usr/bin/env ln -sf /data/web_static/releases/test /data/web_static/current',
}

service { 'nginx':
  ensure    => 'running',
  require   => Package['nginx'],
}

exec {'permission':
  command   => '/usr/bin/env chown -R ubuntu:ubuntu /data',
}
