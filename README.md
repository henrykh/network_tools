# network_tools
* Echo Server
    -Creates a simple server and client, where the server will read in the message sent it by the client and send it back. The client returns this message.
    -If received request is GET and HTTP/1.1, server returns 200 response, if not it returns an appropriate error response
    -Server looks in the root folder for the requested uri, returning the file content if it's a file, a directory listing if it's a directory, or an error if the file cannot be accessed or does not exist.



### Resources
[Sockets in Python](https://docs.python.org/2/library/socket.html)
[Socket walkthrough](http://codefellows.github.io/python-dev-accelerator/assignments/day06/socket_exercise.html)
[HTTP Made Really Easy](http://www.jmarshall.com/easy/http/)
[OS Package Documentation](https://docs.python.org/2/library/os.html#os-file-dir)
[HTTP Headers](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)