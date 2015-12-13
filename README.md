# Digihouse
Flask webapp running on my Netgear R6250 with DD-WRT
----

After many nights of indulgent nerdery, I was able to use the following guide:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; http://dd-wrt.com/wiki/index.php/Optware_on_K3-AC-ARM

to get Python installed on my Netgear R6250 Wireless router. Hell ya!

Still, there were some issues, and the interpreter would not run. There was furious Googling, and rejoice:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; http://www.dd-wrt.com/phpBB2/viewtopic.php?p=994804

There are some restrictions I am working with here, so the code wont be the prettiest.

----
Current functions:
- Control fireplace though particle.io API
- Provide days since last hot tub water change

----
<h4>Things that haven't gone my way 😢</h4>

- Here's what happens when I try to import ssl (you know, to use things like 'requests'):

```
root@Digiport:~# python
Python 2.7.10 (default, Nov 29 2015, 11:57:55)
[GCC 5.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import ssl
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/usr/lib/python2.7/ssl.py", line 97, in <module>
    import _ssl             # if we can't import it, let the error propagate
ImportError: Error relocating /opt/usr/lib/python2.7/lib-dynload/_ssl.so: EC_KEY_free: symbol not found
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; I tried to research this path some, but it didn't really get all that far:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; http://www.dd-wrt.com/phpBB2/viewtopic.php?p=994801

- Here's some fun when trying to use sqlite:
```
root@Digiport:/jffs# python try.py
Traceback (most recent call last):
  File "try.py", line 8, in <module>
    c.execute("INSERT INTO data VALUES('2015-12-12')")
sqlite3.DatabaseError: database disk image is malformed
```
These issues are no doubt due to C libraries that just aren't too happy running on this architecture. 
