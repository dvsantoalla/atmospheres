from subprocess import Popen,PIPE
import logging as log
import os

DAC=True
FILENAME="output.wav"

def get_csd(orchestra,score):
        if DAC:
            output_file="-odac"
        else:
            output_file="-o %s" % FILENAME

	csd = """
<CsoundSynthesizer>
<CsOptions>
        csound -W -G %s
</CsOptions>
<CsInstruments>
        sr = 44100  ; Sample rate.
        kr = 4410  ; Control signal rate.
        ksmps = 10  ; Samples pr. control signal.
        nchnls = 1  ; Number of output channels.

        %s

</CsInstruments>
<CsScore>

        %s	

	e
</CsScore>
</CsoundSynthesizer>
""" % (output_file, ("\n").join(orchestra),("\n").join(score))
	return csd


def write_and_play(csdcontent,tempfile="out.csd"):

	# write score
	out = open(tempfile,"w")
	out.write(csdcontent)
	out.close()

	csound = "csound"
	if os.environ.has_key("CSOUND"):
		csound = os.environ["CSOUND"]
		log.info("Using csound binary: %s" % csound)

	# run generation out to device or wav file
	proc = Popen([csound, tempfile], stdout=PIPE, stderr=PIPE)
	for line in iter(proc.stderr.readline,''):
   		log.debug(line.rstrip())
	rc = proc.returncode
	log.debug(proc.stdout.readlines())


	# Optionally play and/or archive the audio file
