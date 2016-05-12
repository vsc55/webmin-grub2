#!/usr/bin/perl
# edit_file_save.cgi
# Save edited file contents

require './grub2-lib.pl';
&ReadParseMime();

my $file = $in{'name'};

&lock_file($file);
$temp = &transname();
&copy_source_dest($file, $temp);
$in{'content'} =~ s/\r//g;
$in{'content'} =~ s/\s+$//;
@dirs = split(/\n/, $in{'content'});
$lref = &read_file_lines($file);
if (!defined($start)) {
	$start = 0;
	$end = @$lref - 1;
	}
splice(@$lref, $start, $end-$start+1, @dirs);
&flush_file_lines();
if ($config{'test_manual'}) {
	$err = &test_config();
	if ($err) {
		&copy_source_dest($temp, $file);
		&error(&text('manual_etest', "<pre>$err</pre>"));
		}
}
unlink($temp);
&unlock_file($file);
&webmin_log($logtype, "manual", $logname, \%in);

&redirect($return, $text{'index_short'});
