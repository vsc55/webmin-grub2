#!/usr/local/bin/perl
# index.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation

#my %rv;

## add virtual servers
#my @virts = &get_servers();
#foreach $v (@virts) {
##  $idx = &indexof($v, @$conf);
#    $sn = basename($v);
#    push(@vidx, $sn);
#    push(@vname, $sn);
#    push(@vlink, "edit_server.cgi?editfile=$sn");
#	push (@link2, "mklink.cgi?vhost=$sn");
#	push (@ulink, "unlink.cgi?vhost=$sn");
#	%rv = &parse_config ("$config{'nginx_dir'}/$config{'virt_dir'}/$sn", "server_name", "port", "root");
#	push (@vaddr, join ($config{'join_ch'}, @{$rv{'server_name'}}));
#	push (@vport, join ($config{'join_ch'}, @{$rv{'port'}}));
#	push (@vroot, join ($config{'join_ch'}, @{$rv{'root'}}));
#    push(@vurl, "http://$sn/");
#}

# Page header
&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, undef,
#				 $gconfig{'os_type'}. "<br />".
#	&update_button()."<br>".
	&help_search_link("grub2", "man", "doc", "google"), undef, undef,
	&text('index_version', $version));
#&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);
## Check if grub2 is installed
#if (!-x $config{'grub2_dir'}) {
#	print &text('index_notfound', $config{'grub2_dir'}),
#		$text{'index_either'}. &text('index_modify',
#			"$gconfig{'webprefix'}/config.cgi?$module_name").
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
@tabs = (
		 ['entry', 		$text{'tab_entry'}],
		 ['environ', 	$text{'tab_environ'}],
		 ['other', 		$text{'tab_other'}],
		 ['files', 		$text{'tab_files'}],
		 ['summary', 	$text{'tab_sum'}]
		);

my %parsed = &divide_cfg_into_parsed_files();
#print "parsed is ".Dumper (\%parsed)."||||";

#print "parsed cfg is ".Dumper (\%grub2cfg)."||||";

print ui_tabs_start(\@tabs, 'mode', 'summary');

print ui_tabs_start_tab('mode', 'entry');

	#while (my ($key,$value) = each %{$grub2cfg{$sb}{$i}{'opts_vars'}}) {
	#	$array[$key] = $value;
	#}
	#print "grub2cfg_sb_i_'opts_vars' is:".Dumper($grub2cfg{$sb}{$i}{'opts_vars'});

	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("do_entry.cgi", "get");
	print &ui_links_row(\@links);
	print &ui_columns_start([
		$text{'select'},
		$text{'entry_id'},
		$text{'entry_name'},
		$text{'entry_sub_name'},
		$text{'entry_classes'},
		$text{'entry_mods'},
		$text{'entry_opt_var'},
		$text{'entry_protected'},
		$text{'entry_sets'},
		$text{'entry_inners'},
		$text{'entry_opt_if'} ], 100);
	foreach $sb (keys %grub2cfg) {	# each submenu
		foreach $i (keys $grub2cfg{$sb}) {	# each menu entry
			if ($grub2cfg{$sb}{$i}{'valid'}) {	# only show valid entries
				my @cols;
				push (@cols, $grub2cfg{$sb}{$i}{'id'});
				if (length ($grub2cfg{$sb}{$i}{'name'}) > 40) {	# menuentry name
					push (@cols, "<a title=\"".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\" href=\"edit.cgi?".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\">".(($grub2cfg{$sb}{$i}{'is_saved'}) ? "<strong>" : "").&html_escape (cutoff ($grub2cfg{$sb}{$i}{'name'}, 40, "...")).(($grub2cfg{$sb}{$i}{'is_saved'}) ? "</strong>" : "")."</a>");
				} else {
					push (@cols, "<a href=\"edit.cgi?".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\">".(($grub2cfg{$sb}{$i}{'is_saved'}) ? "<strong>" : "").&html_escape ($grub2cfg{$sb}{$i}{'name'}).(($grub2cfg{$sb}{$i}{'is_saved'}) ? "</strong>" : "")."</a>");
				}
				if (length ($grub2cfg{$sb}{'name'}) > 17) {	# submenu name
					push (@cols, "<span title=\"".&html_escape ($grub2cfg{$sb}{'name'})."\">".&html_escape (substr ($grub2cfg{$sb}{'name'}, 0, 17)."...")."</span>");
				} else {
					push (@cols, &html_escape ($grub2cfg{$sb}{'name'}));
				}
				if (length ($grub2cfg{$sb}{$i}{'classes'}) > 7) {	# options-classes
					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'classes'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'classes'}}), 0, 7)."...")."</span>");
				} else {
					push (@cols, &html_escape (join (",", @{$grub2cfg{$sb}{$i}{'classes'}})));
				}
				my @array = ();
				while (my ($key,$val) = each $grub2cfg{$sb}{$i}{'opts_vars'}) {
					push (@array, $key. ' => '. $val);#$grub2cfg{$sb}{$i}{'opts_vars'}{$val}{$val});#$key{$key});#$grub2cfg{$sb}{$i}{'opts_vars'}{$val};
#####$val not correct#####					
				}
				#@array = join(', ', @array);
				#print join(', ', @array);
				if (length ($grub2cfg{$sb}{$i}{'insmod'}) > 5) {	# inner-mods
					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'insmod'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'insmod'}}), 0, 5)."...")."</span>");
				} else {
					push (@cols, &html_escape (cutoff (join (",", @{$grub2cfg{$sb}{$i}{'insmod'}}), 5, "...")));
				}
				push (@cols, &html_escape (cutoff (join (",", @array), 5, "...")));
				#push (@cols, join (",", @{$grub2cfg{$sb}{$i}{'opts_vars'}}));
				if (length ($grub2cfg{$sb}{$i}{'protected'}) > 5) {	# options-unrestricted
					push (@cols, "<span title=\"".&html_escape ($grub2cfg{$sb}{$i}{'protected'})."\">".&html_escape (substr ($grub2cfg{$sb}{$i}{'protected'}, 0, 5)."...")."</span>");
				} else {
					push (@cols, &html_escape ($grub2cfg{$sb}{$i}{'protected'}));
				}
				if (length ($grub2cfg{$sb}{$i}{'set'}) > 5) {
					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'set'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'set'}}), 0, 5)."...")."</span>");
				} else {
					push (@cols, &html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'set'}}), 0, 5)."..."));
				}
				if (length ($grub2cfg{$sb}{$i}{'inners'}) > 5) {
					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'inners'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'inners'}}), 0, 5)."...")."</span>");
				} else {
					push (@cols, &html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'inners'}}), 0, 5)."..."));
				}
				if (length ($grub2cfg{$sb}{$i}{'opts_if'}) > 5) {
					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'opts_if'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'opts_if'}}), 0, 5)."...")."</span>");
				} else {
					push (@cols, &html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'opts_if'}}), 0, 5)."..."));
				}
				push (@cols, $grub2cfg{$sb}{$i}{'is_saved'});
				my @tdtags;	# highlight entire row of saved_entry if any:
				if ($grub2cfg{$sb}{$i}{'is_saved'}) {	for (my $i=1; $i<scalar (@cols)+1; $i++) {	$tdtags[$i]='style="background-color: '.$config{"highlight"}.'"';	}	}
				print &ui_checked_columns_row(\@cols, \@tdtags, "d", "sub=$sb&amp;item=$i,");
			}
		}
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([	["delete", $text{'delete'}], ["mksaved", $text{'entry_mksaved'}], ["edit", $text{'entry_edit'}]	]);

	print "hash_grub2cfg:".Dumper(\%grub2cfg);
	#print "array_grub2cfg:".Dumper(\@grub2cfg);

print ui_tabs_end_tab('mode', 'entry');

print ui_tabs_start_tab('mode', 'environ');

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

	#print Dumper(%env_setts);
	
	my %grub2def = &get_grub2_def();
    @links = ( );
    push(@links, &select_all_link("sel"), &select_invert_link("sel"));
    print &ui_form_start("do_env.cgi", "get");
    print &ui_links_row(\@links);
    print &ui_columns_start([
		$text{'select'},
		$text{'var'},
		$text{'val'} ],	100);
	for (keys %grub2def) {
			my @cols;
#	    push(@cols, "<a class=\"del\" href=\"delenv.cgi\">$text{'del'}</a>".
#			push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$_</a>");
			push (@cols, "<span title=\"".$env_setts{$_}."\">$_</span>");
#			push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$grub2env{$_}</a>");
			push (@cols, $grub2def{$_});
			print &ui_checked_columns_row(\@cols, undef, "sel", "$_&amp;was=$grub2def{$_}");
		#}
    }
    print &ui_columns_end();
    print &ui_links_row(\@links);
    print &ui_form_end([ ["edit", $text{'edit'}], ["delete", $text{'delete'}] ]);
	print "<a class=\"right\" href=\"add_env.cgi\">$text{'add'}</a>";

	my %grub2env = &get_grub2_env();
    @links = ( );
    push(@links, &select_all_link("sel"), &select_invert_link("sel"));
    print &ui_form_start("do_env.cgi", "get");
    print &ui_links_row(\@links);
    print &ui_columns_start([
		$text{'select'},
		$text{'var'},
		$text{'val'} ],	100);
    foreach (%grub2env) {
	    if ($grub2env{$_} && $_) {
			my @cols;
#	    push(@cols, "<a class=\"del\" href=\"delenv.cgi\">$text{'del'}</a>".
#			push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$_</a>");
			push (@cols, $_);
#			push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$grub2env{$_}</a>");
			push (@cols, $grub2env{$_});
			print &ui_checked_columns_row(\@cols, undef, "sel", "$_&amp;was=$grub2env{$_}");
		}
    }
    print &ui_columns_end();
    print &ui_links_row(\@links);
    print &ui_form_end([ ["edit", $text{'edit'}], ["delete", $text{'delete'}] ]);
	print "<a class=\"right\" href=\"add_env.cgi\">$text{'add'}</a>";

print ui_tabs_end_tab('mode', 'environ');

print ui_tabs_start_tab('mode', 'other');

	@array = (
			  0 => 	[	'name' => 	$text{'entry_id'},			'pos' => 0, 'on' => true	],
			  1 => 	[	'name' => 	$text{'entry_name'},		'pos' => 1, 'on' => true	],
			  2 => 	[	'name' => 	$text{'entry_sub_name'},	'pos' => 2, 'on' => true	],
			  3 => 	[	'name' => 	$text{'entry_classes'},		'pos' => 3, 'on' => true	],
			  4 => 	[	'name' => 	$text{'entry_mods'},		'pos' => 4, 'on' => true	],
			  5 => 	[	'name' => 	$text{'entry_opt_var'},		'pos' => 5, 'on' => false	],
			  6 => 	[	'name' => 	$text{'entry_protected'},	'pos' => 6, 'on' => true	],
			  7 => 	[	'name' => 	$text{'entry_sets'},		'pos' => 7, 'on' => true	],
			  8 => 	[	'name' => 	$text{'entry_inners'},		'pos' => 8, 'on' => false	],
			  9 => 	[	'name' => 	$text{'entry_opt_if'},		'pos' => 9, 'on' => true	]
			 );
	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("delete_entry.cgi", "get");
	print &ui_links_row(\@links);
	print &ui_columns_start([
		$text{'select'},
		$text{'item_show'} ], 100);
	for $a (@array) {
		my @cols;
		push (@cols, $a['name']);
		print &ui_checked_columns_row (\@cols, undef, "d", $a, $a['on']);
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([ [ "delete", $text{'delete'} ] ]);

print ui_tabs_end_tab('mode', 'other');
	
print ui_tabs_start_tab('mode', 'files');

	print "<dl>";
	my %cmds = get_cmds();
	for my $a (keys \%cmds) {
		print "<dt>".$cmds{$a}{$os}."</dt>\n";
		while (my ($k, $v) = each %{ $cmds{$a} } ) {
			print "\t<dd>$k = $v</dd>\n" if $k ne "red" && $k ne "deb";
		}
		print "<br />\n";
	}
	print "</dl>";

print ui_tabs_end_tab('mode', 'files');

print ui_tabs_start_tab('mode', 'summary');

	#while (my ($key,$value) = each %{$grub2cfg{$sb}{$i}{'opts_vars'}}) {
	#	$array[$key] = $value;
	#}
	#print "grub2cfg_sb_i_'opts_vars' is:".Dumper($grub2cfg{$sb}{$i}{'opts_vars'});

	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("do_entry.cgi", "get");
	print &ui_links_row(\@links);
	print &ui_columns_start([
		$text{'select'},
		$text{'summ_file'},
		$text{'summ_which'},
		$text{'summ_config'},
		$text{'summ_correct'} ], 100);
#	foreach $sb (keys %grub2cfg) {	# each submenu
#		foreach $i (keys $grub2cfg{$sb}) {	# each menu entry
#			if ($grub2cfg{$sb}{$i}{'valid'}) {	# only show valid entries
#				my @cols;
#				push (@cols, $grub2cfg{$sb}{$i}{'id'});
#				if (length ($grub2cfg{$sb}{$i}{'name'}) > 40) {	# menuentry name
#					push (@cols, "<a title=\"".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\" href=\"edit.cgi?".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\">".(($grub2cfg{$sb}{$i}{'is_saved'}) ? "<strong>" : "").&html_escape (cutoff ($grub2cfg{$sb}{$i}{'name'}, 40, "...")).(($grub2cfg{$sb}{$i}{'is_saved'}) ? "</strong>" : "")."</a>");
#				} else {
#					push (@cols, "<a href=\"edit.cgi?".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\">".(($grub2cfg{$sb}{$i}{'is_saved'}) ? "<strong>" : "").&html_escape ($grub2cfg{$sb}{$i}{'name'}).(($grub2cfg{$sb}{$i}{'is_saved'}) ? "</strong>" : "")."</a>");
#				}
#				if (length ($grub2cfg{$sb}{'name'}) > 17) {	# submenu name
#					push (@cols, "<span title=\"".&html_escape ($grub2cfg{$sb}{'name'})."\">".&html_escape (substr ($grub2cfg{$sb}{'name'}, 0, 17)."...")."</span>");
#				} else {
#					push (@cols, &html_escape ($grub2cfg{$sb}{'name'}));
#				}
#				if (length ($grub2cfg{$sb}{$i}{'classes'}) > 7) {	# options-classes
#					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'classes'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'classes'}}), 0, 7)."...")."</span>");
#				} else {
#					push (@cols, &html_escape (join (",", @{$grub2cfg{$sb}{$i}{'classes'}})));
#				}
#				my @array = ();
#				while (my ($key,$val) = each $grub2cfg{$sb}{$i}{'opts_vars'}) {
#					push (@array, $key. ' => '. $val);#$grub2cfg{$sb}{$i}{'opts_vars'}{$val}{$val});#$key{$key});#$grub2cfg{$sb}{$i}{'opts_vars'}{$val};
######$val not correct#####					
#				}
#				#@array = join(', ', @array);
#				#print join(', ', @array);
#				if (length ($grub2cfg{$sb}{$i}{'insmod'}) > 5) {	# inner-mods
#					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'insmod'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'insmod'}}), 0, 5)."...")."</span>");
#				} else {
#					push (@cols, &html_escape (cutoff (join (",", @{$grub2cfg{$sb}{$i}{'insmod'}}), 5, "...")));
#				}
#				push (@cols, &html_escape (cutoff (join (",", @array), 5, "...")));
#				#push (@cols, join (",", @{$grub2cfg{$sb}{$i}{'opts_vars'}}));
#				if (length ($grub2cfg{$sb}{$i}{'protected'}) > 5) {	# options-unrestricted
#					push (@cols, "<span title=\"".&html_escape ($grub2cfg{$sb}{$i}{'protected'})."\">".&html_escape (substr ($grub2cfg{$sb}{$i}{'protected'}, 0, 5)."...")."</span>");
#				} else {
#					push (@cols, &html_escape ($grub2cfg{$sb}{$i}{'protected'}));
#				}
#				if (length ($grub2cfg{$sb}{$i}{'set'}) > 5) {
#					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'set'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'set'}}), 0, 5)."...")."</span>");
#				} else {
#					push (@cols, &html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'set'}}), 0, 5)."..."));
#				}
#				if (length ($grub2cfg{$sb}{$i}{'inners'}) > 5) {
#					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'inners'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'inners'}}), 0, 5)."...")."</span>");
#				} else {
#					push (@cols, &html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'inners'}}), 0, 5)."..."));
#				}
#				if (length ($grub2cfg{$sb}{$i}{'opts_if'}) > 5) {
#					push (@cols, "<span title=\"".&html_escape (join (", ", @{$grub2cfg{$sb}{$i}{'opts_if'}}))."\">".&html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'opts_if'}}), 0, 5)."...")."</span>");
#				} else {
#					push (@cols, &html_escape (substr (join (",", @{$grub2cfg{$sb}{$i}{'opts_if'}}), 0, 5)."..."));
#				}
#				push (@cols, $grub2cfg{$sb}{$i}{'is_saved'});
#				my @tdtags;	# highlight entire row of saved_entry if any:
#				if ($grub2cfg{$sb}{$i}{'is_saved'}) {	for (my $i=1; $i<scalar (@cols)+1; $i++) {	$tdtags[$i]='style="background-color: '.$config{"highlight"}.'"';	}	}
#				print &ui_checked_columns_row(\@cols, \@tdtags, "d", "sub=$sb&amp;item=$i,");
#			}
#		}
#	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([	["delete", $text{'delete'}], ["mksaved", $text{'entry_mksaved'}], ["edit", $text{'entry_edit'}]	]);

	#print "hash_grub2cfg:".Dumper(\%grub2cfg);
	#print "array_grub2cfg:".Dumper(\@grub2cfg);

print ui_tabs_end_tab('mode', 'summary');

print ui_tabs_end();
#}
ui_print_footer("/", $text{'index'});


=fdisk
&error_setup($text{'index_err'});
&check_fdisk();

# Work out which disks are accessible
@disks = &list_disks_partitions();
@disks = grep { $access{'view'} || &can_edit_disk($_->{'device'}) } @disks;

$pdesc = $has_parted ? $text{'index_parted'} : $text{'index_fdisk'};
&ui_print_header($pdesc, $module_info{'desc'}, "", undef, 1, 1, 0,
	&help_search_link("fdisk", "man", "doc", "howto"));
$extwidth = 250;

# Check for critical commands
if ($has_parted) {
	&has_command("parted") ||
		&ui_print_endpage(&text('index_ecmd', '<tt>parted</tt>'));
	}
else {
	&has_command("fdisk") ||
		&ui_print_endpage(&text('index_ecmd', '<tt>fdisk</tt>'));
	}

# Show a table of just disks
#@disks = sort { $a->{'device'} cmp $b->{'device'} } @disks;
if (@disks) {
	($hasctrl) = grep { defined($d->{'scsiid'}) ||
			    defined($d->{'controller'}) ||
			    $d->{'raid'} } @disks;
	print &ui_columns_start([ $text{'index_dname'},
				  $text{'index_dsize'},
				  $text{'index_dmodel'},
				  $text{'index_dparts'},
				  $hasctrl ? ( $text{'index_dctrl'} ) : ( ),
				  $text{'index_dacts'} ]);
	foreach $d (@disks) {
		$ed = &can_edit_disk($d->{'device'});
		$smart = &supports_smart($d);
		@links = ( );
		@ctrl = ( );
		if (defined($d->{'scsiid'}) && defined($d->{'controller'})) {
			push(@ctrl, &text('index_dscsi', $d->{'scsiid'},
						         $d->{'controller'}));
			}
		if ($d->{'raid'}) {
			push(@ctrl, &text('index_draid', $d->{'raid'}));
			}
		if ($ed && &supports_hdparm($d)) {
			# Display link to IDE params form
			push(@links, "<a href='edit_hdparm.cgi?".
			     "disk=$d->{'index'}'>$text{'index_dhdparm'}</a>");
			}
		if (&supports_smart($d)) {
			# Display link to smart module
			push(@links, "<a href='../smart-status/index.cgi?".
			    "drive=$d->{'device'}:'>$text{'index_dsmart'}</a>");
			}
		if ($ed) {
			push(@links, "<a href='blink.cgi?".
                       		"disk=$d->{'index'}'>$text{'index_blink'}</a>");
                	}
		print &ui_columns_row([
#			$ed ? &ui_link("edit_disk.cgi?device=$d->{'device'}",$d->{'desc'})
#			    : $d->{'desc'},
			$d->{'desc'},
			&ui_link("edit_disk.cgi?device=$d->{'device'}",$d->{'desc'}),
			$d->{'size'} ? &nice_size($d->{'size'}) : "",
			$d->{'model'},
			scalar(@{$d->{'parts'}}),
			$hasctrl ? ( join(" ", @ctrl) ) : ( ),
			&ui_links_row(\@links),
			]);
		}
	print &ui_columns_end();
	}
else {
	print "<b>$text{'index_none2'}</b><p>\n";
	}

&ui_print_footer("/", $text{'index'});

=cut
