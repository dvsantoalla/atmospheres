import spline

D="date"
TM="time"
W="ws"    # in m/s
T="2t"      # in C
P="tp"  # in mm
C="tcc"   # Okta, up to 0-8

# 40 values per matrix, following current EPSGrams 10-day values, four values per day

DATA = {
	"Madrid" : [{D:"2014-07-14",
				TM:12,
				T:[33,24,21,32,34,25,22,34,36,26,23,34,35,27,23,34,33,25,20,27,27,22,19,27,30,23,19,28,32,23,19,32,34,23,20,33,35,26,22,34],
				W:[1.3,3.5,2,1,1.1,2,2,2,1.9,2.2,1.8,4,5,3,1.7,2.5,5,4.2,4.3,5,5.3,2,1,2,2.5,2.2,2.7,0,0.7,4.5,2.2,0.1,1,3,2,0.2,2.2,4.5,2.8,2.5],
				P:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				C:[0,.01,0,.01,.01,0,0,0,.01,0,.2,.1,.3,2.1,.1,7.8,8,8,0,7,.1,0,0,.1,0,.01,0,0,0,0,0,0,.1,.01,.01,.01,.01,.01,.01,3] 
				}],
	"Copenhagen" : [{}],
	"Reading" : [{}]
}


# The first two elements of pair are the "usual" ranges
# and the last two the "extreme" ranges, possible but improbable (define the exact probability)
RANGES = {
        W:(0,30,0,100),
        T:(-20,40,-40,50),
        P:(0,20,0,40),
        C:(0,8)
        }

