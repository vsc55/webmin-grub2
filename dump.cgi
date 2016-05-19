#!/usr/local/bin/perl
# commands.cgi
# Manage GRUB2

require './grub2-lib.pl';
&ReadParse();

use limit;	# limit virtual memory allocation
use Config::IniFiles;

our @returnHere = (	&this_url(), $text{'tab_dump'}	);
#my $head = 	'<meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' \'unsafe-inline\';
#	script-src \'self\' \'unsafe-inline\' \'unsafe-eval\'
#	*.'. $ENV{"HTTP_HOST"}. ' http';
#$head.=	($ENV{"SERVER_PORT"}==443) ? "s" : "";
#$head.=	'://'. $ENV{"SERVER_NAME"}. ':'. $ENV{"SERVER_PORT"}. ' https://ajax.googleapis.com">'. "\n";

# Page header
&ui_print_header (undef, "$text{'index_title'} - $text{'tab_dump'}", "", undef, 1, 1, undef,
				 &returnto ("javascript: history.go(-1)", $text{'prev'}), #$head.
	'<link rel="stylesheet" type="text/css" href="css/grub2.css">'. "\n", undef,
	&text ('index_version', $version));
#if (!%grub2cfg) {
#	print $text{'index_either'}.' '.
#		&text ('index_modify', "$gconfig{'webprefix'}${dir_sep}config.cgi?$module_name").' '.
#		$text{'index_install'}.' '.
#		&text ('index_mkconfig', "make_cfg.cgi");
#}
my %fdiskhash = &fdiskhash();
my %divide = &divide_cfg_lines();
my $prevparent = 1;
my %hash;
my @array;
foreach $key (sort {$a <=> $b} keys %divide) {
	#if ($key>1 && $divide{$key}{'parent'}==$prevparent) {
	#if ($divide{$key}{'parent'}==$prevparent) {
		if ($divide{$key}{'type'}eq"comment") {
			push( @{ $hash{$prevparent}{'content'} }, ' '. $divide{$key}{'more'});
			#$hash{$prevparent} = $hash{$prevparent}. ' '. $divide{$key}{'more'};
		} elsif ($divide{$key}{'type'}eq"if") {
			push( @{ $hash{$prevparent}{'content'} }, ' '. $divide{$key}{'more'});
			#$hash{$prevparent} = $hash{$prevparent}. ' '. $divide{$key}{'more'};
		} else {
			push( @{ $hash{$prevparent}{'content'} }, ' '. $divide{$key}{'content'});
			#$hash{$prevparent} = $hash{$prevparent}. ' '. $divide{$key}{'content'};
		}
	#}
	#} else {
	#	$hash{$prevparent} = $divide{$key}{'content'};
	#}
	#print "$prevparent: ". Dumper ($hash{$prevparent}). "<br />";
	$prevparent = $divide{$key}{'parent'};
}
print "hash_divide:". Dumper(%hash). "|||<br />\n";
foreach $key (sort {$a <=> $b} keys %divide) {
	print "$key: ". Dumper ($divide{$key}). "<br />";
}
	#print "hash_fdiskhash:". Dumper(%fdiskhash). "|||<br />\n";
	#print "hash_grub2cfg:". Dumper(\%grub2cfg). "|||<br />\n";
print &ui_hr();

&ui_print_footer ($return, $text{'index_main'});	# click to return
