import numpy as np
import utils as ut


def main(value_list, q_min, q_max):
    """
    Quantizes a list of values using the given quantization range (q_min, q_max).
    """
    # Step 1: Calculate min and max values
    x_min, x_max = ut.calculate_min_max(value_list)

    # Step 2: Compute scale and zero-point
    s, z = ut.compute_scale_zero_point(x_min, x_max, q_min=q_min, q_max=q_max)

    # Step 3: Quantize each value
    q_list = [ut.quantize_value(x, s, z) for x in value_list]

    # Step 4: Dequantize to verify with 1 decimal place
    dq_list = [ut.dequantize_value(q, s, z) for q in q_list]

    # Report
    print("\nQuantization Variables:\n=============")
    print(f"x_min: {x_min}, x_max: {x_max}")
    print(f"Scale (s): {s}, Zero-Point (z): {z}")

    print("\nVerification:\n=============")
    print("\nOriginal values:\n", value_list)

    print(f"\nQuantized values within [{q_min}, {q_max}]:\n", q_list)
    # 1 decimal only
    print(f"\nDequantized values:\n", [round(dq, 1) for dq in dq_list])
    print(
        f"\nQuantization Error (Dequantized - Original): {round(np.mean(np.abs(np.array(value_list) - np.array(dq_list))), 2)}"
    )


if __name__ == "__main__":
    # Define a list of values
    value_list = [
        191.6,
        -13.5,
        728.6,
        92.14,
        295.5,
        -184,
        0,
        684.6,
        245.5,
    ]
    # Quantize the values between 0 and 255
    main(value_list, q_min=0, q_max=255)
