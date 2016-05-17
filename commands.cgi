#!/usr/local/bin/perl
# commands.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our $return = &this_url();
my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
	*.'. $ENV{"HTTP_HOST"}. ' http';
$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, $text{'index_title'}, "", undef, 1, 1, undef,
				 &test_cfg_button()." <br />".
	&help_search_link ("grub2", "man", "doc", "google"), $head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
my %fdiskhash = &fdiskhash();
	print "hash_fdiskhash:". Dumper(%fdiskhash). "|||<br />\n";
	print "hash_grub2cfg:". Dumper(\%grub2cfg). "|||<br />\n";
