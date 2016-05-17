#!/usr/local/bin/perl
# diagnostic.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_sum'}	);
my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
	*.'. $ENV{"HTTP_HOST"}. ' http';
$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_sum'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), $head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
#print "dump". Dumper (%cmds). "|||";
	#while (my ($key,$value) = each %{$grub2cfg{$sb}{$i}{'opts_vars'}}) {
	#	$array[$key] = $value;
	#}
	#print "grub2cfg_sb_i_'opts_vars' is:".Dumper($grub2cfg{$sb}{$i}{'opts_vars'});
	#print "cfg is:".Dumper(%config);

	my %my_cfg = (
				  thm_dir => "themes directory",
				  def_file => "default settings file",
				  cfgd_dir => "extra configuration files directory",
				  loc_dir => "locales directory",
				  cfg_file => "main configuration file",
				  fonts_dir => "fonts directory",
				  dmap_file => "device map file",
				  sys_file => "system default settings file",
				  mod_dir => "modules directory",
				  grub2_dir => "commands directory",);

	print &ui_columns_start([
		$text{'summ_file'},
		$text{'summ_config'},
		$text{'summ_correct'} ], 100);
	for (keys %config) {	# $config files/directories
		if ($_ ne"highlight" && $_ ne"efi_arg") {
			my @cols;
			my $alt = (-e $config{$_}) ? $text{"yes"} : $text{"no"};
			my $status = "<img alt=\"$alt\" src=\"";
			$status.= ($alt eq $text{"yes"}) ? "images${dir_sep}up.gif" : "images${dir_sep}down.gif";
			$status.= '" />';
			push (@cols, $my_cfg{$_});
			push (@cols, $config{$_});
			push (@cols, $status);
			print &ui_columns_row(\@cols, \@tdtags, "d", "$_");
		}
	}
	for (keys %cmds) {
		my @cols;
		push (@cols, $cmds{$_}{$os});
		my $output = substr (&backquote_command ("(which ".$cmds{$_}{$os}.") 2>&1"), 0, 50);
		my $alt = ($cmds{$_}{$os}eq$output) ? true : false;
		my $status = "<img alt=\"$alt\" src=\"";
		$status.= ($alt eq true) ? "images${dir_sep}up.gif" : "images${dir_sep}down.gif";
		$status.= '" />';
		push (@cols, $output);
		push (@cols, $status);
		print &ui_columns_row(\@cols, \@tdtags, "d", "$_");
	}
	print &ui_columns_end();

&ui_print_footer ("$return", $text{'index_main'});	# click to return
