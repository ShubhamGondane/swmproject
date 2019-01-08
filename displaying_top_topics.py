import pickle
from mako.template import Template

fp=open("svalues.pickle","rb")
topics = pickle.load(fp)
print(topics)
rows=topics

template = """
        <html>
            <body><style type="text/css">
h1{
  font-size: 30px;
  color: #fff;
  text-transform: uppercase;
  font-weight: 300;
  text-align: center;
  margin-bottom: 15px;
}
table{
  width:100%;
  table-layout: fixed;
}
.tbl-header{
  background-color: rgba(255,255,255,0.3);
 }
.tbl-content{
  height:300px;
  overflow-x:auto;
  margin-top: 0px;
  border: 1px solid rgba(255,255,255,0.3);
}
th{
  padding: 20px 15px;
  text-align: left;
  font-weight: 500;
  font-size: 30px;
  color: #fff;
  text-transform: uppercase;
}
td{
  padding: 15px;
  text-align: left;
  vertical-align:middle;
  font-weight: 300;
  font-size: 20px;
  color: #fff;
  border-bottom: solid 1px rgba(255,255,255,0.1);
}


/* demo styles */

@import url(https://fonts.googleapis.com/css?family=Roboto:400,500,300,700);
body{
  background: -webkit-linear-gradient(left, #25c481, #25b7c4);
  background: linear-gradient(to right, #25c481, #25b7c4);
  font-family: 'Roboto', sans-serif;
}
section{
  margin: 50px;
}


/* follow me template */
.made-with-love {
  margin-top: 40px;
  padding: 10px;
  clear: left;
  text-align: center;
  font-size: 10px;
  font-family: arial;
  color: #fff;
}
.made-with-love i {
  font-style: normal;
  color: #F50057;
  font-size: 14px;
  position: relative;
  top: 2px;
}
.made-with-love a {
  color: #fff;
  text-decoration: none;
}
.made-with-love a:hover {
  text-decoration: underline;
}


/* for custom scrollbar for webkit browser*/

::-webkit-scrollbar {
    width: 6px;
} 
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
} 
::-webkit-scrollbar-thumb {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
}</style>
<script>
// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .
$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();
</script>
            <section>
                           <h1>Analysis of Related topics obained by</h1>
                           <h1>Market Basket Analysis</h1>
                           <div class="tbl-header">
    <table cellpadding="0" cellspacing="0" border="0">
      <thead>
        <tr>
          <th>Topic</th>
          <th>#Positive</th>
          <th>#Negative</th>
          <th>#Neutral</th>
        </tr>
      </thead>
    </table>
  </div>
                           <div class="tbl-content">
                <table cellpadding="0" cellspacing="0" border="0">
                      % for row in rows:
                     <tr>
                          % for cell in row:
                          <td>${cell}</td>
                          % endfor
                     </tr>
                     % endfor
                </table>
                </div>
                </section>
            </body>
        </html>"""
print(Template(template).render(rows=rows))
display=open("html/top.html","w")
display.write(Template(template).render(rows=rows))

#First, create the texts of the columns:
#cols = ["<td>{0}</td>". format( "</td><td>".join(t)  ) for t in topics]

#then use it to join the rows (tr)
#for t in topics:
#	rows = "<tr>{0}</tr>".format( "</tr><tr>".join(t) ) 

#finaly, inject it into the html...

\