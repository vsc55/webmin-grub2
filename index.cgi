#!/usr/local/bin/perl
# index.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;

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
@tabs = (['entry', $text{'tab_entry'}], ['environ', $text{'tab_environ'}], ['other', $text{'tab_other'}], ['files', $text{'tab_files'}]);

print ui_tabs_start(\@tabs, 'mode', 'entry');

print ui_tabs_start_tab('mode', 'entry');
#structure:
#submenu
#-menuentry
#--name
#--ins
#--set
#--class
#--other
	my $cfgfile = &load_cfg_file();
	
	my %parsed = &divide_cfg_into_parsed_files();
	#print "parsed is ".Dumper (\%parsed)."||||";
	
	#print "$cfgfile<br />";
	#if ($cfgfile !~ "/menuentry/") {
	if (&indexof ($cfgfile, "menuentry")!=-1) {
	#if (!length $cfgfile) {
		print $text{'index_noentrys'};
		exit();
	}
#my $nsubs = 0;
#while (index($cfgfile, "submenu", 0)!=-1) {
#while ($cfgfile !~ "/submenu/") {
#	$nsubs++;
#}
	my @subs = split /submenu\s+/, $cfgfile;	# separate each submenu
	#my %subs = split /submenu\s/, $cfgfile;	# separate each submenu
	#print join "-----", @subs;
	#print "-;-;-;-;-;-;";
	#print Dumper(\%subs);
#=was
	my %grub2cfg;
#my $nentrys = 0;
##while (index($cfgfile, "menuentry", 0)!=-1) {
#while ($cfgfile !~ "/menuentry/") {
#	$nentrys++;
#}
	#while ($index <= $#subs) {
	#	my $value = $subs[$index];
	#	print "testing $value\n";
	#	if ($value =~ m/^(submenu\s+)/) {
	#		print "removed value $value\n";
	#		splice @subs, $index, 1;
	#	} else {
	#		$value =~ s/^submenu\s+//;
	#		$index++;
	#	}
	#}
	#my @array = qw( alpha beta gamma delta );
	for (my $index = $#subs; $index >= 0; --$index) {
		#print "SUBMENU$index))$subs[$index]((";
		#if ($subs[$index] !~ /^[\"']/) {
		#	#print "removing $index.\n";
		#	print "removing $subs[$index].\n";
		#	splice @subs, $index, 1;	# remove certain elements
		#} else {
		#	$subs[$index] =~ s/^(submenu\s+)//;
		#}
	}
	my $count = 0;
	for my $a (@subs) {
		my $index = 0;
		#if ($a =~ m/^(submenu\s+)/) {
		#	shift @subs;
		#} else {
		#	$a =~ s/^submenu\s+//;
		#}
		my $valid = 0;
		if ($a =~ m/^[\"']([^\"']+)[\"']\s*(.[^\{]+)/) {	$valid = 1;	}
		my $sname = ($valid == 1) ? $1 : "main";
		my $tempopts = $2;
		my $tempopts_noif;
		if ($tempopts =~ m/(if.*fi)/) {
			@temp = split /$1/, $tempopts;
			for (@temp) {
				$tempopts_noif .= $tempopts =~ s/$1//;
			}
		}
		my $sopts = $tempopts =~ s/\s*$//;
		#my %sopts = split / /, $2;
		$grub2cfg{$count} = {
			valid => 	$valid,
			name => 	$sname,
			options => 	(defined $tempopts_noif) ? $tempopts_noif : $sopts,#join "; ", %sopts,
#			all => 		$a
		};
		if (substr($a, 0, 1) =~ /^['"]/) {
			$a =~ /^([\"'])(?:\\\1|.)*?\1/;
			#if (!$sname) {
			#	$sname = "main";
			#}
			#print Dumper($2);
			#$grubcfg{$sname} = [	"name" =	""	];
		}
		#print "SUBMENU:$a<br /><br />";
		@entrys = split /menuentry\s/, $a;	# divide each submenu into menuentries
		#my %entrys = split /menuentry\s/, $a;	# divide each submenu into menuentries
		#print Dumper (\%entrys);
#=was
		my $ecnt = 0;
		for my $entry (@entrys) {
			my $valid = 0;
			if ($entry =~ m/^[\"']([^\"']+)[\"']\s*([^\{]*)\s*\{\s*([^\}]+)\}\s*/) {	$valid = 1;	}
			my $ename = $1;
			my $eopts = $2;
			my @array = split /\s/, $2;
			my $cntr = 0;
			my $key;
			my %eoptsarray;# = [ var => "",	class => "",	unrestricted => ""	];
			for my $e (@array) {
				#print "(".($cntr+1).")$e";
				#print "[".$array[$cntr]."]";
				if ($e =~ /^[^a-zA-z\"']/) {	# first letter is not alpha or quote
					$key = ($e =~ m/^\-\-(.*)$/) ? $1 : $e;
					push(@{$eoptsarray{$key}}, true) if $array[($cntr+1)] =~ m/^[^a-zA-z\"']/;
					#print "*key*";
				} else {
					if ($key) {
						if ($key =~ m/^\$/) {
							push(@{$eoptsarray{'var'}{$key}}, $e);
						} else {
							push(@{$eoptsarray{$key}}, $e);
						}
					} else {
						$eoptsarray{$array[$cntr-1]} = true;
					}
					#print "*value*";
				}
				$cntr++;
			}
			my $cls = $eoptsarray{'class'};
			my $unr = ($eoptsarray{'unrestricted'}) ? true : false;
			my $vars = $eoptsarray{'var'};
			#print "eoptsarray is ".Dumper(\%eoptsarray);
			#print ":options:".Dumper(\@array);
			#my %eopts = split /( |;;)/, join ";;", @array;
			#my @eopts = split /( |;;)/, join ";;", @array;
			my @array = split /\n/, $3;
			my $eins = join ";;", @array;
			$eins =~ s/if.*fi//g;
			$eins =~ s/\t//g;
			$eins =~ s/;;;;/;;/g;
			$eins =~ s/;;$//g;
=skip
			$s = 0;
			for (@array) {
				splice @array, ++$s, 0, "\n";
			}
			#my @array2 = split /\n/, $eins;
			
			print "eins split is ".Dumper(\@array);
			my $cntr = 0;
			my $key;
			my %einsarray;
			for my $d (@array) {
				$d =~ s/if.*fi//g;
				$d =~ s/\t//g;
				$d =~ s/;;;;/;;/g;
				$d =~ s/;;$//g;
				if ($d =~ /;;$/) {
					$key = ($d =~ m/^\-\-(.*)$/) ? $1 : $d;
					push(@{$einsarray{$key}}, true) if $array[($cntr+1)] =~ m/^[^a-zA-z\"']/;
					#print "*key*";
				} else {
					if ($key) {
						if ($key =~ m/^\$/) {
							push(@{$einsarray{'var'}{$key}}, $d);
						} else {
							push(@{$einsarray{$key}}, $d);
						}
					} else {
						$einsarray{$array[$cntr-1]} = true;
					}
					#print "*value*";
				}
				$cntr++;
			}
			my $mods = $einsarray{'insmod'};
			my $linux = $einsarray{'linux'};
			my $init = $einsarray{'initrd'};
			my $sets = $einsarray{'set'};
			#my $othi = $einsarray{'set'};
			print "einsarray is ".Dumper (\%einsarray);
=cut
			#my %eins = split /\s,\n/, $3;
#			chomp $eins;
			#print "<b style=\"background-color:green\">".$entry[0].$entry[1].$entry[2]."</b>";
			#$a =~ /^([\"'])(\\\1|.)*?\1/;
			#my ($name) = $a =~ /^[\"']([^\"']+)[\"']/;
			#$ename = "main" if !defined $ename;
			#($ename) = $entry =~ /^[\"']([^\"']+)[\"']/;
			my ($temppre) = $entry =~ /^[\"'][^\"']+[\"']\s([^\{]+)\s+/;
			my @array = split / /, $temppre;
			my %pre;
			$pre{$_}++ for (@array);
			my ($pre_if) = $pre =~ /(if\s[^(fi)]+fi)/;
			$pre_if = "" if !defined;
			my %real_pre = split / /, $entry;
#			my %real_pre;
#			my @mine;
#			@my_pre = split / /, $pre;
##my %final_hash_long;
##foreach my $data_pair (@data_list) {
##    my $key                = $data_pair->{key};
##    my $value              = $data_pair->{value};
##    $final_hash_long{$key} = $value;
##}
##
#my %real_pre =
#  map { $_->{key} => $_->{value} } @my_pre;
#			my $n_pre = -1;
#			for my $a (@my_pre) {
#				print "$a->{'key'},$a->{'value'}\n";#print $a;
#				$n_pre++;
#				if (!$n_pre || $n_pre % 2) {	# if odd iteration
#					my $key = $a;	# assign as key
#				} else {
#					my $val = $a;	# assign as val if even iteration
#					if ($key ~~ @mine) {
#						$real_pre{$key} .= ' '.$val;
#					} else {
#						$real_pre{$key} = $val;
#					}
#					push(@mine, $key);
#				}
#				print "$n_pre-$key=$val.";
#			}
			#($cls) = $entry =~ /--class\s(\w+)/;
			#my ($cls) = $pre =~ /--class\s([^\s]+)/g;
			#my ($inner) = $entry =~ /^[\"'][^\"']+[\"']\s*[^\{]+\{\s*([^\}]+)/;
			my @array = split / /, $inner;
			#my %ins = split / /, $inner;
			#print Dumper (\%ins);
			#$mods = join(" ", split /insmod\s/, $inner);
			#$sets = join(" ", split /set\s/, $inner);
			#$grub2cfg{$count}{'submenu'} = $a;
			$grub2cfg{$count}{$ecnt} = {
										id =>			$ecnt,
										name =>			(defined $ename) ? $ename : "main",
										valid =>		$valid,
				#						options =>		$eopts,#join " ", $eopts,#join " ", %pre,
										classes =>		$cls,
										protected =>	$unr,
										vars_in_opts =>	$vars,
										opts_if =>		$pre_if,
										inner =>		$eins,#join ", ", @eins,#join " ", %ins,#$inner,
										insmod =>		$mods,
										set =>			$sets,
#										all =>			($name eq $ename) ? '' : $entry
										all =>			$entry
										};
		#if ($entry[0] ne "'" && $entry[0] ne '"') {	# skip first entry if doesn't start with quote
		#	$pre = shift @entrys;
		#}
		#if ($entry =~ /\}\s*\}/) {	# ignore if doesn't end with }
		#	pop @entrys;
		#}
			$ecnt++;
		}
		my $nentrys = scalar(@entrys);
		if (!$nentrys && !$count) {	# no menuentry in mainmenu ????
			print $text{'index_noentrys'};
			exit();
		}
		if (!$count) {
			if ($nentrys != 1) {
				print "mainmenu has $nentrys entries.<br />";
			} else {
				print "mainmenu has $nentrys entry.<br />";
			}
		} else {
			if ($nentrys != 1) {
				print "submenu $count has $nentrys entries.<br />";
			} else {
				print "submenu $count has $nentrys entry.<br />";
			}
		}
		$count++;
		#foreach $entry (@entrys) {
		#	print "$entry<br /><br />";
		#}
#=cut
	}
#=was2
	#print "submenus:scarlar(@subs).menuentrys:scalar(@entrys)<br />";
	#($pre) = $cfgfile =~ /^([^(menuentry)]+)/m;
	#my @bootcfg = extract_multiple(
	#	$cfgfile,
	#	[ sub{extract_bracketed($_[0], '{}')},],
	#	undef,
	#	1
	#);
	#print "<pre>";
	#print $pre;
	#print "$_<br \>" foreach @bootcfg;
	#print "</pre>";
	#my @subs = split /submenu\s/, $cfgfile;	# divide cfg into main, sub0, ...
	#foreach (@subs) {	# add sections (as above) to whole array
	#	push (@bootcfg, $_);
	#}
	#foreach $sub (@subs) {	# add each menuentry to its section of the whole array
	#	foreach (split /menuentry\s/, $sub) {
	#		push (@{$sub}, $_);
	#	}
	#}
	#my @main_entrys = split /menuentry\s/, shift @subs;
	#foreach (@subs) {
	#	push (@subs, split /menuentry\s/);
	#}
	#print Dumper (@bootcfg);
	#my @names = split /menuentry\s.([^'|"]+)./, $entry;
	#my @names = split /menuentry\s.([^'|"]+)./, $cfgfile;#([^\{]+)\{([^\}])}
	#my @names = $cfgfile =~ /menuentry\s.([^'|"]+).(\{(?:[^{}]*|(?0))*\})/xg;
	#@entrys = extract_multiple($text,
	#    [ \&extract_bracketed,
	#		\&extract_quotelike,
	#		\&some_other_extractor_sub,
	#		qr/[xyz]*/,
	#		'literal',
	#	]);
	#(@entrys) = extract_delimited $cfgfile, q{"'};
	#@entrys = extract_codeblock ($cfgfile, '{}');
	#shift @names;
	#print scalar(@names);
	#print "<pre>";
	#foreach (@entrys) {
	#	print "$_<br />";
	#}
	#print "</pre>";
	#print "real_pre:".Dumper(\%real_pre);
	#print "my_pre:".Dumper(\@my_pre);
	#while (my ($key, $value) = each @my_pre) {
	#	print "$key = $value\n";
	#}
#=tryform
	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("delete_entry.cgi", "get");
	print &ui_links_row(\@links);
	print &ui_columns_start([
		$text{'select'},
		$text{'entry_name'},
		$text{'entry_sub_name'},
		$text{'entry_classes'},
		$text{'entry_mods'},
		$text{'entry_opt_var'},
		$text{'entry_protected'},
		$text{'entry_sets'},
		$text{'entry_opt_if'} ], 100);
	foreach $sb (keys %grub2cfg) {	# each submenu
		foreach $i (keys $grub2cfg{$sb}) {	# each menu entry
			if ($grub2cfg{$sb}{$i}{'valid'}) {	# only show valid entries
				my @cols;
				push (@cols, "<a href=\"edit.cgi?".&html_escape ($grub2cfg{$sb}{$i}{'name'})."\">".&html_escape (cutoff ($grub2cfg{$sb}{$i}{'name'}, 40, "..."))."</a>");
				push (@cols, &html_escape (cutoff ($grub2cfg{$sb}{'name'}, 20, "...")));
				push (@cols, &html_escape (cutoff (join (",", $grub2cfg{$sb}{$i}{'classes'}), 10, "...")));
				push (@cols, &html_escape (cutoff ($grub2cfg{$sb}{$i}{'insmod'}, 5, "...")));
				push (@cols, &html_escape (cutoff ($grub2cfg{$sb}{$i}{'vars_in_opts'}, 5, "...")));
				push (@cols, &html_escape (cutoff ($grub2cfg{$sb}{$i}{'protected'}, 5, "...")));
				push (@cols, &html_escape (cutoff ($grub2cfg{$sb}{$i}{'set'}, 5, "...")));
				push (@cols, &html_escape (cutoff ($grub2cfg{$sb}{$i}{'opts_if'}, 5, "...")));
				print &ui_checked_columns_row(\@cols, undef, "d", "$sb-$i");
			}
		}
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([ [ "delete", $text{'delete'} ] ]);
#=cut
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
    @links = ( );
	my %grub2env = &get_grub2_env();
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
print ui_tabs_end_tab('mode', 'other');
	
print ui_tabs_start_tab('mode', 'files');
	print "<dl>";
	my %cmds = get_cmds();
	foreach my $a (keys \%cmds) {
		print "<dt>$a</dt>\n";
		while (my ($k, $v) = each %{ $cmds{$a} } ) {
			print "\t<dd>$k = $v</dd>\n";
		}
		print "<br />\n";
	}
	print "</dl>";
print ui_tabs_end_tab('mode', 'files');

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
