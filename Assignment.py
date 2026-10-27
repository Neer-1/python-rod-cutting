from decimal import Decimal, InvalidOperation

def get_order():
    while True:
        try:
            num_rods = int(input("Enter the number of rods (enter 0 to exit): "))
            if num_rods == 0:
                return None
            elif num_rods < 0:
                print("Input must be a positive integer.")
                continue
            
            rod_lengths = []
            for i in range(num_rods):
                while True:
                    try:
                        length = Decimal(input(f"Enter the length of rod {i+1} in meters: "))
                        if not length.is_finite() or length <= 0 or length > 4:
                            print("Rod length must be greater than 0 and less than or equal to 4.")
                        else:
                            rod_lengths.append(length)
                            break
                    except (ValueError, InvalidOperation):
                        print("Invalid input. Please enter a numerical value.")
            return rod_lengths
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def build_cut_plan(rod_lengths):
    """Greedy decreasing packing, not a guarantee of minimum stock usage.

    Decimal arithmetic preserves entered decimal lengths. Kerf is not modeled.
    The input is never mutated; invalid cuts are rejected before packing.
    """
    lengths = []
    for value in rod_lengths:
        try:
            length = Decimal(str(value))
        except InvalidOperation as exc:
            raise ValueError('Cut lengths must be finite numbers in (0, 4].') from exc
        if not length.is_finite() or not 0 < length <= 4:
            raise ValueError('Cut lengths must be finite numbers in (0, 4].')
        lengths.append(length)
    remaining = sorted(lengths, reverse=True)
    rods = []
    while remaining:
        available = Decimal(4)
        cuts, unplaced = [], []
        for length in remaining:
            if length <= available:
                cuts.append(length)
                available -= length
            else:
                unplaced.append(length)
        rods.append(cuts)
        remaining = unplaced
    total_length = sum(lengths, Decimal(0))
    return {
        'rods': rods,
        'rod_count': len(rods),
        'revenue': total_length * 200,
        'waste': Decimal(4) * len(rods) - total_length,
    }


def cut_rods(rod_lengths):
    plan = build_cut_plan(rod_lengths)
    print('Greedy cutting plan (not guaranteed optimal; no kerf allowance).')
    print('Total number of 4-meter rods used:', plan['rod_count'])
    print(f"Total revenue generated: Rs{plan['revenue']:.2f}")
    print(f"Waste generated: {plan['waste']:.2f} meters")
    for i, rod in enumerate(plan['rods'], 1):
        print(f"Rod {i}: {[str(cut) for cut in rod]} (waste: {4 - sum(rod):.2f} meters)")
    return plan


def main():
    print("Welcome to the rod cutting.")
    print("enter 0 to exit:")
    
    while True:
        try:
            orders = get_order()
        except EOFError:
            print("\nInput ended. No unfinished order was processed.")
            break
        if orders is None:
            break
        cut_rods(orders)

if __name__ == "__main__":
    main()