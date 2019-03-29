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
my $unrestricted = ($in{'unrestricted'}) ? 1 : 0;
my $submit = ($in{'save'}) ? 'save' : ($in{'delete'}) ? 'delete' : 'error';
my $use41 = $in{'save41'};

&ui_print_header ($text{'index_title'}, "$text{'edit'} $text{'menuentry'}", "", undef, undef, undef, undef,
				  &returnto ("javascript: history.go(-1)", $text{'prev'}));
	print "in:".Dumper(%in)."||||<br /><br />\n";
#	print "was:". Dumper ($grub2cfg{$sb}{$i}). "||||<br /><br />\n" if $in{'edit'};
#	if ($submenu ne $nowsubmenu) {
#		$sb = keys %grub2cfg;
#		$i = 0;
#		$grub2cfg{$sb}{'name'} = $nowsubmenu;	# create new submenu
#		$grub2cfg{$sb}{'valid'} = ($name) ? 1 : 0;	#####
#	}
#	$grub2cfg{$sb}{$i}{'valid'} = ($name) ? 1 : 0;	#####
#	$grub2cfg{$sb}{$i}{'name'} = $name;	# set name in hash (sub,item,name)
#	$grub2cfg{$sb}{$i}{'is_saved'} = $saveit;	# set name in hash (sub,item,saveit)
#	$grub2cfg{$sb}{$i}{'unrestricted'} = $unrestricted;	# set name in hash (sub,item,protected)
#	$grub2cfg{$sb}{$i}{'pos'} = sprintf ("%01d > %02d", $sb, $i);
#	for (keys %optvar) {
#		$grub2cfg{$sb}{$i}{'opts_vars'} = {	$optvar{$_}{'var'}, $optvar{$_}{'valu'}	};	# add variable in hash (sub,item,opts_vars)
#		#$grub2cfg{$sb}{$i}{'opts_vars'}{$optvar{$_}{'var'}} = $optvar{$_}{'valu'}; # add variable value in var hash (sub,item,opts_vars)
#	}
#	$grub2cfg{$sb}{$i}{'classes'} = ();	# empty classes first
#	for (@classes) {
#		push (@{ $grub2cfg{$sb}{$i}{'classes'} }, $_) if $_;	# put each class in array inside hash (sub,item,classes)
#	}
#	$grub2cfg{$sb}{$i}{'opts_if'} = "";	# empty opts_if first
#	for (@optifs) {
#		push (@{ $grub2cfg{$sb}{$i}{'opts_if'} }, $_) if $_;	# put each condition in array inside hash (sub,item,opts_if)
#	}
#	$grub2cfg{$sb}{$i}{'users'} = ();	# empty users first
#	for (@users) {
#		push (@{ $grub2cfg{$sb}{$i}{'users'} }, $_) if $_;	# put each user in array inside hash (sub,item,users)
#	}
##	"classes".Dumper(@classes)."||||<br />\n",
##	"delete_classes".Dumper(@delete_classes)."||||<br />\n";
#	print "now:". Dumper ($grub2cfg{$sb}{$i}). "||||<br /><br />\n";

	my $string = "", my $indent = " ", my $end = '', my $found = 0;
	my $fname = ($use41) ? "$config{'cfgd_dir'}${dir_sep}41_custom" : "$config{'cfgd_dir'}${dir_sep}40_custom";
	if ($custom = &get_file ($fname)) {
		@array = split /\n/, $custom;
		my $line_no = 1;
		for (@array) {
			if (/^\s*submenu\s+([^}]+)\}/) {
				$name = $1;
				$test = $nowsubmenu;
				$test =~ s/^[\"']|[\"']$//g;
				if ($name eq $test) {
					$found = 1;
					break;
				}
			}
			++$line_no;
		}
	} else {
		print "!no $fname file!";
	}
	#$string.= substr $custom, $line_no;
	if (!$found && $nowsubmenu && $nowsubmenu ne"main") {
		$string.= "submenu '$nowsubmenu' {\n";
		$indent = "\t";
		$end = '}';
	}
	$string.= $indent. "menuentry '$name'";
	if (scalar (@classes)>0) {
		for (@classes) {
			$string.= " --class $_" if $_;
		}
	}
	$string.= ' --unrestricted' if ($grub2cfg{$sb}{$i}{'unrestricted'});
	if (keys %optvar >0) {
		for (keys %optvar) {
			if (!$optvar{$_}{'valu'}) {	$optvar{$_}{'valu'} = "1";	}
			$string.= ' '. $optvar{$_}{'var'}. ' '. $optvar{$_}{'valu'};	# add variable in hash (sub,item,opts_vars)
		}
	}
	if (scalar (@optifs)>0) {
		for (@optifs) {#grub2cfg{$sb}{$i}{'opts_if'}
			$string.= ' '. $_;	# put each condition in array inside hash (sub,item,opts_if)
		}
	}
	if (scalar (@users)>0) {
		for (@users) {#grub2cfg{$sb}{$i}{'users'}
			$string.= ' '. $_;	# put each user in array inside hash (sub,item,users)
		}
	}
	$string.= " {\n";
	$string.= $indent. "}\n";
	$string.= $end. "\n";
	print "<pre>$string</pre>", $text{'cannot'};
	my $custom1, my $custom2, my $contents;
	if ($found) {
		$custom1 = substr $custom, $line_no;
		$custom2 = substr $custom, -$line_no;
		$contents = "\n$text{'add_str'}\n$custom2\n$string\n$custom1";
	} else {
		$string =~ s/^\s+|\s+$//g;
		$contents = $custom. "\n$text{'add_str'}\n". $string;
	}
	#print "\n\n". 'name=', $fname. '&contents=', $contents. "|<br />\n";
	print &ui_form_start ("edit_file_save.cgi", "form-data"),
		&ui_hidden ("name", $fname),
		&ui_hidden ("content", $contents),
		&ui_submit ($text{'save'}, "save"),
		&ui_form_end ();
	
#print 'returnHere:'. Dumper (@returnHere). "||||<br />\n";
#print 'returnHere ref:'. Dumper (\@returnHere). "||||<br />\n";
print &ui_hr();
&ui_print_footer ($return, $text{'index_main'});	# click to return
