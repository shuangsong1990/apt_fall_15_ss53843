import json
import yahoo_options_data

computedJson = yahoo_options_data.contractAsJson("aapl.dat")
expectedJson = open("aapl.json").read()
expectedJson_change = open("aapl_change.json").read()

if json.loads(computedJson) != json.loads(expectedJson) and json.loads(computedJson) != json.loads(expectedJson_change):
  print "Test failed!"
  print "Expected output:", expectedJson
  print "Your output:", computedJson
#  temp = tuple(set(computedJson) - set(expectedJson))
#  print temp
  assert False
else:
#  print "Your output:", computedJson

  print "Test passed"
