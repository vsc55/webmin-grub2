#!/usr/bin/perl
# do_entry.cgi
# Process the operation on the given arguments

require './grub2-lib.pl';
&ReadParse();

if ($in{'add'}) {
	&redirect("edit.cgi");	#add a custom menuentry
}
my @ids = split /,/, $in{'d'};
my @id2 = ();
for $a (@ids) {
	my ($ss, $ii) = $a =~ /sub=([0-9]+)[^=]+=([0-9]+)/;
	push (@id2, {	"name" => $grub2cfg{$ss}{$ii}{'name'},
					"submenu" => $ss,
					"item" => $ii	});
}
if ($in{'edit'}) {
	&redirect("edit.cgi?sub=".$id2[0]{'submenu'}."&item=".$id2[0]{'item'});
#} elsif ($in{'delete'}) {
#	my $count = 0;
#	for $a (split /\0/, $in{'d'}) {
#		&remove_an_entry ($id2[$count]{'submenu'}, $id2[$count]{'item'}, \%grub2cfg);
#	}
#	$count++;
}

&ui_print_header($title, $text{'manual_title'}, "");
print &text('manual_header', "<tt>$file</tt>"),"<p>\n";
#print "in:". Dumper (%in). "||<br />\n";
#print "id2 is:".Dumper(@id2);

if ($in{'delete'}) {

	@links = ( );
	push(@links, &select_all_link("d"), &select_invert_link("d"));
	print &ui_form_start("del_entry.cgi", "get");
	print &ui_links_row(\@links);
	#my @array;
	#push (@array, $text{'select'}) if $#id2 > 1;	# begin the row with a checkbox
	my @array = ( $text{'select'} );	# begin the row with a checkbox
	for (my $a=0; $a<keys %display; $a++) {
		push (@array, $display{$a}{'name'}) if $display{$a}{'displayed'}==1;	# add each %display if marked as displayed
	}
	print &ui_columns_start(\@array, 100);
	for (@ids) {
		$sb = $id2[$_]{'submenu'};
		$i = $id2[$_]{'item'};
		#print "submenu: $sb|item: $i||||<br />\n";
		my @cols;
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
		#if ($#id2 > 1) {
		#	print &ui_checked_columns_row(\@columns, \@tdtags, "d", "sub=$sb&amp;item=$i,");
		#} else {
		#	print &ui_columns_row(\@columns, \@tdtags);
		#}
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
