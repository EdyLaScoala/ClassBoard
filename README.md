<h3>Despre ClassBoard: </h3>
<p>
  ·	Aplicația constă într-un simplu fișier executabil 'ClassBoard.exe'. Așadar instalarea acesteia nu este complexa.<br>
  ·	Aplicația permite utilizatorului să creeze sau sa deschidă o 'tablă' , care mai târziu se poate salva, unde acesta poate să scrie, desezene informații, să insereze și să redimensioneze imagini din calculatorul personal. Poate să poziționeze imaginile sau să miște întreaga tablă pentru a vedea diferite arii ale tablei.<br>
  ·	Aplicația salvează progresul într-un fișier '.cls' , care poate să fie re-deschis de aplicașție prin dublu-click. Datele fișierului nu sunt encodate sau ascunse de utilizator în această versiune a aplicației pentru motive de demonstare.
</p><br><br>

<h3>Cerințe minime de sistem:</h3>
<p>
  ·	Spațiu de stocare: 38.4MB<br>
  ·	Memorie: 64MB<br>
  ·	CPU: intel pentium Dual-Core(intel pentium G6000)<br>
  ·	Permisiuni de accesare si manipulare a fisierelor: (salvează,deschide si editează fișiere)
</p><br><br>

<h3>Alcătuire:</h3>
<p>
  ·	Aplicația constă în 2 ecrane principale: <br><br>
 
1(BOARD)- Ecranul pe care sunt desenate informațiile ce sunt adăugate de utilizator.<br>
 
2(MENU) - Ecranul pe care este afișat meniul si controalele  ce vor rămâne mereu vizibile utilizatorului cât timp aplicația este deshisă.<br>
 
·	Cele 2 ecrane nu ruleaza independent, așadar, ecranul MENU este dependent de BOARD.(Meniul este închis dacă tabla de scris este închisă).

</p><br><br>

<h3>Resurse:</h3>
<p>
  ·	Tkinter – GUI-ul pentru ecranul MENU a fost construit folosind obiecte de tip TK (tkinter) + alte sub-module TK: filedialog, messagebox, colorchooser, filedialog.<br>
  ·	Pygame - folosit pentru a desena și a creea ecranul BOARD. <br>
  ·	- PIL - folosit pentru a deshide / manipula și redimensiona imaginile importate.<br>
  ·	base64/io - folosit pentru a transforma imaginile deschise de utilizator in baza 64 pentru a putea fii salvate in același fișier '.cls' împreună cu restul datelor ce constituie desenele de pe tabla.<br>
  ·	math - permite calcularea rapidă a distanțelor dintre 2 puncte, etc.<br>
  ·	os / sys  - permite aplicației să deshidă / salveze fișiere folosind sistemul de operare. <br>
  ·	ast - permite aplicației să citească cu ușurință datele salvate in fișiere.<br>
  ·	win32api, win32con, win32gui - toate contribuie la gestionarea celor 2 ecrane BOARD,MENU
</p>
</h3>
