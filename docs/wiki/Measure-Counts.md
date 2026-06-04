# Measure Counts

DrumBurp uses **measure counts** to decide how each beat is subdivided in the
tablature editor. In practical terms, the measure count is the rhythmic grid
shown under the drum lines: it controls where notes can be placed inside each
beat.

Right-click the count text below a measure and choose **Measure Count** to
change the subdivision for that measure.

In translated versions of DrumBurp, these technical rhythm names are shown with
the original English name first and the translation in parentheses. For example:
**Quarter Notes (Negras)** or **16th Triplets (Tresillos de semicorcheas)**.
This keeps DrumBurp compatible with English books, tutorials, and older project
materials while still helping users read the interface in their own language.

## What The Menu Options Mean

The menu entries describe different rhythmic subdivisions:

- **Quarter Notes**: one count position per beat.
- **8ths**: two positions per beat.
- **Triplets**: three evenly spaced positions per beat.
- **Quintuplets**: five evenly spaced positions per beat.
- **Septuplets**: seven evenly spaced positions per beat.
- **16ths**: four positions per beat.
- **32nds**: eight positions per beat.
- **64ths**: sixteen positions per beat.

Entries such as **16th Triplets**, **32nd Triplets**, **16th Quintuplets**, or
**64th Septuplets** provide denser grids for more detailed rhythmic notation.

Entries beginning with **Sparse** use the same rhythmic subdivision internally,
but display a less crowded count line. They are useful when the full count text
would make the tablature harder to read.

## Why This Matters

Changing the measure count does not change which drum is played. It changes the
available timing positions inside the measure. Use a finer subdivision when a
part needs faster notes or tuplets; use a simpler subdivision when the rhythm is
straightforward and readability matters more.

## Related Actions

- **Edit Measure Count** opens the detailed count editor for the current
  measure.
- **Contract Count** simplifies the current measure count when the notes allow
  it.
- **Contract All Counts** tries to simplify measure counts throughout the score.
