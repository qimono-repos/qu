# Source this *inside* `guix shell -m manifest.scm`.
# Guix Python does not search /usr/lib, and pip wheels (NumPy, Aer)
# still look up libz / libstdc++ by soname. Point the dynamic linker
# at the Guix profile that the manifest built.
if [ -n "${GUIX_ENVIRONMENT-}" ]; then
  LD_LIBRARY_PATH="${GUIX_ENVIRONMENT}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  export LD_LIBRARY_PATH
fi
