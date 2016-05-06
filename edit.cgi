#!/usr/bin/perl
# edit.cgi
# edit the GRUB2 menuentry

require './grub2-lib.pl';
&ReadParse();

my $sb = $in{'sub'};
my $i = $in{'item'};
my $heading = ($sb+$i) ? $text{'edit'} : $text{'add'};

#print &ui_print_header ($text{'index_title'}, ");#\"".$grub2cfg{$sb}{$i}{'name'}."\"", "");
&ui_print_header ($text{'index_title'}, "$heading $text{'menuentry'}", "");
#print "sub:$sb|". Dumper (%in). "item:$i||";

if ($sb+$i) {	# existing
	
	print &ui_form_start ("edit_save.cgi", "post"),#"form-data"),
		&ui_hidden ("sb", $sb),# "\n",
		&ui_hidden ("i", $i),
		&ui_hidden ("valid", $grub2cfg{$sb}{$i}{'valid'}),
		&ui_hidden ("id", $grub2cfg{$sb}{$i}{'id'}),
		&ui_hidden ("saveit", $grub2cfg{$sb}{$i}{'is_saved'}),
		&ui_hidden ("pos", "'$sb>$i'"),
		&ui_hidden ("submenu", $grub2cfg{$sb}{'name'}),
		&ui_table_start ($text{'edit_entry'}, "width=100%", 2);#, \@tds)
			print &ui_table_row ($text{'invalid'}, "") if $grub2cfg{$sb}{$i}{'valid'}!=1;
			print &ui_table_row ($text{'edit_id'}, $grub2cfg{$sb}{$i}{'id'});
			print &ui_table_row ($text{'edit_name'},
				&ui_textbox ("entry_name", $grub2cfg{$sb}{$i}{'name'}, 80, 0, undef));# "onChange='$onch'"));
			print &ui_table_row ($text{'edit_save'},
				&ui_checkbox ("saveit", ($grub2cfg{$sb}{$i}{'is_saved'}==1),
					'&nbsp;('.$text{'env_was'}.': '.
					(($grub2cfg{$sb}{$i}{'is_saved'}==1) ? $text{'checked'} : $text{'unchecked'}).')',
					($grub2cfg{$sb}{$i}{'is_saved'}==1)));
			print &ui_table_row ($text{'edit_pos'}, "'$sb>$i'");
			print &ui_table_row ($text{'edit_submenu'}, '"'.$grub2cfg{$sb}{'name'}.'"') if $sb>0;
		my $count = 0;
		for $c (@{ $grub2cfg{$sb}{$i}{'classes'} }) {
#			print &ui_table_row (&hlink($text{'edit_class'}, "entry_name$count"),
			print &ui_table_row (($count==0) ? $text{'edit_class'} : '',
				&ui_textbox ("class", $c, 20, 0, undef).
				&ui_button ($text{'delete'}, "delete_class[$count]"));# "onChange='$onch'"));#$grub2cfg{$sb}{$i}{'classes'}{
			$count++;
		}
			print &ui_table_row ($text{'edit_addclass'},
				&ui_button ($text{'add'}, "class[$count++]"));

#HIDE			#print &ui_table_row ($text{'edit_addclass'},
			#	&ui_textbox ("class$count++", '', 20, 0, undef));
		my $cnt = 0;
		for $v (keys %{ $grub2cfg{$sb}{$i}{'opts_vars'} }) {
			print &ui_table_row (($cnt==0) ? $text{'edit_optvar'} : '',
				&ui_textbox ("optvar", $v, 25, 0, undef). " = ".
				&ui_textbox ("optval", $grub2cfg{$sb}{$i}{'opts_vars'}{$v}, 80, 0, undef).
				&ui_button ($text{'delete'}, "delete_optvar$cnt"));
			$cnt++;
		}
			print &ui_table_row ($text{'edit_protect'},
				&ui_checkbox ("protectit", ($grub2cfg{$sb}{$i}{'protected'}eq"true"),
					'&nbsp;('.$text{'env_was'}.': '.
					(($grub2cfg{$sb}{$i}{'protected'}eq"true") ? $text{'checked'} : $text{'unchecked'}).')',
					($grub2cfg{$sb}{$i}{'protected'}eq"true")));
			#if ($grub2cfg{$sb}{$i}{'protected'} eq true) {
			#	print &ui_table_row ($text{'edit_protected'}, &ui_yesno_radio("protectit", 1));
			#} else {
			#	print &ui_table_row ($text{'edit_protected'}, "");
			#}
		if ($grub2cfg{$sb}{$i}{'opts_if'}) {
			my $cntoif = 0;
			for $v (@{ $grub2cfg{$sb}{$i}{'opts_if'} }) {
				print &ui_table_row (($cntoif==0) ? $text{'edit_opts_if'} : '',
					&ui_textbox ("opts_if", $v, 25, 0, undef).
					&ui_button ($text{'delete'}, "delete_opts_if$cntoif"));
				$cntoif++;
			}
		}
		if ($grub2cfg{$sb}{$i}{'set'}) {
			my $cntiset = 0;
			for $v (@{ $grub2cfg{$sb}{$i}{'set'} }) {
				print &ui_table_row (($cntiset==0) ? $text{'edit_set'} : '',
					&ui_textbox ("set", $v, 25, 0, undef).
					&ui_button ($text{'delete'}, "delete_set$cntiset"));
				$cntiset++;
			}
		}
		print &ui_table_end(),
#		&ui_submit ( ["save", $text{'save'} ], [ "delete", $text{'delete'} ] ),
		&ui_submit ($text{'save'}, "save"),
		&ui_submit ($text{'edit_remove'}, "delete"),
		#&ui_submit ($text{'save'}),
	&ui_form_end();
	
	#print Dumper(%{ $grub2cfg{$sb}{$i} });
#'all'=CentOS Linux (3.10.0-327.10.1.el7.x86_64) 7 (Core)\' --class rhel fedora --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option \'gnulinux-3.10.0-229.20.1.el7.x86_64-advanced-39a93f7d-8195-45e6-ac88-0cefae8bdaec\' {
#	load_video
#	set gfxpayload=keep
#	insmod gzio
#	insmod part_msdos
#	insmod xfs
#	set root=\'hd0,msdos5\'
#	if [ x$feature_platform_search_hint = xy ]; then
#	  search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos5 --hint-efi=hd0,msdos5 --hint-baremetal=ahci0,msdos5 --hint=\'hd0,msdos5\'  dee05a36-8217-49c7-b1fc-6ad1f4684158
#	else
#	  search --no-floppy --fs-uuid --set=root dee05a36-8217-49c7-b1fc-6ad1f4684158
#	fi
#	linux16 /vmlinuz-3.10.0-327.10.1.el7.x86_64 root=UUID=39a93f7d-8195-45e6-ac88-0cefae8bdaec ro rd.lvm.lv=centos/swap crashkernel=auto rhgb quiet LANG=en_CA.UTF-8
#	initrd16 /initramfs-3.10.0-327.10.1.el7.x86_64.img
#}
#';

	&ui_print_footer("$return", $text{'index_short'});	# click to return
} else {	# new entry
	
	print &ui_form_start ("edit_save.cgi", "post"),#"form-data"),
		&ui_table_start ($text{'edit_entry'}, "width=100%", 2);#, \@tds)
			print &ui_table_row ($text{'edit_name'},
				&ui_textbox ("entry_name", $name, 80, 0, undef));# "onChange='$onch'"));
			print &ui_table_row ($text{'edit_save'},
				&ui_checkbox ("saveit", $is_saved));
			print &ui_table_row ($text{'edit_pos'}, $pos);
#			print &ui_table_row ($text{'edit_submenu'}, '"'.$grub2cfg{$sb}{'name'}.'"') if $sb>0;
		my $count = 0;
			print &ui_table_row ($text{'edit_addclass'},
				&ui_button ($text{'add'}, "class[$count++]"));

#HIDE			#print &ui_table_row ($text{'edit_addclass'},
			#	&ui_textbox ("class$count++", '', 20, 0, undef));
		my $cnt = 0;
			print &ui_table_row ($text{'edit_protect'},
				&ui_checkbox ("protectit", $protected));
			#if ($grub2cfg{$sb}{$i}{'protected'} eq true) {
			#	print &ui_table_row ($text{'edit_protected'}, &ui_yesno_radio("protectit", 1));
			#} else {
			#	print &ui_table_row ($text{'edit_protected'}, "");
			#}
		#if ($grub2cfg{$sb}{$i}{'opts_if'}) {
		#	my $cntoif = 0;
		#	for $v (@{ $grub2cfg{$sb}{$i}{'opts_if'} }) {
		#		print &ui_table_row (($cntoif==0) ? $text{'edit_opts_if'} : '',
		#			&ui_textbox ("opts_if", $v, 25, 0, undef).
		#			&ui_button ($text{'delete'}, "delete_opts_if$cntoif"));
		#		$cntoif++;
		#	}
		#}
		#if ($grub2cfg{$sb}{$i}{'set'}) {
		#	my $cntiset = 0;
		#	for $v (@{ $grub2cfg{$sb}{$i}{'set'} }) {
		#		print &ui_table_row (($cntiset==0) ? $text{'edit_set'} : '',
		#			&ui_textbox ("set", $v, 25, 0, undef).
		#			&ui_button ($text{'delete'}, "delete_set$cntiset"));
		#		$cntiset++;
		#	}
		#}
		print &ui_table_end(),
#		&ui_submit ( ["save", $text{'save'} ], [ "delete", $text{'delete'} ] ),
		&ui_submit ($text{'save'}, "save"),
		&ui_submit ($text{'cancel'}, "cancel"),
		#&ui_submit ($text{'save'}),
	&ui_form_end();

}