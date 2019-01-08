tbl = [['Jason', 'Brown', 'Leeds', '40'], 
       ['Sarah', 'Robinson', 'Bristol', '32'], 
       ['Carlo', 'Baldi', 'Manchester', '41']]

#First, create the texts of the columns:
cols = ["<td>{0}</td>". format( "</td><td>".join(t)  ) for t in tbl]

#then use it to join the rows (tr)
rows = "<tr>{0}</tr>".format( "</tr>\n<tr>".join(cols) )

#finaly, inject it into the html...
display = open("html/table.html", 'w')
display.write("""<HTML> <body>
                           <h1>Attendance list</h1>
                            <table>  
                              {0}  
                            </table>
                        </body>  
                  </HTML>""".format(rows))