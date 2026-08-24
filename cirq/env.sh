# Used by ./run (non-interactive). Do not source this in a prompt.
#
# Guix Python does not search /usr/lib, and pip wheels (NumPy, Cirq)
# still look up libz / libstdc++ by soname. Point the dynamic linker
# at the Guix shell profile — but ONLY in a non-interactive child.
# Exporting this in an interactive guix shell makes Ubuntu ls/date load
# Guix libm and fail: version `GLIBC_2.43' not found
#
# Override (debug only): QIMONO_FORCE_GUIX_LDLIB=1 source ./env.sh

_qimono_interactive=0
case ${-:-} in
  *i*) _qimono_interactive=1 ;;
esac

if [ -n "${GUIX_ENVIRONMENT-}" ]; then
  if [ "${QIMONO_FORCE_GUIX_LDLIB-}" = 1 ] || [ "$_qimono_interactive" -eq 0 ]; then
    LD_LIBRARY_PATH="${GUIX_ENVIRONMENT}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    export LD_LIBRARY_PATH
  else
    echo "env.sh: skip LD_LIBRARY_PATH in an interactive shell (breaks host ls)." >&2
    echo "       Run scripts with ./run python … instead." >&2
  fi
fi
unset _qimono_interactive
