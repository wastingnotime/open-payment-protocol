# Cross-provider Scenario Contract Refinement

The five provider-native Pix slices now expose the same minimum report shape
for comparison without normalizing their provider-native projections. The
shared check validates only report structure and observation attribution; it
does not assert common status, identifier, or error semantics.

The next build adds this check as a deterministic test over every current
scenario registry.
