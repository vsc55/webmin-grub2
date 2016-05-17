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
my $saveit = ($in{'is_saved'}) ? 1 : 0;
my $submenu = $in{'wassubmenu'};
my $nowsubmenu = $in{'entry_menu'};
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
	if (/^optval(\d+)$/) {
		$optvar{$1}{'valu'} = $in{"optval$1"};
	}
}
#my @optvars = split /\0/, $in{'optvar'};
#my @optvals = split /\0/, $in{'optval'};
#my @delete_optvars = split /\0/, $in{'delete_optvar'};
#my @delete_optvals = split /\0/, $in{'delete_optval'};
#my @sets = split /\0/, $in{'set'};
#my @delete_sets = split /\0/, $in{'delete_set'};
my $unrestricted = ($in{'unrestricted'}) ? 1 : 0;
#my $save = $in{'save'};
#my $delete = $in{'delete'};
my $submit = ($in{'save'}) ? 'save' : ($in{'delete'}) ? 'delete' : 'error';

&ui_print_header ($text{'index_title'}, "$text{'edit'} $text{'menuentry'}", "", undef, undef, undef, undef,
				  &returnto ("javascript: history.go(-1)", $text{'prev'}));
	print "in:".Dumper(%in)."||||<br /><br />\n";
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
	print "was:". Dumper ($grub2cfg{$sb}{$i}). "||||<br /><br />\n" if $in{'edit'};
	if ($submenu ne $nowsubmenu) {
		$sb = keys %grub2cfg;
		$i = 0;
		$grub2cfg{$sb}{'name'} = $nowsubmenu;	# create new submenu
		$grub2cfg{$sb}{'valid'} = ($name) ? 1 : 0;	#####
	}
	$grub2cfg{$sb}{$i}{'valid'} = ($name) ? 1 : 0;	#####
	$grub2cfg{$sb}{$i}{'name'} = $name;	# set name in hash (sub,item,name)
	$grub2cfg{$sb}{$i}{'is_saved'} = $saveit;	# set name in hash (sub,item,saveit)
	$grub2cfg{$sb}{$i}{'unrestricted'} = $unrestricted;	# set name in hash (sub,item,protected)
	$grub2cfg{$sb}{$i}{'pos'} = sprintf ("%01d > %02d", $sb, $i);
	for (keys %optvar) {
		$grub2cfg{$sb}{$i}{'opts_vars'} = {	$optvar{$_}{'var'}, $optvar{$_}{'valu'}	};	# add variable in hash (sub,item,opts_vars)
		#$grub2cfg{$sb}{$i}{'opts_vars'}{$optvar{$_}{'var'}} = $optvar{$_}{'valu'}; # add variable value in var hash (sub,item,opts_vars)
	}
	$grub2cfg{$sb}{$i}{'classes'} = ();	# empty classes first
	for (@classes) {
		push (@{ $grub2cfg{$sb}{$i}{'classes'} }, $_) if $_;	# put each class in array inside hash (sub,item,classes)
	}
	$grub2cfg{$sb}{$i}{'opts_if'} = "";	# empty opts_if first
	for (@optifs) {
		push (@{ $grub2cfg{$sb}{$i}{'opts_if'} }, $_) if $_;	# put each condition in array inside hash (sub,item,opts_if)
	}
	$grub2cfg{$sb}{$i}{'users'} = ();	# empty users first
	for (@users) {
		push (@{ $grub2cfg{$sb}{$i}{'users'} }, $_) if $_;	# put each user in array inside hash (sub,item,users)
	}
#	"classes".Dumper(@classes)."||||<br />\n",
#	"delete_classes".Dumper(@delete_classes)."||||<br />\n";
	print "now:". Dumper ($grub2cfg{$sb}{$i}). "||||<br /><br />\n";
	print $text{'cannot'};
#print 'returnHere:'. Dumper (@returnHere). "||||<br />\n";
#print 'returnHere ref:'. Dumper (\@returnHere). "||||<br />\n";
print &ui_hr();
&ui_print_footer ($return, $text{'index_main'});	# click to return
