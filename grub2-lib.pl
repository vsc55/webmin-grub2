#!/usr/bin/perl
# grub2-lib.pl
# Common functions for GRUB2 configuration

BEGIN { push(@INC, ".."); };
use WebminCore;
use File::Basename;
use Data::Dumper;#**use Data::Printer;
#use Text::Balanced qw (
#	extract_delimited
#	extract_bracketed
#	extract_quotelike
#	extract_codeblock
#	extract_variable
#	extract_tagged
#	extract_multiple
#	gen_delimited_pat
#	gen_extract_tagged
#);
init_config();
#=skip
#if ($gconfig{'os_type'}=~/(gentoo-linux|redhat-linux|suse-linux)/) {
#	our $os = "red";
#} elsif ($gconfig{'os_type'}=~/(debian|ubuntu)/) {
#	our $os = "deb";
#}
our $os = ($gconfig{'os_type'}=~/(gentoo-linux|redhat-linux|suse-linux)/) 	? 	"red" 	: 	($gconfig{'os_type'}=~/(debian|ubuntu)/) 	? 	"deb" 	: 	();
our %cmds = &get_cmds();
my $output = &backquote_command ($cmds{'install'}{$os}." -V 2>&1");
our $version = (split ' ', $output)[2];	# get common version
our $max_cols = 10;
our $dir_sep = ($gconfig{'os_type'}=~/windows/) ? '\\' : '/';
our %display = (
	0 => 	{	'nick' => "id",		'name' => $text{'entry_id'},		'displayed' => 1	},
	1 => 	{	'nick' => "name",	'name' => $text{'entry_name'},		'displayed' => 1	},
	2 => 	{	'nick' => "sub",	'name' => $text{'entry_sub_name'},	'displayed' => 1	},
	3 => 	{	'nick' => "class",	'name' => $text{'entry_classes'},	'displayed' => 1	},
	4 => 	{	'nick' => "ovar",	'name' => $text{'entry_opt_var'},	'displayed' => 1	},
	5 => 	{	'nick' => "oif",	'name' => $text{'entry_opt_if'},	'displayed' => 0	},
	6 => 	{	'nick' => "pro",	'name' => $text{'entry_protected'},	'displayed' => 1	},
	7 =>	{	'nick' => "users",	'name' => $text{'entry_users'},		'displayed' => 1	},
	8 => 	{	'nick' => "mod",	'name' => $text{'entry_mods'},		'displayed' => 1	},
	9 => 	{	'nick' => "set",	'name' => $text{'entry_sets'},		'displayed' => 0	},
	10 => 	{	'nick' => "ins",	'name' => $text{'entry_inners'},	'displayed' => 0	},
);

my %grub2env = &get_grub2_env();	# read environment
my $cfgfile = &load_cfg_file();	# build config array/hash
#structure:
#submenu
#-menuentry
#--name
#--ins
#--set
#--class
#--other
#print "$cfgfile<br />";
#if ($cfgfile !~ "/menuentry/") {
if (&indexof ($cfgfile, "menuentry")!=-1) {
#if (!length $cfgfile) {
	print $text{'index_noentrys'};
	exit();
}

#
#
#
sub number_subs
{
	my $nsubs = 0;
	#while (index($cfgfile, "submenu", 0)!=-1) {
	while ($cfgfile !~ "/submenu/") {
		$nsubs++;
	}
	return $nsubs;
}
#=skip

my @subs = split /submenu\s+/, $cfgfile;	# separate each submenu
#my %subs = split /submenu\s/, $cfgfile;	# separate each submenu
#print join "-----", @subs;
#print "-;-;-;-;-;-;";
#print Dumper(\%subs);
our %grub2cfg;
#my $nentrys = 0;
##while (index($cfgfile, "menuentry", 0)!=-1) {
#while ($cfgfile !~ "/menuentry/") {
#	$nentrys++;
#}
#while ($index <= $#subs) {
#	my $value = $subs[$index];
#	print "testing $value\n";
#	if ($value =~ m/^(submenu\s+)/) {
#		print "removed value $value\n";
#		splice @subs, $index, 1;
#	} else {
#		$value =~ s/^submenu\s+//;
#		$index++;
#	}
#}
#for (my $index = $#subs; $index >= 0; --$index) {
	#print "SUBMENU$index))$subs[$index]((";
	#if ($subs[$index] !~ /^[\"']/) {
	#	#print "removing $index.\n";
	#	print "removing $subs[$index].\n";
	#	splice @subs, $index, 1;	# remove certain elements
	#} else {
	#	$subs[$index] =~ s/^(submenu\s+)//;
	#}
#}
#my @username, @userpass;	# arrays of users and passwords
#my %hash;	# hash of users
while ($cfgfile =~ /^\s*password\s+(\w)\s+(\w)$/m) {
	#push (@username, $1);	# each user
	#push (@userpass, $2);	# each user's password
#	$hash{$1} = { 'pass' => $2, 'is_super' => 0 };	# add user hash (password, is_super) to hash
	$grub2cfg{'users'}{$1} = { 'pass' => $2, 'is_super' => 0 };	# add user hash (password, is_super) to hash
}
#my $username = join ",", @username;
#my $userpass = join ",", @userpass;
my ($superusers) = $cfgfile =~ /^\s*set superusers=\"([^"]+)$/m;	# all superusers
#my @users = ();	# array of users
if ($superusers) {	# superusers?
	#@users = split /,\s*/, $superusers;	# first append each superuser
	for (keys %hash) {
		#$hash{$_}{'is_super'} = 1;	# set user's is_super as true
		$grub2cfg{'users'}{$_}{'is_super'} = 1;	# set user's is_super as true
	}
	$grub2cfg{'superusers'} = $superusers;	# store superuser string
	#for (@users) {
	#	$hash{$_} = '';	# first set superuser with blank password
	#	if ($userpass =~ /\Q$_\E/) {
	#		$hash{$_} = $1;	# set superuser with password, if exists
	#	}
	#}
#} elsif ($#username) {	# normal users?
#	for (@username) {
#		$hash{$_} = '';	# first set superuser with blank password
#		if ($userpass =~ /\Q$_\E/) {
#			$hash{$_} = $1;	# set superuser with password, if exists
#		}
#	}
}
#$grub2cfg{'users'} = $hash;	# store user hash
my $count = 0;
for my $a (@subs) {
	my $index = 0;
	#if ($a =~ m/^(submenu\s+)/) {
	#	shift @subs;
	#} else {
	#	$a =~ s/^submenu\s+//;
	#}
	my $valid = 0;
	if ($a =~ m/^[\"']([^\"']+)[\"']\s*(.[^\{]+)/) {	$valid = 1;	}
	my $sname = ($valid == 1) ? $1 : $text{'cfg_main'};
	my $tempopts = $2;
	my $tempopts_noif;
	if ($tempopts =~ m/(if.*fi)/) {
		@temp = split /$1/, $tempopts;
		for (@temp) {
			$tempopts_noif .= $tempopts =~ s/$1//;
		}
	}
	my $sopts = $tempopts =~ s/\s*$//;
	#my %sopts = split / /, $2;
	$grub2cfg{$count} = {
		valid => 	$valid,
		name => 	$sname,
		options => 	(defined $tempopts_noif) ? $tempopts_noif : $sopts,#join "; ", %sopts,
#			all => 		$a
		opts_noif =>	$tempopts_noif,
	};
	if (substr($a, 0, 1) =~ /^['"]/) {
		$a =~ /^([\"'])(?:\\\1|.)*?\1/;
		#if (!$sname) {
		#	$sname = "main";
		#}
		#print Dumper($2);
		#$grubcfg{$sname} = [	"name" =	""	];
	}
	#print "SUBMENU:$a<br /><br />";
	@entrys = split /menuentry\s/, $a;	# divide each submenu into menuentries
	#my %entrys = split /menuentry\s/, $a;	# divide each submenu into menuentries
	#print Dumper (\%entrys);
	my $ecnt = 0;
	for my $entry (@entrys) {	# each menuentry
		my $valid = 0;
		if ($entry =~ m/^[\"']([^\"']+)[\"']\s*([^\{]*)\s*\{\s*([^\}]+)\}\s*/) {	$valid = 1;	}
		my ($ename,$eopts,$eins_whole) = ($1,$2,$3);	# grab menuentry name, prefic options, inners
		#my $ename = $1;	# grab menuentry name
		#my $eopts = $2;
		my @array = split /\s/, $2;	# divide each prefix option (space)
		#my $eins = $3;
		
		my $eins = $eins_whole;
		#print "[eins is]:".Dumper($eins)."[||||]";#good
		$loc_if_start = index ($eins, "if");
		$eins_ifs_start = substr ($eins, $loc_if_start);
		##print "[eins_ifs_start is]:".Dumper($eins_ifs_start)."[||||]";#good
		@eins_ifs = split /(\bfi\b)/, $eins_ifs_start;
		my @bettereiifs;
		for (@eins_ifs) {
			$_ =~ s/fi.*$/fi/i;
			push (@bettereiifs, $_);
		}
		@bettereiifs = grep {	/^if/ 	} @bettereiifs;
		#my @bettereiifs = &mk_array_without ($eins, "if", "fi");
		#print "[bettereiifs is:]".Dumper(@bettereiifs)."[||||]";#good
		#my @eiarray = split /\n/, $3;	# divide each inner part (newline)
		#my @eiarray = split /\n/, join ("\n", @bettereiifs);	# divide each inner part (newline)
		my @eiarray = @bettereiifs;
		#my @eins_lines = grep {	!/$eins/	} @bettereiifs;
		for (@bettereiifs) {
			$eins =~ s/$_//;	# remove all bettereiifs lines from $eins
			push(@eins_lines, $eins) if $_ =~ /$eins/;
		}
		my @eins_lines = split /\n/, $eins;
		
		my $cntr = 0;
		my $key;
		my %eoptsarray;# = [ var => "",	class => "",	unrestricted => ""	];
		for	my $e (@array) {	# each prefix option
			#print "(".($cntr+1).")$e";
			#print "[".$array[$cntr]."]";
			if ($e =~ /^[^a-zA-z\"']/) {	# first letter is not alpha or quote
				$key = ($e =~ m/^\-\-(.*)$/) ? $1 : $e;
				push (@{ $eoptsarray{$key} }, true) if $array[($cntr+1)] =~ m/^[^a-zA-z\"']/;
				#print "*key*";
			} else {
				if ($key) {
					if ($key =~ m/^\$/) {
						$eoptsarray{'var'}{$key} = $e;
					} else {
						push (@{ $eoptsarray{$key} }, $e);
					}
				} else {
					$eoptsarray{$array[$cntr-1]} = true;
				}
				#print "*value*";
			}
			$cntr++;
		}
		my $cls = $eoptsarray{'class'};
		my $users = $eoptsarray{'users'};
		my $unr = ($eoptsarray{'unrestricted'}) ? $text{'cfg_open'} : $text{'cfg_close'};
		my $optv = $eoptsarray{'var'};
		#print "eoptsarray is ".Dumper(\%eoptsarray);
		#print ":options:".Dumper(\@array);
		#my %eopts = split /( |;;)/, join ";;", @array;
		#my @eopts = split /( |;;)/, join ";;", @array;
		#my @array = split /\n/, $3;
		#my $eins = join ";;", @array;
		#$eins =~ s/if.*fi//g;
		#$eins =~ s/\t//g;
		#$eins =~ s/;;;;/;;/g;
		#$eins =~ s/;;$//g;
		my %eoptions;
		#for (@eiarray) {	# each inner line
		for (@eins_lines) {	# each inner line
			#print "[line of ei]:$_";#good
			$_ =~ s/\t\s*//;	# remove tab characters with optional spaces
			#print "[line of ei(no tabs)]:$_";#good
			@eiarray2 = split /\s/, $_;	# make an array each of parameter(s)
			#$grub2cfg{$count}{$ecnt}{'inners'}{shift @eiarray2} = @eiarray2;
			my $key = shift @eiarray2;
			#my $val = @eiarray2;
			$eoptions{$key} = @eiarray2;# if $key != "";#$val;
		}
		#print "[eoptions is]:".Dumper (\%eoptions)."[||||]";
#=skip
#		$s = 0;
#		for (@array) {
#			splice @array, ++$s, 0, "\n";
#		}
#		#my @array2 = split /\n/, $eins;
#		
#		print "eins split is ".Dumper(\@array);
#		my $cntr = 0;
#		my $key;
#		my %einsarray;
#		for my $d (@array) {
#			$d =~ s/if.*fi//g;
#			$d =~ s/\t//g;
#			$d =~ s/;;;;/;;/g;
#			$d =~ s/;;$//g;
#			if ($d =~ /;;$/) {
#				$key = ($d =~ m/^\-\-(.*)$/) ? $1 : $d;
#				push(@{ $einsarray{$key} }, true) if $array[($cntr+1)] =~ m/^[^a-zA-z\"']/;
#				#print "*key*";
#			} else {
#				if ($key) {
#					if ($key =~ m/^\$/) {
#						push(@{ $einsarray{'var'}{$key} }, $d);
#					} else {
#						push(@{ $einsarray{$key} }, $d);
#					}
#				} else {
#					$einsarray{$array[$cntr-1]} = true;
#				}
#				#print "*value*";
#			}
#			$cntr++;
#		}
#		my $mods = $einsarray{'insmod'};
#		my $linux = $einsarray{'linux'};
#		my $init = $einsarray{'initrd'};
#		my $sets = $einsarray{'set'};
#		#my $othi = $einsarray{'set'};
#		print "einsarray is ".Dumper (\%einsarray);
#=cut
		#my %eins = split /\s,\n/, $3;
#			chomp $eins;
		#print "<b style=\"background-color:green\">".$entry[0].$entry[1].$entry[2]."</b>";
		#$a =~ /^([\"'])(\\\1|.)*?\1/;
		#my ($name) = $a =~ /^[\"']([^\"']+)[\"']/;
		#$ename = "main" if !defined $ename;
		#($ename) = $entry =~ /^[\"']([^\"']+)[\"']/;
		my ($temppre) = $entry =~ /^[\"'][^\"']+[\"']\s([^\{]+)\s+/;
		my @array = split / /, $temppre;
		my %pre;
		$pre{$_}++ for (@array);
		my ($pre_if) = $pre =~ /(if\s[^(fi)]+fi)/;
		$pre_if = "" if !defined;
		my %real_pre = split / /, $entry;
#			my %real_pre;
#			my @mine;
#			@my_pre = split / /, $pre;
##my %final_hash_long;
##foreach my $data_pair (@data_list) {
##    my $key                = $data_pair->{key};
##    my $value              = $data_pair->{value};
##    $final_hash_long{$key} = $value;
##}
##
#my %real_pre =
#  map { $_->{key} => $_->{value} } @my_pre;
#			my $n_pre = -1;
#			for my $a (@my_pre) {
#				print "$a->{'key'},$a->{'value'}\n";#print $a;
#				$n_pre++;
#				if (!$n_pre || $n_pre % 2) {	# if odd iteration
#					my $key = $a;	# assign as key
#				} else {
#					my $val = $a;	# assign as val if even iteration
#					if ($key ~~ @mine) {
#						$real_pre{$key} .= ' '.$val;
#					} else {
#						$real_pre{$key} = $val;
#					}
#					push(@mine, $key);
#				}
#				print "$n_pre-$key=$val.";
#			}
		#($cls) = $entry =~ /--class\s(\w+)/;
		#my ($cls) = $pre =~ /--class\s([^\s]+)/g;
		#my ($inner) = $entry =~ /^[\"'][^\"']+[\"']\s*[^\{]+\{\s*([^\}]+)/;
		my @array = split / /, $inner;
		#my %ins = split / /, $inner;
		#print Dumper (\%ins);
		#$mods = join(" ", split /insmod\s/, $inner);
		#$sets = join(" ", split /set\s/, $inner);
		#$grub2cfg{$count}{'submenu'} = $a;
		$grub2cfg{$count}{$ecnt} = {	# build cfg hash
									id =>			$ecnt,
									name =>			(defined $ename) ? $ename : $text{'cfg_main'},
									valid =>		$valid,
			#						options =>		$eopts,#join " ", $eopts,#join " ", %pre,
									classes =>		$cls,
									protected =>	$unr,
									users =>		$users,
									opts_vars =>	$optv,
									opts_if =>		$pre_if,
									#inners =>		%eoptions,#@eiarray,#$eins,#join ", ", @eins,#join " ", %ins,#$inner,
			#						insmod =>		$mods,
									set =>			$sets,
#										all =>			($name eq $ename) ? '' : $entry
									all =>			$entry,
									is_saved =>		($grub2env{'saved_entry'}eq$ename) ? 1 : 0,
									};
	#if ($entry[0] ne "'" && $entry[0] ne '"') {	# skip first entry if doesn't start with quote
	#	$pre = shift @entrys;
	#}
	#if ($entry =~ /\}\s*\}/) {	# ignore if doesn't end with }
	#	pop @entrys;
	#}
		$ecnt++;
	}
	my $nentrys = scalar(@entrys);
	if (!$nentrys && !$count) {	# no menuentry in mainmenu ????
		print $text{'index_noentrys'};
		exit();
	}
	#if (!$count) {
	#	if ($nentrys != 1) {
	#		print "mainmenu has $nentrys entries.<br />";
	#	} else {
	#		print "mainmenu has $nentrys entry.<br />";
	#	}
	#} else {
	#	if ($nentrys != 1) {
	#		print "submenu $count has $nentrys entries.<br />";
	#	} else {
	#		print "submenu $count has $nentrys entry.<br />";
	#	}
	#}
	$count++;
	#foreach $entry (@entrys) {
	#	print "$entry<br /><br />";
	#}
#= cut
}
#= was2
#print "submenus:scarlar(@subs).menuentrys:scalar(@entrys)<br />";
#($pre) = $cfgfile =~ /^([^(menuentry)]+)/m;
#my @bootcfg = extract_multiple(
#	$cfgfile,
#	[ sub{extract_bracketed($_[0], '{}')},],
#	undef,
#	1
#);
#print "<pre>";
#print $pre;
#print "$_<br \>" foreach @bootcfg;
#print "</pre>";
#my @subs = split /submenu\s/, $cfgfile;	# divide cfg into main, sub0, ...
#foreach (@subs) {	# add sections (as above) to whole array
#	push (@bootcfg, $_);
#}
#foreach $sub (@subs) {	# add each menuentry to its section of the whole array
#	foreach (split /menuentry\s/, $sub) {
#		push (@{ $sub }, $_);
#	}
#}
#my @main_entrys = split /menuentry\s/, shift @subs;
#foreach (@subs) {
#	push (@subs, split /menuentry\s/);
#}
#print Dumper (@bootcfg);
#my @names = split /menuentry\s.([^'|"]+)./, $entry;
#my @names = split /menuentry\s.([^'|"]+)./, $cfgfile;#([^\{]+)\{([^\}])}
#my @names = $cfgfile =~ /menuentry\s.([^'|"]+).(\{(?:[^{}]*|(?0))*\})/xg;
#@entrys = extract_multiple($text,
#    [ \&extract_bracketed,
#		\&extract_quotelike,
#		\&some_other_extractor_sub,
#		qr/[xyz]*/,
#		'literal',
#	]);
#(@entrys) = extract_delimited $cfgfile, q{"'};
#@entrys = extract_codeblock ($cfgfile, '{}');
#shift @names;
#print scalar(@names);
#print "<pre>";
#foreach (@entrys) {
#	print "$_<br />";
#}
#print "</pre>";
#print "real_pre:".Dumper(\%real_pre);
#print "my_pre:".Dumper(\@my_pre);
#while (my ($key, $value) = each @my_pre) {
#	print "$key = $value\n";
#}
#=skip
#=cut

#
# gets environment
#
sub get_grub2_env
{
	#print Dumper(%cmds);
	my $output = &backquote_command("(".$cmds{'editenv'}{$os}." list) 2>&1");
	my @args = split /\n/, $output;
	my %vars = map { split /=/, $_, 2 } @args;
	return %vars;
}
#=skip

#
# recreate_cfg
#
sub recreate_cfg
{
	#my $output = "recreate_cfg:[backquote_command (".$cmds{'install'}{$os}." $config{'cfg_file'}) 2>&1]";
	my $output = &backquote_command ("(".$cmds{'mkconfig'}{$os}." $config{'cfg_file'}) 2>&1");
	return undef if $output = "";
	return $output;
}

#
# backup a file / dir
#
sub grub2_backup
{
	&redirect ("backup.cgi?what=".@_[0]."&return=". &this_url());
}

#gives this url
sub this_url
{
	my $url = $ENV{'SCRIPT_NAME'};
	$url .= "?$ENV{'QUERY_STRING'}" if ($ENV{'QUERY_STRING'} ne "");
	#chop ($url) if substr ($url, -1)=='/';
	return $url;
}

#
sub check_cfg
{
	my $out = &backquote_command("(".$cmds{'script-chk'}{$os}." ".$config{'cfg_file'}.") 2>&1");
	if ($out =~ /failed/) {
		return "<pre>".&html_escape($out)."</pre>";
    } else {
		return undef;
    }
	return $out;
}

#
sub test_cfg_button
{
	my $localtime = localtime();
	#my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	#$year += 1900;
	#print "$sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst\n";
	my $args = "redir=".&urlize(&this_url());
	my $retn = (check_cfg) ? $text{"cfg_BAD"} : $text{'cfg_OK'};
	$retn.= '&nbsp;:&nbsp;<a href="test_cfg.cgi?'.$args.'">'. $text{'cfg_check'}. '</a><br />';
	$retn.= &text ('when', "$localtime");
	return $retn;
}

#
# gets default settings
#
sub get_grub2_def
{
	my $output = &backquote_command("(cat $config{'def_file'}) 2>&1");
	my @args = split /\n/, $output;
	my %vars = map { split /=/, $_, 2 } @args;
	return %vars;
}
#=cut

#
# get commands hash of arrays
#
sub get_cmds
{
	%cmds = (
		"bios" => 		{	red => "grub2-bios-setup",		deb => "grub-bios-setup",		desc => "Set up images to boot from a device.",											version => ''},
		"editenv" => 	{	red => "grub2-editenv",			deb => "grub-editenv",			desc => "Manage the GRUB environment block.",											version => ''},
		"file" => 		{	red => "grub2-file",			deb => "grub-file",				desc => "Check if FILE is of specified type.",											version => ''},
		"glue-efi" => 	{	red => "grub2-glue-efi",		deb => "grub-glue-efi",			desc => "Create an Apple fat EFI binary.",												version => ''},
		"install" => 	{	red => "grub2-install",			deb => "grub-install",			desc => "Install GRUB on a device.",													version => ''},
		"kbdcomp" => 	{	red => "grub2-kbdcomp",			deb => "grub-kbdcomp",			desc => "Generate a GRUB keyboard layout file.",										version => ''},
		"macbless" => 	{	red => "grub2-macbless",		deb => "grub-macbless",			desc => "Mac-style bless utility for HFS or HFS+",										version => ''},
		"menulst2cf" => {	red => "grub2-menulst2cfg",		deb => "grub-menulst2cfg",		desc => "Convert a configuration file from GRUB 0.xx to GRUB 2.xx format.",				version => ''},
		"mkconfig" => 	{	red => "grub2-mkconfig",		deb => "grub-mkconfig",			desc => "Generate a GRUB configuration file.",											version => ''},
		"mkfont" => 	{	red => "grub2-mkfont",			deb => "grub-mkfont",			desc => "Convert common font file formats into the PF2 format.",						version => ''},
		"mkimage" => 	{	red => "grub2-mkimage",			deb => "grub-mkimage",			desc => "Make a bootable GRUB image.",													version => ''},
		"mklayout" => 	{	red => "grub2-mklayout",		deb => "grub-mklayout",			desc => "Generate a GRUB keyboard layout file.",										version => ''},
		"mknetdir" => 	{	red => "grub2-mknetdir",		deb => "grub-mknetdir",			desc => "Prepare a GRUB netboot directory.",											version => ''},
		"pbkdf2" => 	{	red => "grub2-mkpasswd-pbkdf2",	deb => "grub-mkpasswd-pbkdf2",	desc => "Generate a PBKDF2 password hash.",												version => ''},
		"mkrelpath" => 	{	red => "grub2-mkrelpath",		deb => "grub-mkrelpath",		desc => "Generate a relative GRUB path given an OS path.",								version => ''},
		"mkrescue" => 	{	red => "grub2-mkrescue",		deb => "grub-mkrescue",			desc => "Generate a GRUB rescue image using GNU Xorriso.",								version => ''},
		"mkstanda" => 	{	red => "grub2-mkstandalone",	deb => "grub-mkstandalone",		desc => "Generate a standalone image in the selected format.",							version => ''},
		"ofpathname" => {	red => "grub2-ofpathname",		deb => "grub-ofpathname",		desc => "Generate an IEEE-1275 device path for a specified device.",					version => ''},
		"probe" => 		{	red => "grub2-probe",			deb => "grub-probe",			desc => "Probe device information for a given path.",									version => ''},
		"reboot" => 	{	red => "grub2-reboot",			deb => "grub-reboot",			desc => "Set the default boot menu entry for the next boot only.",						version => ''},
		"label" => 		{	red => "grub2-render-label",	deb => "grub-render-label",		desc => "Render an Apple disk label.",													version => ''},
		"rpm-sort" => 	{	red => "grub2-rpm-sort",		deb => "grub-rpm-sort",			desc => "Sort input according to RPM version compare.",									version => ''},
		"script-chk" => {	red => "grub2-script-check",	deb => "grub-script-check",		desc => "Check GRUB configuration file for syntax errors.",								version => ''},
		"default" => 	{	red => "grub2-set-default",		deb => "grub-set-default",		desc => "Set the default boot menu entry for GRUB.",									version => ''},
		"setpasswd" => 	{	red => "grub2-setpassword",		deb => "grub-setpassword",		desc => "Generate the user.cfg file containing the hashed grub bootloader password.",	version => ''},
		"sparc64-s" => 	{	red => "grub2-sparc64-setup",	deb => "grub-sparc64-setup",	desc => "Set up a device to boot a sparc64 GRUB image.",								version => ''},
		"sysl2cfg" => 	{	red => "grub2-syslinux2cfg",	deb => "grub-syslinux2cfg",		desc => "Transform a syslinux config file into a GRUB config.",							version => ''},
		"fstest" => 	{	red => "grub2-fstest",			deb => "grub-fstest",			desc => "(unknown subject)",															version => ''},
		"grubby" => 	{	red => "grubby",				deb => "grubby",				desc => "command line tool for configuring grub, lilo, elilo, yaboot and zipl",			version => ''},
	);
#	use Config::IniFiles;
#	my $env_s = Config::IniFiles->new (-file => "./webmin-grub2_commands.ini");
#	#print "The value is " . $env_s->val ('Section', 'Parameter') . "." if $env_s->val ('Section', 'Parameter');
#	my %cmds = $env_s->Sections;
#	for $a (keys %cmds){
#		$cmds{$a} = [ red => $env_s->val ($a, 'red'), deb => $env_s->val ($a, 'tydebpe'), desc => $env_s->val ($a, 'desc') ];
#	}
#	$cmds{$_} = map {	[ desc => $env_s->val ($_, 'desc'), red => $env_s->val ($_, 'red'), deb => $env_s->val ($_, 'deb') ]	} keys %cmds;
	for my $a (keys \%cmds) {
		$output = &backquote_command ($cmds{$a}{$os}." -V 2>&1");
		$cmds{$a}{'version'} = (split ' ', $output)[2];
		if ($cmds{$a}{'version'} !~ /\d/) {
			$cmds{$a}{'version'} = $text{'noversion'};
		}
	}
	return %cmds
}

#
# get device.map
#
sub get_devicemap
{
	my $output = &backquote_command("(cat $config{'dmap_file'}) 2>&1");
	my @args = split /\n/, $output;
	my %vars = map {	m/^\s?\((\w+)\)\s+(.*)/	} @args;
	return %vars;
}

#
# load_cfg_file (<optional filename>)
#
sub load_cfg_file
{
	my $file = @_[0];
	my $file = "${dir_sep}boot${dir_sep}grub2${dir_sep}grub.cfg" if @_[0] eq "";	# $config{'cfg_file'}
	my $cfgfile = do {
		local $/ = undef;
		open my $fh, "<", $file
			or die "could not open $file: $!";
		<$fh>;
	};
	#close $fh;
	return $cfgfile;
}

#
# remove_all_comments_from_cfg_file (<optional file contents>)
#
sub remove_all_comments_from_cfg_file
{
	my $cfgfile = @_[0];
	my $cfgfile = load_cfg_file() if @_[0] eq "";
	$cfgfile =~ s/#[^\n]*\n//g;
	return $cfgfile;
}

#
# divide_cfg_into_parsed_files (<optional file contents>)
#
sub divide_cfg_into_parsed_files
{
	my $cfgfile = @_[0];
	my $cfgfile = load_cfg_file() if @_[0] eq "";
	@processed = split /### (BEGIN [^#]+) ###\n/, $cfgfile;	# divide into files parsed
	my %prohash;
	for (my $index = 0; $index < $#processed; $index++) {
		if ($processed[$index] =~ m/^BEGIN/) {
			$processed[$index] =~ s/^BEGIN\s+//;	# remove beginning
			my $temp = $processed[$index];
			$processed[$index+1] =~ s/\n*###\s+END\s+$temp\s+###\n*$//;
			$prohash{$processed[$index]} = $processed[$index+1];	# insert hash row
		}
	}
	return %prohash;
}

############################### cutoff ###############################
# USAGE:                                                             #
# $cutoff = cutoff($string, $length, $end);                          #
# ($cutoff, $restofstring) = cutoff($string, $length, $end);         #
# $string is the string you want to be cut off at a given length     #
# $length is the position you want to start at                       #
# $end is what to put at the end, like a ...                         #
# By using rindex, it will start at that spot, if it is in the       #
# middle of a word, it will move back till it finds a space and cuts #
# it off at that point.                                              #
# Since it uses wantarray, if you want an array back, it will return #
# the portion you want, and the rest of the string. Otherwise, it    #
# will return just the cutoff portion.                               #
######################################################################
sub cutoff {
    my $string = shift;            # get the string to examine
    my $size   = shift;            # get the size to "cut off" at
    my $end    = shift;            # characters to pad the end (...)
    my $length = length($string);  # get the length
    if ($length <= $size) {        # If the length is less than or 
        return($string);           # equal to the size we want to cut 
                                   # off at, don't cut off
    } # end if
    else {
        # This takes the string, and uses rindex (same as index, but
        # reverse). It starts at $size, and goes back till it finds a
        # space and returns that position
        my $pos = rindex($string, " ", $size);
        # With the position to turnicate from, this uses substr to
        # acomplish this.
        my $cutstring    = substr($string, 0, $pos);
    #my $restofstring = substr($string, $pos, length($string));
    #$restofstring =~ s/^\s//; # Remove just the first space
    $cutstring .= $end if ($end);
    # If we want an array, return $cutstring, and $restofstring
    # otherwise return just $cutstring
#        return wantarray ? ($cutstring, $restofstring) : $cutstring;
        return $cutstring;
    } # end else
} # end cutoff
######################################################################

#
# mk_array_without ($string, $start, $end)
#
sub mk_array_without
{
	my $loc_start = index ($string, $start);
	my $string_start = substr ($string, $loc_start);
	@array = split /(\b$end\b)/, $string_start;
	my @better;
	for (@array) {
		$_ =~ s/($end).*$/$1/i;
		push (@better, $_);
	}
	@better = grep {	/^$end/ 	} @better;
	return @better;
}
#=cut

#
# save menuentry as default saved
#
sub save_entry
{
	$name = shift;
	return (&backquote_command("(".$cmds{'default'}{$os}." $name) 2>&1"));
}

#
sub get_defaults
{
	my %env_setts = (
				 wasGRUB_DEFAULT => { desc => "Sets the default menu entry that will be booted next time the computer is rebooted.
				 It can be a numeric value, a complete menu entry quotation, or `saved`. A few examples follow:
				 
				 `GRUB_DEFAULT=2` boots the third (counted from zero) boot menu entry.
				 
				 `GRUB_DEFAULT=2>0` boots the first entry from the third submenu.
				 
				 `GRUB_DEFAULT='Example boot menu entry'` boots the menu entry whose title matches the quotation.
				 
				 `GRUB_DEFAULT=saved` boots the entry specified by the grub2-reboot or grub2-set-default commands.
				 While grub2-reboot sets the default boot entry for the next reboot only, grub2-set-default sets the default boot entry until changed.",
				 type => "text" },
				 
				 GRUB_BACKGROUND => { desc => "Set a background image for the gfxterm graphical terminal.
				 The image must be a file readable by GRUB2 at boot time, and it must end with the .png, .tga, .jpg, or .jpeg suffix.
				 If necessary, the image will be scaled to fit the screen.",
				 type => "text" },
				 
				 GRUB_CMDLINE_LINUX => { desc => "Entries on this line are added to the end of the booting command line for both normal and recovery modes.
				 It is used to pass options to the kernel. eg: 'init=/lib/systemd/systemd', serial: 'console=tty0 console=ttyS0,115200n8'",
				 type => "text" },
				 
				 GRUB_CMDLINE_LINUX_DEFAULT => { desc => "Same as GRUB_CMDLINE_LINUX but the entries are passed and appended in the normal mode only.
				 eg. 'text elevator=deadline zcache nomodeset i915.modeset=0 nouveau.modeset=0 video=vesa:off vga=normal'",
				 type => "text" },
				 
				 GRUB_DEFAULT => { desc => "Sets the default menu entry that will be booted next time the computer is rebooted.
				 It can be a numeric value, a complete menu entry quotation, or `saved`.
				 While grub2-reboot sets the default boot entry for the next reboot only, grub2-set-default sets the default boot entry until changed.",
				 type => "combo", options => [ "saved", "<menuentry name>", "<menuentry position number>" ], default => "saved" },
				 
				 GRUB_DISABLE_LINUX_UUID => { desc => "Set `true` if you don't want GRUB to pass 'root=UUID=xxx' parameter to Linux",
											 type => "select", options => [ "true", "false" ], default => "false" },
				 
				 GRUB_DISABLE_RECOVERY => { desc => "Set `true` to disable generation of recovery mode menu entries.",
										   type => "select", options => [ "true", "false" ], default => "false" },#, ""
				 
				 GRUB_DISABLE_SUBMENU => { desc => "Set `true` to disable submenu branches.",
										  type => "select", options => [ "true", "false" ], default => "false" },
				 
				 GRUB_DISTRIBUTOR => { desc => "OS release version. Fedora/CentOS: '$(sed 's, release .*$,,g' /etc/system-release)',
				 Debian: '`lsb_release -i -s 2> /dev/null || echo Debian`'",
				 type => "text" },
				 
				 GRUB_FONT_PATH => { desc => "Location of font used, eg: '/boot/grub2/fonts/LiberationSerif-Regular.pf2'",
									type => "text" },
				 
				 GRUB_HIDDEN_TIMEOUT => { desc => "Waits the specified number of seconds for the user to press a key.
				 During the period no menu is shown unless the user presses a key.
				 If no key is pressed during the time specified, the control is passed to `GRUB_TIMEOUT`.
				 `GRUB_HIDDEN_TIMEOUT=0` first checks whether Shift is pressed and
				 shows the boot menu if yes, otherwise immediately boots the default menu entry.
				 This is the default when only one bootable OS is identified by GRUB2.",
				 type => "number" },
				 
				 GRUB_HIDDEN_TIMEOUT_QUIET => { desc => "If false is specified, a countdown timer is displayed on a
				 blank screen when the `GRUB_HIDDEN_TIMEOUT` feature is active.",
				 type => "select", options => [ "true", "false" ], default => "false" },
				 
				 GRUB_GFXMODE => { desc => "The resolution used for the gfxterm graphical terminal.
				 Note that you can only use modes supported by your graphics card (VBE).
				 The default is ‘auto’, which tries to select a preferred resolution.
				 You can display the screen resolutions available to GRUB2 by typing vbeinfo in the GRUB2 command line.
				 The command line is accessed by typing c when the GRUB2 boot menu screen is displayed.
				 
				 You can also specify a color bit depth by appending it to the resolution setting, for example GRUB_GFXMODE=1280x1024x24.
				 
				 [Tip]	Setting the same resolution in GRUB2 and the operating system will slightly reduce the boot time.",
				 type => "text" },
				 
				 GRUB_GFXPAYLOAD_LINUX => { desc => "How to handle the Graphics payload on Linux systems, common: 'keep', 'text'",
										   type => "select", options => [ "keep", "text" ], default => "keep" },
				 
				 GRUB2_PASSWORD => { desc => "Global password",
									type => "text" },
# ^^is GRUB2_ correct????				 
 				 GRUB_RECORDFAIL_TIMEOUT => { desc => "For `-1`, there will be no countdown and thus the menu will display;
				 For `0`, menu will not display even for a failed startup;
				 For >=1, menu will display for the specified number of seconds.",
				 type => "number" },
				 
				 GRUB_SAVEDEFAULT => { desc => "If set to true, it will automatically choose the last selected OS
				 from the boot menu as the default boot entry on the next boot.
				 For this to work, you also need to specify `GRUB_DEFAULT=saved`.",
				 type => "select", options => [ "true", "false" ], default => "false" },
				 
				 GRUB_SERIAL_COMMAND => { desc => "Set `GRUB_TERMINAL=serial`. May need to adjust `GRUB_CMDLINE_LINUX`.
				 eg: 'serial --unit=0 --speed=9600 --word=8 --parity=no --stop=1'",
				 type => "text" },
				 
				 GRUB_TERMINAL => { desc => "Enables and specifies input/output terminal device.
				 Can be 'console' (PC BIOS and EFI consoles), 'serial' (serial terminal),
				 'ofconsole' (Open Firmware console), or the default 'gfxterm' (graphics-mode output).",
				 type => "select", options => [ "serial", "console", "ofconsole", "gfxterm" ], default => "gfxterm" },
				 
				 GRUB_TERMINAL_OUTPUT => { desc => "Can be 'console' (PC BIOS and EFI consoles),
				 'serial' (serial terminal), 'ofconsole' (Open Firmware console),
				 or the default 'gfxterm' (graphics-mode output).",
				 type => "select", options => [ "console", "serial", "ofconsole", "gfxterm" ], default => "gfxterm" },
				 
				 GRUB_TIMEOUT => { desc => "Time period in seconds the boot menu is displayed before automatically booting the default boot entry.
				 If you press a key, the timeout is cancelled and GRUB2 waits for you to make the selection manually.
				 `GRUB_TIMEOUT=-1` will cause the menu to be displayed until you select the boot entry manually.",
				 type => "number" },
				 
				 GRUB_VIDEO_BACKEND => { desc => "Device to handle graphical requests, common: 'vbe'",
										type => "select", options => [ "vbe", "none" ], default => "vbe" },
				 
				 saved_entry => { desc => "Name of default menuentry to boot.", type => "text" }
				 
#				 
#				  => "",
			);
#	use Config::IniFiles;
#	my $env_s = Config::IniFiles->new (-file => "./webmin-grub2_defaults.ini");
#	#print "The value is " . $env_s->val ('Section', 'Parameter') . "." if $env_s->val ('Section', 'Parameter');
#	my %env_setts = $env_s->Sections;
#	for $a (keys %env_setts){
#		$env_setts{$a} = [ desc => $env_s->val ($a, 'desc'), type => $env_s->val ($a, 'type'), options => $env_s->val ($a, 'options') ];
#	}
#	$env_setts{$_} = map {	[ desc => $env_s->val ($_, 'desc'), type => $env_s->val ($_, 'type'), options => $env_s->val ($_, 'options') ]	} keys %env_setts;
	return %env_setts;
}
our %env_setts = &get_defaults();

sub get_grub2_files
{
	my %grub2files = (
				   '00_header' => "is the script that loads GRUB settings from `/etc/default/grub`,
				   including timeout, default boot entry, and others. We will talk more about these soon.",
				   '01_users' => "users and passwords",
				   '05_debian_theme' => "defines the background, colors and themes.
				   The name of this script is definitely going to change to when other distributions adopt GRUB 2.",
				   '10_linux' => "loads the menu entries for the installed distribution.",
				   '20_memtest86+' => "loads the memtest utility.",
				   '30_os-prober' => "is the script that will scan the hard disks for other operating systems and add them to the boot menu.",
				   '40_custom' => "is a template that you can use to create additional entries to be added to the boot menu.",
				   '90_persistent' => "This is a special script which copies a corresponding part of the grub.cfg file and outputs it back unchanged.
				   This way you can modify that part of `grub.cfg` directly and the change survives the execution of grub2-mkconfig."
				   );
#	use Config::IniFiles;
#	my $env_s = Config::IniFiles->new (-file => "./webmin-grub2_files.ini");
#	#print "The value is " . $env_s->val ('Section', 'Parameter') . "." if $env_s->val ('Section', 'Parameter');
#	my %grub2files = $env_s->Sections;
#	for $a (keys %grub2files){
#		$grub2files{$a} = [ desc => $env_s->val ($a, 'desc'), type => $env_s->val ($a, 'type'), options => $env_s->val ($a, 'options') ];
#	}
#	$grub2files{$_} = map {	$_ => $env_s->val ('GENERAL', 'options') ]	} keys %grub2files;
	return %grub2files;
}
our %grub2files = &get_grub2_files();
;1
