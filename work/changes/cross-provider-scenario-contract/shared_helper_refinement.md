# Shared Contract Helper Refinement

The test suite and standalone validator currently duplicate report-contract
constants and serialization logic. The next build moves those rules into one
simulation helper while retaining the typed Iugu report compatibility.
