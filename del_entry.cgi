#!/usr/bin/perl
# del_entry.cgi
# Delete a menuentry or mutiple

require './grub2-lib.pl';
&ReadParse();

my @ids = split /,/, $in{'d'};
#my @id2 = ();
for $a (@ids) {
	my ($ss, $ii) = $a =~ /sub=([0-9]+)[^=]+=([0-9]+)/;
	&remove_an_entry ($ss, $ii, \%grub2cfg);
	#push (@id2, {	"name" => $grub2cfg{$ss}{$ii}{'name'},
	#				"submenu" => $ss,
	#				"item" => $ii	});
}

&redirect ($return, $text{'index_short'});
