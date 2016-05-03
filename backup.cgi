#!/usr/bin/perl
# backup.cgi
# Backup a grub2 file / directory

require './grub2-lib.pl';
&ReadParse();

my $retn = $in{'return'};
my $file = $in{'what'};
	#my $file = $config{'cfg_file'};	# cfg file
	#my $file = $config{'def_file'};	# backup default grub file
	#my $dir = $config{'cfgd_dir'};	# backup grub.d directory
	#my $file = $config{'sys_file'};	# backup system grub default file
	#my $file = $config{'dmap_file'};	# backup grub device map file
my $err = &copy_source_dest ($file, "$file.webmin-bak".time());
&error ($err) if $err;
&redirect ($retn);
