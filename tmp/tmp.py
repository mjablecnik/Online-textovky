# -*- coding: utf-8 -*-
content="""<!DOCTYPE HTML>
<html>

<head>
  <title>Brandbook</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  
<!--  
<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<script src="//code.jquery.com/jquery-1.9.1.js"></script>
<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
-->
<script src="/js/jquery-ui-1.10.4/js/jquery-1.10.2.js"></script>
<script src="/js/jquery-ui-1.10.4/js/jquery-ui-1.10.4.js"></script>

<script src="jquery.scrollbar.js"></script>
  <script type="text/javascript" src="js/script.js"></script>
  <link rel="stylesheet" type="text/css" href="css/style.css" />
</head>


<body>
<div id="container">
    <header>
    	<h1><a href="/index">Brand<span>Book</span></a></h1>
    </header>
    <nav>
		  <ul class="sf-menu" id="nav">
			<li class="selected"><a href="http://www.jsiznacka.cz" target="_blank"> Program Jsi značka </a></li>
			<li><a href="/index">Homepage</a></li>
			
			<!--<li><a href="/videa">Videa</a></a></li>-->
			<li><a href="/verejna-zed">Veřejná zeď</a></li>
			<li><a href="/moje-zed">Moje zeď</a></li>
			<li><a href="/chat">Chat</a></li>
			<!--<li><a href="/otazky">Otázky na Tomáše</a></li>-->
			<li><a href="/profil">Profil</a></li>
			<li><a href="/clenove">Členové</a></li>
			<li><a href="/odhlaseni">Odhlásit se</a></li>
		</ul>
      </nav>

    <div id="body">

		<section id="content">
		"""
#end
content+="""
		"""
content+=model["content"]
content+="""

		</section>
        
    	<div class="clear"></div>
    </div>
    <footer>
        <div class="footer-bottom">
            <p>&copy; Brandbook 2014. <a href="http://zypopwebtemplates.com/">Free CSS Website Templates</a> by ZyPOP</p>
         </div>
    </footer>
</div>
</body>
</html>

"""
