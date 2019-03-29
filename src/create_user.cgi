#!/usr/bin/perl
# test_cfg.cgi
# create GRUB2 users file

require './grub2-lib.pl';
&ReadParse();

my $file = $config{'cfgd_dir'}."${dir_sep}01_users";
my $eg = <<EOV;
#!/bin/sh -e
cat << EOF
if [ -f \${prefix}/user.cfg ]; then
	source \${prefix}/user.cfg
	if [ -n "\${GRUB2_PASSWORD}" ]; then
		set superusers="root"
		export superusers
		password_pbkdf2 root \${GRUB2_PASSWORD}
	fi
fi
EOF
EOV

my $err = &check_cfg();
#my $err = &test_config();
#&error($err."will not reload") if ($err);
#my $err = &reload_nginx();
&error($err) if ($err);
sleep(1);
#&webmin_log("apply");
&redirect($in{'redir'});
