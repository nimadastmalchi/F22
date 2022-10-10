transitions = [5.4, 6.48, 7.56, 8.64, 9.72]
def f(t):
    if t in transitions:
        return None
    if t < 5.4:
        return 1
    if t < 6.48:
        return 0
    if t < 7.56:
        return 1
    if t < 8.64:
        return 0
    if t < 9.72:
        return 1
    return 0

tran_ind = 0
T = 1
lag = 0
P = 0
t = 0.5
while t < 11:
    SampleSignal = f(t)
    print('t =', round(t, 2), ',', 'P =', round(P, 2), 'lag =',  round(lag, 2))
    P = P + T + lag
    t += T + lag
    if tran_ind < len(transitions) and t > transitions[tran_ind]:
        A = transitions[tran_ind]
        tran_ind += 1
        lag = A - P
