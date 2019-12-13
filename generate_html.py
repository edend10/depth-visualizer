import sys
import os

input_dir = sys.argv[1] if len(sys.argv) > 1 else 'test_input'
output_file = sys.argv[2] if len(sys.argv) > 2 else 'test_output/index.html'

template = """
<h3>{}</h3>
<table border="1" style="table-layout: fixed;">
  <tr> 
    <td halign="center" style="word-wrap: break-word;" valign="top">
      <p>  
        <a href="images/{}_real_A.png">
          <img src="images/{}_real_A.png" style="width:256px">
        </a><br>
        <p>real_A</p>
      </p> 
    </td>
    <td halign="center" style="word-wrap: break-word;" valign="top">
      <p>  
        <a href="images/{}_feke_B.png">
          <img src="images/{}_fake_B.png" style="width:256px">
        </a><br>
        <p>fake_B</p>
      </p> 
    </td>
    <td halign="center" style="word-wrap: break-word;" valign="top">
      <p>  
        <a href="images/{}_real_B.png">
          <img src="images/{}_real_B.png" style="width:256px">
        </a><br>
        <p>real_B</p>
      </p> 
    </td>
    <td halign="center" style="word-wrap: break-word;" valign="top">
      <p>  
        <a href="gifs/{}_fake_B.gif">
          <img src="gifs/{}_fake_B.gif" style="width:256px">
        </a><br>
        <p>fake_B</p>
      </p> 
    </td>
    <td halign="center" style="word-wrap: break-word;" valign="top">
      <p>  
        <a href="gifs/{}_real_B.gif">
          <img src="gifs/{}_real_B.gif" style="width:256px">
        </a><br>
        <p>real_B</p>
      </p> 
    </td>
  </tr>
</table>\n
"""

var_cnt = template.count('{}')

with open(output_file, 'w') as output_file:
    for filename in os.listdir(input_dir):
        if 'fake_' in filename:
            filename_index = filename.split('_')[0]
            output_file.write(template.format(*[filename_index] * var_cnt))
