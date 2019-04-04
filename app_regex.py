import re

sig_start = r'<div class=\"dev_result_obj\">'
sig_end = r'<span class=\"dev_result_lbracket\" onclick=\"Dev.btHide\(this\);\">]</span>'
ex_attachment = sig_start + r'(.*?)' + sig_end
ex_attachment = re.compile(ex_attachment)

ex_id = r'<span class=\"dev_result_key\">\"id\":</span> <span class=\"dev_result_num\">([0-9]*?)</span>'
ex_id = re.compile(ex_id)

ex_date = r'<span class=\"dev_result_key\">\"date\":</span> <span onmouseover=\"Dev.onMouseOverDate\(this\)\" onmouseout=\"Dev.onMouseOut\(\)\" data-date=\"(?:[0-9]*?)\"><span class=\"dev_result_num\">([0-9]*?)</span></span>'
ex_date = re.compile(ex_date)

ex_size = r'<span class=\"dev_result_key\">\"type\":</span> <span class=\"dev_result_str\">\"(.*?)\"</span>,<br><span class=\"dev_result_key\">\"url\":</span> <span class=\"dev_result_str\">\"<a href=\"(https://pp.userapi.com/.*?)\"'
ex_size = re.compile(ex_size)

ex_next_from = r'<span class=\"dev_result_key\">\"next_from\":</span> <span class=\"dev_result_str\">\"([0-9/]*?)\"</span>'
ex_next_from = re.compile(ex_next_from)

ex_count = r'<span class=\"dev_result_key\">\"count\":</span> <span class=\"dev_result_num\">([0-9]*?)</span>'
ex_count = re.compile(ex_count)

#extentions = ['jpg', 'png']
#ex_url = r'https://pp.userapi.com/(.*?\.(?:{}))'
#ex_url = re.compile(ex_url.format('|'.join(extentions)))
