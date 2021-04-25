<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
</head>
<body>
<h1>大家好</h1>
<%!
	int a=10;
	int b=40;
	int ads(int a,int b){
		return a+b;
	}

%>

<%
	
	out.println("Hello!Spring!"+ads(a,b));

%>
<a href="../WEB-INF/jsp/kefu.jsp" id="kefu" onclick="">tttteeeessssstttt</a><!--  -->
</body>
</html>