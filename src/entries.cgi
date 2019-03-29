#!/usr/local/bin/perl
# entries.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
#use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_entry'}	);
#my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
#	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
#	*.'. $ENV{"HTTP_HOST"}. ' http';
#$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
#$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_entry'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), #$head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}

	our %parsed = &divide_cfg_into_parsed_files();
	#print "display is".Dumper (%display)."||||<br />\n";
	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("do_entry.cgi", "get");
	print &ui_links_row(\@links);
	my @array = ( $text{'select'} );	# begin the row with a checkbox
	for (my $a=0; $a<keys %display; $a++) {
		push (@array, $display{$a}{'name'}) if $display{$a}{'displayed'}==1;	# add each %display if marked as displayed
	}
	print &ui_columns_start(\@array, 100);
	foreach $sb (keys %grub2cfg) {	# each submenu
		foreach $i (keys $grub2cfg{$sb}) {	# each menu entry
			if ($grub2cfg{$sb}{$i}{'valid'}) {	# only show valid entries
				my %cols;
				$cols{'id'} = $grub2cfg{$sb}{$i}{'id'};
				$cols{'pos'} = $grub2cfg{$sb}{$i}{'pos'};
				if (length ($grub2cfg{$sb}{$i}{'name'}) > 40) {	# menuentry name
					$cols{'name'} = "<a title=\"".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\" href=\"edit.cgi?sub=$sb&amp;item=$i\">".(($grub2cfg{$sb}{$i}{'is_saved'}) ? "<strong>" : "").&html_escape (cutoff ($grub2cfg{$sb}{$i}{'name'}, 40, "...")).(($grub2cfg{$sb}{$i}{'is_saved'}) ? "</strong>" : "")."</a>";
				} else {
					$cols{'name'} = "<a href=\"edit.cgi?sub=$sb&amp;item=$i\">".(($grub2cfg{$sb}{$i}{'is_saved'}) ? "<strong>" : "").&html_escape ($grub2cfg{$sb}{$i}{'name'}).(($grub2cfg{$sb}{$i}{'is_saved'}) ? "</strong>" : "")."</a>";
				}
				if (length ($grub2cfg{$sb}{'name'}) > 17) {	# submenu name
					$cols{'sub'} = "<span title=\"".&html_escape ($grub2cfg{$sb}{'name'})."\">".&html_escape (substr ($grub2cfg{$sb}{'name'}, 0, 17)."...")."</span>";
				} else {
					$cols{'sub'} = &html_escape ($grub2cfg{$sb}{'name'});
				}
				if (length ($grub2cfg{$sb}{$i}{'classes'}) > 7) {	# options-classes
					$cols{'class'} = "<span title=\"".&html_escape (join (", ", @{ $grub2cfg{$sb}{$i}{'classes'} }))."\">".&html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'classes'} }), 0, 7)."...")."</span>";
				} else {
					$cols{'class'} = &html_escape (join (",", @{ $grub2cfg{$sb}{$i}{'classes'} }));
				}
				my @array = ();
				while (my ($key,$val) = each $grub2cfg{$sb}{$i}{'opts_vars'}) {
					push (@array, &html_escape ($key).' = '.&html_escape ($val));
				}
				my $together = join ', ', @array;
				if (length ($together) > 20) {
					#push (@cols, &html_escape (cutoff (join (",", @array), 5, "...")));
					$cols{'ovar'} = '<span title="'.$together.'">'.&html_escape (substr ($together, 0, 20)."...").'</span>';
				} else {
					$cols{'ovar'} = &html_escape ($together);#join (',', @array)));
				}
				if (length ($grub2cfg{$sb}{$i}{'opts_if'}) > 5) {
					$cols{'oif'} = "<span title=\"".&html_escape (join (", ", @{ $grub2cfg{$sb}{$i}{'opts_if'} }))."\">".&html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'opts_if'} }), 0, 5)."...")."</span>";
				} else {
					$cols{'oif'} = &html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'opts_if'} }), 0, 5)."...");
				}
				my $unr = ($grub2cfg{$sb}{$i}{'unrestricted'}) ? $text{'cfg_open'} : $text{'cfg_close'};
				if (length ($unr) > 10) {	# options-unrestricted
					$cols{'pro'} = "<span title=\"".&html_escape ($unr)."\">".&html_escape ($unr)."</span>";
				} else {
					$cols{'pro'} = &html_escape ($unr);
				}
				if (length ($grub2cfg{$sb}{$i}{'users'}) > 5) {	# options-users
					$cols{'users'} = "<span title=\"".&html_escape ($grub2cfg{$sb}{$i}{'users'})."\">".&html_escape (substr ($grub2cfg{$sb}{$i}{'users'}, 0, 5)."...")."</span>";
				} else {
					$cols{'users'} = &html_escape ($grub2cfg{$sb}{$i}{'users'});
				}
				if (length ($grub2cfg{$sb}{$i}{'insmod'}) > 5) {	# inner-mods
					$cols{'mod'} = "<span title=\"".&html_escape (join (", ", @{ $grub2cfg{$sb}{$i}{'insmod'} }))."\">".&html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'insmod'} }), 0, 5)."...")."</span>";
				} else {
					$cols{'mod'} = &html_escape (cutoff (join (",", @{ $grub2cfg{$sb}{$i}{'insmod'} }), 5, "..."));
				}
				if (length ($grub2cfg{$sb}{$i}{'set'}) > 5) {
					$cols{'set'} = "<span title=\"".&html_escape (join (", ", @{ $grub2cfg{$sb}{$i}{'set'} }))."\">".&html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'set'} }), 0, 5)."...")."</span>";
				} else {
					$cols{'set'} = &html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'set'} }), 0, 5)."...");
				}
				if (length ($grub2cfg{$sb}{$i}{'inners'}) > 5) {
					$cols{'ins'} = "<span title=\"".&html_escape (join (", ", @{ $grub2cfg{$sb}{$i}{'inners'} }))."\">".&html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'inners'}}), 0, 5)."...")."</span>";
				} else {
					$cols{'ins'} = &html_escape (substr (join (",", @{ $grub2cfg{$sb}{$i}{'inners'} }), 0, 5)."...");
				}
				#push (@cols, $grub2cfg{$sb}{$i}{'is_saved'});
				my @tdtags;	# highlight entire row of saved_entry if any:
				if ($grub2cfg{$sb}{$i}{'is_saved'}) {	for (my $i=1; $i<(keys %cols)+1; $i++) {	$tdtags[$i]='style="background-color: '.$config{"highlight"}.'"';	}	}
				my @columns = ();	# make the row...
				for (my $a=0; $a<keys %cols; $a++) {
					my $item = $display{$a}{'nick'};	# sort the columns using %display as a guide
					push (@columns, $cols{$item}) if 1 == $display{$a}{'displayed'};	# only if marked as displayed
				}
				print &ui_checked_columns_row(\@columns, \@tdtags, "d", "sub=$sb&amp;item=$i,");
			}
		}
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([	["delete", $text{'delete'}], 	["mksaved", $text{'entry_mksaved'}], 	["edit", $text{'entry_edit'}]	]);
	print &ui_hr(),
		&ui_buttons_start(),
		&ui_buttons_row("edit.cgi", $text{'add'}, $text{'add_me'}),
		&ui_buttons_end(),
    #print &ui_form_start("edit.cgi", "post");
	#print &ui_form_end([	 ["add", $text{'add'}]	]),
	&ui_hr();
#print 'return1:'. Dumper (@returnHere). "||||<br />\n";
#print 'return1 ref:'. Dumper (\@returnHere). "||||<br />\n";
&ui_print_footer ($return, $text{'index_main'});	# click to return
