# Case 04 — React useEffect Infinite Loop

The diff introduces a `useEffect` that lists `filters` as a dependency,
where `filters` is an object literal constructed on every render. React
uses referential equality for dependency comparison, so `filters` always
appears changed. Each effect run calls `setProducts`, which triggers a
re-render, which creates a new `filters` object, which triggers the effect
again — an infinite render loop that freezes the browser tab.

**Ground truth:** 1 SERIOUS finding (`logic_error`).
**Category:** bug.
**Expected position:** REJECT.
