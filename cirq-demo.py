import cirq

print("Cirq version:", cirq.__version__)

def list_top_level_names(mod, limit=30):
	return [n for n in dir(mod) if not n.startswith("_")][:limit]

try:
	# Prefer the `cirq.google` namespace when available (older packaging).
	google_mod = getattr(cirq, "google", None)
	if google_mod is None:
		# Newer packaging provides a separate `cirq_google` package.
		import cirq_google as google_mod  # type: ignore
		# Attach the separate package to `cirq.google` for compatibility with
		# older examples that reference `cirq.google` directly.
		try:
			cirq.google = google_mod
		except Exception:
			# If assignment fails for any reason, keep going — we'll still use
			# the `google_mod` local variable below.
			pass
		print("Imported `cirq_google` as fallback (separate package).")
	else:
		print("Using bundled `cirq.google` namespace.")

	names = list_top_level_names(google_mod)
	print("Top-level names in cirq google module:", names)

	# Show a few known attributes if present, in case the user expects them.
	for candidate in ("foxtail_v2", "FoxtailV2", "Engine", "EngineProcessor", "EngineProgram"):
		if hasattr(google_mod, candidate):
			print(f"Found {candidate} ->", getattr(google_mod, candidate))
except Exception as e:
	print("Could not access cirq google module; import or introspection failed:", e)

# Resolve a module reference we can safely use at the end of the script.
# If we successfully imported or found a `google_mod` above, use that.
if 'google_mod' in globals() and google_mod is not None:
	google = google_mod
else:
	google = getattr(cirq, 'google', None)

if google is None:
	print('No cirq google module available to show Foxtail-related symbols.')
else:
	# Show any attributes that mention 'foxtail' so users can find the right name.
	foxtail_matches = [n for n in dir(google) if 'foxtail' in n.lower()]
	print('Foxtail-related names in cirq.google:', foxtail_matches)

	# Try several common candidate names and print whichever exist.
	for candidate in ('Foxtail', 'FoxtailV2', 'foxtail', 'foxtail_v2'):
		if hasattr(google, candidate):
			print(f"Found {candidate} ->", getattr(google, candidate))
		else:
			print(f"{candidate} not found in cirq.google")

	# If no real Foxtail device is available, print a mock ASCII layout similar
	# to the tutorial screenshot so users see the expected grid structure.
	if not foxtail_matches:
		def print_mock_foxtail(rows=2, cols=12):
			width = 9
			connector = '----'

			def label(r, c):
				return f'({r}, {c})'.center(width)

			# Top row
			top = ''.join(label(0, c) + (connector if c != cols-1 else '') for c in range(cols))

			# Vertical connector line (choose a pattern to match tutorial feel)
			verts = []
			# Place vertical bars under a selection of columns for visual similarity
			bar_cols = {0, 3, 4, 7, 8}
			for c in range(cols):
				if c in bar_cols:
					# put '|' in the center of the cell
					cell = ' ' * (width//2) + '|' + ' ' * (width - width//2 - 1)
				else:
					cell = ' ' * width
				verts.append(cell + ( '    ' if c != cols-1 else ''))
			vert_line = ''.join(verts)

			# Bottom row
			bottom = ''.join(label(1, c) + (connector if c != cols-1 else '') for c in range(cols))

			print(top)
			print(vert_line)
			print(bottom)

		print('\nMock Foxtail-like device layout:')
		print_mock_foxtail()