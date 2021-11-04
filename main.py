import esprima
from bs4 import BeautifulSoup

program = 'const answer = 42'

print(type(esprima.parseScript(program)))
a = dict(esprima.parseScript(program))
print(a)
a = """
<html>
<head>
<% getIndex("startHtml"); %>
<script src='help.js'></script>
<script>
$(function(){
	var help = new $.Help({
			container:"help",
			content:["DHCPARP_TABLE"]
		});
});
</script>
</head>
<body>
<div class="view">
<div id="help" >
</div>
<table>
  <tr><td><b><script>dw(Js_ArpTable)</script></b></td></tr>
</table>
<table border="1">
<tr class="table_title">
<td><script>dw(MM_IpAddr)</script></td>
<td><script>dw(MM_MacAddr)</script></td>
<td><script>dw(Js_RouteInterface)</script></td></tr>
<% arpTableList(); %>
</table>
<br>
<br>
<form action=/boafrm/formReflashClientTbl method=POST name="formClientTbl">
<table>
  <tr><td><b><script>dw(Js_DhcpClients_Table)</script></b></td></tr>
</table>
<table border="1">
<tr class="table_title"><td><script>dw(dhcp_hostname)</script></td>
<td><script>dw(MM_IpAddr)</script></td>
<td><script>dw(MM_MacAddr)</script></td>
<td><script>dw(Js_TimeExpired)</script></td></tr>
<% dhcpClientList(); %>
</table>
<table class="sub-btn">
<tr><td>
<input type="submit" value="Refresh" id="refresh" name="refresh">
<input type="hidden" value="/dhcptbl.htm" name="submit-url">
<script>
$("#refresh").val(MM_Refresh);
</script></tr></td>
</table>
</form>
</div>
</body>
</html>
"""


def HtmlParser(body):
    soup = BeautifulSoup(body, 'lxml')
    forms = soup.find_all('form')



HtmlParser(a)
