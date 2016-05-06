#!/usr/bin/perl
# do_entry.cgi
# Process the operation on the given arguments

require './grub2-lib.pl';
&ReadParse();

if ($in{'add'}) {
	#add a custom menuentry
	&redirect("edit.cgi");
}
my @ids = split /,/, $in{'d'};
#print "ids is:".Dumper(@ids);
#my $cfgfile = &load_cfg_file();
#print Dumper(%grub2cfg);
#$count = scalar (@ids);
my @id2 = ();
for $a (@ids) {
	my ($ss, $ii) = $a =~ /sub=([0-9]+)[^=]+=([0-9]+)/;
	push (@id2, {	"name" => $grub2cfg{$ss}{$ii}{'name'},
					"submenu" => $ss,
					"item" => $ii	});
}
if ($in{'edit'}) {
	&redirect("edit.cgi?sub=".$id2[0]{'submenu'}."&item=".$id2[0]{'item'});
}
=was
my $file = "$server_root/$config{'virt_dir'}/$in{'editfile'}";
if (!-e $file) {
  $file = "$server_root/$in{'editfile'}";
}
=cut
&ui_print_header($title, $text{'manual_title'}, "");
print &text('manual_header', "<tt>$file</tt>"),"<p>\n";
print "in:". Dumper (%in). "||<br />\n";
#print "id2:". Dumper (@id2). "||<br />\n";
#for $a (keys %in) {
#	print "$a => $in{$a}\n";
#}
#print "in is".Dumper(%in);
#print "looking for:\"submenu\"$id2[0]{$ss}.\"item\"$id2[0]{$ii}.";
print "id2 is:".Dumper(@id2);

if ($in{'delete'}) {
	#delete item(s)
	print &text('deleting', $count);
	print $text{'entry'} if $count == 1;
	print $text{'entries'} if $count > 1;
	print "<br >\n";

	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("del_entry.cgi", "get");
	print &ui_links_row(\@links);
	print &ui_columns_start([
		$text{'select'},
		"count i",
		"count j",
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
	my $cnt_i = 0;
	foreach $sb (keys %grub2cfg) {	# each submenu
		my $cnt_j = 0;
		foreach $i (keys $grub2cfg{$sb}) {	# each menu entry
			for $a (@id2) {
				print $a{'submenu'}." eq $cnt_i gand ".$a{'item'}." eq $cnt_j";
				if ($a{'submenu'}==$cnt_i && $a{'item'}==$cnt_j) {
					my @cols;
					push (@cols, $grub2cfg{$sb}{$i}{'id'});
					push (@cols, $cnt_i);
					push (@cols, $cnt_j);
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
	#				while (my ($key,$val) = each $grub2cfg{$sb}{$i}{'opts_vars'}) {
	#					push (@array, $key. ' => '. $val);#$grub2cfg{$sb}{$i}{'opts_vars'}{$val}{$val});#$key{$key});#$grub2cfg{$sb}{$i}{'opts_vars'}{$val};
	######$val not correct#####					
	#				}
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
					#print &ui_checked_columns_row(\@cols, \@tdtags, "d", "sub=$sb&amp;item=$i,");
					print &ui_columns_row(\@cols, \@tdtags);
				}
			}
			$cnt_j++;
		}
		$cnt_i++;
	}
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([	["delete", $text{'cdelete'}]	]);

} elsif ($in{'edit'}) {
	#edit item(s)
	print &text('editing', $count);
	print $text{'entry'} if $count == 1;
	print $text{'entries'} if $count > 1;
	print "<br >\n";
} elsif ($in{'mksaved'}) {
	#set as default
	if (!$count) {
		print $text{'no_selected'};
		exit();
	} elsif ($count > 1) {
		print $text{'no_selected'};
		exit();
	}
	print 'Making "<tt>'.$id2[0]{'name'}.'</tt>" default';
	#saved_entry = $id2[0]{'name'}
}

=was2
# textbox form
print &ui_form_start("edit_save.cgi", "form-data");
print &ui_hidden("editfile", $file),"\n";

$lref = &read_file_lines($file);
if (!defined($start)) {
	$start = 0;
	$end = @$lref - 1;
	}
for($i=$start; $i<=$end; $i++) {
	$buf .= $lref->[$i]."\n";
	}
print &ui_textarea("directives", $buf, 25, 80, undef, undef,"style='width:100%'"),"<br>\n";
print &ui_submit($text{'save'});
print &ui_form_end();
=cut

&ui_print_footer($return, $text{'index_short'});
