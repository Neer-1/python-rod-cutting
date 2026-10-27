# Python Rod Cutting

A small console demonstration that packs requested cuts into four-metre stock rods using a descending greedy heuristic. It prints the actual plan, rods used, leftover length and gross revenue under a coursework price assumption.

**Author (provisional public identifier):** [Neer-1](https://github.com/Neer-1). Preferred display name pending confirmation.

This is a university Python programming assignment with later improvements. It is **not a universally optimal cutting algorithm**. See [academic provenance](PROVENANCE.md).

## Requirements and setup

Tested with Python 3.12.3. Only the Python standard library is used: no dependency installation, account, network connection, database or environment secrets are required.

From the repository directory:

```powershell
python -B Assignment.py
```

Enter the number of requested pieces, then each length in metres. Lengths must be finite numbers greater than zero and at most four. Enter `0` at the next piece-count prompt to exit. End-of-input exits cleanly without processing an unfinished order.

## Example

Enter these lines when prompted:

```text
3
2.5
2.5
2.5
0
```

The plan uses three four-metre rods, each with a 2.5m cut. Summary:

```text
Total number of 4-meter rods used: 3
Total revenue generated: Rs1500.00
Waste generated: 4.50 meters
```

The same input is in [examples/basic-input.txt](examples/basic-input.txt). In PowerShell:

```powershell
Get-Content examples/basic-input.txt | python -B Assignment.py
```

On shells that support stdin redirection:

```sh
python -B Assignment.py < examples/basic-input.txt
```

Revenue uses the original assumption of Rs 200 per metre of requested cuts. It is not profit and does not include stock cost.

## How the heuristic works

1. Validate the lengths and sort a separate copy in descending order.
2. Open a four-metre rod and scan the remaining lengths, placing each cut that fits.
3. Repeat with the unplaced cuts until the order is packed.
4. Count the rods actually produced, then calculate revenue and waste.

A length-only lower bound can be infeasible: three 2.5m cuts total 7.5m but still require three rods. The program reports the actual plan rather than claiming two rods from total length alone.

The greedy plan can also be worse than a feasible alternative. For cuts `[2.4, 2, 1.2, 0.8, 0.8, 0.8]`, it uses three rods. Two suffice with `[2.4, 0.8, 0.8]` and `[2, 1.2, 0.8]`. The tests explicitly preserve this counterexample; the program does not claim to meet a universal optimality requirement.

## Tests

```powershell
python -B -m unittest discover -s tests -v
```

The 10 tests cover actual stock count, decimal exact-fit examples, input preservation, cut conservation, empty orders, invalid/nonfinite values, console EOF and invalid-input recovery, direct Decimal console parsing, the known suboptimal case, and 923 small-instance comparisons against an independent exhaustive oracle. These finite checks do not prove universal feasibility or optimality for every possible input.

The exhaustive oracle is test-only and is not used by the application.

## Limits

- No cutting kerf, stock cost, multiple stock lengths or industrial constraints.
- Decimal arithmetic uses Python's default precision; it is not an arbitrary-precision optimizer. If calling `build_cut_plan` directly, pass Decimal values or decimal strings to avoid precision already lost in floating-point inputs.
- No resource limits for very large orders; intended for small educational examples.
- Revenue and displayed two-decimal values follow the coursework assumptions, not a commercial quotation system.
- Source and tests are provided without claiming a complete implementation of every original assessment criterion.

## License

No open-source license has been selected or included. Do not describe this repository as MIT-licensed or otherwise open-source licensed.
