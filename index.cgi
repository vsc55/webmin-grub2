#!/usr/local/bin/perl
# index.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation

our $return = &this_url();

# Page header
&ui_print_header (undef, $text{'index_title'}, "", undef, 1, 1, undef,
				 &test_cfg_button()." <br />".
	&help_search_link ("grub2", "man", "doc", "google"), undef, undef,
	&text ('index_version', $version));

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
@tabs = (
		 ['entry', 		$text{'tab_entry'}],
		 ['environ', 	$text{'tab_environ'}],
		 ['disks',		$text{'tab_disks'}],
		 ['users', 		$text{'tab_users'}],
		 ['other', 		$text{'tab_other'}],
		 ['files', 		$text{'tab_files'}],
		 ['summary', 	$text{'tab_sum'}],
		 ['dump',	 	$text{'tab_dump'}],
		);

#print "parsed cfg is ".Dumper (\%grub2cfg)."||||";

print ui_tabs_start(\@tabs, 'mode', 'entry');

###### entry tab ######
print ui_tabs_start_tab('mode', 'entry');

	my %parsed = &divide_cfg_into_parsed_files();
	
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
				if (length ($grub2cfg{$sb}{$i}{'protected'}) > 5) {	# options-unrestricted
					$cols{'pro'} = "<span title=\"".&html_escape ($grub2cfg{$sb}{$i}{'protected'})."\">".&html_escape (substr ($grub2cfg{$sb}{$i}{'protected'}, 0, 5)."...")."</span>";
				} else {
					$cols{'pro'} = &html_escape ($grub2cfg{$sb}{$i}{'protected'});
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
	print &ui_form_end([	["delete", $text{'delete'}], ["mksaved", $text{'entry_mksaved'}], ["edit", $text{'entry_edit'}]	]);

print ui_tabs_end_tab('mode', 'entry');

###### environ tab ######
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

	my %grub2def = &get_grub2_def();
	my %grub2env = &get_grub2_env();
    for my $a (keys %grub2env) {
	    if ($grub2env{$a} && $a) {
			$grub2def{$a} = $grub2env{$a};
		}
	}
	
	#print "grub2def is".Dumper (%grub2def)."||||";
	#print "env_setts is".Dumper (%env_setts)."||||";
    @links = ( );
	# HTML 4~
			$jsHTML4combo.= '<script type="text/javascript">
				function comboInit(thelist)
				{
					theinput = document.getElementById(theinput);  
					var idx = thelist.selectedIndex;
					var content = thelist.options[idx].innerHTML;
					if (theinput.value == "")
						theinput.value = content;	
				}
				function combo(thelist, theinput)
				{
					theinput = document.getElementById(theinput);  
					var idx = thelist.selectedIndex;
					var content = thelist.options[idx].innerHTML;
					theinput.value = content;	
				}
				</script>';
    push(@links, &select_all_link("sel"), &select_invert_link("sel"));
    print &ui_form_start("do_env.cgi", "get");
    print &ui_links_row(\@links);
    print &ui_columns_start([
		$text{'select'},
		$text{'var'},
		$text{'env_was'},
		$text{'val'} ],	100);
	for my $a (keys %grub2def) {
		my @cols;
##	    push(@cols, "<a class=\"del\" href=\"delenv.cgi\">$text{'del'}</a>".
##		push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$_</a>");
		push (@cols, '<span title="'.$env_setts{$a}{'desc'}.'">'.$a.'</span>');
##		push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$grub2env{$_}</a>");
		push (@cols, $grub2def{$a});
		if ($env_setts{$a}{'type'} eq "select" && $env_setts{$a}{'options'}) {
			my $string = '<select name="'.$a.'">'."\n";
			for my $opt (@{ $env_setts{$a}{'options'} }) {
				$string.= '<option value="'.$opt.'"';
				$string.= ' selected="selected"' if $opt eq $env_setts{$a}{'default'};
				$string.= '>'.$opt.'</option>'."\n";
			}
			$string.= '</select>'."\n";
			push (@cols, $string);
		} elsif ($env_setts{$a}{'type'} eq "combo") {	# HTML 5
			my $value = $grub2def{$a};
			$value =~ s/\"/\'/g;
			#my $string = '<input type="text" value="'.$value.'" size="80" list="mylist" id="'.$a.'" name="'.$a.'" />'."\n";
			#my $string = '<style type="text/css">.search_field {display: inline-block;border: 1px inset #ccc;}.search_field input {border: none;}.search_field button {border: none;background: none;}</style>';#padding: 0;
			#$string.= '<div class="search_field">';
			my $string;
			$string.= '<input type="text" size="80" value="'.$value.'" list="mylist" id="input_'.$a.'" name="'.$a.'" />'."\n";# value="'.$value.'"
			$string.= '<img id="img_'.$a.'" src="images/clear.png" alt="'.$text{'clear'}.'" />';#onclick="javascript:document.getElementById("input_'.$a.'").value=\'\'" 
			$string.= '<script type="text/javascript">
			var nameElement = document.getElementById("img_'.$a.'");
			function nameClear(e) {
				document.getElementById("input_'.$a.'").value=\'\';
			}
			if ( nameElement.addEventListener ) {	nameElement.addEventListener("click", nameClear, false);
			} else if ( nameElement.attachEvent ) {	nameElement.attachEvent("onclick", nameClear);	}
			</script>';
			#$string.= '<script language="JavaScript">'."\n\t".'document.getElementById("selected").defaultSelected = true;'."\n".'</script>'."\n";
			$string.= '<datalist id="mylist">'."\n";	# HTML 5
			#$string.= "<select name=\"".$grub2def{$a}."\" onchange=\"combo(this, '".$grub2def{$a}."')\" onmouseout=\"comboInit(this, '".$grub2def{$a}."')\" >";	# HTML 4~
			for my $opt (@{ $env_setts{$a}{'options'} }) {
				if ($opt =~ /<menuentry name>/) {
					for my $op (keys %grub2cfg) {
						for my $op2 (%{ $grub2cfg{$op} }) {
							if ($grub2cfg{$op}{$op2}{'valid'}==1) {
								$string.= "\t".'<option';
								$string.= ' value="'.$grub2cfg{$op}{$op2}{'name'}.'"';
								$string.= ' selected id="selected"' if $grub2cfg{$op}{$op2}{'name'} eq $env_setts{$a}{'default'};
								$string.= '> ';
								$string.= $grub2cfg{$op}{'name'}.' > ';# if $grub2cfg{$op}{'name'};
								$string.= $grub2cfg{$op}{$op2}{'name'}."\n";
							}
						}
					}
					next;
				}
				if ($opt =~ /<menuentry position number>/) {
					for my $op (keys %grub2cfg) {
						for my $op2 (%{ $grub2cfg{$op} }) {
							if ($grub2cfg{$op}{$op2}{'valid'}==1) {
								$string.= "\t".'<option';
								$string.= ' value="'.$op.'>'.$op2.'"';
								$string.= ' selected id="selected"' if $grub2cfg{$op}{$op2}{'name'} eq $env_setts{$a}{'default'};
								$string.= '> ';
								$string.= $grub2cfg{$op}{'name'}.' > ';# if $grub2cfg{$op}{'name'};
								$string.= $grub2cfg{$op}{$op2}{'name'}."\n";
							}
						}
					}
					next;
				} else {
					$string.= "\t".'<option';
					$string.= ' value="'.$opt.'"';
					$string.= ' selected id="selected"' if $opt eq $env_setts{$a}{'default'};
					$string.= '> ';
					$string.= $opt;
					#$string.= ' </option>';	# HTML 4~
					$string.= "\n";
				}
			}
			$string.= '</datalist>'."\n";
			#$string.= '</div>';
			push (@cols, $string);
		} else {#elsif ($env_setts{$a}{'type'} eq "text") {
			my $string = $grub2def{$a};
			$string =~ s/\"/\'/g;
			push (@cols, '<input type="'.$env_setts{$a}{'type'}.'" value="'.$string.'" size="80" />');
		}
		print &ui_checked_columns_row(\@cols, undef, "sel", "$a");#&amp;was=$grub2def{$a}");
    }
    print &ui_columns_end();
    print &ui_links_row(\@links);
    print &ui_form_end([ ["edit", $text{'edit'}], ["delete", $text{'delete'}] ]);
	print "<a class=\"right\" href=\"add_env.cgi\">$text{'add'}</a>";

#	my %grub2env = &get_grub2_env();
#	@links = ( );
#	push(@links, &select_all_link("sel"), &select_invert_link("sel"));
#	print &ui_form_start("do_env.cgi", "get");
#	print &ui_links_row(\@links);
#	print &ui_columns_start([
#		$text{'select'},
#		$text{'var'},
#		$text{'val'} ],	100);
#	foreach (%grub2env) {
#		if ($grub2env{$_} && $_) {
#			my @cols;
##		push(@cols, "<a class=\"del\" href=\"delenv.cgi\">$text{'del'}</a>".
##			push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$_</a>");
#			push (@cols, $_);
##			push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$grub2env{$_}</a>");
#			push (@cols, '<input type="text" value="'.$grub2env{$_}.'" size="80" />');
#			print &ui_checked_columns_row(\@cols, undef, "sel", "$_&amp;was=$grub2env{$_}");
#		}
#	}
#	print &ui_columns_end();
#	print &ui_links_row(\@links);
#	print &ui_form_end([ ["edit", $text{'edit'}], ["delete", $text{'delete'}] ]);
#	print "<a class=\"right\" href=\"add_env.cgi\">$text{'add'}</a>";

print ui_tabs_end_tab('mode', 'environ');

###### other tab ######
print ui_tabs_start_tab('mode', 'other');

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
		push (@cols, '<input type="text" name="disp_name" value="'.$display{$a}{'name'}.'" />'."\n".#$count.'|'.$display{$a}{'name'}
			  #'<input type="hidden" name="disp_all" value="'.$count.'|'.$display{$a}{'displayed'}.'|'.$display{$a}{'nick'}.'|'.$display{$a}{'name'}.'" />');
			  "");
		#print &ui_checked_columns_row (\@cols, undef, "disp", $display{$a}{'nick'}, $display{$a}{'displayed'});#
		print &ui_checked_columns_row (\@cols, undef, "disp", $count.'|'.$display{$a}{'displayed'}.'|'.$display{$a}{'nick'}.'|'.$display{$a}{'name'}, $display{$a}{'displayed'});#
		++$count;
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	#print &ui_form_end();
	print &ui_form_end([ [ "save", $text{'save'} ] ]);
	
	#print Dumper(%hash);

print ui_tabs_end_tab('mode', 'other');
	
###### files tab ######
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

###### summary tab ######
print ui_tabs_start_tab('mode', 'summary');

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
			push (@cols, $my_cfg{$_});
			push (@cols, $config{$_});
			push (@cols, (-e $config{$_}) ? $text{"yes"} : $text{"no"});
			print &ui_columns_row(\@cols, \@tdtags, "d", "$_");
		}
	}
	for (keys %cmds) {
		my @cols;
		push (@cols, $cmds{$_}{$os});
		my $output = substr (&backquote_command ("(which ".$cmds{$_}{$os}.") 2>&1"), 0, 50);
		push (@cols, $output);
		push (@cols, ($cmds{$_}{$os}eq$output) ? true : false);
		print &ui_columns_row(\@cols, \@tdtags, "d", "$_");
	}
	print &ui_columns_end();

print ui_tabs_end_tab('mode', 'summary');

###### disks tab ######
print ui_tabs_start_tab('mode', 'disks');

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

print ui_tabs_end_tab('mode', 'disks');

###### users tab ######
print ui_tabs_start_tab('mode', 'users');

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
	print &ui_form_end (\@form_btns);
	
	#print Dumper(%hash);

print ui_tabs_end_tab('mode', 'users');

###### dump tab ######
print ui_tabs_start_tab('mode', 'dump');

	print "hash_grub2cfg:".Dumper(\%grub2cfg);

print ui_tabs_end_tab('mode', 'dump');

print ui_tabs_end();

#ui_print_footer("/", $text{'index'});


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
			scalar(@{ $d->{'parts'} }),
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
