import sys

args = sys.argv
if len(args) < 2:
    print("usage:\n python parse_protobuf.py protobuf_data_file")
    sys.exit(0)
print("args is {0}".format(args))
import infaCliResponse_pb2 as icr

resp = icr.InfaCliResponse()

fn = args[1]
f = open(fn, 'rb')

resp.ParseFromString(f.read())


print("retcode: {0}\nstdout: {1}\nmessages: ".format(resp.retcode, resp.stdout))

msg = resp.messages
for i in range(len(msg)):
    a = msg.pop()
    print("\t {0}: {1}".format(a.name, a.value))
