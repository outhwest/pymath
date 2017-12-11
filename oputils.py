def sliceToRange(s, length):
    if not isinstance(s, slice):
        raise TypeError("Did not receive a slice")
    step  = s.step  if s.step  else 1

    startDefault = 0      if step > 0 else -1
    stopDefault  = length if step > 0 else -1*length - 1
    
    start = s.start if s.start else startDefault
    stop  = s.stop  if s.stop  else stopDefault


    return range(start, stop, step)
