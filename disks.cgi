#!/usr/local/bin/perl
# disks.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_disks'}	);
my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
	*.'. $ENV{"HTTP_HOST"}. ' http';
$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_disks'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), $head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
	my %dmap = &get_devicemap();
	#print "dmap:".Dumper(%dmap)."||||";
	if ($dir_sep == '/') {
		my @disks = &backquote_command ("(find /dev -group disk) 2>&1");
		#print "disks:".Dumper(@disks)."||||";
		my @array = ();
		my %hash;
		for my $a (keys %dmap) {
			for my $b (@disks) {
				if ($b =~ /$dmap{$a}/) {
					push (@array, $b);
					#push (@{ $hash{$a} }, $b) if $b !~ /^$dmap{$a}$/;
					my $more = ($b =~ /^$dmap{$a}$/) ? "($text{'mbr'}) " : "";
					push (@{ $hash{$a} }, "$b $more");
				}
			}
		}
		#print "disks:".Dumper(@array)."||||<br />";
		#print "hash:".Dumper(%hash)."||||";
	
#	my @array = grep {	/(k	} @disks;
		@links = ( );
		push(@links, &select_all_link("d"), &select_invert_link("d"));
		print &ui_form_start("install_grub2.cgi", "get");
		print &ui_links_row(\@links);
		print &ui_columns_start([
			$text{'select'},
			$text{'disks_grub'},
			$text{'disks_part'},
			#$text{'disks_grub'}
			], 100);
		for my $a (keys %hash) {
			my $previ;
			for my $b (@{ $hash{$a} }) {
				my @cols;
				#push (@cols, "$a : $dmap{$a}");
				push (@cols, "($a)");
				push (@cols, $b);
				print &ui_radio_columns_row (\@cols, \@tdtags, "sel", "chosen", 1);
				print &ui_columns_row (undef);# if $prev eq $b;
				$previ = $b;
			}
			#if ($_ ne"highlight" && $_ ne"efi_arg") {
			#	my @cols;
			#	push (@cols, $my_cfg{$_});
			#	push (@cols, $config{$_});
			#	push (@cols, (-e $config{$_}) ? $text{"yes"} : $text{"no"});
			#	print &ui_columns_row(\@cols, \@tdtags, "d", "$_");
			#}
		}
		#for (keys %cmds) {
		#	my @cols;
		#	push (@cols, $cmds{$_}{$os});
		#	my $output = substr (&backquote_command ("(which ".$cmds{$_}{$os}.") 2>&1"), 0, 50);
		#	push (@cols, $output);
		#	push (@cols, ($cmds{$_}{$os}eq$output) ? true : false);
		#	print &ui_columns_row(\@cols, \@tdtags, "d", "$_");
		#}
		print &ui_columns_end();
		print &ui_links_row(\@links);
		print &ui_form_end([	["install", $text{'disks_install'}]	]);
	}
	print &ui_hr();
&ui_print_footer ("$return", $text{'index_main'});	# click to return
