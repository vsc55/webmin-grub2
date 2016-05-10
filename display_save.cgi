#!/usr/bin/perl
# display_save.cgi
# Save the columns list

require './grub2-lib.pl';
&ReadParse();

#&ui_print_header ($text{'index_title'}, "$text{'edit'} $text{'menuentry'}", "");

my @ons = split /\0/, $in{'disp'};
my %hash;
my $count = 0;
for (keys %in) {
	if (/^disp_name-(.*)$/) {
		$hash{$count}{'nick'} = $1;
		$hash{$count}{'name'} = $in{$_};
		$hash{$count}{'displayed'} = 0;
	}
	++$count;
}
#my %names = split /\0/, $in{'disp_name'};
#my @disps = split /\0/, $in{'disp_all'};
#my @parts;
for my $a (@ons) {
	if ($a =~ /^(\d+)\|(\d)\|([^|]+)\|(.+)$/) {
		my $pos = $1;
		$hash{$pos}{'displayed'} = int($2);
		#$hash{$pos}{'nick'} = $3;
		#$hash{$pos}{'name'} = $4;
		#for my $b (@ons) {
		#	$hash{$pos}{'displayed'} = ($hash{$pos}{'nick'} eq $b) ? 1 : 0;
		#}
	}
}
for (keys %display) {
	delete $display{$_};
}
our %display = %hash;

#print "disps:".Dumper(@disps)."||||<br />\n",
#	"ons:".Dumper(@ons)."||||<br />\n",
#	"names:".Dumper(%names)."||||<br />\n",
#	"hash:".Dumper(%hash)."||||<br />\n",
#	"in:".Dumper(%in)."||||<br />\n",
#	"parts:".Dumper(@parts)."||||<br />\n";
#
#
#print $text{'cannot'};
&redirect ($return);#&redirect ("/grub2");