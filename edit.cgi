#!/usr/bin/perl
# edit.cgi
# edit the GRUB2 menuentry

require './grub2-lib.pl';
&ReadParse();

my $sb = $in{'sub'};
my $i = $in{'item'};
my $heading = ($sb+$i) ? $text{'edit'} : $text{'add'};

&ui_print_header (	$text{'index_title'}, "$heading $text{'menuentry'}", "", undef, undef, undef, undef, undef);

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
			#print &ui_table_row (($count==0) ? $text{'edit_class'} : '',
			#	&ui_textbox ("class", $c, 20, 0, undef).
			#	&ui_button ($text{'delete'}, "delete_class[$count]"));# "onChange='$onch'"));#$grub2cfg{$sb}{$i}{'classes'}{
			#$count++;
		}
$ins_str = sprintf (&ui_table_row ($text{'edit_class'},
												  '<div id="div_'.$count.'">'.
												  &ui_textbox ("class". $count++, '', 20, 0, undef)).
													'<input type="button" id="btn_'.$count.'" name="btn_'.$count.'" value="'.$text{'delete'}.'" /></div>');
			my @array = keys %{{ map{$_=>1} @classList }};
			print &ui_table_row ($text{'entry_classes'},
								 &ui_multi_select ("classes[]", \@array, \@array, 10).
								 '<div id="new_btn">'.
									&ui_button ("$text{'add'} $text{'edit_class'}", "multiselect_add").
								 '</div>'.
								 '<div id="new_box" style="visibility: hidden">'.
									&ui_textbox ("new_class", "", 30, 0, undef).
									&ui_button ($text{'edit_submit'}, "multiselect_submit", 0).
								 '</div>'
			);
			#print &ui_table_row ($text{'edit_addclass'},
			#	&ui_button ($text{'add'}, "class[$count++]"));
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
		&ui_submit ($text{'save'}, "save"),
		&ui_submit ($text{'edit_remove'}, "delete"),
	&ui_form_end();

} else {	# new entry
	
	print &ui_form_start ("edit_save.cgi", "post"),#"form-data"),
		&ui_table_start ($text{'edit_entry'}, "width=100%", 2);#, \@tds)
			print &ui_table_row ($text{'edit_name'},
				&ui_textbox ("entry_name", $name, 80, 0, undef));# "onChange='$onch'"));
			print &ui_table_row ($text{'edit_save'},
				&ui_checkbox ("saveit", $is_saved));
			my $string = '<input type="text" name="entry_menu" size="80" value="" placeholder="'.$text{'combo_all'}.'" id="input_entry_menu" list="mylist" />'."\n";
			$string.= '<img id="img_entry_menu" src="images/clear.png" alt="'.$text{'clear'}.'" />'."\n";
			$string.= '<script type="text/javascript">
			var nameElement = document.getElementById("img_entry_menu");
			function nameClear(e) {
				document.getElementById("input_entry_menu").value=\'\';
				document.getElementById("input_entry_menu").placeholder=\''.$text{'combo_all'}.'\';
			}
			if ( nameElement.addEventListener ) {	nameElement.addEventListener("click", nameClear, false);
			} else if ( nameElement.attachEvent ) {	nameElement.attachEvent("onclick", nameClear);	}
			</script>'."\n";
			$string.= '<datalist id="mylist">'. "\n";
			for my $sb (keys %grub2cfg) {
				$string.= "\t". '<option';
				$string.= ' value="'. $grub2cfg{$sb}{'index'}. '"';
				#$string.= ' selected id="selected"' if $grub2cfg{$sb}{'name'} eq $env_setts{lc $a}{'default'};
				$string.= '> ';
				$string.= $grub2cfg{$sb}{'name'}. "\n";
			}
			$string.= '</datalist>'. "\n";
			print &ui_table_row ($text{'edit_submenu'}, $string);
			my $count = 0;
			my $ins_str = sprintf (&ui_table_row ($text{'edit_class'},
												  '<div id="div_'.$count.'">'.
												  &ui_textbox ("class". $count++, '', 20, 0, undef)).
													'<input type="button" id="btn_'.$count.'" name="btn_'.$count.'" value="'.$text{'delete'}.'" /></div>');
			my @array = keys %{{ map{$_=>1} @classList }};
			print &ui_table_row ($text{'entry_classes'},
								 &ui_multi_select ("classes[]", \@array, \@array, 10).
								 '<div id="new_btn">'.
									&ui_button ("$text{'add'} $text{'edit_class'}", "multiselect_add").
								 '</div>'.
								 '<div id="new_box" style="visibility: hidden">'.
									&ui_textbox ("new_class", "", 30, 0, undef).
									&ui_button ($text{'edit_submit'}, "multiselect_submit", 0).
								 '</div>'
			);
			my $cnt = 0;
			print &ui_table_row ($text{'edit_protect'},
				&ui_checkbox ("protectit", $protected));
		print &ui_table_end(),
		&ui_submit ($text{'save'}, "save"),
		&ui_submit ($text{'cancel'}, "cancel"),
	&ui_form_end();

}
print '<script type="text/javascript">
			var nameElem = document.getElementById("multiselect_add");
			function addAClass(e) {
				document.getElementById("new_btn").style.visibility = "hidden";
				document.getElementById("new_box").style.visibility = "visible";
				document.getElementById("new_class").focus();
			}
			var addBtn = document.getElementById("multiselect_submit");
			function addIt(e) {
				document.getElementById("new_box").style.visibility = "hidden";
				var myval = document.getElementById("new_class").value;
				var opt = document.createElement("option");
				opt.value = myval;
				opt.innerHTML = myval;
				document.getElementById("classes[]_vals").appendChild(opt);
				document.getElementById("new_btn").style.visibility = "visible";
			}
			if ( nameElem.addEventListener ) {	nameElem.addEventListener("click", addAClass, false);
			} else if ( nameElem.attachEvent ) {	nameElem.attachEvent("onclick", addAClass);	}
			if ( addBtn.addEventListener ) {	addBtn.addEventListener("click", addIt, false);
			} else if ( addBtn.attachEvent ) {	addBtn.attachEvent("onclick", addIt);	}
	</script>'. "\n";

&ui_print_footer ("$return", $text{'index_short'});	# click to return
