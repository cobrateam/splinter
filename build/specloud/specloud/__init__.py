import sys
import subprocess


def main():
    sys.exit(
            subprocess.call(['nosetests',
                    '-i',
                    '^(it|ensure|must|should|deve|specs?|examples?)',
                    '-i',
                    '(specs?|examples?|exemplos?)(.py)?$',
                    '--with-spec',
                    '--spec-color',
                    ] + sys.argv[1:]))

