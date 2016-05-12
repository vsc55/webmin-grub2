#!/usr/bin/perl
# edit.cgi
# edit the GRUB2 menuentry

require './grub2-lib.pl';
&ReadParse();

my $sb = $in{'sub'};
my $i = $in{'item'};
my $heading = ($sb+$i) ? $text{'edit'} : $text{'add'};

&ui_print_header (	$text{'index_title'}, "$heading $text{'menuentry'}", "", undef, undef, undef, undef, undef,
				  '<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n"	);

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
					'&nbsp;('.&text ('env_was', "").': '.
					(($grub2cfg{$sb}{$i}{'is_saved'}==1) ? $text{'checked'} : $text{'unchecked'}).')',
					($grub2cfg{$sb}{$i}{'is_saved'}==1)));
# submenu:
			my $value = $grub2cfg{$sb}{'name'};
			my $string = '<input type="text" name="entry_menu" size="80" value="'.$value.'" placeholder="'.$text{'combo_all'}.'" id="input_entry_menu" list="mylist" style="vertical-align: super;" />'."\n";
			$string.= '<img id="img_entry_menu" src="images/clear.png" alt="'.$text{'clear'}.'" />'."\n";
			$string.= '&nbsp;('.&text ('env_was', ""). ': "'. $grub2cfg{$sb}{'name'}. '")';
			$string.= '<script type="text/javascript">
			var nameElement = document.getElementById("img_entry_menu");
			function nameClear(e) {
				document.getElementById("input_entry_menu").value=\'\';
				document.getElementById("input_entry_menu").placeholder=\''.$text{'combo_all'}.'\';
			}
			if (nameElement) {
				if (nameElement.addEventListener) {	nameElement.addEventListener("click", nameClear, false);
				} else if (nameElement.attachEvent) {	nameElement.attachEvent("onclick", nameClear);	}
			}
			</script>'."\n";
			$string.= '<datalist id="mylist">'. "\n";
			for my $sb (keys %grub2cfg) {
				$string.= "\t". '<option';
				$string.= ' value="'. $grub2cfg{$sb}{'name'}. '"';#$grub2cfg{$sb}{'index'}. '"';
				#$string.= ' selected id="selected"' if $grub2cfg{$sb}{'name'} eq $env_setts{lc $a}{'default'};
				$string.= '> ';
#				$string.= $grub2cfg{$sb}{'name'}. "\n";
			}
			$string.= '</datalist>'. "\n";
			print &ui_table_row ($text{'edit_submenu'}, $string);
# option classes:
			my @array = keys %{{ map{$_=>1} @classList }};	# erase all non-unique elements
			@array = map {	[	$_, $_	]	} @array;	# duplicate value, desc.
			my @seld = map {	[	$_, $_	]	} @{ $grub2cfg{$sb}{$i}{'classes'} };#sort { $a cmp $b }
			print &ui_table_row ($text{'edit_class'},#$text{'entry_classes'},
								 &ui_multi_select ("classes[]", \@seld, \@array, 7, 1, 0,
												   "<span style=\"text-align: right\">($text{'edit_selboxhead'})</span>",
												   "<span style=\"text-align: right\">($text{'edit_seldboxhead'})</span>").
								 '<div id="new_btn">'.
									&ui_button ("$text{'add'} $text{'edit_class'}", "multiselect_add").
								 '</div>'.
								 '<div id="new_box" style="visibility: hidden">'.
									#&ui_table_row ($text{'edit_new_class'},
									'<label for="new_class">'.$text{'edit_new_class'}.'</label>'.
										&ui_textbox ("new_class", "", 30, 0, undef).
										&ui_button ($text{'edit_submit'}, "multiselect_submit", 0).
										&ui_button ($text{'cancel'}, "multiselect_cancel", 0).
								 '</div>'
			);
# option variables:
		my $cnt = 0;
		for $v (keys %{ $grub2cfg{$sb}{$i}{'opts_vars'} }) {	# existing vars
			print &ui_table_row (($cnt==0) ? $text{'edit_optvar'} : '',
								'<div id="optvarRow' .$cnt. '">'.
				&ui_textbox ("optvar$cnt", $v, 25, 0, undef). " = ".
				&ui_textbox ("optval$cnt", $grub2cfg{$sb}{$i}{'opts_vars'}{$v}, 80, 0, undef).
				&ui_button ($text{'edit_deleteVar'}, "delete_optvar$cnt", 0, 'class="delete_optvar"').
								'</div>');
			$cnt++;
		}
		print &ui_table_row ("",	# add a new option variable
							'<div id="new_btn_optvar">'.
								&ui_button ("$text{'add'} $text{'edit_optvar'}", "optvar_add").
							'</div>'.
							'<div id="new_box_optvar" style="visibility: hidden">'.
								'<label for="new_optvar">'.$text{'edit_new_optvar'}.'</label>'.
								&ui_textbox ("new_optvar", "", 30, 0, undef).
								&ui_button ($text{'edit_submit'}, "optvar_submit", 0).
								&ui_button ($text{'cancel'}, "optvar_cancel", 0).
							'</div>');
# protection:
			print &ui_table_row ($text{'edit_protect'},
				&ui_checkbox ("protectit", ($grub2cfg{$sb}{$i}{'protected'}eq"true"),
					'&nbsp;('.&text ('env_was', "").': '.
					(($grub2cfg{$sb}{$i}{'protected'}eq"true") ? $text{'checked'} : $text{'unchecked'}).')',
					($grub2cfg{$sb}{$i}{'protected'}eq"true")));
# option conditions:
		if ($grub2cfg{$sb}{$i}{'opts_if'}) {
			my $cntoif = 0;
			for $v (@{ $grub2cfg{$sb}{$i}{'opts_if'} }) {
				print &ui_table_row (($cntoif==0) ? $text{'edit_opts_if'} : '',
					&ui_textbox ("opts_if", $v, 25, 0, undef).
					&ui_button ($text{'delete'}, "delete_opts_if$cntoif"));
				$cntoif++;
			}
		}
# option sets:
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
# submenu:
			my $string = '<input type="text" name="entry_menu" size="80" value="" placeholder="'.$text{'combo_all'}.'" id="input_entry_menu" list="mylist" />'."\n";
			$string.= '<img id="img_entry_menu" src="images/clear.png" alt="'.$text{'clear'}.'" />'."\n";
			$string.= '<script type="text/javascript">
			var nameElement = document.getElementById("img_entry_menu");
			function nameClear(e) {
				document.getElementById("input_entry_menu").value=\'\';
				document.getElementById("input_entry_menu").placeholder=\''.$text{'combo_all'}.'\';
			}
			if (nameElement) {
				if (nameElement.addEventListener) {	nameElement.addEventListener("click", nameClear, false);
				} else if (nameElement.attachEvent) {	nameElement.attachEvent("onclick", nameClear);	}
			}
			</script>'."\n";
			$string.= '<datalist id="mylist">'. "\n";
			for my $sb (keys %grub2cfg) {
				$string.= "\t". '<option';
				$string.= ' value="'. $grub2cfg{$sb}{'name'}. '"';#$grub2cfg{$sb}{'index'}. '"';
				#$string.= ' selected id="selected"' if $grub2cfg{$sb}{'name'} eq $env_setts{lc $a}{'default'};
				$string.= '> ';
#				$string.= $grub2cfg{$sb}{'name'}. "\n";
			}
			$string.= '</datalist>'. "\n";
			print &ui_table_row ($text{'edit_submenu'}, $string);
# option classes:
			my @array = keys %{{ map{$_=>1} @classList }};	# existing classes
			print &ui_table_row ($text{'entry_classes'},	# add a new class
								 &ui_multi_select ("classes[]", \@seld, \@array, 7, 1, 0,
												   "<span style=\"text-align: right\">($text{'edit_selboxhead'})</span>",
												   "<span style=\"text-align: right\">($text{'edit_seldboxhead'})</span>").
								 '<div id="new_btn">'.
									&ui_button ("$text{'add'} $text{'edit_class'}", "multiselect_add").
								 '</div>'.
								 '<div id="new_box" style="visibility: hidden">'.
									'<label for="new_class">'.$text{'edit_new_class'}.'</label>'.
									&ui_textbox ("new_class", "", 30, 0, undef).
									&ui_button ($text{'edit_submit'}, "multiselect_submit", 0).
									&ui_button ($text{'cancel'}, "multiselect_cancel", 0).
								 '</div>'
			);
# option variables:
			my $cnt = 0;
			for $v (keys %{ $grub2cfg{$sb}{$i}{'opts_vars'} }) {	# existing vars
				print &ui_table_row (($cnt==0) ? $text{'edit_optvar'} : '',
								'<div id="optvarRow' .$cnt. '">'.
					&ui_textbox ("optvar$cnt", $v, 25, 0, undef). " = ".
					&ui_textbox ("optval$cnt", $grub2cfg{$sb}{$i}{'opts_vars'}{$v}, 80, 0, undef).
					&ui_button ($text{'delete'}, "delete_optvar$cnt").
#					&ui_button ($text{'cancel'}, "cancel_optvar$cnt")
								'</div>');
				$cnt++;
			}
			print &ui_table_row ($text{'edit_optvar'},	# add new option variable
							'<div id="new_btn_optvar">'.
								&ui_button ("$text{'add'} $text{'edit_optvar'}", "optvar_add").
							'</div>'.
							'<div id="new_box_optvar" style="visibility: hidden">'.
								'<label for="new_optvar">'.$text{'edit_new_optvar'}.'</label>'.
								&ui_textbox ("new_optvar", "", 30, 0, undef).
								&ui_button ($text{'edit_submit'}, "optvar_submit", 0).
								&ui_button ($text{'cancel'}, "optvar_cancel", 0).
							'</div>');
# protection:
			print &ui_table_row ($text{'edit_protect'},
				&ui_checkbox ("protectit", $protected));
		print &ui_table_end(),
		&ui_submit ($text{'save'}, "save"),
		&ui_submit ($text{'cancel'}, "cancel"),
	&ui_form_end();

}
# javascript:
print '<script type="text/javascript">
			function addAClass(e) {
				document.getElementById("new_btn").style.visibility = "hidden";
				document.getElementById("new_box").style.visibility = "visible";
				document.getElementById("new_class").focus();
			}
			function addIt(e) {
				var myval = document.getElementById("new_class").value;
				var opt = document.createElement("option");
				opt.value = myval;
				opt.innerHTML = myval;
				document.getElementById("classes[]_opts").appendChild(opt);
				revertClass(e);
			}
			function revertClass(e) {
				document.getElementById("new_box").style.visibility = "hidden";
				document.getElementById("new_btn").style.visibility = "visible";
			}
			var nameElem = document.getElementById("multiselect_add");
			if (nameElem) {
				if (nameElem.addEventListener) {	nameElem.addEventListener("click", addAClass, false);
				} else if (nameElem.attachEvent) {	nameElem.attachEvent("onclick", addAClass);	}
			}
			var addBtn = document.getElementById("multiselect_submit");
			if (addBtn) {
				if (addBtn.addEventListener) {	addBtn.addEventListener("click", addIt, false);
				} else if (addBtn.attachEvent) {	addBtn.attachEvent("onclick", addIt);	}
			}
			var cancelClass = document.getElementById("multiselect_cancel");
			if (cancelClass) {
				if (cancelClass.addEventListener) {	cancelClass.addEventListener("click", revertClass, false);
				} else if (cancelClass.attachEvent) {	cancelClass.attachEvent("onclick", revertClass);	}
			}
	</script>'. "\n";
print '<script type="text/javascript">
			function addAoptvar(e) {
				document.getElementById("new_btn_optvar").style.visibility = "hidden";
				document.getElementById("new_box_optvar").style.visibility = "visible";
				document.getElementById("new_optvar").focus();
			}
			function addItoptvar(e) {
				var myval = document.getElementById("new_optvar").value;
				var div = document.createElement("div");
				var input = document.createElement("input");
				var text = document.createTextNode (" = ");
				var input2 = document.createElement("input");
				var button = document.createElement("input");
				var i = getAllSiblings (document.getElementById ("optvarRow0"), exampleFilter).length;
				div.id = "optvarRow"+ i;
				input.type = "text";
				input.id = "optvar"+i;
				input.size = 25;
				input.value = myval;
				input.name = "optvarname" +i;
				/*input.className = "css-class-name";*/
				input2.type = "text";
				input2.id = "optval" +i;
				input2.size = 80;
				input2.value = "";
				button.type = "button";
				button.id = "delete_optvar" +i;
				button.value = "'.$text{'edit_deleteVar'}.'";
				div.appendChild (input);
				div.appendChild (text);
				div.appendChild (input2);
				div.appendChild (button);
				document.getElementById("optvarRow0").parentNode.appendChild(div);
				revertOptVar(e);
			}
			function revertOptVar(e) {
				document.getElementById("new_box_optvar").style.visibility = "hidden";
				document.getElementById("new_btn_optvar").style.visibility = "visible";
			}
			function getAllSiblings(elem, filter) {
				var sibs = [];
				elem = elem.parentNode.firstChild;
				do {
					if (!filter || filter(elem)) sibs.push(elem);
				} while (elem = elem.nextSibling)
				return sibs;
			}
			function exampleFilter(elem) {
				switch (elem.nodeName.toUpperCase()) {
					case "DIV":
						return true;
					/*case "SPAN":
						return true;*/
					default:
						return false;
				}
			}
			var nameElemoptvar = document.getElementById("optvar_add");
			if (nameElemoptvar) {
				if (nameElemoptvar.addEventListener) {	nameElemoptvar.addEventListener("click", addAoptvar, false);
				} else if (nameElemoptvar.attachEvent) {	nameElemoptvar.attachEvent("onclick", addAoptvar);	}
			}
/*			var optvarDel = document.getElementById("delete_optvar0");
			if (optvarDel) {
				if (nameElemoptvar.addEventListener) {	nameElemoptvar.addEventListener("click", addAoptvar, false);
				} else if (nameElemoptvar.attachEvent) {	nameElemoptvar.attachEvent("onclick", addAoptvar);	}
			}*/
			var addBtnoptvar = document.getElementById("optvar_submit");
			if (addBtnoptvar) {
				if (addBtnoptvar.addEventListener) {	addBtnoptvar.addEventListener("click", addItoptvar, false);
				} else if (addBtnoptvar.attachEvent) {	addBtnoptvar.attachEvent("onclick", addItoptvar);	}
			}
			var cancelOptVar = document.getElementById("optvar_cancel");
			if (cancelOptVar) {
				if (cancelOptVar.addEventListener) {	cancelOptVar.addEventListener("click", revertOptVar, false);
				} else if (cancelOptVar.attachEvent) {	cancelOptVar.attachEvent("onclick", revertOptVar);	}
			}
			document.onkeydown = function(e) {	/*	activate when key is pressed	*/
				var e = e || window.event;
				var node = e.target || e.srcElement || e.currentTarget;
				var keycode = e.keyCode || e.which;
				switch (keycode) {
					case 13:	/*	ENTER key	*/
						if (node === nameElem || node === document.getElementById("new_class")) {
							addIt();
							return false;
						}
						if (node === nameElemoptvar || node === document.getElementById("new_optvar")) {
							addItoptvar();
							return false;
						}
					case 27:	/*	ESCAPE key	*/
						if (node === nameElem || node === document.getElementById("new_class")) {
							revertClass();
							return false;
						}
						if (node === nameElemoptvar || node === document.getElementById("new_optvar")) {
							revertOptVar();
							return false;
						}
				}
			}
	</script>'. "\n";

&ui_print_footer ("$return", $text{'index_short'});	# click to return
