# A7 W2 operations and limits

W1 commit: b711b3f. Generation/edit order is 01, 02, 00, 03, 04.
Raw constrained edits are saved unmodified. They are not full-frame replacements:
the tool reframes and repaints the target despite the invariants. The runtime
edits retain A6 structural pixels, with masked unit-scale anchor texture
transfers. Raw generator pixels are explicitly NOT adopted. A7 is still
PLACEHOLDER where these limited changes cannot satisfy the full spec.

Initial `prepare_a7_frames.py --finish 01` exited 1 due to a missing `json`
import at the SOURCES append, after saving the complete attempt/runtime/JSON.
The import was corrected and the missing JSON appended; no raw image was
overwritten and no additional generation attempt was made.
