# Anki cards

This is a collection of cards for the Anki spaced-repetition system.

## Why plain text

Cards live here as tab-separated text (`.tsv`), not as binary `.apkg` decks. Text diffs cleanly in git, anyone on the team (Albert, Claude, ChatGPT) can append a card with a normal commit, and Anki imports it directly.

## Structure

Folders mirror the deck hierarchy. One `.tsv` file is one leaf deck.

```
anki/
  quantum-computing/            Deck: Quantum Computing
    hardware/                   Deck: Quantum Computing::Hardware
      superconductors.tsv       Deck: Quantum Computing::Hardware::Superconductors
```

To add a topic, add a folder. To add a leaf deck, add a `.tsv` inside it.

## File format

Each `.tsv` starts with Anki header lines, so the import needs no manual setup:

```
#separator:tab
#html:false
#notetype:Basic
#deck:Quantum Computing::Hardware::Superconductors
#columns:Front	Back	Tags
#tags column:3
```

Then one card per line: `Front<TAB>Back<TAB>Tags`.

Rules:
- No tab characters inside a field.
- Tags are space-separated. Use `::` for tag hierarchy, e.g. `qcfx1::week2::superconducting`.
- Add a `source::...` tag pointing at the transcript or paper the answer comes from, so every card can be checked against its source.

## Importing

Anki desktop: File > Import > pick the `.tsv`. The header sets the separator, note type, deck and tags column. Re-importing an updated file updates existing cards that have the same Front.
