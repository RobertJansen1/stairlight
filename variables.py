valr=151
valg=0
valb=151
valw=501
val0=str(0)
pvalr=50
pvalg=50
pvalb=50
rgbr=str(23)
rgbg=str(24)
rgbb=str(25)
tree1w=str(1)
tree2w=str(2)
tree3w=str(3)
tree4w=str(4)
tree5w=str(5)
tree6w=str(6)
tree7w=str(7)
tree8w=str(8)
tree9w=str(9)
tree10w=str(10)
tree11w=str(11)
tree12w=str(12)
tree13w=str(13)
timeout = 20
shuttimeout = 5
wait = .3
ndel = .01
fdel = .01
treetimeout = 0
stepsize = 2
PIRB_PIN = 21
PIRT_PIN = 20
valred = {}
for trede in (range(1,14)):
  valred[trede] = 50
valblue = {}
for trede in (range(1,14)):
  valblue[trede] = 0
for trede in (range(10,14)):
  valblue[trede] = 50
valgreen = {}
for trede in (range(1,14)):
  valgreen[trede] = 0
for trede in (range(5,10)):
  valgreen[trede] = 50
valwhite = {}
for trede in (range(1,14)):
  valwhite[trede] = 201
red = {
  0: 50,
  1: 50,
  2: 50,
  3: 50,
  4: 25,
  5: 0,
  6: 0,
  7: 0,
  8: 0,
  9: 0,
  10: 25,
  11: 50,
  12: 50,
  13: 50,
  14: 50,
}
blue = {
  0: 0,
  1: 0,
  2: 0,
  3: 0,
  4: 0,
  5: 0,
  6: 25,
  7: 50,
  8: 50,
  9: 50,
  10: 50,
  11: 50,
  12: 25,
  13: 0,
  14: 0,
}
green = {
  0: 0,
  1: 0,
  2: 25,
  3: 50,
  4: 50,
  5: 50,
  6: 50,
  7: 50,
  8: 25,
  9: 0,
  10: 0,
  11: 0,
  12: 0,
  13: 0,
  14: 0,
}
