from urllib2 import urlopen
html = urlopen("http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu")
print(html.read())
