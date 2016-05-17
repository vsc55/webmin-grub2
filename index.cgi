#!/usr/local/bin/perl
# index.cgi
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
#&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);
## Check if grub2 is installed
#if (!-x $config{'grub2_dir'}) {
#	print &text('index_notfound', $config{'grub2_dir'}),
#		$text{'index_either'}. &text('index_modify',
#			"$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").
#		$text{'index_install'};	#, "<p>\n";
#
#	&foreign_require("software", "software-lib.pl");
#	$lnk = &software::missing_install_link("grub2", $text{'index_grub2'},
#		"../$module_name/", $text{'index_title'});
#	print $lnk,"<p>\n" if ($lnk);
#
#	&ui_print_footer("/", $text{'index_return'});
#	exit;
#}

## Check if configuration matches which command
# which gets the wrong path!!
#my $whnginx = &backquote_command("(which nginx) 2>&1");
#if ($whnginx ne $config{'nginx_path'}) {
#	print &text('index_mismatch', $whnginx, $config{'nginx_path'}),
#		&text('index_modify', "$gconfig{'webprefix'}/config.cgi?$module_name");
#
#	&ui_print_footer("/", $text{'index_return'});
#	exit;
#}

# Start main display
	print &ui_hr(), $text{'index_intro'};
    $entry_icon = { "icon" => "images/entries.gif",#nginx_edit.png",
            "name" => $text{'tab_entry'},
            "link" => "entries.cgi" };
    $environ_icon = { "icon" => "images/environ.gif",#edit_proxy.png",
            "name" => $text{'tab_environ'},
            "link" => "environ.cgi" };
    $configs_icon = { "icon" => "images/configs.gif",#nginx_details.png",
            "name" => $text{'tab_configs'},
            "link" => "configs.cgi" };
    $disks_icon = { "icon" => "images/disks.gif",#files.gif",
            "name" => $text{'tab_disks'},
            "link" => "disks.cgi" };
    $users_icon = { "icon" => "images/users.gif",#nginx_edit.png",
            "name" => $text{'tab_users'},
            "link" => "users.cgi" };
    $style_icon = { "icon" => "images/style.gif",#edit_proxy.png",
            "name" => $text{'tab_style'},
            "link" => "styling.cgi" };
    $other_icon = { "icon" => "images/other.gif",#nginx_details.png",
            "name" => $text{'tab_other'},
            "link" => "display.cgi" };
    $files_icon = { "icon" => "images/files.gif",
            "name" => $text{'tab_files'},
            "link" => "files.cgi" };
    $summary_icon = { "icon" => "images/summary.gif",#nginx_edit.png",
            "name" => $text{'tab_sum'},
            "link" => "diagnostic.cgi" };
    $dump_icon = { "icon" => "images/dump.gif",#edit_proxy.png",
            "name" => $text{'tab_dump'},
            "link" => "dump.cgi" };
        &config_icons ($entry_icon, $environ_icon, $configs_icon, $disks_icon, $users_icon,
					   $style_icon, $other_icon, $files_icon, $summary_icon, $dump_icon);
