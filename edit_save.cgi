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
my @classes = split /\0/, $in{'class'};
my @delete_classes = split /\0/, $in{'delete_class'};
my @optvars = split /\0/, $in{'optvar'};
my @optvals = split /\0/, $in{'optval'};
my @delete_optvars = split /\0/, $in{'delete_optvar'};
my @delete_optvals = split /\0/, $in{'delete_optval'};
my @sets = split /\0/, $in{'set'};
my @delete_sets = split /\0/, $in{'delete_set'};
my $protectit = $in{'protectit'};
my $save = $in{'save'};
my $delete = $in{'delete'};
my $saveit = $in{'saveit'};
my $submit = ($in{'save'}) ? 'save' : ($in{'delete'}) ? 'delete' : 'error';

&ui_print_header ($text{'index_title'}, "$text{'edit'} $text{'menuentry'}", "");
print $text{'cannot'};
#print "in:".Dumper(%in)."||||<br />\n",
#	"sb is $sb<br />\n
#	i is $i<br />\n
#	protectit is $protectit<br />\n
#	submit is $submit<br />\n
#	id is $id<br />\n
#	submenu is $submenu<br />\n
#	name is $name<br />\n
#	valid is $valid<br />\n
#	saveit is $saveit<br />\n
#	pos is $pos<br />\n",
#	"classes".Dumper(@classes)."||||<br />\n",
#	"delete_classes".Dumper(@delete_classes)."||||<br />\n";
