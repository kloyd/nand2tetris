#!/usr/bin/env perl 
   
use strict;
use warnings;

print "$#ARGV\n";

if ($#ARGV != 0) {
	print "Usage: hackasm <assembly source file>\n";
	exit(0);
}

my $asmsourcename = $ARGV[0] . ".asm";
my $asmoutputname = $ARGV[0] . ".hack";

my %symbols = (
    'SP' => '0',
    'LCL' => '1',
    'ARG' => '2',
    'THIS' => '3',
    'THAT' => '4',
    'R0' => '0',
    'R1' => '1',
    'R2' => '2',
    'R3' => '3',
    'R4' => '4',
    'R5' => '5',
    'R6' => '6',
    'R7' => '7',
    'R8' => '8',
    'R9' => '9',
    'R10' => '10',
    'R11' => '11',
    'R12' => '12',
    'R13' => '13',
    'R14' => '14',
    'R15' => '15',
    'SCREEN' => '16384',
    'KBD' => '24576'
    );

my %destinations = (
    'none' => '000',
    'M' => '001',
    'D' => '010',
    'MD' => '011',
    'A' => '100',
    'AM' => '101',
    'AD' => '110',
    'AMD' => '111'
    );

my %jumps = (
    'none' => '000',
    'JGT' => '001',
    'JEQ' => '010',
    'JGE' => '011',
    'JLT' => '100',
    'JNE' => '101',
    'JLE' => '110',
    'JMP' => '111'
    );

my %comps = (
    '0' =>   '0101010',
    '1' =>   '0111111',
    '-1' =>  '0111010',
    'D' =>   '0001100',
    'A' =>   '0110000',
    '!D' =>  '0001101',
    '!A' =>  '0110001',
    '-D' =>  '0001111',
    '-A' =>  '0110011',
    'D+1' => '0011111',
    'A+1' => '0110111',
    'D-1' => '0001110',
    'A-1' => '0110010',
    'D+A' => '0000010',
    'D-A' => '0010011',
    'A-D' => '0000111',
    'D&A' => '0000000',
    'D|A' => '0010101',
    'M' =>   '1110000',
    '!M' =>  '1110001',
    '-M' =>  '1110011',
    'M+1' => '1110111',
    'M-1' => '1110010',
    'D+M' => '1000010',
    'D-M' => '1010011',
    'M-D' => '1000111',
    'D&M' => '1000000',
    'D|M' => '1010101'
    );

my $linenum = 0;
my $nextsymboladdr = 16;  ## address symbols start at 16 ### first pass, (symbols).
my $opcode_class = '[\w\!\+\&\|\-]+';

open(my $symsource, '<:encoding(UTF-8)', $asmsourcename)
    or die "Could not open file '$asmsourcename' $!";
    print "labels pass...\n";
    while (my $symline = <$symsource>) {
    next if $symline =~ /^\s$/;
    $symline =~ s/[\r\n]//g;
    next if $symline =~ /^\/\//;
    # finds (sym) symbols.
    if ($symline =~ /^\s*\((.+)\)/ ) {
        if (!exists $symbols{$1}) {
            $symbols{$1} = $linenum;
            #print "$1 : $linenum\n";
        }
    } else {
        # Symbol (xxx) does not count as a line number, only inc 
        # when it's not a symbol (xxx)
        $linenum++;
    }
}
close $symsource;

print "assembly pass...\n";

open(my $asmsource, '<:encoding(UTF-8)', $asmsourcename)
    or die "Could not open file '$asmsourcename' $!";

$linenum = 0;
my $instruction = "";
my $format_output = "";

open(my $asmoutput, '>', $asmoutputname);

while (my $asmline = <$asmsource>) {
    ## Skip if empty or comments.
    next if $asmline =~ /^\s$/;
    next if $asmline =~ /^\/\//;
    ## get rid of both kinds of line endings.
    $asmline =~ s/[\r\n]//g;
    
    ## check for variable symbols.
    if ($asmline =~ /@(\D[A-Za-z0-9_\.]+)/) {
        if (!exists $symbols{$1}) {
            #print "found symbol: $1:$nextsymboladdr\n";
            $symbols{$1} = $nextsymboladdr;
            $nextsymboladdr++;
        }
    }

    # is thi an A or C Instruction ?
    if ($asmline =~ /@(.+)\s*/ ) {
    	# A instruction
    	# is it a symbol ?
        my $addrval = '';
        if (exists $symbols{$1}) {
            $addrval = $symbols{$1};
        } else {
            $addrval = $1;
        }
    	$instruction = sprintf("%016b", $addrval);
		# print("A Instruction\n");
    } else {
		my $dest = "none";
		my $comp = "";
		my $jump = "none";

        if ($asmline =~ /^\s*\((.+)\)/ ) {
            print "$asmline\n";
            next;
        }

    	# C Instruction
    	if ($asmline =~ /([\w\!]*)=([\w\-\+\!\&\|]+);(J..)/) {
    		$dest = $1;
    		$comp = $2;
    		$jump = $3;
    		#print("C Instruction, dest, comp, jump\n");
    	} 

    	if ($asmline =~ /([\w\!]+)=([\w\-\+\!\&\|]+)/) {
			$dest = $1;
			$comp = $2;
			#print("C Instruction, dest, comp\n");

    	}

    	if ($asmline =~ /([\w\-\!\&\|]+);(J..)/) {
    		$comp = $1;
			$jump = $2;
			#print("C Instruction, comp, jump\n");
    	}

        #print("C Instruction d:[$dest], c:[$comp], j:[$jump] \n");

    	$instruction = "111" . $comps{$comp} . $destinations{$dest} . $jumps{$jump};
    }

    $format_output = sprintf("% 4d % -20s %15s", $linenum, $asmline, $instruction);
    print "$format_output\n";

    print $asmoutput "$instruction\n";
    $linenum++;

}

close $asmsource;
close $asmoutput;

print "\nSymbol Table:\n";
foreach my $key (sort keys %symbols)
{
  # do whatever you want with $key and $value here ...
  my $value = $symbols{$key};
  my $format_output = sprintf("% -40s %.6d", $key, $value);
  print "$key:$value\n";
}

