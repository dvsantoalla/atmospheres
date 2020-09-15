import logging as log
import os
import sys
from subprocess import Popen, PIPE

DAC = True
FILENAME = "output.wav"


def get_csd(orchestra, score, headers=[]):

    if "pytest" in sys.modules:
        output_file = "-o pytest.wav"
    elif DAC:
        output_file = "-odac"
    else:
        output_file = "-o %s" % FILENAME

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
        %s

</CsInstruments>
<CsScore>
%s	

e
</CsScore>
</CsoundSynthesizer>
""" % (output_file, ("\n").join(headers), ("\n").join(orchestra), ("\n").join(score))
    return csd


def write_and_play(csdcontent, tempfile="out.csd"):
    # write score
    out = open(tempfile, "w")
    out.write(csdcontent)
    out.close()

    if "pytest" in sys.modules:
        use_dac = False
    else:
        use_dac = DAC

    csound = os.environ.get("CSOUND", "csound")
    log.debug("Using csound binary: %s" % csound)

    # run generation out to device or wav file
    proc = Popen([csound, tempfile], stdout=PIPE, stderr=PIPE)
    if use_dac:
        for line in iter(proc.stderr.readline, ''):
            log.debug(line.rstrip())
    rc = proc.returncode

    if not use_dac:
        errout = proc.stderr.readlines()
        for ln in errout:
            log.debug(ln)

    stdout = proc.stdout.readlines()
    for ln in stdout:
        log.debug(ln)


# Optionally play and/or archive the audio file
