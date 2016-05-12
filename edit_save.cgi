#!/usr/bin/perl
# edit_save.cgi
# Save manually entered directives

require './grub2-lib.pl';
&ReadParse();

if ($in{'cancel'}) {
	&redirect ($return);#$text{'index_short'})
}

my $sb = $in{'sb'};
my $i = $in{'i'};
my $id = $in{'id'};
my $valid = $in{'valid'};
my $pos = $in{'pos'};
my $saveit = $in{'saveit'};
my $submenu = $in{'submenu'};
my $name = $in{'entry_name'};
my @classes = split /\s/, $in{'classes[]'};
#my @delete_classes = split /\0/, $in{'delete_class'};
my @users = split /\s/, $in{'users[]'};
my @optifs = split /\s/, $in{'users[]'};
my %optvar;
for (keys %in) {	# go though each posted value
	if (/^optvar(\d+)$/) {
		$optvar{$1}{'var'} = $in{"optvar$1"};	# store each variable in hash
	}
	if (/^optvals(\d+)$/) {
		$optvar{$1}{'valu'} = $in{"optvals$1"};
	}
}
#my @optvars = split /\0/, $in{'optvar'};
#my @optvals = split /\0/, $in{'optval'};
#my @delete_optvars = split /\0/, $in{'delete_optvar'};
#my @delete_optvals = split /\0/, $in{'delete_optval'};
#my @sets = split /\0/, $in{'set'};
#my @delete_sets = split /\0/, $in{'delete_set'};
my $protectit = $in{'protectit'};
#my $save = $in{'save'};
#my $delete = $in{'delete'};
my $saveit = $in{'saveit'};
my $submit = ($in{'save'}) ? 'save' : ($in{'delete'}) ? 'delete' : 'error';

&ui_print_header ($text{'index_title'}, "$text{'edit'} $text{'menuentry'}", "");
	print "in:".Dumper(%in)."||||<br />\n";
	#"sb is $sb<br />\n
	#i is $i<br />\n
	#protectit is $protectit<br />\n
	#submit is $submit<br />\n
	#id is $id<br />\n
	#submenu is $submenu<br />\n
	#name is $name<br />\n
	#valid is $valid<br />\n
	#saveit is $saveit<br />\n
	#pos is $pos<br />\n",
	print "was:". Dumper ($grub2cfg{$sb}{$i}). "||||<br />\n";
	if ($submenu ne $grub2cfg{$sb}{'name'}) {
		$sb = keys %grub2cfg;
		$i = 0;
		$grub2cfg{$sb}{'name'} = $submenu;	# create new submenu
		$grub2cfg{$sb}{'valid'} = ($name) ? 1 : 0;	#####
	}
	$grub2cfg{$sb}{$i}{'valid'} = ($name) ? 1 : 0;	#####
	$grub2cfg{$sb}{$i}{'name'} = $name;	# set name in hash (sub,item,name)
	$grub2cfg{$sb}{$i}{'saveit'} = $saveit;	# set name in hash (sub,item,saveit)
	$grub2cfg{$sb}{$i}{'protected'} = $protectit;	# set name in hash (sub,item,protected)
	$grub2cfg{$sb}{$i}{'pos'} = "'$sb > $i'";
	for (keys %optvar) {
		$grub2cfg{$sb}{$i}{'opts_vars'} = $optvar{$_}{'var'};	# add variable in hash (sub,item,opts_vars)
		$grub2cfg{$sb}{$i}{'opts_vars'}{$optvar{$_}{'var'}} = $optvar{$_}{'valu'}; # add variable value in var hash (sub,item,opts_vars)
	}
	for (@classes) {
		push (@{ $grub2cfg{$sb}{$i}{'classes'} }, $_);	# put each class in array inside hash (sub,item,classes)
	}
	for (@optifs) {
		push (@{ $grub2cfg{$sb}{$i}{'opts_if'} }, $_);	# put each condition in array inside hash (sub,item,opts_if)
	}
	for (@users) {
		push (@{ $grub2cfg{$sb}{$i}{'users'} }, $_);	# put each user in array inside hash (sub,item,users)
	}
#	"classes".Dumper(@classes)."||||<br />\n",
#	"delete_classes".Dumper(@delete_classes)."||||<br />\n";
	print "now:". Dumper ($grub2cfg{$sb}{$i}). "||||<br />\n";
	print $text{'cannot'};
&ui_print_footer ($return, $text{'index_short'});	# click to return
