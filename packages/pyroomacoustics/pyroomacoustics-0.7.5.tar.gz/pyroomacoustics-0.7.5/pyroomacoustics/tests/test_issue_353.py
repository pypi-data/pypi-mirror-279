"""
# Test for Issue 353

[issue #353](https://github.com/LCAV/pyroomacoustics/issues/353)

The cause of the issue was that the time of the maximum delay
in the RIR is used to determine the necessary size of the array.

The float64 value of the delay was used to determine the size and construct the array.
However, the `rir_build` routine takes float32.
After conversion, the array size would evaluate to one delay more due to rounding
offset and an array size check would fail.

Converting the delay time array to float32 before creating the rir array
solved the issue.
"""

import numpy as np

import pyroomacoustics as pra


def test_issue_353():
    room_dims = np.array([10.0, 10.0, 10.0])
    room = pra.ShoeBox(
        room_dims, fs=24000, materials=None, max_order=22, use_rand_ism=False
    )

    source = np.array([[6.35551912], [4.33308523], [3.69586303]])
    room.add_source(source)

    mic_array_in_room = np.array(
        [
            [1.5205189, 1.49366285, 1.73302404, 1.67847898],
            [4.68430529, 4.76250254, 4.67956424, 4.60702604],
            [2.68214263, 2.7980202, 2.55341851, 2.72701718],
        ]
    )
    room.add_microphone_array(mic_array_in_room)

    room.compute_rir()
