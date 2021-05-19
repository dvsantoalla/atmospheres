

def gen08(fnumber, data, number_of_points=16777216, comment=None):
    """
    http://www.csounds.com/manual/html/GEN08.html
    """

    # generate parts off data
    step = number_of_points / len(data)

    gen = "f%s 0 %s -8 " % (fnumber, number_of_points)
    for i in data:
        gen += "%s %s " % (i, step)

    if comment is not None:
        gen += "; %s" % comment

    return gen


def basic_wave(instrument_number=1, function_number=1):
    """
    http://www.csounds.com/manual/html/GEN10.html
    Requires a function f function_number defining the waveform, eg
        f1 0 16384 10 1                                          ; Sine
        f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth
        f3 0 16384 10 1 0   0.3 0    0.2 0     0.14 0     .111   ; Square
        f4 0 16384 10 1 1   1   1    0.7 0.5   0.3  0.1          ; Pulse
    """

    csd = """
            
    instr %s
        asig oscil p4, cpspch(p5), %s
        out asig
    endin

    """ % (instrument_number, function_number)
    return csd


def table_modulated_basic_wave(instrument_number=1, oscillator_function_number=1, modulating_function_number=2,
                         seq_length=7, table_length=16384, use_function_as_envelope=False, amplitude=50000):
    """
    http://www.csounds.com/manual/html/GEN10.html
    Requires a function f function_number defining the waveform, eg
        f1 0 16384 10 1                                          ; Sine
        f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth
        f3 0 16384 10 1 0   0.3 0    0.2 0     0.14 0     .111   ; Square
        f4 0 16384 10 1 1   1   1    0.7 0.5   0.3  0.1          ; Pulse

    Also requires a modulating function number, eg
    http://www.csounds.com/manual/html/GEN20.html
        f2 0 16384 20 2 1 ; Hanning window

    Parameter 'amp' (p4) is going to represent the index to this function window,
        relative to the number of notes of the sequence. Eg, if 14 notes, index should be 0-13
    """

    oscillator = """
        asig oscil iamp * %s, cpspch(p5), %s
    """ % (amplitude, oscillator_function_number)

    if use_function_as_envelope:
        oscillator = """
        kampidx line 0, p3, %s  ; p3 is duration
        kampfactor table kampidx, %s
        asig oscil iamp * %s * kampfactor , cpspch(p5), %s
    """ % (table_length, modulating_function_number, amplitude, oscillator_function_number)

    csd = """

        instr %s
            
            ;printks "p4 (index) %%d \\n", 1, p4 
            ;printks "p5 (pitch) %%d \\n", 1, p5

            iidx = ( p4 / %s )  * %s
            iamp  table iidx, %s
            ;printks "iidx: %%d\\n",  1, iidx
            ;printks "iamp: %%f\\n",  1, iamp
    %s
            out asig
            
        endin

        """ % (instrument_number, seq_length, table_length, modulating_function_number,
               oscillator)
    return csd


def oscillator1(points, instrument_number=1):

    csd = """

    instr %s
        kidx 	line 0, p3, %s ; p3 (duration) is in beats, "line" requires seconds. Ok as long as BPM=60
        kpar 	table kidx, p5 
        kfreq	= kpar*100 +100
        a1 	oscil p4, kfreq, 1  ; Simple oscillator.  
        out a1  ; Output. 

        ; printks "kidx: %%d\\n",  1, kidx
        ; printks "kpar: %%f\\n", 1, kpar
        ; printks "kfreq: %%d\\n", 1, kfreq
    endin 
    """ % (instrument_number,points-1)

    return csd


def oscillator2(points,instrument_number=2):

    csd = """

    instr %s
        kidx 	line 0, p3, %s ; p3 (duration) is in beats, "line" requires seconds. Ok as long as BPM=60
        kpar1 	table kidx, p5 
        kpar2 	table kidx, p6 
        kfreq	= kpar1*100 +100
        kamp	= kpar2*100 +100

        a1 	oscil kamp, kfreq, 1  ; Simple oscillator.  
        out a1  ; Output. 

        ; printks "kidx: %%d\\n",  1, kidx
        ; printks "kpar1: %%f\\n", 1, kpar2
        ; printks "kpar2: %%f\\n", 1, kpar3
        ; printks "kfreq: %%d\\n", 1, kfreq
    endin 
    """ % (instrument_number,points-1)

    return csd


def oscillator_dual(points,instrument_number=3):

    csd = """

    instr %s
        kidx 	line 0, p3, %s ; p3 (duration) is in beats, "line" requires seconds. Ok as long as BPM=60
        kpar1 	table kidx, p5 
        kpar2 	table kidx, p6 

        kfreq	= kpar1*100 +100
        kdiff	= kpar2

        a1 	oscil p4, kfreq, 1  ; Simple oscillator. 
        a2 	oscil p4, kfreq-kdiff, 1  ; Simple oscillator. 

        out a1+a2  ; Output. 

        ; printks "kidx: %%d\\n",  1, kidx
        ; printks "kpar1: %%f\\n", 1, kpar2
        ; printks "kpar2: %%f\\n", 1, kpar3
        ; printks "kfreq: %%d\\n", 1, kfreq
    endin 
    """ % (instrument_number,points-1)
    return csd


def wgpluck2(instrument_number=5,iplk=0.75, krefl=0.85):
    """ Parameters p4: amp, p5: cps """

    csd = """
    instr %s
        iplk = %s
        kamp = p4
        icps = cpspch(p5)
        kpick = 0.50
        krefl = %s

        apluck wgpluck2 iplk, kamp, icps, kpick, krefl

        out apluck
    endin """ % (instrument_number,iplk,krefl)

    return csd


def wgpluck(instrument_number=4, function_number=4, iplk=0):
    """ Parameters p4:amp, p5:cps """

    csd = """

    ; Requires table like "f 1 0 16384 10 1"

    instr %s
        icps = cpspch(p5)
        iamp = p4
        kpick = 0.5
        iplk = 0
        idamp = 10
        ifilt = 1000

        axcite oscil 1, 1, %s ; kamp, kfreq, function number
        apluck wgpluck icps, iamp, kpick, iplk, idamp, ifilt, axcite

        out apluck
    endin
    """ % (instrument_number, function_number)

    return csd


def partikkel(instrument_number=5, function_number=1):

    """
    http://www.csounds.com/manual/html/partikkel.html

    a1 [, a2, a3, a4, a5, a6, a7, a8] partikkel agrainfreq, \
              kdistribution, idisttab, async, kenv2amt, ienv2tab, ienv_attack, \
              ienv_decay, ksustain_amount, ka_d_ratio, kduration, kamp, igainmasks, \
              kwavfreq, ksweepshape, iwavfreqstarttab, iwavfreqendtab, awavfm, \
              ifmamptab, kfmenv, icosine, ktraincps, knumpartials, kchroma, \
              ichannelmasks, krandommask, kwaveform1, kwaveform2, kwaveform3, \
              kwaveform4, iwaveamptab, asamplepos1, asamplepos2, asamplepos3, \
              asamplepos4, kwavekey1, kwavekey2, kwavekey3, kwavekey4, imax_grains \
              [, iopcode_id]

<CsScore>
i1 0 5  ; partikkel
e
</CsScore>
    """

    csd = """
    
sr = 44100
ksmps = 20
nchnls = 2

giSine          ftgen   0, 0, 65537, 10, 1
giCosine        ftgen   0, 0, 8193, 9, 1, 1, 90

instr 1

kgrainfreq      = 200                   ; 4 grains per second
kdistribution   = 0                     ; periodic grain distribution
idisttab        = -1                    ; (default) flat distribution used for grain distribution    
async           = 0                     ; no sync input
kenv2amt        = 0                     ; no secondary enveloping
ienv2tab        = -1                    ; default secondary envelope (flat)
ienv_attack     = -1 ;                  ; default attack envelope (flat)
ienv_decay      = -1 ;                  ; default decay envelope (flat)
ksustain_amount = 0.5                   ; time (in fraction of grain dur) at sustain level for each grain
ka_d_ratio      = 0.5                   ; balance between attack and decay time
kduration       = (0.5/kgrainfreq)*1000 ; set grain duration relative to grain rate
kamp            = 5000                  ; amp
igainmasks      = -1                    ; (default) no gain masking
kwavfreq        = 440                   ; fundamental frequency of source waveform
ksweepshape     = 0                     ; shape of frequency sweep (0=no sweep)
iwavfreqstarttab = -1                   ; default frequency sweep start (value in table = 1, which give no frequency modification)
iwavfreqendtab  = -1                    ; default frequency sweep end (value in table = 1, which give no frequency modification)
awavfm          = 0                     ; no FM input
ifmamptab       = -1                    ; default FM scaling (=1)
kfmenv          = -1                    ; default FM envelope (flat)
icosine         = giCosine              ; cosine ftable
kTrainCps       = kgrainfreq            ; set trainlet cps equal to grain rate for single-cycle trainlet in each grain
knumpartials    = 3                     ; number of partials in trainlet
kchroma         = 1                     ; balance of partials in trainlet
ichannelmasks   = -1                    ; (default) no channel masking, all grains to output 1
krandommask     = 0                     ; no random grain masking
kwaveform1      = giSine                ; source waveforms
kwaveform2      = giSine                ;
kwaveform3      = giSine                ;
kwaveform4      = giSine                ;
iwaveamptab     = -1                    ; (default) equal mix of all 4 sourcve waveforms and no amp for trainlets
asamplepos1     = 0                     ; phase offset for reading source waveform
asamplepos2     = 0                     ;
asamplepos3     = 0                     ;
asamplepos4     = 0                     ;
kwavekey1       = 1                     ; original key for source waveform
kwavekey2       = 1                     ;
kwavekey3       = 1                     ;
kwavekey4       = 1                     ;
imax_grains     = 100                   ; max grains per k period

asig    partikkel kgrainfreq, kdistribution, idisttab, async, kenv2amt, ienv2tab, \
               ienv_attack, ienv_decay, ksustain_amount, ka_d_ratio, kduration, kamp, igainmasks, \
               kwavfreq, ksweepshape, iwavfreqstarttab, iwavfreqendtab, awavfm, \
               ifmamptab, kfmenv, icosine, kTrainCps, knumpartials, \
               kchroma, ichannelmasks, krandommask, kwaveform1, kwaveform2, kwaveform3, kwaveform4, \
               iwaveamptab, asamplepos1, asamplepos2, asamplepos3, asamplepos4, \
               kwavekey1, kwavekey2, kwavekey3, kwavekey4, imax_grains

outs    asig, asig
endin    
    
    """ % (instrument_number, function_number)

    return csd


