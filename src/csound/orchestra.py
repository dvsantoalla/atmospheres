

def gen08(fnumber,data,number_of_points=16777216, comment=None):

        # generate parts off data
        step = number_of_points / len(data)

        gen = "f%s 0 %s -8 " % (fnumber,number_of_points)
        for i in data:
                gen += "%s %s " % (i, step)

        return gen

def basic_wave(instrument_number=1, function_number=1):
        """
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

def oscillator1(points,instrument_number=1):

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

def partikkel(instrument_number=5):

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


