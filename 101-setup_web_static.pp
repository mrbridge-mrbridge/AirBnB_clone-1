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
  provider  => shell,
  command   => '/usr/bin/env mkdir -p /data/web_static/releases/test/',
}

-> exec { 'mkdir2':
  provider  => shell,
  command   => '/usr/bin/env mkdir -p /data/web_static/shared/',
}

-> exec { 'index.html':
  command   => 'echo "Welcome to MrBridge" > /data/web_static/releases/test/index.html',
  path      => '/usr/bin',
}

-> exec { 'other_tasks':
  provider  => shell,
  command   => 'ln -sf /data/web_static/releases/test /data/web_static/current; chown -R ubuntu /data; chgrp -R ubuntu /data',
  path      => '/usr/bin',
} 

#exec { 'symlinked':
#  provider  => shell,
#  command   => 'sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled',
#}

-> exec { 'config_nginx':
  command   => '/usr/bin/env sed -i "/listen 80 default_server/location /hbnb_static/ {\n\t\talias /data/web_static/current/;" /etc/nginx/sites-available/default',
}

-> service { 'nginx':
  ensure    => 'running',
  require   => Package['nginx'],
}
