from numpy     import arange


def prepare_array(*dims):
   ""

   dimension = 1
   for k in dims:
     dimension = dimension * k

   list = arange(dimension)*0.0
   list.shape = dims

   return(list)


def frange(start, stop, step):
   i = start
   while i < stop:
     yield i
     i += step
