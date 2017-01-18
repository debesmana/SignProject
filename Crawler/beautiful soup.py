import urllib

website = urllib.urlopen("http://www.dainuskapis.lv/katalogs/1.-Par-dziesmam-un-dziedasanu")
htmlSource = website.read()
website.close

print htmlSource
