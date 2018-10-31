import os
import re

if not os.path.isdir("html"):
    os.mkdir("html")

with open("template.html", "r") as t:
    ward = "\#ward\#"
    template = t.read()
    for i in range(1, 51):
        with open(os.path.join("html", "ward{}.html".format(i)), "w") as f:
            output = re.sub(ward, str(i), template)
            f.write(output)