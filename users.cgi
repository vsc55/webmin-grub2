#!/usr/local/bin/perl
# users.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_users'}	);
#my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
#	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
#	*.'. $ENV{"HTTP_HOST"}. ' http';
#$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
#$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_users'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), #$head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
	my %users = $grub2cfg{'users'};
	my @form_btns = ( );
	push (@form_btns, [	"add", $text{'add'}	]);
	print &ui_form_start ("user_edit.cgi", "post");
	
	if (keys %users>1) {
		push (@form_btns, [	"delete", $text{'delete'}	]);
		print "users:".Dumper(%users)."|||";
		@links = ( );
		push (@links, &select_all_link("d"), &select_invert_link("d"));
		print &ui_links_row (\@links);
		print &ui_columns_start ([
			$text{'select'},
			$text{'all'},
			$text{'user_name'},
			$text{'user_pass'},
			$text{'user_pass2'},
			$text{'user_super'},
			], 100);
		for my $a (keys %users) {
			my @cols;
			push (@cols, "a:".Dumper($a)."|||");
			push (@cols, '<input type="text" name="user_name" value="'.$a.'" />'."\n");
			push (@cols, ($users{$a}{'pass'}) ? '*****' : '');
			push (@cols, ($a{'pass'}) ? '**a**' : 'a');
			push (@cols, ($a{'is_super'}>0) ? $text{'yes'} : $text{'no'});
			print &ui_checked_columns_row (\@cols, undef, "d", "d_value:$a");
		}
		print &ui_columns_end();
		print &ui_links_row(\@links);
	} elsif (!-f $config{'cfgd_dir'}. $dir_sep. '01_users') {
		print &text('user_init', "create_user.cgi");
		&make_user_file();
	} else {
		print $text{'user_none'};
	}
	print &ui_form_end (\@form_btns), &ui_hr();
	
	#print Dumper(%hash);

&ui_print_footer ("$return", $text{'index_main'});	# click to return
