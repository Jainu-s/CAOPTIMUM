from bs4 import BeautifulSoup


def find_element(html_code, target, sub_text=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    target_elements = soup.find_all(text=lambda text: target in text.strip())

    if not target_elements:
        return ["Element not found."]

    paths = []
    distances = []
    for target_element in target_elements:
        path = []
        current = target_element
        distance = 0

        while current.parent:
            tag = current.name
            index = sum(1 for sibling in current.previous_siblings if sibling.name == tag) + 1
            path.insert(0, f"{tag}[{index}]")
            current = current.parent

            if sub_text:
                if sub_text in current.get_text():
                    break

            distance += 1

        paths.append(path)
        distances.append(distance)

    if not paths:
        return ["Element not found."]

    min_distance = min(distances)
    closest_path_index = distances.index(min_distance)
    closest_path = paths[closest_path_index]

    return [closest_path]


html_code = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="style.css" />
  <title>Browser</title>
</head>

<body>
  <div>
    <div class="banking_section corp_section">
      <span class="corp_icon"><img src="sbijava/images/ybbi_corp.png" alt="yono BUSINESS"></span>
      <a href="https://yonobusiness.sbi/" class="personal"><span class="personal_highlight">CORPORATE</span> BANKING</a>
    
        <div>
          <p>TOP</p>
          <span> ON</span>
        </div>
        <div class='namede'>
          <h1>
            1st Block
          </h1>
          <p>
            <span> Hello <a href='https://www.google.com'>LOGIN</a> HERE</span>
          </p>
        </div>
    </div>
    <div class='namede'>
      <h1>
        2nd Block
      </h1>
      <span> Hello <a href='https://www.google.com'>LOGIN</a> HERE</span>
    </div>
  </div>
  <script src="script.js"></script>
</body>

</html>
"""

target_text = "LOGIN"
sub_text = "CORPORATE BANKING"

result = find_element(html_code, target_text, sub_text)
print("Element found at paths:")
for path in result:
    print(path)
