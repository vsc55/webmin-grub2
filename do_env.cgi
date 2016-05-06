#!/usr/bin/perl
# edit_env.cgi
# Edit a GRUB2 environment setting

require './grub2-lib.pl';
&ReadParse();

#if ($in{'edit'}) {
#	my @all = split /\&was=/, $in{'sel'};	# manually separate post var, was
#	my $var = $all[0];
#	my $was = $all[1];
#	
#	&ui_print_header($title, "$text{'env_edit'} $text{'env_var'} \"$var\"", "");
#	print "$text{'env_edit'} $text{'env_var'} <tt>$var</tt>", "<p>\n";
#	
#	# textbox form
#	print &ui_form_start("edit_save.cgi", "form-data");
#		print &ui_hidden("was", $was), "\n",
#			&text('env_was', $was),
#			&ui_textbox("val", $val, 50),
#			&ui_submit($text{'save'});
#	print &ui_form_end();
#	
#	&ui_print_footer("$return", $text{'index_short'});	# click to return
if ($in{'comment'}) {
	#code
} elsif ($in{'delete'}) {
	#code
} else {
	&redirect("");	# just retrurn
}