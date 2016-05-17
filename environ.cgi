#!/usr/local/bin/perl
# environ.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_environ'}	);
my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
	*.'. $ENV{"HTTP_HOST"}. ' http';
$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_environ'}", "", undef, 1, 1, undef,
				  &returnto ("javascript: history.go(-1)", $text{'prev'}),
				 #$head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
if (!%grub2cfg) {
	print $text{'index_either'}.' '.
		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
		$text{'index_install'}.' '.
		&text ('index_mkconfig', "make_cfg.cgi");
}
#print "env_setts:". Dumper (%env_setts). "||||";

	my %grub2def = &get_grub2_def();
	my %grub2env = &get_grub2_env();
    for my $a (keys %grub2env) {
	    if ($grub2env{$a} && $a) {
			$grub2def{$a} = $grub2env{$a};
		}
	}
	
#	print "grub2def is".Dumper (%grub2def)."||||<br />\n";
#	print "env_setts is".Dumper (%env_setts)."||||<br />\n";
#	print "cmds is".Dumper (%cmds)."||||<br />\n";
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
    push (@links, &select_all_link("sel"), &select_invert_link("sel"));
    print &ui_form_start ("do_env.cgi", "get");
    print &ui_links_row (\@links);
    print &ui_columns_start([
		$text{'select'},
		$text{'var'},
		&text ('env_was', ''),
		$text{'val'} ],	100);
	for my $a (keys %grub2def) {
		#$a = lc $a;
		my @cols;
##	    push(@cols, "<a class=\"del\" href=\"delenv.cgi\">$text{'del'}</a>".
##		push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$_</a>");
		push (@cols, '<span title="'.$env_setts{lc $a}{'desc'}.'">'.$a.'</span>');
##		push (@cols, "<a href=\"do_env.cgi?var=".&urlize($_)."&amp;was=".&urlize($grub2env{$_}."&edit=Edit")."\">$grub2env{$_}</a>");
		push (@cols, $grub2def{$a});
		#print "type:". $env_setts{lc $a}{'type'}. "|||<br />\n";
		#print "opts:". $env_setts{lc $a}{'options'}. "|||<br />\n";
		my @options = split /,\s*/, $env_setts{lc $a}{'options'};
		if ($env_setts{lc $a}{'type'} eq "select" && $env_setts{lc $a}{'options'}) {
			my $string = '<select name="'.$a.'">'."\n";
			for my $opt (@options) {
				$string.= '<option value="'.$opt.'"';
				$string.= ' selected="selected"' if $opt eq $env_setts{lc $a}{'default'};
				$string.= '>'.$opt.'</option>'."\n";
			}
			$string.= '</select>'. "\n";
			push (@cols, $string);
		} elsif ($env_setts{lc $a}{'type'} eq "selectselect") {
			my $value = $grub2def{$a};
			$value =~ s/\"/\'/g;
			my ($string, $string2);
			$string2.= '<script type="text/javascript">'. "\n\t". 'var Select_List_Data = {'. "\n\t\t". '"choices": {';#. "\n"
			$string.= '<select id="selgroup_'.$a.'" name="selgroup">'."\n";#value="'.$value.'" 
#			$string.= '<datalist id="mylist">'."\n";
			for my $opt (@options) {
				$string.= "\t". '<option value="'. $opt. '"';
				$string.= ' selected id="selected"' if $opt eq $env_setts{lc $a}{'default'};
				$string.= '> '. $opt. "</option>\n";
				if ($opt =~ /^\(menuentry name\)$/) {
					$string2.= ",\n\t\t\t\"". $opt. "\": \n";
					$string2.= "\t\t\t\t". '[ ';
					for my $op (keys %grub2cfg) {
						my $i = 0;
						for my $op2 (%{ $grub2cfg{$op} }) {
							if ($grub2cfg{$op}{$op2}{'valid'}==1) {
								$string2.= ', ' if $i;
								$string2.= '["'. $grub2cfg{$op}{$op2}{'name'}. '", "'. $grub2cfg{$op}{$op2}{'name'}. '"]';
								$i++;
							}
						}
					}
					$string2.= " ]";
					next;
				}
				if ($opt =~ /^\(menuentry position number\)$/) {
					$string2.= ",\n\t\t\t\"". $opt. "\": \n";
					$string2.= "\t\t\t\t". '[ ';
					for my $op (keys %grub2cfg) {
						my $i = 0;
						for my $op2 (%{ $grub2cfg{$op} }) {
							if ($grub2cfg{$op}{$op2}{'valid'}==1) {
								$string2.= ', ' if $i;
								$string2.= '["'. $grub2cfg{$op}{$op2}{'name'}. '", "'. $op. '>'. $op2. '"]';
								$i++;
							}
						}
					}
					$string2.= " ]";#\n\t\t
					next;
				} else {
					my $i = 0;
					$string2.= ',' if $i;
					$string2.= "\n\t\t\t\"". $opt. "\": \n";
					$string2.= "\t\t\t\t". '[ ["'. $opt. '", "'. $opt;
					$string2.= "\"] ]";#\n\t\t
					$i++;
				}
			}
			$string.= '</select>'. "\n". '<select name="choices" id="choices"> <!-- populated using JavaScript --> </select>';
			$string2.= "\n\t\t}\n\t}
	function fillChoices(e) {
		var relName = 'choices';
		var obj = Select_List_Data[ relName ][ this.value ];
		alert('form elems='+relList);
		alert('obj='+obj);
	}
	window.onload= function () {
		var selgroup = document.getElementById('selgroup_".$a."');
		if (selgroup.addEventListener) {	selgroup.addEventListener('change', fillChoices, false);
		} else if (selgroup.attachEvent) {	selgroup.attachEvent('onchange', fillChoices);	}
	}";
			$string2.= '</script>'. "\n";
			push (@cols, $string);
			print $string2;
		} elsif ($env_setts{lc $a}{'type'} eq "combo") {	# HTML 5
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
				document.getElementById("input_'.$a.'").placeholder=\''.$text{'combo_all'}.'\';
			}
			window.onload= function () {
				if ( nameElement.addEventListener ) {	nameElement.addEventListener("click", nameClear, false);
				} else if ( nameElement.attachEvent ) {	nameElement.attachEvent("onclick", nameClear);	}
			}
			</script>';
			#$string.= '<script language="JavaScript">'."\n\t".'document.getElementById("selected").defaultSelected = true;'."\n".'</script>'."\n";
			$string.= '<datalist id="mylist">'."\n";	# HTML 5
			#$string.= "<select name=\"".$grub2def{$a}."\" onchange=\"combo(this, '".$grub2def{$a}."')\" onmouseout=\"comboInit(this, '".$grub2def{$a}."')\" >";	# HTML 4~
			for my $opt (@options) {
				if ($opt =~ /^<menuentry name>$/) {
					for my $op (keys %grub2cfg) {
						for my $op2 (%{ $grub2cfg{$op} }) {
							if ($grub2cfg{$op}{$op2}{'valid'}==1) {
								$string.= "\t".'<option';
								$string.= ' value="'.$grub2cfg{$op}{$op2}{'name'}.'"';
								$string.= ' selected id="selected"' if $grub2cfg{$op}{$op2}{'name'} eq $env_setts{lc $a}{'default'};
								$string.= '> ';
								$string.= $grub2cfg{$op}{'name'}.' > ';# if $grub2cfg{$op}{'name'};
								$string.= $grub2cfg{$op}{$op2}{'name'}."\n";
							}
						}
					}
					next;
				}
				if ($opt =~ /^<menuentry position number>$/) {
					for my $op (keys %grub2cfg) {
						for my $op2 (%{ $grub2cfg{$op} }) {
							if ($grub2cfg{$op}{$op2}{'valid'}==1) {
								$string.= "\t". '<option';
								$string.= ' value="'. $op. '>'. $op2. '"';
								$string.= ' selected id="selected"' if $grub2cfg{$op}{$op2}{'name'} eq $env_setts{lc $a}{'default'};
								$string.= '> ';
								$string.= $grub2cfg{$op}{'name'}.' > ';# if $grub2cfg{$op}{'name'};
								$string.= $grub2cfg{$op}{$op2}{'name'}. "\n";
							}
						}
					}
					next;
				} else {
					$string.= "\t". '<option';
					$string.= ' value="'. $opt. '"';
					$string.= ' selected id="selected"' if $opt eq $env_setts{lc $a}{'default'};
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
			push (@cols, '<input type="'. $env_setts{lc $a}{'type'}. '" name="'. $a. '" value="'. $string. '" size="80" />');
		}
		print &ui_checked_columns_row(\@cols, undef, "sel", "$a");#&amp;was=$grub2def{$a}");
    }
	print &ui_columns_end();
	print &ui_links_row(\@links);
	print &ui_form_end([	["delete", $text{'delete'}], ["save", $text{'save'}]	]);
	print 	'<div id="new_btn">'.
				&ui_button ("$text{'add'} $text{'var'}", "newvar_add").
			'</div>'.
			'<div id="new_box" style="visibility: hidden">'.
				'<label for="new_var">'.$text{'env_newvar'}.'</label>'.
				&ui_textbox ("new_var", "", 30, 0, undef).
				&ui_button ($text{'env_submit'}, "newvar_submit", 0).
				&ui_button ($text{'cancel'}, "newvar_cancel", 0).
			'</div>';
print '<script type="text/javascript">
			function addAvar(e) {
				document.getElementById("new_btn").style.visibility = "hidden";
				document.getElementById("new_box").style.visibility = "visible";
				document.getElementById("new_var").focus();
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
			function addItVar(e) {
				var myval = document.getElementById("new_var").value;
				/*var i = getAllSiblings (document.getElementById ("sortableTableNaN"), exampleFilter).length;*	find a <tr>	*/
				var tr = document.createElement("tr");
				tr.id = "row_sel_"+ myval;
				tr.bgcolor = "#f5f5f5";
				tr.class = "row"+ i+ "ui_checked_columns mainbody";
				tr.onMouseOver="this.className = document.getElementById(\'sel_"+ myval+ "\').checked ? \'mainhighsel\' : \'mainhigh\'";/****/
				tr.onMouseOut="this.className = document.getElementById(\'sel_"+ myval+ "\').checked ? \'mainsel\' : \'mainbody row"+ i+ "\'";/****/
				var td = document.createElement("td");
				td.class="ui_checked_checkbox";
				var input = document.createElement("input");
				input.class="ui_checkbox";
				input.type="checkbox";
				input.name="sel";
				input.id="sel_"+ myval;
				input.onclick="document.getElementById(\'row_sel_"+ myval+ "\').className = this.checked ? \'mainhighsel\' : \'mainhigh\';";/****/
				var td2 = document.createElement("td");
				var label = document.createElement("label");
				labal.for="sel_"+ myval;
				var label2 = document.createElement("label");
				var span = document.createElement("span");
				span.title="";/****/
				span.innerHTML=myval;
				/*span.value=myval;*/
				var td3 = document.createElement("td");
				var label2 = document.createElement("label");
				label2.for="sel_"+ myval;
				label2.innerHTML="";
				var td4 = document.createElement("td");
				var input2 = document.createElement("input");
				input2.type="text";/****/
				input2.name=myval;
				input2.size=80;
				td4.appendChild(input2);
				td3.appendChild(label2);
				label.appendChild(span);
				td2.appendChild(label);
				td.appendChild(input);
				tr.appendChild(td);
				tr.appendChild(td2);
				tr.appendChild(td3);
				tr.appendChild(td4);
				/*document.getElementById ("sortableTableNaN").appendChild(tr);*//*	add to <tbody>	*	class: ui_table sortable ui_columns	*/
				revertVar(e);
			}
			function revertVar(e) {
				document.getElementById("new_box").style.visibility = "hidden";
				document.getElementById("new_btn").style.visibility = "visible";
			}
			window.onload= function () {
				var nameElem = document.getElementById("newvar_add");
				if (nameElem) {
					if (nameElem.addEventListener) {	nameElem.addEventListener("click", addAvar, false);
					} else if (nameElem.attachEvent) {	nameElem.attachEvent("onclick", addAvar);	}
				}
				var addnewvarBtn = document.getElementById("newvar_submit");
				if (addnewvarBtn) {
					if (addnewvarBtn.addEventListener) {	addnewvarBtn.addEventListener("click", addItVar, false);
					} else if (addnewvarBtn.attachEvent) {	addnewvarBtn.attachEvent("onclick", addItVar);	}
				}
				var cancelVar = document.getElementById("newvar_cancel");
				if (cancelVar) {
					if (cancelVar.addEventListener) {	cancelVar.addEventListener("click", revertVar, false);
					} else if (cancelVar.attachEvent) {	cancelVar.attachEvent("onclick", revertVar);	}
				}
				document.onkeydown = function(e) {	/*	activate when key is pressed	*/
					var e = e || window.event;
					var node = e.target || e.srcElement || e.currentTarget;
					var keycode = e.keyCode || e.which;
					switch (keycode) {
						case 13:	/*	ENTER key	*/
							if (node === nameElem || node === document.getElementById("new_var")) {
								addItVar();
								return false;
							}
						case 27:	/*	ESCAPE key	*/
							if (node === nameElem || node === document.getElementById("new_var")) {
								revertVar();
								return false;
							}
					}
				}
			}
	</script>'. "\n";

#	print &ui_form_start("add_env.cgi", "post");
#	print &ui_form_end([ ["add", $text{'add'}] ]);

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
	print &ui_hr();
&ui_print_footer ($return, $text{'index_main'});	# click to return
