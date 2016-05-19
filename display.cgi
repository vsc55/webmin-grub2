#!/usr/local/bin/perl
# display.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_other'}	);
#my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
#	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
#	*.'. $ENV{"HTTP_HOST"}. ' http';
#$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
#$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_other'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), #$head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
	@links = ( );
	push(@links, &select_all_link("disp"), &select_invert_link("disp"));
	print &ui_form_start("display_save.cgi", "post");
	print &ui_links_row(\@links);
	print &ui_columns_start([
		$text{'disp_show'},
		$text{'disp_item'} ], 100);
	my $count = 0;
	for my $a (sort keys %display) {
		my @cols;
		push (@cols, '<input type="text" name="disp_name-'.$display{$a}{'nick'}.'" value="'.$display{$a}{'name'}.'" />'."\n".#$count.'|'.$display{$a}{'name'}
			  #'<input type="hidden" name="disp_all" value="'.$count.'|'.$display{$a}{'displayed'}.'|'.$display{$a}{'nick'}.'|'.$display{$a}{'name'}.'" />');
			  "");
		#print &ui_checked_columns_row (\@cols, undef, "disp", $display{$a}{'nick'}, $display{$a}{'displayed'});#
		print &ui_checked_columns_row (\@cols, undef, "disp", $count.'|'.$display{$a}{'displayed'}.'|'.$display{$a}{'nick'}.'|'.$display{$a}{'name'}, $display{$a}{'displayed'});#
		++$count;
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	#print &ui_form_end();
	print &ui_form_end([ [ "save", $text{'save'} ] ]), &ui_hr();
	
	#print Dumper(%hash);

&ui_print_footer ("$return", $text{'index_main'});	# click to return
