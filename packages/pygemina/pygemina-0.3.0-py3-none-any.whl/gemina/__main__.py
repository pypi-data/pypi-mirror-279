# flake8: noqa
"""Usage:
  gemina encrypt -i INFILE -o OUTFILE [-V N] (-p | -k) [INPUT]
  gemina decrypt -i INFILE -o OUTFILE (-p | -k) [INPUT]
  gemina verify  -i INFILE (-p | -k) [INPUT]
  gemina create  -o OUTFILE [-V N]

Commands:
  encrypt  encrypt a file
  decrypt  decrypt a file
  verify   verify a file
  create   create a secret key

Argument:
  INPUT    password or keyfile
           if omitted it will be asked for (password w/o echoing)

Options:
  -i INFILE --input   INFILE   input file
  -o OUTFILE --output OUTFILE  output file
  -V N  format version (N: one of 1, 2, 3, 4, 5) [default: 1]
  -p --password  use password
  -k --keyfile   use keyfile

  -h --help  show this help
  --version  show the version
"""
import sys
from getpass import getpass

from salmagundi.files import read_all, write_all
from salmagundi.utils import docopt_helper

from . import *
from . import __version__


def _version_conv(n):
    n = int(n)
    if n == 1:
        return Version.V1
    if n == 2:
        return Version.V2
    if n == 3:
        return Version.V3
    if n == 4:
        return Version.V4
    if n == 5:
        return Version.V5
    raise ValueError('version must be one of 1, 2, 3, 4, 5')


def _get_input(passwd):
    try:
        in_put = getpass() if passwd else input('Keyfile: ')
        if not in_put:
            sys.exit('no input')
        return in_put
    except EOFError:
        print()
        sys.exit()


def main():
    """Main function."""
    args = docopt_helper(__doc__, version=__version__,
                         converters={'-V': _version_conv})
    try:
        if args['create']:
            write_all(args['--output'],
                      create_secret_key(version=args['-V']), True)
        else:
            if not args['INPUT']:
                in_put = _get_input(args['--password'])
            else:
                in_put = args['INPUT']
            indata = read_all(args['--input'], True)
            if args['encrypt']:
                if args['--password']:
                    outdata = encrypt_with_password(in_put.encode(),
                                                    indata, version=args['-V'])
                else:
                    outdata = encrypt_with_key(read_all(in_put, True),
                                               indata, version=args['-V'])
                write_all(args['--output'], outdata, True)
            elif args['decrypt']:
                if args['--password']:
                    outdata = decrypt_with_password(in_put.encode(), indata)
                else:
                    outdata = decrypt_with_key(read_all(in_put, True), indata)
                write_all(args['--output'], outdata, True)
            else:  # verify
                if args['--password']:
                    ok = verify_with_password(in_put.encode(), indata)
                else:
                    ok = verify_with_key(read_all(in_put, True), indata)
                if ok:
                    print('verified')
                else:
                    sys.exit('NOT verified')
    except KeyboardInterrupt:
        print()
    except Exception as ex:
        sys.exit(ex)


if __name__ == '__main__':
    main()
