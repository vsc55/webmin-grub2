#!/usr/bin/perl
# make_cfg.cgi
# Generate the GRUB2 cfg file

require './grub2-lib.pl';
&ReadParse();

my $retn = $in{'return'};

	#my $output = "recreate_cfg:[backquote_command (".$cmds{'install'}{$os}." $config{'cfg_file'}) 2>&1]";
	my $output = &backquote_command ("(".$cmds{'mkconfig'}{$os}." -o $config{'cfg_file'}) 2>&1");
	if ($output =~ /failed/) {
		&error ($output);
	}

&redirect ($retn);
