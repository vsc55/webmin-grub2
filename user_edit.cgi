#!/usr/bin/perl
# user_edit.cgi
# Create / edit user

require './grub2-lib.pl';
&ReadParse();

#my $user = $grub2cfg{'users'};

my $do = "$text{'edit'} $text{'user'} \"$in{'name'}\"";
$do = "$text{'add'} $text{'user'}" if $in{'add'};
&ui_print_header ($text{'index_title'}, "$do", "", undef, undef, undef, undef, &returnto ("javascript: history.go(-1)", $text{'prev'}));
#print "in:".Dumper(%in)."||||<br />\n";

	print &ui_form_start ("user_save.cgi", "post"),#"form-data"),
		&ui_table_start ($text{'user_'}, "width=100%", 2);#, \@tds)
			my $name = "";
			$name = $grub2cfg{'users'}{$i}{'name'} if $in{'edit'};
			print &ui_table_row ($text{'user_name'},
				&ui_textbox ("user_name", $name, 80, 0, undef));# "onChange='$onch'"));
			my $pass = "";
			$pass = $grub2cfg{'users'}{$i}{'pass'} if $in{'edit'};
			print &ui_table_row ($text{'user_pass'},
				&ui_textbox ("user_pass", $pass, 50, 0, undef));# "onChange='$onch'"));
			print &ui_table_row ($text{'user_conf'},
				&ui_textbox ("user_conf", '', 50, 0, undef)) if $in{'add'};
			my $issuper = '';
			if ($in{'edit'}) {
				$issuper = ($grub2cfg{'users'}{$i}{'is_super'}==1);
				$issuper = '&nbsp;('. &text ('env_was', $issuper). ')';
				my $is_super = (($issuper) ? $text{'checked'} : $text{'unchecked'});
			}
			print &ui_table_row ($text{'user_super'},
				&ui_checkbox ("super", ($is_super==1), $issuper, $is_super));
		print &ui_table_end(),
		&ui_submit ($text{'save'}, "save"),
		&ui_submit ($text{'user_cancel'}, "cancel");
		print &ui_submit ($text{'delete'}, "delete") if $in{'edit'};
	print &ui_form_end(), &ui_hr();
&ui_print_footer ($return, $text{'index_main'});	# click to return
