#!/usr/bin/perl
# test_cfg.cgi
# check GRUB2 configuration file

require './grub2-lib.pl';
&ReadParse();

my $err = &check_cfg();
#my $err = &test_config();
#&error($err."will not reload") if ($err);
#my $err = &reload_nginx();
&error($err) if ($err);
sleep(1);
#&webmin_log("apply");
&redirect($in{'redir'});
