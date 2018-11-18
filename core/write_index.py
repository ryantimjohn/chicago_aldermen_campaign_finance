start = """<!DOCTYPE html>
<html lang="en">

<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Aldermen Campaign Finance Test</title>
</head>

<body>
"""
end = """
</body>

</html>
"""

for i in range(1, 51):
    ward = '<p><a href="html/ward{ward}.html">Ward {ward}</a></p>\n'.format(**{'ward': i})
    start += ward
start += end

with open("index.html", "w") as f:
    f.write(start)

