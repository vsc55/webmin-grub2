#!/usr/bin/perl
# do_entry.cgi
# Display a text box for manually editing directives

require './nginx-lib.pl';
&ReadParse();
=was
my $file = "$server_root/$config{'virt_dir'}/$in{'editfile'}";
if (!-e $file) {
  $file = "$server_root/$in{'editfile'}";
}
=cut
&ui_print_header($title, $text{'manual_title'}, "");
print &text('manual_header', "<tt>$file</tt>"),"<p>\n";
print %in;

=was2
# textbox form
print &ui_form_start("edit_file_save.cgi", "form-data");
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

&ui_print_footer("$return", "server listing");
