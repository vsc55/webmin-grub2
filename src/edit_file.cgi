#!/usr/bin/perl
# edit_file.cgi
# Display a text box for manually editing a configuration file

require './grub2-lib.pl';
&ReadParse();

my $file = "$config{'cfgd_dir'}$dir_sep$in{'name'}";
#if (!-e $file) {
#  $file = "$server_root/$in{'editfile'}";
#}

&ui_print_header ($title, $text{'manual_title'}, "", undef, undef, undef, undef, &returnto ("javascript: history.go(-1)", $text{'prev'}));
print &text ('manual_header', "<tt>$file</tt>"), "<p>\n";
#print %in;

# textbox form
print &ui_form_start ("edit_file_save.cgi", "form-data");
print &ui_hidden ("name", $file),"\n";

$lref = &read_file_lines($file);
if (!defined($start)) {
	$start = 0;
	$end = @$lref - 1;
	}
for($i=$start; $i<=$end; $i++) {
	$buf .= $lref->[$i]."\n";
	}
print &ui_textarea ("content", $buf, 25, 80, undef, undef, "style='width:100%'"), "<br>\n";
print &ui_submit ($text{'save'});
print &ui_form_end(), &ui_hr();

&ui_print_footer($return, $text{'index_main'});
