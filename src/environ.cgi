#!/usr/local/bin/perl
# environ.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_environ'}	);
#my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
#	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
#	*.'. $ENV{"HTTP_HOST"}. ' http';
#$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
#$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

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
			#$jsHTML4combo.= '<script type="text/javascript">
			#	function comboInit(thelist)
			#	{
			#		theinput = document.getElementById(theinput);  
			#		var idx = thelist.selectedIndex;
			#		var content = thelist.options[idx].innerHTML;
			#		if (theinput.value == "")
			#			theinput.value = content;	
			#	}
			#	function combo(thelist, theinput)
			#	{
			#		theinput = document.getElementById(theinput);  
			#		var idx = thelist.selectedIndex;
			#		var content = thelist.options[idx].innerHTML;
			#		theinput.value = content;	
			#	}
			#	</script>';
    push (@links, &select_all_link("sel"), &select_invert_link("sel"));
    print &ui_form_start ("do_env.cgi", "get");
    print &ui_links_row (\@links);
    print &ui_columns_start([
		$text{'select'},
		$text{'var'},
		&text ('env_was', ''),
		$text{'val'} ],	100);
	for my $a (keys %grub2def) {
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
			my $string = '<select title="'.$text{'env_select'}.'" name="'.$a.'">'."\n";
			for my $opt (@options) {
				$string.= '<option value="'.$opt.'"';
				$string.= ' selected="selected"' if $opt eq $env_setts{lc $a}{'default'};
				$string.= '>'.$opt.'</option>'."\n";
			}
			$string.= '</select>'. "\n";
			push (@cols, $string);
		} elsif ($env_setts{lc $a}{'type'} eq "filterselect") {
			my $value = $grub2def{$a};
			$value =~ s/\"/\'/g;
			my $string;
			our $string2;
			$string2.= '<script type="text/javascript">'. "\n\t". 'var Select_Data = {';
			$string.= '<select id="selfilter_'.$a.'" title="'.$text{'env_filter'}.'" name="selfilter" placeholder="Filter by:">'."\n";#value="'.$value.'"  type="'. $env_setts{lc $a}{'type'}. '"
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
								#if ($i!=0) {	$string2.= ', ';	}
								$string2.= '["'. $grub2cfg{$op}{$op2}{'name'}. '", "'. $grub2cfg{$op}{$op2}{'name'}. '"], ';
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
								#if ($i!=0) {	$string2.= ', ';	}
								$string2.= '["'. $grub2cfg{$op}{$op2}{'name'}. '", "'. $op. '>'. $op2. '"], ';
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
					$string2.= "\"] ]";
					$i++;
				}
			}
			$string.= '</select>'. "\n". '<select name="'.$a.'" title="'.$text{'env_select'}.'" id="choices"> <!-- populated using JavaScript --> </select>';
			$string2.= "\n\t\t};
	function fillChoices(e) {
		choices.options.length = 0; // clear out existing items
		for (var i=0; i < Select_Data[selfilter.value].length; i++) {
			var d = Select_Data[selfilter.value][i];
			choices.options.add(new Option(d[0], d[1]));
		}
	}
	function hiddenChoice(e) {
		var input = document.createElement('input');
		input.type = 'hidden';
		input.name = '".$a."_name';
		input.value = choices.options[choices.selectedIndex].text;
		document.forms[0].appendChild(input);
	}
	/*window.onload = function () {*/
		var choices = document.getElementById('choices');
		if (choices) {
			if (choices.addEventListener) {	choices.addEventListener('change', hiddenChoice, false);
			} else if (choices.attachEvent) {	choices.attachEvent('onchange', hiddenChoice);	}
		}
		var selfilter = document.getElementById('selfilter_".$a."');
		if (selfilter) {
			if (selfilter.addEventListener) {	selfilter.addEventListener('change', fillChoices, false);
			} else if (selfilter.attachEvent) {	selfilter.attachEvent('onchange', fillChoices);	}
			fillChoices();
		}
	/*}*/";
			$string2.= '</script>'. "\n";
			push (@cols, $string);
		} elsif ($env_setts{lc $a}{'type'} eq "combo") {	# HTML 5
			my $value = $grub2def{$a};
			$value =~ s/\"/\'/g;
			my $string;
			$string.= '<input type="text" size="80" value="'.$value.'" title="'.$text{'combo_all'}.'" list="mylist" id="input_'.$a.'" name="'.$a.'" />'."\n";# value="'.$value.'"
			$string.= '<img id="img_'.$a.'" src="images/clear.png" alt="'.$text{'clear'}.'" />';#onclick="javascript:document.getElementById("input_'.$a.'").value=\'\'" 
			$string.= '<script type="text/javascript">
			var nameElement = document.getElementById("img_'.$a.'");
			function nameClear(e) {
				document.getElementById("input_'.$a.'").value=\'\';
				document.getElementById("input_'.$a.'").placeholder=\''.$text{'combo_all'}.'\';
			}
			window.onload = function () {
				if ( nameElement.addEventListener ) {	nameElement.addEventListener("click", nameClear, false);
				} else if ( nameElement.attachEvent ) {	nameElement.attachEvent("onclick", nameClear);	}
			}
			</script>';
			$string.= '<datalist id="mylist">'."\n";	# HTML 5
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
	print $string2;
	#print 	'<div id="new_btn">'.
	#			&ui_button ("$text{'add'} $text{'var'}", "newvar_add").
	#		'</div>'.
	#		'<div id="new_box" style="visibility: hidden">'.
	#			'<label for="new_var">'.$text{'env_newvar'}.'</label>'.
	#			&ui_textbox ("new_var", "", 30, 0, undef).
	#			&ui_button ($text{'env_submit'}, "newvar_submit", 0).
	#			&ui_button ($text{'cancel'}, "newvar_cancel", 0).
	#		'</div>';
	#print '<script type="text/javascript">
	#			function addAvar(e) {
	#				document.getElementById("new_btn").style.visibility = "hidden";
	#				document.getElementById("new_box").style.visibility = "visible";
	#				document.getElementById("new_var").focus();
	#			}
	#			function getAllSiblings(elem, filter) {
	#				var sibs = [];
	#				elem = elem.parentNode.firstChild;
	#				do {
	#					if (!filter || filter(elem)) sibs.push(elem);
	#				} while (elem = elem.nextSibling)
	#				return sibs;
	#			}
	#			function exampleFilter(elem) {
	#				switch (elem.nodeName.toUpperCase()) {
	#					case "DIV":
	#						return true;
	#					/*case "SPAN":
	#						return true;*/
	#					default:
	#						return false;
	#				}
	#			}
	#			function addItVar(e) {
	#				var myval = document.getElementById("new_var").value;
	#				/*var i = getAllSiblings (document.getElementById ("sortableTableNaN"), exampleFilter).length;*	find a <tr>	*/
	#				var tr = document.createElement("tr");
	#				tr.id = "row_sel_"+ myval;
	#				tr.bgcolor = "#f5f5f5";
	#				tr.class = "row"+ i+ "ui_checked_columns mainbody";
	#				tr.onMouseOver="this.className = document.getElementById(\'sel_"+ myval+ "\').checked ? \'mainhighsel\' : \'mainhigh\'";/****/
	#				tr.onMouseOut="this.className = document.getElementById(\'sel_"+ myval+ "\').checked ? \'mainsel\' : \'mainbody row"+ i+ "\'";/****/
	#				var td = document.createElement("td");
	#				td.class="ui_checked_checkbox";
	#				var input = document.createElement("input");
	#				input.class="ui_checkbox";
	#				input.type="checkbox";
	#				input.name="sel";
	#				input.id="sel_"+ myval;
	#				input.onclick="document.getElementById(\'row_sel_"+ myval+ "\').className = this.checked ? \'mainhighsel\' : \'mainhigh\';";/****/
	#				var td2 = document.createElement("td");
	#				var label = document.createElement("label");
	#				labal.for="sel_"+ myval;
	#				var label2 = document.createElement("label");
	#				var span = document.createElement("span");
	#				span.title="";/****/
	#				span.innerHTML=myval;
	#				/*span.value=myval;*/
	#				var td3 = document.createElement("td");
	#				var label2 = document.createElement("label");
	#				label2.for="sel_"+ myval;
	#				label2.innerHTML="";
	#				var td4 = document.createElement("td");
	#				var input2 = document.createElement("input");
	#				input2.type="text";/****/
	#				input2.name=myval;
	#				input2.size=80;
	#				td4.appendChild(input2);
	#				td3.appendChild(label2);
	#				label.appendChild(span);
	#				td2.appendChild(label);
	#				td.appendChild(input);
	#				tr.appendChild(td);
	#				tr.appendChild(td2);
	#				tr.appendChild(td3);
	#				tr.appendChild(td4);
	#				/*document.getElementById ("sortableTableNaN").appendChild(tr);*//*	add to <tbody>	*	class: ui_table sortable ui_columns	*/
	#				revertVar(e);
	#			}
	#			function revertVar(e) {
	#				document.getElementById("new_box").style.visibility = "hidden";
	#				document.getElementById("new_btn").style.visibility = "visible";
	#			}
	#			window.onload = function () {
	#				var nameElem = document.getElementById("newvar_add");
	#				/*if (nameElem) {*/
	#					if (nameElem.addEventListener) {	nameElem.addEventListener("click", addAvar, false);
	#					} else if (nameElem.attachEvent) {	nameElem.attachEvent("onclick", addAvar);	}
	#				/*}*/
	#				var addnewvarBtn = document.getElementById("newvar_submit");
	#				/*if (addnewvarBtn) {*/
	#					if (addnewvarBtn.addEventListener) {	addnewvarBtn.addEventListener("click", addItVar, false);
	#					} else if (addnewvarBtn.attachEvent) {	addnewvarBtn.attachEvent("onclick", addItVar);	}
	#				/*}*/
	#				var cancelVar = document.getElementById("newvar_cancel");
	#				/*if (cancelVar) {*/
	#					if (cancelVar.addEventListener) {	cancelVar.addEventListener("click", revertVar, false);
	#					} else if (cancelVar.attachEvent) {	cancelVar.attachEvent("onclick", revertVar);	}
	#				/*}*/
	#				document.onkeydown = function(e) {	/*	activate when key is pressed	*/
	#					var e = e || window.event;
	#					var node = e.target || e.srcElement || e.currentTarget;
	#					var keycode = e.keyCode || e.which;
	#					switch (keycode) {
	#						case 13:	/*	ENTER key	*/
	#							if (node === nameElem || node === document.getElementById("new_var")) {
	#								addItVar();
	#								return false;
	#							}
	#						case 27:	/*	ESCAPE key	*/
	#							if (node === nameElem || node === document.getElementById("new_var")) {
	#								revertVar();
	#								return false;
	#							}
	#					}
	#				}
	#			}
	#	</script>'. "\n";
	print &ui_hr();
	print $text{'add_env'}, &ui_hr();
&ui_print_footer ($return, $text{'index_main'});	# click to return
