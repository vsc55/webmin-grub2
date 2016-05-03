#!/usr/bin/perl
# display_save.cgi
# Save the columns list

require './grub2-lib.pl';
&ReadParse();

&ui_print_header ($text{'index_title'}, "$text{'edit'} $text{'menuentry'}", "");

my @ons = split /\0/, $in{'disp'};
#my @names = split /\0/, $in{'disp_name'};
#my @disps = split /\0/, $in{'disp_all'};
my %hash;
my @parts;
for my $a (@ons) {
	if ($a =~ /^(\d+)\|(\d)\|([^|]+)\|(.+)$/) {
		my $pos = $1;
		$hash{$pos}{'displayed'} = int($2);
		$hash{$pos}{'nick'} = $3;
		$hash{$pos}{'name'} = $4;
		#for my $b (@ons) {
		#	$hash{$pos}{'displayed'} = ($hash{$pos}{'nick'} eq $b) ? 1 : 0;
		#}
	}
}
#our %display = %hash;

print "disps:".Dumper(@disps)."||||<br />\n",
	"ons:".Dumper(@ons)."||||<br />\n",
	"names:".Dumper(@names)."||||<br />\n",
	"hash:".Dumper(%hash)."||||<br />\n",
	"display:".Dumper(%display)."||||<br />\n",
	"parts:".Dumper(@parts)."||||<br />\n";


print $text{'cannot'};
