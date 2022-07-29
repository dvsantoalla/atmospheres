import logging as log
import os
import datetime
import traceback
from subprocess import Popen, PIPE, STDOUT
from shutil import which

DAC = True
FILENAME = "output.wav"


def get_csd(orchestra, score, headers=[]):

    if "ATMOSPHERES_WAV_OUTPUT" in os.environ:
        output_file = "-o pytest.wav"
    elif DAC:
        output_file = "-odac"
    else:
        output_file = "-o %s" % FILENAME

    # Who generated this file
    a = traceback.extract_stack(limit=3)
    trace_list = traceback.format_list(a)
    traces = "\n\n; Traces for the file generation call, called at %s\n" % datetime.datetime.now()
    for item in trace_list:
        for line in item.split("\n"):
            traces += "; %s \n" % line
    log.info("Traces into file: %s" % traces)

    csd = """
<CsoundSynthesizer>
<CsOptions>
        csound -W -G %s
%s
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
""" % (output_file, traces, ("\n").join(headers), ("\n").join(orchestra), ("\n").join(score))
    return csd


def write_and_play(csdcontent, tempfile="out.csd"):
    # write score
    out = open(tempfile, "w")
    out.write(csdcontent)
    out.close()

    if "ATMOSPHERES_WAV_OUTPUT" in os.environ:
        use_dac = False
    else:
        use_dac = DAC

    csound = find_csound_executable()

    # run generation out to device or wav file
    proc = Popen([csound, tempfile], stdout=PIPE, stderr=STDOUT, text=True)
    stdout, stderr = proc.communicate()
    if use_dac:
        for line in iter(stdout.readline, b""):
            error_line = line.rstrip()
            if len(error_line) == 0:
                break
            else:
                log.debug(error_line.rstrip())
    rc = proc.returncode
    log.debug("Process %s returned code %s from %s" % (csound, rc, proc))

    if stdout is not None:
        for i in stdout.split("\n"):
            log.info(i)
    if stderr is not None:
        for i in stderr.split("\n"):
            log.warning(i)


def find_csound_executable():

    try_paths = ["/opt/homebrew/bin/csound", "/bin/csound", "/usr/bin/csound"]

    log.debug("Trying to find 'csound' in CSOUND environment variable, if present...")
    csound = os.environ.get("CSOUND", None)
    if csound is None:
        log.debug("Trying to find 'csound' in standard PATH...")
        csound = which("csound")
    if csound is None:
        log.debug("Trying to find 'csound' in predefined standard locations %s ..." %(try_paths))
        for p in try_paths:
            log.warning("Looking for 'csound' in path %s ..." % p)
            if os.access(p, os.X_OK):
                log.debug("'csound' found in path %s" % p)
                csound = p
                break

    if csound is not None:
        log.debug("Using csound binary: %s" % csound)
        return csound
    else:
        raise BaseException("'csound' binary not found. Tried standard PATH, environment variable CSOUND and paths in %s)"
              % (try_paths))

# Optionally play and/or archive the audio file
