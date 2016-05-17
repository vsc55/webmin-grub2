#!/usr/local/bin/perl
# configs.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_configs'}	);
my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
	*.'. $ENV{"HTTP_HOST"}. ' http';
$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header ("", "$text{'index_title'} - $text{'tab_configs'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), $head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
	#print "grub2files:". Dumper (\%grub2files). "||||<br />\n";
	#@links = ( );
	#push(@links, &select_all_link("sel"), &select_invert_link("sel"));
	#print &ui_form_start("display_save.cgi", "post");
	#print &ui_links_row(\@links);
	print &ui_columns_start([
	#	$text{'select'},
		$text{'configs_file'},
#		"full",
		], 100);
	for (sort keys %grub2files) {
		if ($_ ne 'src') {
			my @cols;
			push (@cols, '<a href="edit_file.cgi?name='.$_.'" title="'.$grub2files{$_}{'desc'}.'" />'. $_. "\n");#$parsed{"$config{'cfgd_dir'}$dir_sep$_"}
			#push (@cols, "$config{'cfgd_dir'}$dir_sep$_");
			print &ui_columns_row (\@cols, undef);
			#print &ui_checked_columns_row (\@cols, undef, "sel", $a);
		}
	}
	print &ui_columns_end();
	#print &ui_links_row(\@links);
	#print &ui_form_end([ [ "save", $text{'save'} ] ]);

#    #plain open document creation here
#    print &ui_form_start("create_server.cgi", "form-data");
#
#	    print &ui_table_start($text{'index_create'}, undef, 2);
#	    print &ui_table_row("Server Name",
#	        &ui_textbox("newserver", undef, 40));
#
#	    print &ui_table_row("Config",
#	        &ui_textarea("directives", undef, 25, 80, undef, undef,"style='width:100%'"));
#
#	    print &ui_table_row("",
#	        &ui_submit($text{'save'}));
#
#	    print &ui_table_end();
#    print &ui_form_end();

&ui_print_footer ("$return", $text{'index_main'});	# click to return
