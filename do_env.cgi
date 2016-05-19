#!/usr/bin/perl
# edit_env.cgi
# Edit a GRUB2 environment setting

require './grub2-lib.pl';
&ReadParse();

my @array = split /\0/, $in{'sel'};
	
if ($in{'delete'}) {

	&ui_print_header ($title, "$in{'delete'} $text{'tab_environ'} $text{'var'}", "", undef, undef, undef, undef,
					  &returnto ("javascript: history.go(-1)", $text{'prev'})) if scalar (@array)==1;
	&ui_print_header ($title, "$in{'delete'} $text{'tab_environ'} $text{'vars'}", "", undef, undef, undef, undef,
					  &returnto ("javascript: history.go(-1)", $text{'prev'})) if scalar (@array)!=1;
	#	print "$text{'env_edit'} $text{'env_var'} <tt>$var</tt>", "<p>\n";
	print "in:". Dumper (%in). "|||<br /><br />\n";
	
		for my $a (@array) {
			print "deleting $a|||<br />\n";
			&remove_an_env ($a, \%grub2def);
		}
	print &ui_hr();
	&ui_print_footer ("$return", $text{'index_main'});	# click to return

} elsif ($in{'edit'}) {

#	# textbox form
#	print &ui_form_start("edit_save.cgi", "form-data");
#		print &ui_hidden("was", $was), "\n",
#			&text('env_was', $was),
#			&ui_textbox("val", $val, 50),
#			&ui_submit($text{'save'});
#	print &ui_form_end();
#	

} elsif ($in{'save'}) {

	&ui_print_header ($title, "$in{'save'} $text{'env_var'}", "", undef, undef, undef, undef, &returnto ("javascript: history.go(-1)", $text{'prev'}));
	print "in:". Dumper (%in). "|||<br /><br />\n";

		for my $a (@array) {
			print "deleting $a|||<br />\n";
			&remove_an_env ($a, \%grub2def);
		}
	print &ui_hr();
	&ui_print_footer ("$return", $text{'index_main'});	# click to return

} else {

	&ui_print_header ($title, "$in{'delete'} $text{'env_var'} \"$var\"", "", undef, undef, undef, undef,
					  &returnto ("javascript: history.go(-1)", $text{'prev'}));
	print $text{'cannot'},
	print &ui_hr();
	&redirect ($return, $text{'index_main'});	# just retrurn
}
