#!/usr/bin/perl
# user_save.cgi
# Save user and details

require './grub2-lib.pl';
&ReadParse();
#&redirect ($return) if $in{'user_name'}eq"" || $in{'cancel'}ne"";	# just retrurn
#&redirect ($return) if $in{'user_name'}eq"";	# just retrurn if no name given
&redirect ($return) if $in{'cancel'}ne"";	# just retrurn if selected cancel

my $name = $in{'user_name'};
my $pass = $in{'user_pass'};
my $cpass = $in{'user_conf'};
my $super = int ($in{'super'});

&ui_print_header ($text{'index_title'}, "$text{'save'} $text{'user'} \"$name\"", "");
print "in:". Dumper (%in). "|||";
	
	if (!$name) {
		&error ($text{'error'}. &text ('missing', ' '. $text{'user_name'}));
	}
	if (!$pass) {
		&error ($text{'error'}. &text ('missing', ' '. $text{'user_pass'}));
	}
	if (!$cpass) {
		&error ($text{'error'}. &text ('missing', ' '. $text{'user_pass'}. ' '. $text{'user_conf'}));
	}
	if ($pass ne $cpass) {
		&error ($text{'user_passmm'});
	} elsif ($pass && $cpass) {
		$grub2cfg{'users'}{$name} = {	'pass' => $pass,	'is_super' => $super	};
		if ($super) {
			$grub2cfg{'superusers'}.= ($grub2cfg{'superusers'}) ? (substr ($grub2cfg{'superusers'}, -1)ne',' ? ',' : '') : '';
			$grub2cfg{'superusers'}.= $name;
		}
	}
	#print Dumper (%grub2cfg);
	print "users:". Dumper ($grub2cfg{'users'}). "|||<br />\n";
	print "supers:". Dumper ($grub2cfg{'superusers'}). "|||<br />\n";
	print &text ('user_adding', $name, $pass). "<br />\n";
	print '<a href="backup.cgi?what='. $config{'cfg_file'}. '&return='. &this_url(). '">'.$text{'confirm'}.'</a>';
	&error ($err) if (my $err = &recreate_cfg());
	
&ui_print_footer ($return, $text{'index_short'});	# click to return
