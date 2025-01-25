#  Sets up web servers for deployment of web_static

$html_content="
<html>
<head>
</head>
<body>
Welcome to Nginx Server - ALX
</body>
</html>
"

$location_block="
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
"

$nginx_config_file='/etc/nginx/sites-available/default'

exec { 'apt-get update':
  command => '/usr/bin/apt-get update -y',
  path    => '/usr/bin:/usr/sbin:/bin',
}

package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt-get update'],
}

file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => $html_content,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static/releases/test/index.html']
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

exec { 'update_nginx_config':
  command => "sed -i '/server_name _;/a ${location_block}' /etc/nginx/sites-available/default",
  unless  => 'grep -qF "location /hbnb_static/ {" /etc/nginx/sites-available/default',
  require => File['/data/web_static/current'],
  path    => '/usr/bin:/usr/sbin:/bin',
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Exec['update_nginx_config'],
}
