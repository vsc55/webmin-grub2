#!/usr/local/bin/perl
# files.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_files'}	);
my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
	*.'. $ENV{"HTTP_HOST"}. ' http';
$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_files'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), $head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
	print "<dl>";
	my %cmds = get_cmds();
	for my $a (keys \%cmds) {
		print "<dt>".$cmds{$a}{$os}."</dt>\n";
		while (my ($k, $v) = each %{ $cmds{$a} } ) {
			print "\t<dd>$k = $v</dd>\n" if $k ne "red" && $k ne "deb";
		}
		print "<br />\n";
	}
	print "</dl>\n", &ui_hr();

&ui_print_footer ($return, $text{'index_main'});	# click to return
