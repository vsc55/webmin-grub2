#!/usr/bin/perl
# add_env.cgi
# Add an environment variable

require './grub2-lib.pl';
&ReadParse();

#, undef, undef, undef, undef, &returnto ("javascript: history.go(-1)", $text{'prev'})
print &ui_hr();