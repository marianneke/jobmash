def ModelIt(fromUser  = 'Default', jobs = []):
  in_state = len(jobs)
  print 'The number of jobs is %i' % in_state
  result = in_state
  if fromUser != 'Default':
    return result
  else:
    return 'check your input'