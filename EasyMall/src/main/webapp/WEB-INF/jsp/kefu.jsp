<%@ page language="java" import="java.util.*" pageEncoding="utf-8" isELIgnored="false" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns:th="http://www.thymeleaf.org">
<head>

	<meta http-equiv="Content-type" content="text/html; charset=UTF-8" />
    <title>QQ简易聊天框</title>
    <script type="text/javascript" src="${ pageContext.request.contextPath }/js/jquery-1.4.2.js"></script>
    <style type="text/css">
	*{font-size: 14px; padding:0; margin:0;}
	.main{
 	position: relative;
 	margin: 20px auto;
 	border: 1px solid steelblue;
	width: 660px;
	height: 635px;
	}
	.msgInput{
 	display: block;
 	width: 645px;
 	height: 100px;
	margin: 10px auto;
 
	}
	.sendbtn{
	position: absolute;
 	width: 100px;
	height: 29px;
	bottom: 5px;
	right: 10px;
	}
	.content{
	list-style: none;
	width: 640px;
	height: 480px;
	margin: 5px auto;
	border: 1px dotted #D1D3D6;
	overflow-y: scroll;
	}
	.msgContent{
	width:auto;
	max-width: 250px;
	height: auto;
	word-break: break-all;
	margin: 5px;
	padding: 3px;
	border-radius: 5px;
	}
 
	.content .left{
	float: left;
	text-align: left;
	background-color: lightgrey;
	}
	.content .right{
	float: right;
	text-align: right;
	background-color: yellowgreen;
	}
 
 
	</style>
	<script type="text/javascript">
window.onload=function(){
 
	/*var input = document.getElementById('msg_input');//查找缓存
	document.getElementById('sendbtn').onclick=function () {
	//var input1 = document.getElementById('msg_input');//
	//input0
 
	sendMsg();
	}
 
 */
 
	//快捷键 发送
	document.onkeypress = function (event) {
	var e = event || window.event;
	var keycode = e.keyCode || e.which;
	console.log(e)
	if( keycode==10){//判断同时按下ctrl 和enter
	sendMsg()
	 }
	}
 
	//将内容添加到聊天框内
	function sendMsg() {
	var input = document.getElementById('msg_input');//查找缓存
	var ul = document.getElementById('content1');
 
	var newLi = document.createElement('li');
	newLi.innerHTML = input.value;
	newLi.setAttribute("style","font-size:130%");
	newLi.className = 'msgContent right';
	ul.appendChild(newLi);
 
	var div = document.createElement('div');
	div.setAttribute("style", "clear:both");
	ul.appendChild(div);
 
 
	ajax({
	url:'http://jisuznwd.market.alicloudapi.com/iqa/query?question='+input.value,
	success:function (res) {
	//  console.log(res)
	var obj = JSON.parse(res);
	console.log(obj)
	var array = obj.result.content;
	//   var zhengzhou = array[0];
	var tmp = array;
	//   var tmp = '温度:'+zhengzhou.day_air_temperature+','+zhengzhou.day_weather;
	console.log(tmp)
 
	var newLi = document.createElement('li');
	newLi.innerHTML = tmp;
	newLi.className = 'msgContent left';
	ul.appendChild(newLi);
 
	var div = document.createElement('div');
	div.style = 'clear:both';
	ul.appendChild(div);
	input.value = '';
	newLi.scrollIntoView();//将元素滚动到可见位置
	}
	})
 
	input.value = '';
	newLi.scrollIntoView();//将元素滚动到可见位置
	}
 
}
 
 
 
	function ajax(obj) {
	//?lastCursor=6610&pageSize=10
	//  var url = 'reg.php';
	var xhr = null;
	if(window.ActiveXObject){
	xhr = new ActiveXObject('Microsoft.XMLHTTP')
	}else{
	xhr = new XMLHttpRequest();
	}
	// $username = $_REQUEST['username'];
	// $password = $_REQUEST['password'];
 
	//打开与服务器的连接
	if(obj.method){
	xhr.open(obj.method,obj.url,true);
	}else{
	xhr.open('get',obj.url,true);
	}
	xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xhr.setRequestHeader("Authorization","APPCODE 3e9dfb924f464e9593a95f9d2bbf4348")
 
 
	// {username:'zhangsa',password:123123}
	// sendData = encodeURIComponent(sendData);
 
 
	// 发送请求
	//console.log(res);
	//回调函数
	xhr.onreadystatechange = function () {
	//  console.log(xhr.readyState)
	if(xhr.readyState == 4){
	//数据接收完毕
	if(xhr.status == 200){
	//   console.log('请求成功',xhr.responseText)
	if(obj.success){
	obj.success(xhr.responseText)
	}
 
	}else{
	//   console.log(xhr.status,'请求出错')
	if(obj.failure){
	obj.failure('请求失败')
	}
	}
  }
 }
	//  var sendData = 'username=zhangsan&password=123456';
	if( obj.method == undefined ||obj.method.toLowerCase() =='get'){
	xhr.send(null);//
	}else{
	xhr.send(obj.params);//
 
	}
	}
 
 
	</script>
 
</head>
 
<body>


	<!-- 将头部(_head.jsp)包含进来--> 
	<%@ include file="_head.jsp" %>
 	

	<!-- 聊天框主体 -->
	<div id="main" class="main">
	<ul id="content1" class="content">
	
	<li class="msgContent left" style="font-size:130%">您好！这里是EasyMall的客服小莫。</li>
	<c:forEach items="${msg}" var="text">
			<li>${text.texttime}</li>
			<li>${text.text}</li>
			</c:forEach>
		</ul>
	<form action="${ pageContext.request.contextPath }/kefu/sendtext" method="POST">

	

	<input type="text" name="texture" class="msgInput" value=""/>
	<button id="send" class="sendbtn">发送</button>
	</form>
	</div>
 
	<!-- 将底部(_foot.jsp)包含进来 -->
	<jsp:include page="/WEB-INF/jsp/_foot.jsp"/>
	
</body>

</html>